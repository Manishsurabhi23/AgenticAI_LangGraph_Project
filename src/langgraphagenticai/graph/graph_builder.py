from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.prompts import ChatPromptTemplate
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.nodes.chatbot_with_Tool_node import ChatbotWithToolNode
from src.langgraphagenticai.tools.search_tool import get_tools, create_tool_node
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode


class GraphBuilder:

    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)  # fresh graph on every setup

    def basic_chatbot_build_graph(self):
        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def chatbot_with_tools_build_graph(self):
        tools = get_tools()
        tool_node = create_tool_node(tools)

        obj_chatbot_with_node = ChatbotWithToolNode(self.llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools)

        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")

    def ai_news_build_graph(self):
        ai_news_node = AINewsNode(self.llm)

        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result", ai_news_node.save_result)

        self.graph_builder.add_edge(START, "fetch_news")  # use START instead of set_entry_point
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)

    def setup_graph(self, usecase: str):
        try:
            usecase = usecase.strip()
            self.graph_builder = StateGraph(State)  # reset graph on every call

            if usecase == "Basic Chatbot":
                self.basic_chatbot_build_graph()
            elif usecase == "Chatbot with Tool":
                self.chatbot_with_tools_build_graph()
            elif usecase == "AI News":
                self.ai_news_build_graph()
            else:
                raise ValueError(f"Unknown usecase: '{usecase}'. Expected one of: 'Basic Chatbot', 'Chatbot with Tool', 'AI News'")

            return self.graph_builder.compile()

        except ValueError as e:
            raise ValueError(f"Graph setup failed - {e}")
        except Exception as e:
            raise RuntimeError(f"Graph setup failed - {e}")