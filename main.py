from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return


@app.post("/post")
def get_post():
    return
