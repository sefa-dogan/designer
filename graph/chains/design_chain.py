import sys
import os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOT_DIR)
from langchain_core.runnables import RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv


load_dotenv()

class ResponseFormatter(BaseModel):
    """Always use this tool to structure your response to the user."""
    encodedImage: str = Field(description="Processed image as base64 format")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp-image-generation",
    temperature=1
)
# structuredLlm=llm.with_structured_output(ResponseFormatter)
# raw_image_base64=""
# with open(os.path.join(ROOT_DIR, "lsch.jpeg"), "rb") as raw_image:
#     raw_image_base64 = base64.b64encode(raw_image.read()).decode("utf-8") 
    

def build_multimodal_prompt(raw_image_base64: str):
    return [{
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{raw_image_base64}"
                },
            },
            {
                "type": "text",
                "text": """
            I am giving you a photo of a room and the writings on this photo indicate the objects and their location. Place these objects in the room in an appropriate manner, also paying attention to perspective.\n
     While doing this, you should never remove or move anything from the room.
     While doing this, you should never change features of room
     Create new image after analyze
            """,
            },
        ],
    }]
prompt_builder=RunnableLambda(
    lambda inputs: build_multimodal_prompt(
        inputs["raw_image_base64"], # type: ignore
        
    )
)
design_chain=prompt_builder | RunnableLambda(
    lambda prompt: llm.invoke(
        prompt, # type: ignore
        generation_config={"response_modalities": ["TEXT", "IMAGE"]}
    )
)
