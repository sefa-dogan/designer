import base64
import os
import sys
from typing import Dict
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOT_DIR)
from graph.chains.extract_furnitures_chain import extract_furniture_chain
from graph.state import GraphState
# raw_image_base64=""
# with open(os.path.join(ROOT_DIR, "lsch.jpeg"), "rb") as raw_image:
#     raw_image_base64 = base64.b64encode(raw_image.read()).decode("utf-8") 

def extract_furniture(state:GraphState)->Dict[str,any]:
    raw_image = state["encoded_raw_image"]
    response =extract_furniture_chain.invoke({
        "raw_image_base64":raw_image
    })
    print("EXTRACTED")
    # print(response)
    return {"items":response.furniturelist}