import base64
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import datetime

load_dotenv()
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

OUTPUT_DIR = Path(f"output")
OUTPUT_DIR.mkdir(exist_ok=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

##
# Text - Using the Chat Completions API instead of Response API
##

print("📝 OpenAI Text")

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text":"""Você é uma escritora especialista em literatura infantil.
                    Você irá receber diversos temas do usuário e deverá criar histórias curtas de 9 a 12 linhas que abordem tais temas.
                    Você tem um tom didático, descomplicado e amigável."""
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": """Gere uma história com os seguintes temas:
            - Higiene pessoal
            - Dentes
            - Rotina noturna"""
        }
      ]
    }
  ],
  temperature=1,
  max_tokens=450,
  response_format={
    "type": "text"
  }
)

historia = response.choices[0].message.content
print(historia)

with open(f"{OUTPUT_DIR}/{timestamp}-01-historia-text.txt", "w", encoding="utf-8") as f:
    f.write(historia)


##
# Audio (TTS)
##

print("\n🎤 OpenAI Audio (TTS - Text-to-Speech)")

speech_file_path = f"{OUTPUT_DIR}/{timestamp}-02-historia-audio.mp3"
with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="fable",
    input=historia,
    instructions="Fale com tom descomplicado e amigável digirido para uma criança.",
) as response:
    response.stream_to_file(speech_file_path)


##
# Images - DALL-E 3
##

print("\n🏞️ OpenAI Images (DALL-E 3)")

prompt=f"""Gere uma imagem ficticia baseada na história infantil abaixo. 
A imagem deve contar a história através de ilustrações inspiradas no texto. 
A imagem deve usar um estilo de ilustração infantil.

<historia>
    {historia}
</historia>
"""

result = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    response_format="b64_json"
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# Save the image to a file
with open(f"{OUTPUT_DIR}/{timestamp}-03-historia-image-dalle3.png", "wb") as f:
    f.write(image_bytes)