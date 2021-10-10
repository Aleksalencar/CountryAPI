 # app.py
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

def _find_next_id():
    return max(country.country_id for country in countries) + 1

class Country(BaseModel):
    country_id: int = Field(default_factory=_find_next_id, alias="id")
    name: str
    capital: str
    area: int

countries = [
    Country(id=1, name="Thailand", capital="Bangkok", area=513120),
    Country(id=2, name="Australia", capital="Canberra", area=7617930),
    Country(id=3, name="Egypt", capital="Cairo", area=1010408),
]

@app.get("/")
async def index():
     index = {'authors':[
         {'name': 'Aleksander Alencar Junior'},
         {'name': 'Aleksander Alencar Junior 2'}]
     }
     return index


@app.get("/countries")
async def get_countries():
    return countries

@app.post("/countries", status_code=201)
async def add_country(country: Country):
    countries.append(country)
    return country

# Path parameter
@app.get("/countries/{id}")
async def get_countries(id: int):
    for country in countries:
        if country.country_id == id:
            return country

# Query parameter
@app.get("/search/")
async def get_countries(key: str, limit: Optional[int] = 50):
    result_list = []
    for index in range(len(countries)):
        if index == limit:
            break

        key = key.lower()

        country_name = countries[index].name
        country_name = country_name.lower()

        if key in country_name:
            result_list.append(countries[index])
    return result_list

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)