import base64
import os
import sys
from typing import Dict
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOT_DIR)
from graph.chains.image_grader import image_grader
from graph.state import GraphState
# processed_image_base64=""
# with open(os.path.join(ROOT_DIR, "ls.jpeg"), "rb") as processed_image:
#     processed_image_base64 = base64.b64encode(processed_image.read()).decode("utf-8") 

def testing_image(state:GraphState)->Dict[str,any]:
    processed_image = state["encoded_processed_image"]
    items = state["items"]
    response =image_grader.invoke({
        "processed_image_base64":processed_image,
        "items":items
    })
    print("TESTED")
    return {"correct_design":response.placedAllFurnitures}
    