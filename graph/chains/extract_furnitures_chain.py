from typing import List,TypedDict
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class ResponseFormatter(BaseModel):
    """Always use this tool to structure your response to the user."""
    furniturelist:List[str]=Field(description="list of all furniture names in the image")
    
parser = PydanticOutputParser(pydantic_object=ResponseFormatter)

load_dotenv()
llm=ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp-image-generation",
    temperature=0
)

def build_multimodal_prompt(raw_image_base64: str):
    return [
        {
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
                "text": f"""
You are an extractor that extract all furniture text inside given image to you.\n
You should extract all furniture texts in the image above\n

{parser.get_format_instructions()}"""
            },
        ],
    }]
prompt_builder=RunnableLambda(
    lambda inputs: build_multimodal_prompt(
        
        inputs["raw_image_base64"],
        
    )
)

extract_furniture_chain=prompt_builder | RunnableLambda(
    lambda prompt: llm.invoke(
        prompt,
        generation_config={"response_modalities": ["TEXT", "IMAGE"]}
    )
)|parser
