import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
from main import main
import base64
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
from find_job_titles import FinderAcora
from calculate.metric import *
from calculate.pickle import *
from util.log_and_config import *
import cv2
import argparse
import pprint

class Image_str(BaseModel):
    image_str: str

logger = get_logger()
app = FastAPI()
finder = FinderAcora()
config = load_config()
tokenizer = config["model"]["tokenizer"]
model_dir = config["model"]["model_dir"]
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained(tokenizer)
model = AutoModelForTokenClassification.from_pretrained(model_dir)
model.to(device)


@app.post("/")
async def print_result(image_str: Image_str) -> str:

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

def run(args):
    if args.calculate:
        if not os.path.exists("./pred.pkl"):
            save_pred_pickle(callback_fn=main, model=model, tokenizer=tokenizer, device=device, finder=finder)

        pred = load_pred_pickle()

        true = make_true_list("./data_info.csv")

        print(f"CAL ACC : {calculate_accuracy(true, pred)}")

    else:
        torch.multiprocessing.set_start_method("spawn", force=True)
        # uvicorn.run(app, host="0.0.0.0", port=30001)
        img = cv2.imread("/opt/ml/final/data/image/image41.jpg")
        img = cv2.imencode(".PNG", img)[1].tobytes()
        pprint.pprint(
            main(img=img, model=model, tokenizer=tokenizer, device=device, finder=finder)
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Metric 측정용 Argument
    parser.add_argument('--calculate', type=bool, default=False,
                        help='Calculate Accuracy')

    args= parser.parse_args()
    run(args)
    # img = cv2.imread("/opt/ml/img/raw_image_3.jpg")
    # img = cv2.imencode(".PNG", img)[1].tobytes()
    # print(main(img=img, model=model, tokenizer=tokenizer, device=device, finder=finder))
