from typing import List
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field




load_dotenv()



class ResponseFormatter(BaseModel):
    """Always use this tool to structure your response to the user."""
    placedAllFurnitures:str=Field(description="Are all the items on the list given in the given photo?'yes' or 'no'")
    
parser = PydanticOutputParser(pydantic_object=ResponseFormatter)

load_dotenv()
llm=ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp-image-generation",
    temperature=0
)

def build_multimodal_prompt(processed_image_base64: str,items:str):
    return [
        {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{processed_image_base64}"
                },
            },
            
            {
                "type": "text",
                "text": f"""
Are the items on the list given to you again in the photo again? If it is only 'yes', if not, just return 'no' result\n
Furniture list: {items}
{parser.get_format_instructions()}"""
            },
        ],
    }]
prompt_builder=RunnableLambda(
    lambda inputs: build_multimodal_prompt(
        inputs["processed_image_base64"],
        inputs["items"],
        
    )
)

image_grader=prompt_builder | RunnableLambda(
    lambda prompt: llm.invoke(
        prompt,
        generation_config={"response_modalities": ["TEXT", "IMAGE"]}
    )
)|parser
