from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models import Employee
from mongoengine import connect
import json
import pymongo

app = FastAPI()
connect(db="hrms", host="localhost", port=27017)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/get_all_employees")
def get_all_employees():
    myTests = pymongo.MongoClient('localhost', 27017)
    dataBase = myTests["test"]
    collection = dataBase["test"]
    x = jsonable_encoder(list(collection.find({},{"_id":0})))
    return JSONResponse(content=x)


@app.delete("/delete_employee")
def delete_employee(name: str):
    myTests = pymongo.MongoClient("localhost", 27017)
    dataBase = myTests["hrms"]
    collection = dataBase["employee"]
    myQuery = {"name": name}
    collection.delete_one(myQuery)

    return{}

@app.post("/create_employee")
def create_employee( name: str,age: str,teams:list):
    myTests = pymongo.MongoClient("localhost", 27017)
    dataBase = myTests["hrms"]
    collection = dataBase["employee"]

    myQuery = {"name":name, "age": age, "teams":teams}
    collection.insert_one(myQuery)

    return{}

@app.put("/update_employee")
def update_employee( oldname: str,name: str,age: str,teams: list):
    myTests = pymongo.MongoClient("localhost", 27017)
    dataBase = myTests["hrms"]
    collection = dataBase["employee"]

    myOldQuery = {"name":oldname}
    myQuery = {"$set":{"name":name, "age": age, "teams": teams}}
    collection.update_one(myOldQuery,myQuery)

    return{}