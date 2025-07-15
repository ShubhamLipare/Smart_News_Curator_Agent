from agents.multiagent_graph import build_multiagent

multiagent=build_multiagent()

def run_pipeline(query:str,max_iterations:int)->dict:
    return multiagent.invoke({
        "query": query,
        "articles": [],
        "summaries": [],
        "url": [],
        "current_summary": "",
        "evaluation": "",
        "final_summary": "",
        "iteration": 0,
        "max_iterations": max_iterations
    }
    )
