import base64
import sys
import os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOT_DIR)
from PIL import Image
from io import BytesIO
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from core.base64_extraction import extract_base64_image
from graph.state import GraphState
from typing import Dict,Any

load_dotenv()

class ResponseFormatter(BaseModel):
    """Always use this tool to structure your response to the user."""
    encodedImage: str = Field(description="Processed image as base64 format")

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.0-flash-exp-image-generation",
    temperature=1
)
# structuredLlm=llm.with_structured_output(ResponseFormatter)
raw_image_base64=""
with open(os.path.join(ROOT_DIR, "lsch.jpeg"), "rb") as raw_image:
    raw_image_base64 = base64.b64encode(raw_image.read()).decode("utf-8") 
message = {
    "role": "user",
    "content": [
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{raw_image_base64}"},
        },
        {
            "type": "text",
            "text": """
   I am giving you a photo of a room and the writings on this photo indicate the objects and their location. Place these objects in the room in an appropriate manner, also paying attention to perspective.\n
While doing this, you should never remove or move anything from the room.
While doing this, you should never change features of room
                                         
""",
        },
    ],
}
def design_chain(state:GraphState)->Dict[str,any]:
    response = llm.invoke(
        [message],
        generation_config=dict(response_modalities=["TEXT", "IMAGE"]),
    )

    processedImage=extract_base64_image(response=response)
    with open("decoded_output.txt", "w", encoding="utf-8") as f:
        f.write(str(response))
    image_base64 = processedImage.split(",")[-1]
    image_data_base64 = base64.b64decode(image_base64)

    with open("generated_image.png", "wb") as f:
        f.write(image_data_base64)
    print("Image has been saved as 'generated_image.png'")

    image = Image.open(BytesIO(image_data_base64))
    return {"encoded_processed_image":image_data_base64}
# image.show()