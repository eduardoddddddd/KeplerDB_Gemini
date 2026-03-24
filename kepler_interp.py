# =============================================================================
# kepler_interp.py  —  Motor de interpretaciones Kepler para astro_dashboard
# =============================================================================
import sqlite3, re, os

# Ruta dinámica para que funcione tanto local como en la nube (Docker)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "kepler.db")

PLANET_MAP = {
    'Sol':'Sol','Luna':'Luna','Mercurio':'Mercurio','Venus':'Venus',
    'Marte':'Marte','Jupiter':'Júpiter','Saturno':'Saturno',
    'Urano':'Urano','Neptuno':'Neptuno','Pluton':'Plutón',
    'NodoN':'Nodo Norte','ASC':'Ascendente','MC':'Medio Cielo',
}
SIGN_MAP = {
    'Aries':'Aries','Tauro':'Tauro','Géminis':'Géminis','Geminis':'Géminis',
    'Cáncer':'Cáncer','Cancer':'Cáncer','Leo':'Leo','Virgo':'Virgo',
    'Libra':'Libra','Escorpio':'Escorpio','Sagitario':'Sagitario',
    'Capricornio':'Capricornio','Acuario':'Acuario','Piscis':'Piscis',
}
ASPECT_MAP = {
    'Conj':'Conjunción',
    'Sext':'Armónico',
    'Trig':'Armónico',
    'Cuad':'Tensión',
    'Opoc':'Tensión',
}
SIGN_ESP = ['Aries','Tauro','Géminis','Cáncer','Leo','Virgo',
            'Libra','Escorpio','Sagitario','Capricornio','Acuario','Piscis']

SIGN_RULER_CLASSIC = {
    'Aries':'Marte','Tauro':'Venus','Géminis':'Mercurio','Cáncer':'Luna',
    'Leo':'Sol','Virgo':'Mercurio','Libra':'Venus','Escorpio':'Marte',
    'Sagitario':'Jupiter','Capricornio':'Saturno','Acuario':'Saturno','Piscis':'Jupiter'
}

def _conn(): return sqlite3.connect(DB_PATH)
def _signo(lon): return SIGN_ESP[int((lon % 360) / 30)]
def _casa(lon, cusps):
    for i in range(12):
        s = cusps[i]%360; e = cusps[(i+1)%12]%360; l = lon%360
        if s<=e:
            if s<=l<e: return i+1
        else:
            if l>=s or l<e: return i+1
    return 1

def _asp_short(angle, orbe=8):
    for deg,name in [(0,'Conj'),(60,'Sext'),(90,'Cuad'),(120,'Trig'),(180,'Opoc')]:
        d=min(abs(angle-deg),abs(angle-(360-deg)))
        if d<=orbe: return name,round(d,2)
    return None,None

def get_planeta(planeta_dash, signo_str, casa_num):
    p = PLANET_MAP.get(planeta_dash, planeta_dash)
    s = SIGN_MAP.get(signo_str, signo_str)
    conn = _conn(); cur = conn.cursor()
    results = []
    if p == 'Sol':
        cur.execute("SELECT cabecera,texto,'sol' FROM interpretaciones WHERE planeta1='Sol' AND signo=? AND fichero='SOL.ASC' LIMIT 1", (s,))
        r = cur.fetchone(); 
        if r: results.append(r)
    if p == 'Ascendente':
        cur.execute("SELECT cabecera,texto,'signo' FROM interpretaciones WHERE planeta1='Ascendente' AND signo=? AND fichero='ASCEN.ASC' LIMIT 1", (s,))
    else:
        cur.execute("SELECT cabecera,texto,'signo' FROM interpretaciones WHERE planeta1=? AND signo=? AND fichero='PLANETAS.ASC' LIMIT 1", (p, s))
    r = cur.fetchone(); 
    if r: results.append(r)
    if p != 'Ascendente':
        cur.execute("SELECT cabecera,texto,'casa' FROM interpretaciones WHERE signo=? AND casa=? AND fichero='CASAS.ASC' LIMIT 1", (s, casa_num))
        r = cur.fetchone(); 
        if r: results.append(r)
    conn.close(); return results

def get_aspecto(p1_dash, p2_dash, asp_dash):
    p1=PLANET_MAP.get(p1_dash,p1_dash); p2=PLANET_MAP.get(p2_dash,p2_dash)
    asp=ASPECT_MAP.get(asp_dash,asp_dash)
    conn=_conn(); cur=conn.cursor()
    cur.execute("SELECT cabecera,texto FROM interpretaciones WHERE aspecto=? AND ((planeta1=? AND planeta2=?) OR (planeta1=? AND planeta2=?)) AND fichero='ASPECTOS.ASC' LIMIT 1", (asp,p1,p2,p2,p1))
    row=cur.fetchone(); conn.close(); return row

