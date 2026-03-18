from typing import Annotated, Literal, Optional
from typing_extensions import TypedDict
from langgraph.graph import add_messages
from typing import TypedDict, Annotated, List
from langchain_core.messages import HumanMessage, AIMessage

class State(TypedDict):
    """
    Represents the structure of the state used in the graph
    """

    messages: Annotated[list, add_messages]