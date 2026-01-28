from groq import Groq

class IAAssistant:
    def __init__(self):
        # Tu clave de Groq integrada
        self.api_key = "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"
        
        if self.api_key:
            # Groq es compatible con el formato de OpenAI, lo que lo hace muy robusto
            self.client = Groq(api_key=self.api_key)
            # Usamos Llama 3.3, uno de los modelos gratuitos más potentes actualmente
            self.model_id = "llama-3.3-70b-versatile"
        else:
            self.client = None

    def responder(self, pregunta, contexto_productos=""):
        if not self.client:
            return "Error: Clave de Groq no configurada correctamente."

        try:
            # Generamos la respuesta con contexto de tu inventario en MongoDB
            completion = self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {
                        "role": "system", 
                        "content": f"""Eres el asistente experto de 'ElectroShop'. 
                        Usa este inventario real para responder:
                        {contexto_productos}
                        
                        Instrucciones:
                        1. Sé amable y breve.
                        2. Si el producto existe, da el precio exacto.
                        3. Si no existe en la lista, ofrece una alternativa similar."""
                    },
                    {"role": "user", "content": pregunta}
                ],
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error con la IA de Groq: {str(e)}"