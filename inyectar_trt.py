# -*- coding: utf-8 -*-
import sqlite3
import re
import os

DB_PATH = r"C:\Users\Edu\Documents\GitHub\KeplerDB_Gemini\kepler.db"
PLAN_PATH = r"C:\Program Files (x86)\Kepler 4\PLAN4.TRT"
ENC = "cp850"

P_MAP = {'S':'Sol','L':'Luna','H':'Mercurio','V':'Venus','M':'Marte','J':'Jupiter','S':'Saturno','U':'Urano','N':'Neptuno','P':'Pluton'}
# Nota: 'S' puede ser Sol o Saturno dependiendo de la posicion, pero en el codigo de 3 letras:
# La 1ra S suele ser Saturno. El Sol suele ser 'E' (Ente/Estrella).
P_CODE = {'E':'Sol','L':'Luna','H':'Mercurio','V':'Venus','M':'Marte','J':'Jupiter','S':'Saturno','U':'Urano','N':'Neptuno','P':'Pluton'}
ASP_CODE = {'C':'Conjunción', 'F':'Armónico', 'D':'Tensión'}

def inyectar_trt():
    if not os.path.exists(PLAN_PATH): return
    raw = open(PLAN_PATH, 'rb').read().decode(ENC, errors='replace')
    
    # Dividir por ==
    bloques = re.split(r'==', raw)
    inyectados = 0
    
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    
    for b in bloques:
        b = b.strip()
        if not b: continue
        lineas = b.split('\n')
        cod = lineas[0].strip() # Ej: VDE
        if len(cod) < 3: continue
        
        texto = " ".join([l.strip() for l in lineas[2:] if l.strip()])
        texto = re.sub(r'\s+', ' ', texto).strip()
        
        p1_c = cod[0]; asp_c = cod[1]; p2_c = cod[2]
        
        p1 = P_CODE.get(p1_c)
        p2 = P_CODE.get(p2_c)
        asp = ASP_CODE.get(asp_c)
        
        if p1 and p2 and asp:
            cur.execute("""
                INSERT INTO interpretaciones (fichero, indice, cabecera, texto, planeta1, planeta2, aspecto)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ('PLAN4.TRT', inyectados + 1, f"Tránsito {cod}", texto, p1, p2, asp))
            inyectados += 1

    conn.commit(); conn.close()
    print(f"Inyectados {inyectados} bloques desde PLAN4.TRT")

if __name__ == "__main__":
    inyectar_trt()
