from src.langgraphagenticai.state.state import State


class BasicChatbotNode:
    """Single-step conversational node for LLM-based message processing and response generation."""
    
    def __init__(self, model):
        """Initialize chatbot node with specified language model.
        
        Args:
            model: Language model instance for inference.
        """
        self.llm = model

    def process(self, state: State) -> dict:
        """Process conversation state and generate LLM response.
        
        Args:
            state: Current conversation state containing message history.
            
        Returns:
            Updated state with LLM-generated response appended to message history.
        """
        return {"messages": self.llm.invoke(state['messages'])}

