import os

folders=[
    "agents",
    "tools",
    "prompts",
    "schemas",
    "memory",
    "langgraph_workflow",

    "data",
]

files=[
    "agents/__init__.py",
    "agents/curator_agent.py",
    "agents/critic_agent.py",
    "agents/multiagent_graph.py",

    "tools/__init__.py",
    "tools/news_fetcher.py",
    "tools/summarizer.py",
    "tools/summary_store.py",
    "tools/entity_extractor.py",

    "prompts/__init__.py",
    "prompts/summarization_prompt.txt",
    "prompts/critic_prompt.py",

    "schemas/__init__.py",
    "schemas/models.py",

    "memory/__init__.py",
    "memory/memory.py",

    "langgraph_workflow/__init__.py",
    "langgraph_workflow/graph_builder.py",

    "data/summaries.db",

    "experiments.ipynb",
    "app.py",
    "api.py",
    "main.py",
    "utils.py",

]

for i in folders:
    os.makedirs(i,exist_ok=True)

    
for i in files:
    filepath=os.path.join(i)

    if not os.path.exists(filepath):

        with open(filepath,"w") as file:
            file.write("")

