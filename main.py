from fastapi import FastAPI, HTTPException, Response
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from pydantic import BaseModel, field_validator
import pexpect
import time
import re
import json

app = FastAPI()


# job 資料結構
class Job(BaseModel):
    domain: str

    @field_validator("domain")
    def check_domain(cls, v):
        if not is_subdomain(v):
            raise HTTPException(status_code=400, detail="domain is not a subdomain")
        else:
            return v


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def is_subdomain(s):
    # 正则表达式，匹配类似 www.abc.com 的子域名
    pattern = r"(?!-)[A-Za-z0-9-]{1,63}(?<!-)\." \
              r"(?!-)[A-Za-z0-9-]{1,63}(?<!-)\." \
              r"[A-Za-z]{2,6}"
    return re.fullmatch(pattern, s) is not None


uri = "mongodb+srv://Max:AA951753@bat.zcefrvy.mongodb.net/bat?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, ssl=True, ssl_cert_reqs='CERT_NONE')
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['cname_ssl']

collection = db['SSLJobs']


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/job")
async def create_job(job: Job):
    collection.insert_one(job.model_dump())
    return {
        "status": "success",
    }


@app.get("/jobs")
async def get_jobs():
    # list all collections data without id
    jobs_cursor = collection.find({}, {"_id": 0})
    jobs = list(jobs_cursor)
    return {"jobs": jobs}


@app.get("sslJob")
async def get_ssl_job():
    # Start the subprocess
    child = pexpect.spawn(
        'sudo certbot certonly --email a0958057936@gmail.com -d test.hqsmaxtest.online --agree-tos --manual --staging --config-dir /Users/manias/Desktop/work_space/cname_ssl_v7')

    # Wait for password prompt and send password
    index = child.expect(['Password:'])
    if index == 0:
        child.sendline('951753')
        time.sleep(5)  # Wait for 5 seconds

        child.expect('Press Enter to Continue')
        print(child.before.decode('utf-8'))
        challengeData = child.before.decode('utf-8')
        collection.insert_one({'domain': 'test.hqsmaxtest.online', 'challengeData': challengeData})
        # with open('challenge_info.txt', 'w') as file:
        #     # Write the challenge data and URL to the file
        #     file.write('Challenge data: ' + child.before.decode('utf-8') + '\n')

        index = child.expect(['Press Enter to Continue'])
        if index == 0:
            child.sendline('\n')


@app.get("/certificate/{challenge_route}")
async def get_certificate(challenge_route: str):
    result = collection.find_one({
        "challengeRoute": challenge_route
    }, {"_id": 0})
    # result['challengeData'] 純文字 排除"
    s = result['challengeData'].replace('"', '')
    return Response(content=s, media_type="text/plain")