def get_regente(casa_origen, casa_del_regente):
    conn = _conn(); cur = conn.cursor()
    cur.execute("SELECT cabecera, texto FROM interpretaciones WHERE fichero='REGENTES.ASC' AND cabecera LIKE ? LIMIT 1", (f'REGENTE DE CASA {casa_origen} %CASA {casa_del_regente}',))
    row = cur.fetchone(); conn.close(); return row

# --- NARRATIVA NOVELA ---

def generar_informe_completo(carta_activa):
    planets_lon = carta_activa.get('planets', {})
    cusps = carta_activa.get('cusps', [i*30 for i in range(12)])
    nombre = carta_activa.get('nombre', 'Carta')
    fecha = carta_activa.get('fecha_str', '')
    ORDEN = ['Sol','Luna','Mercurio','Venus','Marte','Jupiter','Saturno','Urano','Neptuno','Pluton']
    
    sec = [f'<div style="max-width:800px; margin:0 auto; font-family:\'Georgia\', serif; color:#2c3e50; background:#fff; padding:40px; border:1px solid #eee; box-shadow:0 10px 30px rgba(0,0,0,0.05)">']
    sec.append(f'<div style="text-align:center; border-bottom:1px double #ccc; padding-bottom:30px; margin-bottom:40px"><h1 style="font-size:32px; color:#1a237e; margin-bottom:10px">El Mapa de tu Cielo</h1><p style="font-style:italic; color:#7f8c8d; font-size:18px">Análisis Astrológico para {nombre}</p><p style="font-size:13px; color:#bdc3c7">{fecha}</p></div>')

    ASC_lon = carta_activa.get('ASC')
    if ASC_lon is not None:
        asc_sig = _signo(ASC_lon)
        rows_asc = get_planeta('ASC', asc_sig, 1)
        if rows_asc:
            sec.append(f'<div style="margin-bottom:50px"><h2 style="font-variant:small-caps; border-bottom:1px solid #eee; color:#1a237e">I. El Amanecer de la Personalidad</h2><p style="font-size:17px; line-height:1.8; text-align:justify">Tu viaje comienza con el <b>Ascendente en {asc_sig}</b>. Esta es la máscara que portas ante el mundo y el filtro a través del cual percibes la realidad. {rows_asc[0][1]}</p></div>')

    sec.append('<h2 style="font-variant:small-caps; border-bottom:1px solid #eee; color:#1a237e; margin-top:60px">II. La Configuración de las Fuerzas</h2>')
    for pname in ORDEN:
        if pname not in planets_lon: continue
        lon = planets_lon[pname]; sig = _signo(lon); casa = _casa(lon, cusps)
        rows = get_planeta(pname, sig, casa)
        if not rows: continue
        texto_unificado = " ".join([r[1] for r in rows])
        sec.append(f'<div style="margin-bottom:35px"><h3 style="color:#283593; font-size:20px; margin-bottom:10px">{pname} en {sig} <span style="font-weight:normal; color:#95a5a6; font-size:14px"> (Casa {casa})</span></h3><div style="display:flex; justify-content:space-between; align-items:flex-start"><p style="font-size:16px; line-height:1.7; text-align:justify; flex:1">{texto_unificado}</p><span class="gemini-trigger" onclick="modernizarConGemini(this)" style="cursor:pointer; margin-left:15px; font-size:18px">✨</span></div><div class="txt-original" style="display:none">{texto_unificado}</div></div>')

    sec.append('<h2 style="font-variant:small-caps; border-bottom:1px solid #eee; color:#1a237e; margin-top:60px">III. El Diálogo de los Astros</h2>')
    planet_list = [(n, planets_lon[n]) for n in ORDEN if n in planets_lon]
    for i in range(len(planet_list)):
        for j in range(i+1, len(planet_list)):
            n1, lon1 = planet_list[i]; n2, lon2 = planet_list[j]
            ang = abs(lon1-lon2)%360; asp_s, orb = _asp_short(ang if ang<=180 else 360-ang)
            if not asp_s: continue
            row = get_aspecto(n1, n2, asp_s)
            if row:
                sec.append(f'<div style="margin-bottom:25px; padding-left:20px; border-left:2px solid #f0f0f0"><p style="font-size:15px; line-height:1.6; text-align:justify"><b style="color:#283593">{n1} y {n2}</b> en diálogo dinámico: {row[1]}</p><div class="txt-original" style="display:none">{row[1]}</div></div>')

    sec.append('</div>')
    return "\n".join(sec)

