from fastapi import FastAPI, UploadFile, File, Response, Request, HTTPException
from PIL import Image
import io
import requests
import base64
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sdk import ObjectRecognitionSDK
import json
import uvicorn

sdk = ObjectRecognitionSDK()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageRequest(BaseModel):
    image: str                                                                                 

class ImageResponse(BaseModel):
    image: str
    metadata: dict

with open('company_data.json', 'r') as file:
    company_data = file.read()

company_data_dict = json.loads(company_data)


def process_image(image):
    try:
        obj_dict, obj_lst, result_img = sdk.recognize_objects(image)

        stopwords = ['person', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe']

        for stopword in stopwords:
            if stopword in obj_lst:
                obj_lst.remove(stopword)

        similarity_response = sdk.categorize_objects(obj_lst)
        result_img = Image.fromarray(result_img)

        return result_img, obj_dict, similarity_response

    except Exception as e:
        raise HTTPException(status_code=500, detail="Image processing failed")


@app.post("/api/objectrecognition/processimage")
async def process_image_route(request: ImageRequest):
    try:
        image_data = request.image
        image_data = base64.b64decode(image_data)
        image_pil = Image.open(io.BytesIO(image_data))


        processed_image, obj_dict, similarity_response = process_image(image_pil)

        image_bytes = io.BytesIO()
        processed_image.save(image_bytes, format="JPEG")
        image_bytes = image_bytes.getvalue()
        final_img = base64.b64encode(image_bytes).decode("utf-8")

        metadata = {'objects': obj_dict,
                    'clusters': similarity_response}

        response = ImageResponse(image=final_img, metadata=metadata)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to process the image")

@app.get("/api/objectrecognition/getcompanies/{industry_key}")
async def get_values(industry_key: str):
    try:
        if industry_key not in company_data_dict:
            raise HTTPException(status_code=404, detail="Industry key not found")
        return {industry_key: company_data_dict[industry_key]}

    except Exception as e:
        raise HTTPException(status_code=404, detail="Failed to fetch data for the given industry key")

