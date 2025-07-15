from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from tools.news_fetcher import fetch_news
from tools.summarizer import summarise_article
#from tools.topic_classifier import classify_topic
#from tools.entity_extractor import extract_entities
from typing import TypedDict, List
from schemas.models import Summary
from langchain_core.tracers.langchain import LangChainTracer

class AgentState(TypedDict):
    query: str
    articles: List[dict]
    summaries: List[Summary]
    url:List[str]

def build_agent():
    graph = StateGraph(AgentState)

    def fetch(state: AgentState) -> AgentState:
        articles = fetch_news.invoke(state["query"])
        state["articles"] = articles
        return state

    def summarise_all(state: AgentState) -> AgentState:
        summaries = []
        for article in state["articles"]:
            content = article.get("content","")
            state["url"].append(article["url"])
            text = summarise_article(article["title"], content=content)
            #category = classify_topic(text)["labels"][0] ##commenting both these for low latency
            #entities = [e["word"] for e in extract_entities(text)]  
            summaries.append(Summary(
                title=article["title"],
                summary=text,
                #category=category,
                #entities=entities
            ))

        #for validatoin
        with open("validation/summaries.txt", "w") as f:
            for summary in summaries:
                f.write(f"{summary}\n")
                
        state["summaries"] = summaries
        return state

    graph.add_node("fetch", RunnableLambda(fetch))
    graph.add_node("summary", RunnableLambda(summarise_all))
    graph.set_entry_point("fetch")
    graph.add_edge("fetch", "summary")
    graph.add_edge("summary", END)

    return graph.compile()