def generar_informe_sinastria(c1, c2, orbe=6):
    n1 = c1.get('nombre','Persona 1'); n2 = c2.get('nombre','Persona 2')
    lons1 = c1.get('planets', {}); lons2 = c2.get('planets', {})
    if c1.get('ASC'): lons1['ASC'] = c1['ASC']
    if c2.get('ASC'): lons2['ASC'] = c2['ASC']
    ORDEN = ['Sol','Luna','Mercurio','Venus','Marte','Jupiter','Saturno','Urano','Neptuno','Pluton','ASC']
    
    sec = [f'<div style="max-width:800px; margin:0 auto; font-family:\'Georgia\', serif; color:#2c3e50; background:#fff; padding:40px; border:1px solid #eee; box-shadow:0 10px 30px rgba(0,0,0,0.05)">']
    sec.append(f'<div style="text-align:center; border-bottom:1px double #ccc; padding-bottom:30px; margin-bottom:40px"><h1 style="font-size:32px; color:#4a148c; margin-bottom:10px">Vínculos Celestiales</h1><p style="font-style:italic; color:#7f8c8d; font-size:18px">Sinastría: {n1} ↔ {n2}</p></div>')

    bloques = []
    for p1 in ORDEN:
        if p1 not in lons1: continue
        for p2 in ORDEN:
            if p2 not in lons2: continue
            ang = abs(lons1[p1]-lons2[p2])%360; asp_s, orb = _asp_short(ang if ang<=180 else 360-ang, orbe=orbe)
            if not asp_s: continue
            row = get_sinastria(p1, p2, asp_s)
            if row: bloques.append((orb, p1, p2, asp_s, row[1]))

    bloques.sort(key=lambda x: x[0])
    for orb, p1, p2, asp, txt in bloques:
        sec.append(f'<div style="margin-bottom:30px"><h3 style="color:#4a148c; font-size:18px">{p1} ({n1}) ↔ {p2} ({n2})</h3><p style="font-size:16px; line-height:1.7; text-align:justify">{txt}</p></div>')
    
    if not bloques: sec.append('<p style="text-align:center; color:#999">No se han detectado aspectos significativos en esta unión.</p>')
    sec.append('</div>')
    return "\n".join(sec)

def generar_informe_rs(c_natal, c_rs):
    nombre = c_natal.get('nombre', 'Consultante'); anio = c_rs.get('anio_rs', '')
    planets_rs = c_rs.get('planets', {}); cusps_n = c_natal.get('cusps', [i*30 for i in range(12)])
    ORDEN = ['Sol','Luna','Mercurio','Venus','Marte','Jupiter','Saturno','Urano','Neptuno','Pluton']
    
    sec = [f'<div style="max-width:800px; margin:0 auto; font-family:\'Georgia\', serif; color:#2c3e50; background:#fff; padding:40px; border:1px solid #eee; box-shadow:0 10px 30px rgba(0,0,0,0.05)">']
    sec.append(f'<div style="text-align:center; border-bottom:1px double #ccc; padding-bottom:30px; margin-bottom:40px"><h1 style="font-size:32px; color:#1b5e20; margin-bottom:10px">El Retorno del Sol</h1><p style="font-style:italic; color:#7f8c8d; font-size:18px">Revolución Solar {anio} — {nombre}</p></div>')

    for pname in ORDEN:
        if pname not in planets_rs: continue
        casa_n = _casa(planets_rs[pname], cusps_n)
        row = get_planeta_rev(pname, casa_n)
        if row:
            sec.append(f'<div style="margin-bottom:30px"><h3 style="color:#1b5e20; font-size:19px">{pname} en Casa Natal {casa_n}</h3><p style="font-size:16px; line-height:1.7; text-align:justify">{row[1]}</p></div>')
    
    sec.append('</div>')
    return "\n".join(sec)

