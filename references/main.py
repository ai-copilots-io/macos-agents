import os

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI

def setup_proxy() -> None:
    os.environ["http_proxy"] = "http://127.0.0.1:2022"
    os.environ["https_proxy"] = "http://127.0.0.1:2022"
    os.environ["all_proxy"] = "socks5://127.0.0.1:2022"
    os.environ["no_proxy"] = "localhost,127.0.0.1"

    os.environ["HTTP_PROXY"] = "http://127.0.0.1:2022"
    os.environ["HTTPS_PROXY"] = "http://127.0.0.1:2022"
    os.environ["ALL_PROXY"] = "socks5://127.0.0.1:2022"
    os.environ["NO_PROXY"] = "localhost,127.0.0.1"


def main() -> None:
    setup_proxy()

    model = ChatOpenAI(
        use_responses_api=True,
        model="gpt-4o-mini",
    )
    tool = {"type": "web_search_preview"}
    model_with_tools = model.bind_tools([tool])

    lc_conversation_messages = [
        SystemMessage(content="You are a helpful weather assistant. Be brief."),
        HumanMessage(content="My name is Simon"),
        AIMessage(content="Hello Simon, nice to meet you. How can I help you today?"),
        HumanMessage(content="what is the weather in sf")
    ]
    
    for token in model_with_tools.stream(lc_conversation_messages):
        print(token.text(), end="")
    

if __name__ == "__main__":
    main()
