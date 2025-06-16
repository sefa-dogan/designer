import base64
import os
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)
from langgraph.graph import StateGraph,START,END
from graph.graph_consts import DESIGN,EXTRACT,TESTINGIMAGE
from graph.nodes.design import design
from graph.nodes.extract_furniture import extract_furniture
from graph.nodes.testing_image import testing_image
from IPython.display import Image, display

from graph.state import GraphState

def check_correct_design(state:GraphState):
    if(state["correct_design"]=="no"):
        return DESIGN
    else:
        print("DONE")
        return END
    

workflow=StateGraph(GraphState)

workflow.add_node(DESIGN,design)
workflow.add_node(EXTRACT,extract_furniture)
workflow.add_node(TESTINGIMAGE,testing_image)

workflow.add_edge(START,EXTRACT)
workflow.add_edge(EXTRACT,DESIGN)
workflow.add_edge(DESIGN,TESTINGIMAGE)
workflow.add_conditional_edges(TESTINGIMAGE,check_correct_design)

app = workflow.compile()

# raw_image_base64=""
# with open(os.path.join(ROOT_DIR, "ytkodsi-raw-image-ing.jpeg"), "rb") as raw_image:
#     raw_image_base64 = base64.b64encode(raw_image.read()).decode("utf-8") 
    
# graph_result=app.invoke(input={"encoded_raw_image":raw_image_base64})

# print(graph_result["encoded_processed_image"])
# base64_string = graph_result["encoded_processed_image"]
# base64_string = base64_string.split(',')[-1]
# # Dosyaya yazılacak çıktı dosya adı (uzantıya dikkat!)
# output_file = "output_image.png"

# # Base64 string'ini decode edip dosyaya yaz
# with open(output_file, "wb") as f:
#     f.write(base64.b64decode(base64_string))