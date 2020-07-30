from typing import Optional, List
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from mongodb import mongodbinit, get_random_lines, insert_many, insert_many_t2, get_t2_lines, clear_total
from  random import randint

origins = [
    "http://127.0.0.1:8080",
    "http://localhost:8080"
]

# init mongodb 
mongodbinit()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    province: str
    city: str
    latitude: str
    longitude: str
    weight: int

class cityData(BaseModel):
    cityData: List

@app.get("/")
def read_root():
    return {"welcome": "Shanghai"}


# create random city array data and return to client
@app.get("/city_array")
async def create_city_array():
    random_city_data = await get_random_lines(20)
    # 添加随机整数，作为点半径
    for ele in random_city_data:
        ele['weight'] = randint(4,12)
    #print(random_city_data )
    return {"random_city_data": random_city_data}


# clear 累计呈现 数据库表 :bitoct2
@app.get("/clear_total")
async def clearTotal():
    result = await clear_total()
    return {"result": result}


# add latest city array data to collection: bitoct1
@app.post("/city_array_once")
async def fresh_city_array(citydata: cityData):
    #print(citydata.dict()['cityData'][0])
    response = await insert_many(citydata.dict()['cityData'])
    if response:
        return {"error": response}
    else:
        return ('ok')


# add latest city array data to collection: bitoct2 . bitoct2 is a Capped Collection, max 700 lines 
@app.post("/city_array_total")
async def sum_city_array(citydata: cityData):
    #print(citydata.dict()['cityData'][0])
    response = await insert_many_t2(citydata.dict()['cityData'])
    if response:
        return {"error": response}
    else:
        return ('ok')


# get latest 100 lines data of bitoct2
@app.get("/city_array_total")
async def sum_city_array_get():
    city_data = await get_t2_lines(100)
    #print(city_data)
    return {"city_data": city_data}
