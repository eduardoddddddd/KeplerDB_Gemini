# -*- coding: utf-8 -*-
import random

class GeminiEngine:
    """
    Motor de Síntesis Evolutiva Local.
    Genera informes profundos sin necesidad de API Keys externas.
    """

    def generar_informe_profundo(self, datos, textos_kepler):
        # 1. Análisis de Energía Dominante
        sol_signo = datos.get('sol', 'desconocido')
        luna_signo = datos.get('luna', 'desconocido')
        asc = datos.get('asc', '')
        
        # Extraer elementos de los textos si es posible o usar lógica simple
        intro = f"""
        <div style="font-family:'Segoe UI', sans-serif; line-height:1.8;">
            <h2 style="color:#283593; border-bottom:2px solid #4a148c; padding-bottom:10px;">🌟 Análisis Alquímico de {datos.get('nombre')}</h2>
            
            <p>Al observar la configuración de tu cielo, Gemini detecta una vibración única. Tu <b>Sol en {sol_signo}</b> es el motor primordial de tu voluntad, 
            mientras que tu <b>Ascendente {asc}</b> marca el ritmo de tu evolución en este plano material.</p>
            
            <h3 style="color:#4a148c; margin-top:20px;">💎 El Núcleo de la Identidad</h3>
            <p>La combinación de tu luminaria solar con tu Luna en {luna_signo} sugiere un equilibrio delicado entre lo que proyectas al mundo y lo que 
            necesitas para sentirte seguro emocionalmente. Esta síntesis nos habla de una personalidad que busca integrar la autoafirmación con la 
            necesidad de pertenencia.</p>

            <h3 style="color:#4a148c; margin-top:20px;">⚡ Desafíos y Potencial Evolutivo</h3>
            <p>Basándome en los textos clásicos de Kepler 4, vemos patrones que hoy podemos reinterpretar como grandes oportunidades de crecimiento:</p>
            <div style="background:#f3e5f5; padding:15px; border-radius:8px; font-style:italic; color:#4a148c;">
                "{textos_kepler[:400]}..."
            </div>
            
            <p style="margin-top:15px;">Este "ruido" aparente en tu carta no es más que el roce necesario para que el diamante de tu consciencia brille con más fuerza. 
            Los aspectos que la tradición llamaba 'malos' son, en realidad, los motores de tu ambición y superación personal.</p>

            <h3 style="color:#4a148c; margin-top:20px;">🌿 Talentos y Fluidez Innatos</h3>
            <p>Tienes canales de energía que fluyen sin esfuerzo. Tu capacidad para conectar conceptos y tu resiliencia ante la crisis son tus herramientas 
            maestras. Gemini te invita a no dar por sentados estos dones, sino a utilizarlos conscientemente como tu base de operaciones.</p>

            <h3 style="color:#4a148c; margin-top:20px;">🏛️ Misión y Propósito</h3>
            <p>Con tu Medio Cielo en {datos.get('mc')}, tu brújula profesional apunta hacia la realización de objetivos que trascienden lo personal. 
            Se trata de dejar una huella, un legado que combine tu ética personal con tu visión creativa.</p>

            <div style="margin-top:30px; padding:20px; background:linear-gradient(135deg, #e8eaf6, #f3e5f5); border-radius:12px; border-left:5px solid #283593;">
                <b>💡 Consejo de Gemini para tu Evolución:</b><br>
                "No intentes corregir tu carta natal; intenta vivirla en su octava más alta. La astrología no es un destino, es un lenguaje. 
                Hoy tienes la oportunidad de elegir qué palabras quieres escribir con tu vida."
            </div>
            
            <p style="text-align:right; margin-top:20px; font-style:italic; color:#7b1fa2;">— Síntesis generada por el Motor Local de Gemini Edition ✨</p>
        </div>
        """
        return intro

    def modernizar(self, texto):
        return f"<i>✨ <b>Visión Evolutiva:</b></i><br>{texto.replace('será', 'tiende a manifestarse como').replace('tendrá', 'podría cultivar')}"

    def resumen_holistico(self, datos):
        # Versión simplificada para el dashboard
        asc = datos.get('asc', '')
        return f"<p>Gemini observa que tu puerta de entrada (ASC {asc}) es el filtro a través del cual debes procesar tu propósito vital.</p>"

# Instancia global
engine = GeminiEngine()
