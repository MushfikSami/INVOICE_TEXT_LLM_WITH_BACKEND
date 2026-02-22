import os 
import io 
import hashlib 
import redis 
from fastapi import FastAPI,UploadFile,File,Form,Depends,HTTPException,Header,Request 
from prometheus_fastapi_instrumentator import Instrumentator 
import google.generativeai as genai 
from PIL import Image  
from dotenv import load_dotenv 


load_dotenv()


app=FastAPI(title='Gemini Invoice API')


@app.middleware('http')
async def add_custom_header(request:Request,call_next):
    response=await call_next(request)
    response.headers['X-Processing-Node']='FastAPI-Backend'
    return response 



Instrumentator().instrument(app).expose(app)


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
REDIS_HOST=os.getenv("REDIS_HOST",'localhost')
redis_client=redis.Redis(REDIS_HOST,port=6379,db=0,decode_responses=True)


API_TOKEN=os.getenv("API_TOKEN")

def verify_token(x_api_token:str=Header(...)):
    if x_api_token!=API_TOKEN:
        raise HTTPException(status_code=401,detail='Unauthorized API Token')


@app.post('/extract',dependencies=[Depends(verify_token)])
async def extract_invoice(prompt:str=Form(...),file:UploadFile=File(...)):
    image_bytes=await file.read()

    cache_key=hashlib.sha256(prompt.encode()+image_bytes).hexdigest()
    cached_result=redis_client.get(cache_key)

    if cached_result:
        return {'source':'redis_cache','answer':cached_result}
    
    try:
        image=Image.open(io.BytesIO(image_bytes))
        model=genai.GenerativeModel('gemini-3-flash-preview')
        response=model.generate_content([prompt,image])
        redis_client.setex(cache_key,3600,response.text)

        return {'source':"gemini_api",'answer':response.text}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))