# -*- coding: utf-8 -*-
import sqlite3
import re
import os

DB_PATH = r"C:\Users\Edu\Documents\GitHub\KeplerDB_Gemini\kepler.db"
TRINT_PATH = r"C:\KEPLER70\Trint1.tcs"
ENC = "cp850"

PLANET_MAP_EN = {
    'Sun':'Sol', 'Moon':'Luna', 'Mercury':'Mercurio', 'Venus':'Venus', 'Mars':'Marte',
    'Jupiter':'Jupiter', 'Saturn':'Saturno', 'Uranus':'Urano', 'Neptune':'Neptuno', 'Pluto':'Pluton'
}
ASP_MAP_EN = {
    'conjunction':'Conjunción', 'sextile':'Armónico', 'trine':'Armónico',
    'square':'Tensión', 'opposition':'Tensión'
}

def inyectar_transitos():
    if not os.path.exists(TRINT_PATH):
        print(f"Error: No se encuentra {TRINT_PATH}")
        return

    raw = open(TRINT_PATH, 'rb').read().decode(ENC, errors='replace')
    
    # Expresión regular para capturar bloques entre * y @
    # Estructura: * Planeta1 aspecto Planeta2 \n Texto @
    bloques = re.findall(r'\*\s*(.*?)\n(.*?)\@', raw, re.DOTALL)
    print(f"Detectados {len(bloques)} bloques de tránsito.")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    inyectados = 0
    for cab, texto in bloques:
        cab = cab.strip()
        texto = re.sub(r'\s+', ' ', texto).strip()
        
        # Intentar parsear Planeta1 Aspecto Planeta2
        # Ej: "Sun conjunction Moon"
        partes = cab.split(' ')
        if len(partes) >= 3:
            p1_en = partes[0]
            asp_en = partes[1]
            p2_en = partes[2]
            
            p1 = PLANET_MAP_EN.get(p1_en)
            p2 = PLANET_MAP_EN.get(p2_en)
            asp = ASP_MAP_EN.get(asp_en)
            
            if p1 and p2 and asp:
                cur.execute("""
                    INSERT INTO interpretaciones (fichero, indice, cabecera, texto, planeta1, planeta2, aspecto)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, ('Trint1.tcs', inyectados + 1, f"Tránsito {cab}", texto, p1, p2, asp))
                inyectados += 1

    conn.commit()
    conn.close()
    print(f"Inyección completada: {inyectados} registros nuevos en interpretaciones.")

if __name__ == "__main__":
    inyectar_transitos()
