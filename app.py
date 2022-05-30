from fastapi import FastAPI
import uvicorn
from main import main
import base64
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
import cv2

class Image_str(BaseModel):
    image_str : str
    
app = FastAPI()

_tokenizer = "klue/roberta-large"
_model_dir = "/opt/ml/final/model/best_model/bert_final_roberta"

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

tokenizer = AutoTokenizer.from_pretrained(_tokenizer)
model = AutoModelForTokenClassification.from_pretrained(_model_dir)
model.to(device) 

@app.post("/")
def print_result(image_str:Image_str):

    imgdata = base64.b64decode(image_str.image_str)

    return main(img_byte=imgdata, model=model, tokenizer=tokenizer, device=device)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=30001)
