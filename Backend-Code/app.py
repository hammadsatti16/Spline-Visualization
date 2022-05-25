from distutils import extension
from distutils.log import debug
import uvicorn
from fastapi import FastAPI,File,UploadFile
import numpy as np
from PIL import Image
import cv2
from img_ann import data ,ann_file
from param_spline import get_tck_param, calculate_spine_params, image_spline
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import aiofiles

app = FastAPI()
db = []
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/api/File")
async def create_upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        x = file.content_type.split("/")[-1]
        if x == "png" or x =="jpg" or x =="jpeg":
            async with aiofiles.open(file.filename, 'wb') as out_file:
                while content := await file.read(1024):  # async read file chunk
                    await out_file.write(content)  # async write file chunk
            img = cv2.imread(file.filename)
            
        if x =="json" or x=="JSON":
            annotation = data(file.filename)
            annotation = ann_file(annotation)
            t, c, k = get_tck_param(annotation)
            spine_param = calculate_spine_params(c, k)
            imag = image_spline(c,k,img)
            cv2.imwrite("Result_spline_image.jpeg", imag) 

    return {"Result": "Success", "filenames": [file.filename for file in files]}
if __name__ == '__main__':
    uvicorn.run(app, host='192.168.18.189', port=8080, debug=True)