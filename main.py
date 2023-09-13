from fastapi import FastAPI, Response
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()


@app.get("/")
async def root():
    try:
        domain = 'test.hqsmaxtest.online'
        current_file_path = os.path.abspath(__file__)
        project_path = os.path.dirname(os.path.dirname(current_file_path))
        temp_ssl_path = os.path.join(project_path, 'cname_ssl_v7', 'module', 'ssl', 'temp_ssl')
        full_path = os.path.join(temp_ssl_path, domain)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        os.system(f'sudo openssl req -new -newkey rsa:2048 -nodes -keyout {full_path}/privkey.pem -out {full_path}/csr.pem -subj "/CN={domain}"')
        print(f'sudo ~/.acme.sh/acme.sh --issue --webroot {full_path} -d {domain} --csr {full_path}/csr.pem --fullchainpath {full_path}/fullchain.pem --keypath {full_path}/privkey.pem --force')
        # os.system(f'sudo ~/.acme.sh/acme.sh --issue --webroot {full_path} -d {domain} --csr {full_path}/csr.pem --fullchainpath {full_path}/fullchain.pem --keypath {full_path}/privkey.pem')
    except Exception as e:
        print(e)


@app.get("/.well-known/acme-challenge/{challenge_route}")
async def get_certificate(challenge_route: str, response: Response):
    full_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'zero_ssl', 'module', 'ssl', 'temp_ssl', 'test.hqsmaxtest.online')
    with open(os.path.join(full_path, challenge_route), 'r') as f:
        response.body = f.read()
    response.headers['Content-Type'] = 'text/plain'
    return response
