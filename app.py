from fastapi import FastAPI
import uvicorn
from main import main
import base64
from pydantic import BaseModel

class Image_str(BaseModel):
    image_str : str
    
app = FastAPI()


@app.post("/")
def print_result(image_str:Image_str):

    imgdata = base64.b64decode(image_str.image_str)
    filename = './image.jpg'
    with open(filename, 'wb') as f:
        f.write(imgdata)

    return main('/opt/ml/Fast_API/image.jpg')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
