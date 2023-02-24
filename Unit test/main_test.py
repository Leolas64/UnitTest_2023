import unittest
import json
import pymongo
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestEmployeeFunctions(unittest.TestCase):
    
    def setUp(self):
        self.mongo_client = pymongo.MongoClient('localhost', 27017)
        self.db = self.mongo_client['hrms']
        self.collection = self.db['employee']

    def test_create_employee(self):
        data = {"name": "John Doe", "age": 25, "teams": ["Marketing", "Sales"]}
        response = client.post("/create_employee", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.collection.count_documents(data), 1)
    
    def test_get_all_employees(self):
        data = {"name": "John Doe", "age": 25, "teams": ["Marketing", "Sales"]}
        self.collection.insert_one(data)
        response = client.get("/get_all_employees")
        self.assertEqual(response.status_code, 200)
    
    def test_delete_employee(self):
        data = {"name": "John Doe", "age": 25, "teams": ["Marketing", "Sales"]}
        self.collection.insert_one(data)
        response = client.delete(f"/delete_employee?name={data['name']}")
        self.assertEqual(response.status_code, 200)
    
    def test_update_employee(self):
        old_data = {"name": "John Doe", "age": 25, "teams": ["Marketing", "Sales"]}
        new_data = {"name": "John Smith", "age": 30, "teams": ["Sales", "Development"]}
        self.collection.insert_one(old_data)
        response = client.put(f"/update_employee?oldname={old_data['name']}", json=new_data)
        self.assertEqual(response.status_code, 200)

