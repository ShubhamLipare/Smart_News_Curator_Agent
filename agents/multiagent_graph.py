from langgraph.graph import StateGraph, END
from agents.critic_agent import build_agent as build_critic_agent
from agents.curator_agent import build_agent as build_curator_agent
from typing import TypedDict, List
from langsmith import traceable
from langchain_core.runnables import RunnableLambda
from schemas.models import Summary

class MultiAgentState(TypedDict):
    query: str
    articles: List[dict]
    summaries: List[Summary]
    current_summary: str
    evaluation: str
    final_summary: str
    iteration: int
    max_iterations: int

@traceable(name="multiagent_news_summary")
def build_multiagent():
    graph = StateGraph(MultiAgentState)

    # Subgraphs
    curator_graph = build_curator_agent()
    critic_graph = build_critic_agent()

    @traceable(name="curator_runner")
    def run_curator(state: MultiAgentState) -> MultiAgentState:
        print("[Curator agent] Fetching news and summarizing...")
        curator_state = curator_graph.invoke({
            "query": state["query"],
            "articles": [],
            "summaries": []
        })
        summaries = curator_state["summaries"]
        state["summaries"] = summaries
        #state["current_summary"] = summaries[0].summary 
        state["current_summary"] = next(
            (s.summary for s in summaries ), #if "bitcoin" in s.summary.lower()
            summaries[0].summary  # fallback
            )
        return state

    @traceable(name="critic_runner")
    def run_critic(state: MultiAgentState) -> MultiAgentState:
        print("\n[Critic Agent] Evaluating and refining summary...")
        critic_state = critic_graph.invoke({
            "current_summary": state["current_summary"],
            "evaluation": "",
            "final_summary": ""
        })
        state["evaluation"] = critic_state["evaluation"]
        state["final_summary"] = critic_state["final_summary"]
        state["iteration"] += 1
        return state

    def should_continue(state: MultiAgentState) -> str:
        need_improvement = state["final_summary"].strip() != state["current_summary"].strip()
        within_limit = state["iteration"] < state["max_iterations"]
        if need_improvement and within_limit:
            print("[Loop] Critic wants to revise. Looping again...")
            state["current_summary"] = state["final_summary"]
            return "continue_critic"
        print("[Done] Summary is finalized or max iterations reached.")
        return "end"

    # Define nodes
    graph.add_node("curator", RunnableLambda(run_curator))
    graph.add_node("critic", RunnableLambda(run_critic))

    # Conditional branching from critic
    graph.add_conditional_edges(
        "critic",
        should_continue,
        {
            "continue_critic": "critic",
            "end": END
        }
    )

    graph.set_entry_point("curator")
    graph.add_edge("curator", "critic")

    return graph.compile()

"""
if __name__ == "__main__":
    agent = build_multiagent()
    result = agent.invoke({
        "query": "Business",
        "articles": [],
        "summaries": [],
        "current_summary": "",
        "evaluation": "",
        "final_summary": "",
        "iteration": 0,
        "max_iterations": 3
    })

    print("\n🧠 Final Summary:\n", result["final_summary"])
    print("\n📝 Evaluation:\n", result["evaluation"])
    print("\n📝 Evaluation:\n", result["iteration"])
"""