# =============================================================================
# app.py  —  KeplerDB Web App
# Flask app standalone: calcula carta natal + interpretaciones Kepler
# Ejecutar: py -X utf8 app.py  →  abre http://localhost:7860
# =============================================================================
import sys, os, io, base64, re, json, traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, render_template, request, jsonify
import swisseph as swe
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import kepler_interp as ki
import gemini_engine as ge

swe.set_ephe_path(None)
app = Flask(__name__)

# --- CONFIGURACIÓN Y MAPEOS ---
SIGN_ESP = ['Aries','Tauro','Géminis','Cáncer','Leo','Virgo',
            'Libra','Escorpio','Sagitario','Capricornio','Acuario','Piscis']
SIGN_GLYPHS = ['♈','♉','♊','♋','♌','♍','♎','♏','♐','♑','♒','♓']
PLANET_GLYPHS = {
    'Sol':'☉','Luna':'☽','Mercurio':'☿','Venus':'♀','Marte':'♂',
    'Jupiter':'♃','Saturno':'♄','Urano':'⛢','Neptuno':'♆','Pluton':'♇','NodoN':'☊'
}
PCOLS = {
    'Sol':'#FFD700','Luna':'#AAAAFF','Mercurio':'#FFAA44','Venus':'#88EE88',
    'Marte':'#FF5555','Jupiter':'#CC88FF','Saturno':'#88CCFF',
    'Urano':'#44DDCC','Neptuno':'#8888FF','Pluton':'#FF88AA','NodoN':'#FFAA00'
}
SISTEMAS = {'Placidus':b'P','Koch':b'K','Whole Sign':b'W',
            'Equal':b'E','Campanus':b'C','Regiomontanus':b'R'}
PLANET_IDS = {
    'Sol':swe.SUN,'Luna':swe.MOON,'Mercurio':swe.MERCURY,
    'Venus':swe.VENUS,'Marte':swe.MARS,'Jupiter':swe.JUPITER,
    'Saturno':swe.SATURN,'Urano':swe.URANUS,'Neptuno':swe.NEPTUNE,'Pluton':swe.PLUTO
}

# --- HELPERS DE CONVERSIÓN SEGURA ---
def to_int(v, default=0):
    try:
        if v is None or str(v).strip() == "": return default
        return int(float(v))
    except: return default

def to_float(v, default=0.0):
    try:
        if v is None or str(v).strip() == "": return default
        return float(v)
    except: return default

def deg_to_sign(deg):
    deg = deg % 360
    s = int(deg/30); d = deg%30; m = int((d%1)*60)
    return SIGN_ESP[s], int(d), m, s

def which_house(lon, cusps):
    for i in range(12):
        s = cusps[i]%360; e = cusps[(i+1)%12]%360; l = lon%360
        if s<=e:
            if s<=l<e: return i+1
        else:
            if l>=s or l<e: return i+1
    return 1

def asp_short(angle, orbe=8):
    for deg,name in [(0,'Conj'),(60,'Sext'),(90,'Cuad'),(120,'Trig'),(180,'Opoc')]:
        d = min(abs(angle-deg), abs(angle-(360-deg)))
        if d<=orbe: return name, round(d,2)
    return None, None

def calcular_carta(Y,M,D,h,m,off,lat,lon_geo,sistema='Regiomontanus'):
    H_utc = h + off + m/60.0
    JD = swe.julday(Y,M,D,H_utc)
    sis_b = SISTEMAS.get(sistema, b'R')
    cusps, ascmc = swe.houses(JD, lat, lon_geo, sis_b)
    ASC, MC = ascmc[0], ascmc[1]
    planets_raw = {}
    for name, pid in PLANET_IDS.items():
        res = swe.calc_ut(JD, pid)
        planets_raw[name] = {'lon': res[0][0], 'spd': res[0][3]}
    nn = swe.calc_ut(JD, swe.TRUE_NODE)
    planets_raw['NodoN'] = {'lon': nn[0][0], 'spd': nn[0][3]}
    return {
        'JD': JD, 'ASC': ASC, 'MC': MC,
        'cusps': list(cusps),
        'planets': {k:v['lon'] for k,v in planets_raw.items()},
        'planets_spd': {k:v['spd'] for k,v in planets_raw.items()},
        'sistema': sistema,
    }