def generar_informe_transitos(natal_lons, planets_trans, fecha_str):
    ORDEN_T = ['Sol','Luna','Mercurio','Venus','Marte','Jupiter','Saturno','Urano','Neptuno','Pluton']
    ORDEN_N = ['Sol','Luna','Mercurio','Venus','Marte','Jupiter','Saturno','Urano','Neptuno','Pluton','NodoN']
    
    sec = [f'<div style="max-width:800px; margin:0 auto; font-family:\'Georgia\', serif; color:#2c3e50; background:#fff; padding:40px; border:1px solid #eee; box-shadow:0 10px 30px rgba(0,0,0,0.05)">']
    sec.append(f'<div style="text-align:center; border-bottom:1px double #ccc; padding-bottom:30px; margin-bottom:40px"><h1 style="font-size:32px; color:#1565c0; margin-bottom:10px">Climas Celestiales</h1><p style="font-style:italic; color:#7f8c8d; font-size:18px">Tránsitos para el {fecha_str}</p></div>')

    aspectos = []
    for pt in ORDEN_T:
        if pt not in planets_trans: continue
        for pn in ORDEN_N:
            if pn not in natal_lons: continue
            ang = abs(planets_trans[pt]['lon'] - natal_lons[pn]) % 360
            asp_s, orb = _asp_short(ang if ang<=180 else 360-ang, orbe=2 if pt in ['Sol','Luna'] else 3)
            if asp_s:
                row = get_transito(pt, pn, asp_s)
                if row: aspectos.append((orb, pt, pn, asp_s, row[1]))

    aspectos.sort(key=lambda x: x[0])
    for orb, pt, pn, asp, txt in aspectos:
        sec.append(f'<div style="margin-bottom:25px; border-left:3px solid #1565c0; padding-left:15px"><p style="font-size:15px; line-height:1.6; text-align:justify"><b style="color:#1565c0">{pt} transitante</b> sobre tu <b>{pn} natal</b>: {txt}</p></div>')
    
    if not aspectos: sec.append('<p style="text-align:center; color:#999">No hay tránsitos mayores destacados para esta fecha.</p>')
    sec.append('</div>')
    return "\n".join(sec)

# --- Helpers DB ---
_PAREJA_CODE = {'Sol':'E','Luna':'L','Mercurio':'H','Venus':'V','Marte':'M','Jupiter':'J','Saturno':'S','Urano':'U','Neptuno':'N','Pluton':'P','NodoN':'D','ASC':'A','MC':'C'}
_PAREJA_TIPO = {'Conj':'B','Trig':'B','Sext':'B','Cuad':'M','Opoc':'M'}

def get_sinastria(p1_dash, p2_dash, asp_dash):
    c1 = _PAREJA_CODE.get(p1_dash); c2 = _PAREJA_CODE.get(p2_dash); t = _PAREJA_TIPO.get(asp_dash)
    if not c1 or not c2 or not t: return None
    conn = _conn(); cur = conn.cursor()
    for key in (f'{c1}{c2}{t}', f'{c2}{c1}{t}'):
        cur.execute("SELECT cabecera,texto FROM interpretaciones WHERE fichero='PAREJA.ASC' AND cabecera=?", (f'Sinastría {key}',))
        row = cur.fetchone()
        if row: conn.close(); return row
    conn.close(); return None

def get_transito(p_trans, p_natal, asp_dash):
    p1 = PLANET_MAP.get(p_trans, p_trans); p2 = PLANET_MAP.get(p_natal, p_natal)
    asp = ASPECT_MAP.get(asp_dash, asp_dash)
    conn = _conn(); cur = conn.cursor()
    # Prioridad 1: Texto específico de Tránsitos Kepler 4 (PLAN4.TRT)
    cur.execute("""SELECT cabecera, texto FROM interpretaciones 
                   WHERE fichero='PLAN4.TRT' AND planeta1=? AND planeta2=? AND aspecto=? 
                   LIMIT 1""", (p1, p2, asp))
    row = cur.fetchone()
    if not row:
        # Prioridad 2: Kepler 7.0 (Trint1.tcs)
        cur.execute("""SELECT cabecera, texto FROM interpretaciones 
                       WHERE fichero='Trint1.tcs' AND planeta1=? AND planeta2=? AND aspecto=? 
                       LIMIT 1""", (p1, p2, asp))
        row = cur.fetchone()
    if not row:
        # Prioridad 3: Texto de aspectos natales (Kepler 4)
        cur.execute("""SELECT cabecera, texto FROM interpretaciones 
                       WHERE fichero='ASPECTOS.ASC' AND aspecto=? 
                       AND ((planeta1=? AND planeta2=?) OR (planeta1=? AND planeta2=?)) 
                       LIMIT 1""", (asp, p1, p2, p2, p1))
        row = cur.fetchone()
    conn.close(); return row
def get_planeta_rev(p, casa):
    p_db = PLANET_MAP.get(p, p); conn = _conn(); cur = conn.cursor()
    cur.execute("SELECT cabecera,texto FROM interpretaciones WHERE fichero='PLANETAS.REV' AND planeta1=? AND casa=? LIMIT 1", (p_db, casa))
    row = cur.fetchone(); conn.close(); return row
