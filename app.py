from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from main import main
import base64
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
from find_job_titles import FinderAcora

class Image_str(BaseModel):
    image_str : str
    
app = FastAPI()

finder = FinderAcora()
_tokenizer = "klue/roberta-large"
_model_dir = "/opt/ml/final/model/best_model/bert_final_roberta"

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

tokenizer = AutoTokenizer.from_pretrained(_tokenizer)
model = AutoModelForTokenClassification.from_pretrained(_model_dir)
model.to(device) 

@app.post("/")
def print_result(image_str:Image_str):

    imgdata = base64.b64decode(image_str.image_str)

    content = main(img_byte=imgdata, model=model, tokenizer=tokenizer, device=device, finder=finder)

    return JSONResponse(content=content)


if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=30001)
    import cv2
    file_path = f"/opt/ml/final/data/test_image/test_image_raw/raw_image_3.jpg"
    img = cv2.imread(file_path)
    print("image type : ", type(img))

    imgdata = cv2.imencode('.PNG', img)[1].tobytes()

    content = main(img_byte=imgdata, model=model, tokenizer=tokenizer, device=device, finder=finder)

    print(content)
    
