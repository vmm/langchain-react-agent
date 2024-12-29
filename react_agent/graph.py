# react_agent/graph.py
import json
from typing import Dict, List, TypedDict

from langgraph.graph import END, StateGraph

from react_agent.agent import get_agent_executor


class AgentState(TypedDict):
    messages: List[dict]
    next_step: str


agent_executor = get_agent_executor()


def agent_node(state):
    messages = state["messages"]
    result = agent_executor.invoke({"input": messages[-1]["content"]})
    # Include both the final output and any intermediate steps in the response
    output = result["output"]
    if "intermediate_steps" in result:
        steps = "\n".join(
            f"{action[0].tool}: {action[0].tool_input} -> {action[1]}"
            for action in result["intermediate_steps"]
        )
        output = f"{steps}\n\nFinal Answer: {output}"
    return {
        "messages": messages + [{"role": "assistant", "content": output}],
        "next_step": "route",
    }


def route_node(state):
    messages = state["messages"]
    last_message = messages[-1]["content"]
    next_step = "end" if "Final Answer:" in last_message else "agent"
    return {"next_step": next_step}


workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("route", route_node)
workflow.set_entry_point("agent")
workflow.add_edge("agent", "route")
workflow.add_conditional_edges(
    "route", lambda x: x["next_step"], {"agent": "agent", "end": END}
)
chain = workflow.compile()

print(chain.get_graph().draw_mermaid())
chain.get_graph().print_ascii()
chain.get_graph().draw_mermaid_png(output_file_path="../graph.png")


def get_chain():
    return chain
