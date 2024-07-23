from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

# Load data from a JSON file
def load_json(filename):
    with open(filename,'r',encoding='utf-8') as file:
        return json.load(file)

# Load the JSON data
data = load_json('address/countries.json')


class Country(BaseModel):
    id: int
    name: str

@app.get("/countries" )
def get_countries():
    # raw_dump=
    return {'status':200,'data':[{"id":country["id"],"name": country["name"]} for country in data],'message':'Success'}
    # [{"id":country["id"],"name": country["name"]} for country in data]

