import os

root = r"C:\Program Files (x86)\Kepler 4"
target = b"cohartado"

for r, d, files in os.walk(root):
    for f in files:
        path = os.path.join(r, f)
        try:
            with open(path, "rb") as fh:
                if target in fh.read():
                    print(f"¡ENCONTRADO en: {path}")
        except:
            pass
