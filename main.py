from fastapi import FastAPI, Response
from dotenv import load_dotenv
import time
import os

load_dotenv()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/domain")
async def domain():
    try:
        domain = 'test.hqsmaxtest.online'
        current_file_path = os.path.abspath(__file__)
        project_path = os.path.dirname(os.path.dirname(current_file_path))
        temp_ssl_path = os.path.join(project_path, 'cname_ssl_v7', 'module', 'ssl', 'temp_ssl')
        full_path = os.path.join(temp_ssl_path, domain)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        os.system(f'sudo openssl req -new -newkey rsa:2048 -nodes -keyout {full_path}/privkey.pem -out {full_path}/csr.pem -subj "/CN={domain}"')
        # print(f'sudo ~/.acme.sh/acme.sh --issue --webroot {full_path} -d {domain} --csr {full_path}/csr.pem --fullchainpath {full_path}/fullchain.pem --keypath {full_path}/privkey.pem --force')
        # 開放 full_path 裡面的檔案權限
        os.system(f'sudo chmod -R 777 {full_path}')
        os.system(f'acme.sh --issue --webroot {full_path} -d {domain} --csr {full_path}/csr.pem --fullchainpath {full_path}/fullchain.pem --keypath {full_path}/privkey.pem --force --debug')
        return {"message": "success"}
    except Exception as e:
        print(e)


@app.get("/.well-known/acme-challenge/{challenge_route}")
async def get_certificate(challenge_route: str):
    try:
        print(challenge_route)
        full_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cname_ssl_v7', 'module', 'ssl', 'temp_ssl', 'test.hqsmaxtest.online')
        print(full_path)
        with open(os.path.join(full_path, '.well-known', 'acme-challenge', challenge_route), 'r') as f:
            content = f.read()
        return Response(content)
    except Exception as e:
        print(e)
