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
