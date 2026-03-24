# -*- coding: utf-8 -*-
import sqlite3

DB_PATH = r"C:\Users\Edu\Documents\GitHub\KeplerDB_Gemini\kepler.db"

def buscar_frase():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    frase = "%mucho éxito en sus relaciones sociales%"
    cur.execute("SELECT fichero, cabecera, planeta1, planeta2, aspecto, texto FROM interpretaciones WHERE texto LIKE ?", (frase,))
    
    rows = cur.fetchall()
    conn.close()
    
    for r in rows:
        print(f"Fichero: {r[0]}")
        print(f"Cabecera: {r[1]}")
        print(f"Planetas: {r[2]} - {r[3]}")
        print(f"Aspecto: {r[4]}")
        print(f"Texto: {r[5][:100]}...")
        print("-" * 30)

buscar_frase()
