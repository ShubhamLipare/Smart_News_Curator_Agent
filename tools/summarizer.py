from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def summarise_article(title,content):
    llm = ChatGroq(model="llama3-8b-8192")
    prompt_template = """Title: {title}
    Content: {content}

    Summarize this article in 3 bullet points.
    Also, validate whether the news is recent or not using this timestamp: {time}.
    Format:
    Title: [Article Title]
    1. ...
    2. ...
    3. ...
    """
    prompt=ChatPromptTemplate.from_template(prompt_template)  
    formated_prompt=prompt.format(title=title,content=content,time=current_time())

    response= llm.invoke([HumanMessage(content=formated_prompt)])

    return response.content

