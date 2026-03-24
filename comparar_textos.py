# -*- coding: utf-8 -*-
import sqlite3
import os

DB_PATH = r"C:\Users\Edu\Documents\GitHub\KeplerDB_Gemini\kepler.db"

def comparar():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Buscamos el texto de Venus en aspecto Armónico (Trígono/Sextil) a Venus
    # En Kepler 4, 'Favorable' suele mapearse a 'Armónico' en la DB
    cur.execute("""
        SELECT cabecera, texto 
        FROM interpretaciones 
        WHERE planeta1='Venus' AND planeta2='Venus' AND aspecto='Armónico'
        LIMIT 1
    """)
    
    res = cur.fetchone()
    conn.close()
    
    print("--- RESULTADO DE TU BASE DE DATOS (kepler.db) ---")
    if res:
        print(f"Cabecera: {res[0]}")
        print(f"Texto: {res[1]}")
    else:
        print("No se encontró el texto exacto.")

    print("\n--- TEXTO EN KEPPPLER.TXT (Original) ---")
    print("Tendrá mucho éxito en sus relaciones sociales. Ocurrirá algo que le hará estar más unido a su pareja. En general será un momento de tranquila felicidad. Estará dispuesto a disfrutar de los placeres que se le brinden y de las cosas bellas.")

comparar()
