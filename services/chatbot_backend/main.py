from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import twillio_api

# creating fastapi
app = FastAPI(title="GenAI WhatsApp")

# connect router to main api
app.include_router(twillio_api.router)

# adding middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["kushaldulani.com"],  # add your domains here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# homeurl
@app.get("/", tags=["Home"])
def index():
    return {
        "Message": "Hello, Welcome to GenAI WhatsApp API, goto /docs for more information"
    }

import redis

# Connect to Redis server
redis_host = 'redis'
redis_port = 6379
redis_db = 0
redis_password = None

# Connect to Redis
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)

# Example key and value
key = 'kd'
value = 'kushal dulani'

key2 = 'kd2'
value2 = 134567

# SET operation
redis_client.set(key, value)
redis_client.set(key2, value2)

# GET operation
result = redis_client.get(key)
result = redis_client.get(key2)

# Decode the result if necessary (Redis stores bytes)
if result is not None:
    result = result.decode('utf-8')

print("Value for key '{}' is: {}".format(key, result))