def rueda_png(carta, nombre='', fecha=''):
    planets = carta['planets']
    cusps   = carta['cusps']
    ASC     = carta['ASC']
    fig, ax = plt.subplots(1,1, figsize=(8,8),
                           subplot_kw={'projection':'polar'}, facecolor='#ffffff')
    ax.set_facecolor('#f8f9fa')
    lp = lambda lon: np.radians(180.0+(lon-ASC)%360) % (2*np.pi)
    R_ZI=0.78; R_ZO=0.92; R_PL=0.72; R_HI=0.56
    ELEM_COLS=['#fff0f0','#f0fff0','#f0f0ff','#f5f0ff']
    for i in range(12):
        t1 = lp(i*30); t2 = lp((i+1)*30)
        if t2 < t1: t1, t2 = t2, t1
        if t2-t1 > np.pi: t1 += 2*np.pi
        tv = np.linspace(t1, t2, 40) % (2*np.pi)
        ax.fill_between(tv, R_ZI, R_ZO, color=ELEM_COLS[i%4], alpha=0.7)
        ax.fill_between(tv, R_ZI, R_ZO, color='none', edgecolor='#334466', linewidth=0.5)
        mid = np.radians(180.0+((i+0.5)*30-ASC)%360) % (2*np.pi)
        ax.text(mid, (R_ZI+R_ZO)/2, SIGN_GLYPHS[i], ha='center', va='center', fontsize=11, color='#3949ab', fontweight='bold')
    for i, c in enumerate(cusps):
        th = lp(c); lw = 1.6 if i in (0,3,6,9) else 0.7
        ax.plot([th,th],[R_HI,R_ZI], color='#334455', lw=lw, zorder=5)
        ax.text(th, R_HI-0.04, str(i+1), ha='center', va='center', fontsize=7, color='#424242')
    ORDEN = ['Sol','Luna','Mercurio','Venus','Marte','Jupiter','Saturno','Urano','Neptuno','Pluton','NodoN']
    for pname in ORDEN:
        if pname not in planets: continue
        th = lp(planets[pname]); col = PCOLS.get(pname, '#ffffff')
        ax.text(th, R_PL, PLANET_GLYPHS.get(pname, ''), ha='center', va='center', fontsize=13, color=col, fontweight='bold', zorder=9)
    ax.text(0, 0, '☽', ha='center', va='center', fontsize=18, color='#3949ab', zorder=10)
    ax.set_rticks([]); ax.set_xticks([]); ax.spines['polar'].set_visible(False); ax.set_ylim(0, 1.01)
    buf = io.BytesIO(); plt.savefig(buf, format='png', dpi=140, facecolor='#ffffff', bbox_inches='tight'); plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# --- RUTAS ---
@app.route('/')
def index():
    return render_template('index.html', sistemas=list(SISTEMAS.keys()))

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        d = request.json
        Y, M, D = to_int(d.get('anio'), 1970), to_int(d.get('mes'), 1), to_int(d.get('dia'), 1)
        h, m, off = to_int(d.get('hora'), 12), to_int(d.get('min'), 0), to_float(d.get('offset'), 0.0)
        lat, lon_geo = to_float(d.get('lat'), 40.42), to_float(d.get('lon'), -3.70)
        nombre, sistema = d.get('nombre','Sin nombre'), d.get('sistema','Regiomontanus')

        carta = calcular_carta(Y,M,D,h,m,off,lat,lon_geo,sistema)
        fecha_str = f'{D:02d}/{M:02d}/{Y} {h:02d}:{m:02d}h'

        tabla = []
        ORDEN = ['Sol','Luna','Mercurio','Venus','Marte','Jupiter','Saturno','Urano','Neptuno','Pluton','NodoN']
        for pname in ORDEN:
            if pname not in carta['planets']: continue
            lon = carta['planets'][pname]
            sig, deg, minn, _ = deg_to_sign(lon)
            casa = which_house(lon, carta['cusps'])
            retro = ' ℞' if carta['planets_spd'].get(pname, 0) < 0 else ''
            tabla.append({'planeta': pname, 'glyph': PLANET_GLYPHS.get(pname,''), 'pos': f"{deg}°{sig[:3]}{minn:02d}'", 'signo': sig, 'casa': casa, 'retro': retro, 'color': PCOLS.get(pname,'#fff')})

        asc_sig, asc_d, asc_m, _ = deg_to_sign(carta['ASC'])
        mc_sig,  mc_d,  mc_m,  _ = deg_to_sign(carta['MC'])

        aspectos = []
        planet_lons = [(n, carta['planets'][n]) for n in ORDEN if n in carta['planets']]
        ASP_CLR = {'Conj':'#bb8800','Trig':'#226622','Sext':'#224488','Cuad':'#882200','Opoc':'#880022'}
        for i in range(len(planet_lons)):
            for j in range(i+1, len(planet_lons)):
                n1,lon1 = planet_lons[i]; n2,lon2 = planet_lons[j]
                ang = abs(lon1-lon2)%360; asp, orb = asp_short(ang if ang<=180 else 360-ang)
                if asp: aspectos.append({'p1':n1,'p2':n2,'asp':asp,'orb':orb,'col':ASP_CLR.get(asp,'#555')})

        svg_data = {'planets': [{'name':p, 'glyph':PLANET_GLYPHS.get(p,''), 'lon':carta['planets'][p], 'color':PCOLS.get(p,'#000')} for p in ORDEN if p in carta['planets']], 'cusps': carta['cusps'], 'asc': carta['ASC'], 'mc': carta['MC']}
        
        import importlib; importlib.reload(ki)
        kepler_html = ki.generar_informe_completo({'nombre':nombre, 'fecha_str':fecha_str, 'sistema':sistema, 'ASC':carta['ASC'], 'MC':carta['MC'], 'cusps':carta['cusps'], 'planets':carta['planets'], 'planets_spd':carta['planets_spd']})

        return jsonify({'ok': True, 'tabla': tabla, 'asc': f"{asc_d}°{asc_sig[:3]}{asc_m:02d}'", 'mc': f"{mc_d}°{mc_sig[:3]}{mc_m:02d}'", 'aspectos': aspectos, 'rueda': rueda_png(carta, nombre, fecha_str), 'svg_data': svg_data, 'kepler': kepler_html, 'nombre': nombre, 'fecha': fecha_str})
    except Exception:
        return jsonify({'ok': False, 'error': traceback.format_exc()})

