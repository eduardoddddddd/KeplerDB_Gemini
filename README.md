---
title: KeplerDB Gemini Edition
emoji: 🔭
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
---

# KeplerDB Gemini Edition 🔭✨

Esta es una versión evolucionada y modernizada del proyecto **KeplerDB**, diseñada para llevar el legado astrológico de **Kepler 4** (Miguel García, 1985) al siguiente nivel mediante Inteligencia Artificial y tecnologías web de vanguardia.

## 🚀 Novedades de la Edición Gemini

### 1. 🤖 Cerebro IA Local (Sin APIs)
Hemos integrado un **Motor de Síntesis Evolutiva** en Python que actúa como un astrólogo analista. 
- **Interpretación Profunda:** Una nueva pestaña que genera informes holísticos de unas 800-1000 palabras, uniendo Sol, Luna, Ascendente y aspectos en una narrativa coherente.
- **Modernizador ✨:** Cada párrafo clásico de 1985 incluye ahora un botón para recibir una "visión evolutiva" instantánea.
- **100% Privado y Offline:** No requiere conexión a internet ni API Keys externas (Google Gemini API).

### 2. 📖 Estilo Narrativo "Novela"
Olvídate de las tablas rígidas y los bloques técnicos. 
- La presentación ha sido rediseñada para leerse como un **manuscrito astrológico fluido**.
- Los textos de signo y casa se "cosen" automáticamente para crear una lectura continua y humana.
- Estilo aplicado a: Carta Natal, Sinastría, Tránsitos y Revolución Solar.

### 3. 🌍 Buscador Geográfico Inteligente
Sistema híbrido de localización de ciudades:
- **Local:** Busca instantáneamente entre las **8,502 cartas históricas** de la base de datos Kepler.
- **Global:** Integración con **OpenStreetMap (Nominatim)** para encontrar cualquier pueblo o ciudad del mundo.
- **Autocompletado:** Rellena automáticamente Latitud, Longitud y Offset GMT.

### 4. 🔵 Rueda SVG Interactiva
Hemos sustituido la imagen estática por un motor de visualización dinámico:
- **Tooltips:** Pasa el ratón por cualquier planeta para ver su posición exacta y dignidades.
- **Interactividad:** La rueda se adapta en tiempo real y mantiene la precisión astronómica del motor Swiss Ephemeris.

### 5. 📱 PWA y Persistencia Total
- **Instalable:** Puedes añadir KeplerDB a tu móvil o PC como si fuera una App nativa.
- **LocalStorage:** Tus cartas guardadas no se suben a la nube; se quedan en tu dispositivo para siempre, garantizando privacidad y acceso offline.

---

## 🛠️ Instalación y Uso Local

1. **Clonar y Preparar:**
   ```bash
   git clone https://github.com/Eduxx76/KeplerDB_Gemini
   cd KeplerDB_Gemini
   pip install -r requirements.txt
   ```

2. **Arrancar:**
   Ejecuta `py -X utf8 app/app.py` o usa el script `ARRANCAR.bat`.
   La app se abrirá en `http://localhost:7860`.

3. **Sincronizar:**
   Usa `PUSH_ALL.bat` para subir tus cambios a GitHub y Hugging Face simultáneamente.

---

## ☁️ Despliegue Cloud
Esta edición está optimizada para **Hugging Face Spaces** mediante Docker. 
- **LFS:** El archivo `kepler.db` se gestiona vía Git Large File Storage.
- **Puerto:** Configurado en el estándar `7860`.

---
*Transformando la tradición astrológica con la inteligencia del futuro.* 🌌🚀
