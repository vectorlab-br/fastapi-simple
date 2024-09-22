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

def load_names(file_name: str) -> list[str]:
    with open(file_name, '+r', encoding='utf-8') as f:
        return [x.strip() for x in f.readlines()]


def str_to_bool(value):
    return value.lower() in ('true', 't', 'yes', 'y', '1')

def https_url_for(request: Request, name: str, **path_params: any) -> str:
    http_url = request.url_for(name, **path_params)
    print(f"Should use https: {use_htpps}, var type: {type(use_htpps)}")
    if str_to_bool(use_htpps):
        new_url = http_url.replace(scheme="https")
        # print(f"::: URL Return: {new_url}, type: {type(new_url)}")
    else:
        new_url = http_url.replace(scheme="http")
        # print(f"]]] URL Return: {new_url}, type: {type(new_url)}")

    return new_url

cemiterios = load_names('./nomes_cemiterios.txt')
pessoas = load_names('./nomes_pessoas.txt')

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
    selected = random.choice(cemiterios)
    cem_index = 999
    if selected in cemiterios:
        cem_index = cemiterios.index(selected)
    else:
        print(f'||| [{selected}] NOT IN LIST |||')

    qr_code, uuid_value = generate_qr_code(cem_index)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": "Hello, qrCode!", 
        "timeinfo": value,
        "cemiterio": selected,
        "qr_code": qr_code,
        "uuid": uuid_value.split('.digital/')[1]
    })

# @app.get("/qr")
def generate_qr_code(cem_index=999):
    # Generate QR code with current timestamp
    qr = qrcode.QRCode(version=1, box_size=10, border=3.5)
    # value = str(datetime.datetime.now()).split('.')[0]
    new_uuid = str(uuid.uuid4()).split('-')
    new_uuid[1] = f"{cem_index:04x}"
    random_uuid = "http://www.eternamente.digital/" + "-".join(new_uuid)
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