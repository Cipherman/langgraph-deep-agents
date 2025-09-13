from langchain_core.messages import HumanMessage
from src.graphs.deep_research.scope.builder import build_scope_graph

#scope = build_scope_graph()

#result = scope.invoke({"messages":[HumanMessage(content="I want to research the best hotel in Tokyo.")]})
#print(result)

def main(graph):
    while True:
        #user_id = input("User ID: ")
        #config = {"configurable": {"thread_id": user_id}}
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        events =  graph.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            #config,
            stream_mode="values",
        )
        for event in events:
            event["messages"][-1].pretty_print()
            #for value in event.values():
            #    print("Assistant", value["messages"][-1].content)

if __name__ == "__main__":
    graph = build_scope_graph()
    main(graph)