from langgraph.graph import StateGraph
from src.langgraphagenticai.state.state import State
from langgraph.graph import START, END
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode


class GraphBuilder:
    """Manages LangGraph workflow construction and execution for multi-step reasoning tasks."""
    
    def __init__(self, model):
        """Initialize graph builder with specified LLM model.
        
        Args:
            model: Language model instance for inference.
        """
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        """Construct basic conversational agent graph with single-step processing.
        
        Adds chatbot node as entry and exit points, creating a simple message-to-response flow.
        """
        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def setup_graph(self, usecase: str):
        """Compile and return executable graph for specified use case.
        
        Args:
            usecase: String identifier for the workflow type (e.g., "Basic Chatbot").
            
        Returns:
            Compiled LangGraph ready for execution.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()

        return self.graph_builder.compile()
