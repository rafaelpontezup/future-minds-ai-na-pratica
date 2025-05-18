import base64
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import datetime


OUTPUT_DIR = Path(f"output")
OUTPUT_DIR.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

##
# Text
##

print("📝 OpenAI Text")

response = client.responses.create(
    model="gpt-4o-mini",
    instructions="""Você é uma escritora especialista em literatura infantil.
                    Você irá receber diversos temas do usuário e deverá criar histórias curtas de 9 a 12 linhas que abordem tais temas.
                    Você tem um tom didático, descomplicado e amigável.""",
    input="""Gere uma história com os seguintes temas:
            - Fada do dente
            - Doces
            - Rotina noturna""",
    temperature=1,
    max_output_tokens=450,
)

historia = response.output_text
print(historia)

textual_file_path = OUTPUT_DIR / f"{timestamp}-01-historia-text.txt"
with open(textual_file_path, "w", encoding="utf-8") as f:
    f.write(historia)


##
# Audio (TTS)
##

print("\n🎤 OpenAI Audio (TTS - Text-to-Speech)")

speech_file_path = OUTPUT_DIR / f"{timestamp}-02-historia-audio.mp3"
with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="fable",
    input=historia,
    instructions="Fale com tom descomplicado e amigável digirido para uma criança.",
) as response:
    response.stream_to_file(speech_file_path)


##
# Images
##

print("\n🏞️ OpenAI Images")

prompt=f"""Gere uma imagem ficticia baseada na história infantil abaixo. 
A imagem deve contar a história através de ilustrações inspiradas no texto. 
A imagem deve usar um estilo de ilustração infantil.

<historia>
    {historia}
</historia>
"""
result = client.images.generate(
    model="gpt-image-1",
    prompt=prompt,
    quality="medium",
    size="1024x1024",
    # moderation="low",
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# Save the image to a file
image_file_path = OUTPUT_DIR / f"{timestamp}-03-historia-image.png"
with open(image_file_path, "wb") as f:
    f.write(image_bytes)