from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
from main import main
import base64
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
from find_job_titles import FinderAcora
from util import log_and_config
import cv2


class Image_str(BaseModel):
    image_str: str


app = FastAPI()

finder = FinderAcora()
config = log_and_config.load_config()
tokenizer = config["model"]["tokenizer"]
model_dir = config["model"]["model_dir"]
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(tokenizer)
model = AutoModelForTokenClassification.from_pretrained(model_dir)
model.to(device)


@app.post("/")
def print_result(image_str: Image_str) -> str:

    imgdata = base64.b64decode(image_str.image_str)

    content = main(
        img=imgdata, model=model, tokenizer=tokenizer, device=device, finder=finder
    )

    return JSONResponse(content=content)


@app.post("/static")
def image_upload():
    return FileResponse("temp.jpg")


@app.get("/static")
def image_upload():
    return FileResponse("temp.jpg")


if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=30001)
    img = cv2.imread("/opt/ml/final/data/image/image64.jpg")
    img = cv2.imencode(".PNG", img)[1].tobytes()
    print(
        main(img=img, model=model, tokenizer=tokenizer, device=device, finder=finder)
    )
