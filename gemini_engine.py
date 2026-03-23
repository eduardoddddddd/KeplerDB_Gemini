# -*- coding: utf-8 -*-
import re

class GeminiEngine:
    """
    Motor de transformación semántica para modernizar textos astrológicos clásicos.
    Reencuadra interpretaciones deterministas (Kepler 4) hacia un enfoque 
    psicológico, evolutivo y de empoderamiento.
    """
    
    # Mapeo de términos clásicos a conceptos modernos/evolutivos
    TRANSFORMACIONES = {
        r'\bmal[oa]\b': 'desafiante',
        r'\bpeligro\b': 'oportunidad de aprendizaje',
        r'\benemigo[s]?\b': 'maestros ocultos o proyecciones',
        r'\bsuerte\b': 'sincronicidad o flujo',
        r'\bdesgracia\b': 'crisis de transformación',
        r'\bpobreza\b': 'bloqueo de abundancia',
        r'\bmuerte\b': 'final de un ciclo o transmutación profunda',
        r'\benfermedad\b': 'somatización o necesidad de cuidado',
        r'\bmatrimonio\b': 'vínculo de compromiso o asociación',
        r'\bhijo[s]?\b': 'creaciones o legados',
        r'\bguerra\b': 'conflicto interno o lucha por la autoafirmación',
        r'\bpoder\b': 'empoderamiento personal',
        r'\blujuria\b': 'pasión creativa o intensidad vincular',
        r'\bvicio[s]?\b': 'patrones repetitivos o mecanismos de evasión',
        r'\bvirtud\b': 'talento innato o fortaleza interior',
    }

    INTRODUCCIONES = [
        "Desde una perspectiva evolutiva, esta configuración sugiere...",
        "Gemini observa que este aspecto te invita a...",
        "Más allá de la interpretación clásica, aquí reside un potencial para...",
        "A nivel psicológico, este patrón se manifiesta como...",
        "Tu alma busca integrar esta energía a través de..."
    ]

    def modernizar(self, texto):
        if not texto or len(texto) < 5:
            return texto
            
        # 1. Limpieza básica
        t = texto.strip()
        
        # 2. Aplicar transformaciones semánticas
        for pattern, replacement in self.TRANSFORMACIONES.items():
            t = re.sub(pattern, replacement, t, flags=re.IGNORECASE)
            
        # 3. Suavizar lenguaje determinista
        t = t.replace("será", "tiende a manifestarse como")
        t = t.replace("tendrá", "podría desarrollar")
        t = t.replace("es ", "se expresa a menudo como ")
        t = t.replace("debe ", "se le invita a ")
        
        # 4. Añadir matiz de "Gemini"
        import random
        intro = random.choice(self.INTRODUCCIONES)
        
        # 5. Estructurar respuesta
        resultado = f"<i>✨ <b>Visión de Gemini:</b> {intro}</i><br><br>{t}"
        
        return resultado

    def resumen_holistico(self, datos):
        """
        Sintetiza los puntos clave de la carta en un resumen ejecutivo.
        """
        planetas = datos.get('tabla', [])
        asc = datos.get('asc', '')
        mc = datos.get('mc', '')
        
        # Encontrar Sol, Luna y ASC
        sol = next((p for p in planetas if p['planeta'] == 'Sol'), None)
        luna = next((p for p in planetas if p['planeta'] == 'Luna'), None)
        
        resumen = f"<h3>🌟 Síntesis Holística de Gemini</h3>"
        resumen += f"<p>Esta carta presenta una dinámica fascinante. Con el <b>Ascendente en {asc.split('°')[1][:3]}</b>, la puerta de entrada a tu experiencia vital es de naturaleza receptiva y proyectiva a la vez.</p>"
        
        if sol:
            resumen += f"<p>Tu <b>Sol en {sol['signo']}</b> (Casa {sol['casa']}) indica que tu esencia brilla a través de la autoexpresión y el propósito consciente. </p>"
            
        if luna:
            resumen += f"<p>Emocionalmente, tu <b>Luna en {luna['signo']}</b> sugiere una necesidad profunda de seguridad a través de la introspección y el cuidado de tus raíces emocionales.</p>"
            
        resumen += "<br><b>💡 Recomendación Evolutiva:</b> Honra el equilibrio entre tu voluntad consciente y tus necesidades instintivas para integrar esta potente configuración."
        
        return resumen

# Instancia global
engine = GeminiEngine()
