from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return "Hello, world!"


@app.get("/add")
def x_y(x: int, y: int) -> int:
    return x + y
