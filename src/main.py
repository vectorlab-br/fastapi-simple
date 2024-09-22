from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from starlette.datastructures import URL
import uvicorn
import qrcode
import io
import uuid
import base64
import random
from dotenv import load_dotenv
import os

import datetime

load_dotenv(override=True)
use_htpps = os.getenv('USE_HTTPS')

def str_to_bool(value):
    return value.lower() in ('true', 't', 'yes', 'y', '1')

def https_url_for(request: Request, name: str, **path_params: any) -> str:
    http_url = request.url_for(name, **path_params)
    print(f"Should use https: {use_htpps}, var type: {type(use_htpps)}")
    if str_to_bool(use_htpps):
        new_url = http_url.replace(scheme="https")
        print(f"::: URL Return: {new_url}, type: {type(new_url)}")
    else:
        new_url = http_url.replace(scheme="http")
        print(f"]]] URL Return: {new_url}, type: {type(new_url)}")

    return new_url

cemiterios = ['Parque das flores', 'Bosque da saudade', 'Eterno descanso', 'Para sempre saudosos', 'Campos eternos']

app = FastAPI()


# Mount a static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")
# if use_htpps:
#     print(">>> Using https_url_for <<<")
templates.env.globals["url_for"] = https_url_for
# else:
#     print(">>> Using default url_for <<<")

# else:
#     templates.env.globals["https_url_for"] = url_for

@app.get("/")
async def read_root(request: Request):
    value = str(datetime.datetime.now()).split('.')[0]
    cemiterio = random.choice(cemiterios),
    qr_code, uuid_value = generate_qr_code()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": "Hello, qrCode!", 
        "timeinfo": value,
        "cemiterio": list(cemiterio)[0],
        "qr_code": qr_code,
        "uuid": uuid_value.split('.digital/')[1]
    })

# @app.get("/qr")
def generate_qr_code():
    # Generate QR code with current timestamp
    qr = qrcode.QRCode(version=1, box_size=10, border=3.5)
    # value = str(datetime.datetime.now()).split('.')[0]
    random_uuid = "http://www.eternamente.digital/" + str(uuid.uuid4())
    qr.add_data(random_uuid)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="#DDD")
    
    # Save image to bytes buffer
    buf = io.BytesIO()
    img.save(buf, kind='PNG')
    # buf.seek(0)

    encoded_img = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return encoded_img, random_uuid


if __name__ == "__main__":
    PORT = 5000
    is_debug = True
    print(f"<<< Listening on port {PORT} >>>")
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=is_debug)