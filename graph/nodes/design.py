from typing import Dict

from core.base64_extraction import extract_base64_image
from graph.chains.design_chain import design_chain
from graph.state import GraphState

def design(state:GraphState)->Dict[str,any]:
    raw_image=state["encoded_raw_image"]
    response=design_chain.invoke({"raw_image_base64":raw_image},)
    processed_image=extract_base64_image(response)
    print("----------")
    print("DESIGN")
    print("----------------")
    return {"encoded_processed_image":processed_image}
