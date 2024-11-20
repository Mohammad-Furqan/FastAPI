from fastapi import FastAPI

#uvicorn main:app --reload

app=FastAPI()

@app.get("/")
def hello():
    return {"greeting":"Hello, world" }

@app.get("/about")
def about():
    return {"about":"This is a fastapi test"}



