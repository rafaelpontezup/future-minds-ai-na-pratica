import base64
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import datetime


OUTPUT_DIR = Path(f"output-edit")
OUTPUT_DIR.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


##
# Images
##

print("\n🏞️ OpenAI Images | Studio Ghibli")

input_file = "eu-alberto-jordi.jpeg"
result = client.images.edit(
    model="gpt-image-1",
    prompt="Transforme essa imagem em uma ilustração parecida com os desenhos do studio Ghibli.",
    image=open(input_file, "rb"),
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# Save the image to a file
image_file_path = OUTPUT_DIR / f"{timestamp}-{input_file}.png"
with open(image_file_path, "wb") as f:
    f.write(image_bytes)