@app.route('/transitos', methods=['POST'])
def transitos():
    try:
        d = request.json
        YT,MT,DT = to_int(d.get('t_anio')), to_int(d.get('t_mes')), to_int(d.get('t_dia'))
        hT, mT, offT = to_int(d.get('t_hora', 12)), to_int(d.get('t_min', 0)), to_float(d.get('offset', -1))
        YN,MN,DN = to_int(d.get('anio')), to_int(d.get('mes')), to_int(d.get('dia'))
        hN,mN,offN = to_int(d.get('hora')), to_int(d.get('min')), to_float(d.get('offset'))
        latN, lonN = to_float(d.get('lat')), to_float(d.get('lon'))
        sistema = d.get('sistema', 'Regiomontanus')

        carta_natal = calcular_carta(YN,MN,DN,hN,mN,offN,latN,lonN,sistema)
        H_utc_t = hT + offT + mT/60.0; JD_t = swe.julday(YT,MT,DT,H_utc_t)
        planets_trans = {n: {'lon': swe.calc_ut(JD_t, pid)[0][0], 'spd': swe.calc_ut(JD_t, pid)[0][3]} for n, pid in PLANET_IDS.items()}

        import importlib; importlib.reload(ki)
        fecha_str = f'{DT:02d}/{MT:02d}/{YT}'; html = ki.generar_informe_transitos(carta_natal['planets'], planets_trans, fecha_str)
        return jsonify({'ok': True, 'html': html, 'fecha_trans': fecha_str})
    except Exception:
        return jsonify({'ok': False, 'error': traceback.format_exc()})

@app.route('/sinastria', methods=['POST'])
def sinastria():
    try:
        d = request.json
        def _parse(p):
            Y,M,D_ = to_int(d.get(f'{p}anio')), to_int(d.get(f'{p}mes')), to_int(d.get(f'{p}dia'))
            h,m_,off = to_int(d.get(f'{p}hora',12)), to_int(d.get(f'{p}min',0)), to_float(d.get(f'{p}offset',0))
            lat,lon_ = to_float(d.get(f'{p}lat',40.42)), to_float(d.get(f'{p}lon',-3.70))
            c = calcular_carta(Y,M,D_,h,m_,off,lat,lon_,d.get(f'{p}sistema','Regiomontanus'))
            c['nombre'] = d.get(f'{p}nombre','Persona')
            return c
        import importlib; importlib.reload(ki)
        c1, c2 = _parse('p1_'), _parse('p2_')
        return jsonify({'ok': True, 'html': ki.generar_informe_sinastria(c1, c2, orbe=to_int(d.get('orbe', 6))), 'nombre1': c1['nombre'], 'nombre2': c2['nombre']})
    except Exception:
        return jsonify({'ok': False, 'error': traceback.format_exc()})

