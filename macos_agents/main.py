import os

from pydantic import BaseModel

from langgraph.graph import StateGraph, START, END

def setup_proxy() -> None:
    os.environ["http_proxy"] = "http://127.0.0.1:2022"
    os.environ["https_proxy"] = "http://127.0.0.1:2022"
    os.environ["all_proxy"] = "socks5://127.0.0.1:2022"
    os.environ["no_proxy"] = "localhost,127.0.0.1"

    os.environ["HTTP_PROXY"] = "http://127.0.0.1:2022"
    os.environ["HTTPS_PROXY"] = "http://127.0.0.1:2022"
    os.environ["ALL_PROXY"] = "socks5://127.0.0.1:2022"
    os.environ["NO_PROXY"] = "localhost,127.0.0.1"

class AppState(BaseModel):
    foo: str = "bar"

def w_1(state: AppState) -> AppState:
    state.foo = f"{state.foo}-w_1"
    return state

def w_2(state: AppState) -> AppState:
    state.foo = f"{state.foo}-w_2"
    return state

def w_3(state: AppState) -> AppState:
    state.foo = f"{state.foo}-w_3"
    return state

def main() -> None:
    setup_proxy()

    graph_builder = StateGraph(AppState)

    graph_builder.add_node("w_1", w_1)
    graph_builder.add_node("w_2", w_2)
    graph_builder.add_node("w_3", w_3)

    graph_builder.add_edge(START, "w_1")
    graph_builder.add_edge("w_1", "w_2")
    graph_builder.add_edge("w_2", "w_3")
    graph_builder.add_edge("w_3", END)

    graph = graph_builder.compile()

    result = graph.invoke({"foo": "baz"})
    print(result)

if __name__ == "__main__":
    main()
