from fastapi import FastAPI
from main import run_pipeline
from pydantic import BaseModel

class Input(BaseModel):
    query:str
    max_iterations:int

app=FastAPI()

@app.post("/news")
def fetch_date(request:Input):
    result=run_pipeline(request.query,request.max_iterations)
    return {
        "final_summary": result["final_summary"],
        "evaluation": result["evaluation"],
        "iteration":result["iteration"]
    }
