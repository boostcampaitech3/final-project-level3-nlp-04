from fastapi import FastAPI
import uvicorn
from main import main

app = FastAPI()


@app.get("/")
def print_result():
    return main()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
