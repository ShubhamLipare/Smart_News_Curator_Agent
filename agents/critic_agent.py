from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from prompts.critic_prompt import critic_prompt
import re
from langgraph.graph import StateGraph,END
from langchain_core.runnables import RunnableLambda
from langsmith import traceable
from typing import TypedDict

class CriticAgentState(TypedDict):
    current_summary: str
    evaluation: str
    final_summary: str

llm=ChatGroq(model="llama3-8b-8192")

@traceable(name="critic_evaluation")
def critic_summary(summary: str) -> dict:
    prompt = critic_prompt.format(summary=summary)
    response = llm.invoke([HumanMessage(content=prompt)])
    text = response.content.strip()

    evaluation = "No evaluation"
    revised = summary

    # Updated regex
    eval_match = re.search(r"(?i)evaluation\s*:\s*(.*?)(?:\n|$)", text, re.DOTALL)
    revised_match = re.search(r"(?i)revised summary.*?:\s*(.*)", text, re.DOTALL)

    if eval_match:
        evaluation = eval_match.group(1).strip()

    if revised_match:
        revised_text = revised_match.group(1).strip()
        if "no change needed" not in revised_text.lower():
            revised = revised_text

    return {
        "evaluation": evaluation,
        "final_summary": revised
    }


def build_agent():
   graph=StateGraph(CriticAgentState)

   def review(state:CriticAgentState)->CriticAgentState:
    result=critic_summary(state["current_summary"])
    state["evaluation"]=result["evaluation"]
    state["final_summary"] = result["final_summary"]
    return state
   
   graph.add_node("critic",RunnableLambda(review))
   graph.set_entry_point("critic")
   graph.add_edge("critic",END)

   return graph.compile()

'''
if __name__=="__main__":
   
    summary = """
        1. AI is getting popular everywhere.
        2. Many companies are using AI.
        3. This shows how AI is useful in the future.
    """
    workflow=build_agent()
    result=workflow.invoke({
    "current_summary":summary, 
    "evaluation": "",
    "final_summary": ""})
    print("----------------------------------")
    print(result["evaluation"])
    print("---------------------------------")
    print(result["final_summary"])

'''
