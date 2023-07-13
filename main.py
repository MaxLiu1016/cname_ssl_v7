
from fastapi import FastAPI, HTTPException
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from pydantic import BaseModel, field_validator
import re
import json

app = FastAPI()


# job 資料結構
class Job(BaseModel):
    domain: str

    @field_validator("domain")
    def domain_validator(cls, v):
        if not is_subdomain(v):
            raise ValueError("domain is not valid")


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
        "status": "fail",
        "message": "domain is not valid"
    }


@app.get("/jobs")
async def get_jobs():
    # list all collections data without id
    jobs_cursor = collection.find({}, {"_id": 0})
    jobs = list(jobs_cursor)
    return {"jobs": jobs}

