from fastapi import FastAPI, Response
from dotenv import load_dotenv
import time
import os
import asyncio

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
        await run_command(f'sudo openssl req -new -newkey rsa:2048 -nodes -keyout {full_path}/privkey.key -out {full_path}/csr.pem -subj "/CN={domain}"')
        print(f'sudo openssl req -new -newkey rsa:2048 -nodes -keyout {full_path}/privkey.pem -out {full_path}/csr.pem -subj "/CN={domain}"')
        await run_command(f'sudo chmod -R 777 {full_path}')
        await run_command(f'acme.sh --issue --webroot {full_path} -d {domain} --signcsr --csr {full_path}/csr.pem --fullchain-file {full_path}/fullchain.pem --force --debug')
        return {"message": "success"}
    except Exception as e:
        print(e)
        return {"message": f"error: {e}"}


async def run_command(cmd: str):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        raise RuntimeError(f"'{cmd}' failed with error code {process.returncode}: {stderr.decode().strip()}")


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
