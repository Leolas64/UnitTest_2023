import unittest
from pymongo import MongoClient
from fastapi.testclient import TestClient
from main import app
import json
        
class TestCrudRequest(unittest.TestCase):
   
    def setUp(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client["hrms"]
        self.collection = self.db["employee"]
        self.test_client = TestClient(app)
        
        
    def test_post(self):
        retour = self.test_client.post("/create_employee", params={"name": "John Doe", "age": "26", "teams": ["Marketing"]} )
        self.assertEqual(retour.status_code, 200)
        self.assertEqual(retour.json(), ["Test Ajout"]) 
        ajout = self.collection.find_one({"name": "John Doe"})
        self.assertIsNotNone(ajout)
        self.assertEqual(ajout["name"], "John Doe")
        self.assertEqual(ajout["age"], "26")
        self.assertEqual(ajout["Teams"], ["Marketing"])
        
    def test_get(self):
        self.collection.insert_one({"name": "John Doe", "age": "26", "teams": ["Marketing"]})
        retour = self.test_client.get("/get_all_employees")
        self.assertEqual(retour.status_code, 200)
        test_utilisateur = json.loads(retour.content)
        self.assertEqual(test_utilisateur[0]["name"], "John Doe")


    def test_put(self):
        retour = self.test_client.put("/update_employee", params = {"oldname": "John Doe", "name": "Pierre Dupont", "age": "50", "teams": ["Technologies"]})
        self.assertEqual(retour.status_code, 200)
        self.assertEqual(retour.json(), ["Modification effectuée"]) 
        ajout = self.collection.find_one({"name": "Pierre Dupont"})
        self.assertIsNotNone(ajout)
        self.assertEqual(ajout["name"], "Pierre Dupont")
        self.assertEqual(ajout["age"], "50")
        self.assertEqual(ajout["teams"], ["Technologies"])

    def test_delete(self):
        
        retour = self.test_client.delete("/delete_employee", params = {"name": "Pierre Dupont", "age": "50", "teams":["Technologies"]})
        self.assertEqual(retour.status_code, 200)
        self.assertEqual(retour.json(), ["Suppression 1"])
        retour = self.test_client.delete("/delete_employee", params = {"name": "John Doe", "age": "25", "teams": ["Marketing"]})
        self.assertEqual(retour.status_code, 200)
        self.assertEqual(retour.json(), ["Suppression 2"])
        self.assertEqual(self.collection.count_documents({"name": "Pierre Dupont", "age": "50", "teams":["Technologies"]}), 0)
        self.assertEqual(self.collection.count_documents({"name": "John Doe", "age": "25", "teams": ["Marketing"]}), 0)
        
if __name__ == "__main__":
    unittest.main()