@app.route('/revolucion_solar', methods=['POST'])
def revolucion_solar():
    try:
        d = request.json
        YN,MN,DN = to_int(d['anio']), to_int(d['mes']), to_int(d['dia'])
        hN,mN,offN = to_int(d['hora']), to_int(d['min']), to_float(d['offset'])
        latN,lonN = to_float(d['lat']), to_float(d['lon'])
        anio_rs = to_int(d['anio_rs'])
        
        H_utc_n = hN + offN + mN/60.0; JD_n = swe.julday(YN,MN,DN,H_utc_n)
        sol_n = swe.calc_ut(JD_n, swe.SUN)[0][0]
        JD_est = swe.julday(anio_rs, MN, DN, 12.0)
        for _ in range(50):
            sol_r = swe.calc_ut(JD_est, swe.SUN)[0][0]; diff = sol_n - sol_r
            if abs(diff) < 0.00001: break
            if diff > 180: diff -= 360
            if diff < -180: diff += 360
            JD_est += diff / 360.0

        planets_rs = {n: swe.calc_ut(JD_est, pid)[0][0] for n, pid in PLANET_IDS.items()}
        cusps_r, ascmc_r = swe.houses(JD_est, latN, lonN, SISTEMAS.get(d.get('sistema'), b'R'))
        
        yr,mo,dy,hr = swe.revjul(JD_est); f_rs = f'{int(dy):02d}/{int(mo):02d}/{int(yr)} {int(hr):02d}:{int((hr%1)*60):02d}h UTC'
        c_natal = calcular_carta(YN,MN,DN,hN,mN,offN,latN,lonN,d.get('sistema'))
        c_natal['nombre'] = d.get('nombre','')
        c_rs = {'nombre': d.get('nombre'), 'anio_rs': anio_rs, 'ASC': ascmc_r[0], 'MC': ascmc_r[1], 'cusps': list(cusps_r), 'planets': planets_rs}
        
        import importlib; importlib.reload(ki)
        return jsonify({'ok':True, 'html':ki.generar_informe_rs(c_natal, c_rs), 'rueda':rueda_png(c_rs, f'RS {anio_rs}', f_rs), 'fecha_rs': f_rs, 'anio_rs': anio_rs})
    except Exception:
        return jsonify({'ok':False,'error':traceback.format_exc()})

@app.route('/famosos/buscar')
def famosos_buscar():
    q = request.args.get('q','').strip()
    if len(q) < 2: return jsonify({'ok': True, 'famosos': []})
    import sqlite3 as _sq
    conn = _sq.connect(ki.DB_PATH); cur = conn.cursor()
    cur.execute("SELECT id,nombre,lugar,anio,mes,dia,hora,min,gmt,lat,lon,descripcion FROM cartas WHERE nombre LIKE ? OR descripcion LIKE ? LIMIT 20", (f'%{q}%', f'%{q}%'))
    rows = cur.fetchall(); conn.close()
    return jsonify({'ok': True, 'famosos': [{'id':r[0],'nombre':r[1],'lugar':r[2] or '','anio':r[3],'mes':r[4],'dia':r[5],'hora':r[6],'min':r[7],'gmt':r[8],'lat':r[9],'lon':r[10],'desc': (r[11] or '').split(':')[-1].strip()[:40]} for r in rows]})

@app.route('/geo/buscar')
def geo_buscar():
    q = request.args.get('q', '').strip()
    if len(q) < 3: return jsonify([])
    results = []
    try:
        import sqlite3 as _sq
        conn = _sq.connect(ki.DB_PATH); cur = conn.cursor()
        cur.execute("SELECT DISTINCT lugar, lat, lon, gmt FROM cartas WHERE lugar LIKE ? LIMIT 5", (f'%{q}%',))
        for r in cur.fetchall(): results.append({'nombre': f"🏠 {r[0]}", 'lat': r[1], 'lon': r[2], 'gmt': r[3]})
        conn.close()
        if len(results) < 5:
            import requests
            r_osm = requests.get(f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=5", headers={'User-Agent': 'KeplerDB_Gemini'}, timeout=3)
            if r_osm.status_code == 200:
                for item in r_osm.json(): results.append({'nombre': f"🌍 {item['display_name']}", 'lat': float(item['lat']), 'lon': float(item['lon']), 'gmt': 0})
    except: pass
    return jsonify(results)

@app.route('/gemini/informe_profundo', methods=['POST'])
def gemini_informe_profundo():
    d = request.json
    return jsonify({'ok': True, 'informe': ge.engine.generar_informe_profundo({'nombre': d.get('nombre'), 'sol': d.get('sol'), 'luna': d.get('luna'), 'asc': d.get('asc'), 'mc': d.get('mc')}, d.get('textos', ''))})

@app.route('/gemini/resumen', methods=['POST'])
def gemini_resumen():
    return jsonify({'ok': True, 'resumen': ge.engine.resumen_holistico(request.json)})

@app.route('/gemini/modernizar', methods=['POST'])
def gemini_modernizar():
    return jsonify({'ok': True, 'modernizado': ge.engine.modernizar(request.json.get('texto', ''))})

if __name__ == '__main__':
    import webbrowser, threading
    threading.Timer(1.2, lambda: webbrowser.open('http://localhost:7860')).start()
    app.run(debug=False, port=7860)
