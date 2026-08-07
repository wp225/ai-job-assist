from langgraph.graph import StateGraph
from ..models.pipeline_state import PipelineState
from .cv_parser_node import cv_parser

def create_cv_parsing_graph():
    """Create graph with just cv_parser node"""
    graph = StateGraph(PipelineState)
    
    graph.add_node("cv_parser", cv_parser)
    graph.set_entry_point("cv_parser")
    graph.set_finish_point("cv_parser")
    
    return graph.compile()

# Create compiled graph
cv_parsing_graph = create_cv_parsing_graph()