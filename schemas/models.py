from pydantic import BaseModel

class Article(BaseModel):
    title:str
    url:str
    description:str


class Summary(BaseModel):
    title: str
    summary: str
    #category: str ##commenting both these for low latency
    #entities: list[str]
