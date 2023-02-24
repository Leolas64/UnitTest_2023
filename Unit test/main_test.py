import unittest
import json
import pymongo
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestEmployeeFunctions(unittest.TestCase):
    
    def setUp(self):
        # se connecter à la base de données de test
        self.mongo_client = pymongo.MongoClient('localhost', 27017)
        self.db = self.mongo_client['hrms']
        self.collection = self.db['employee']

    def test_create_employee(self):
        # envoyer une requête POST pour créer un nouvel employé
        data = {"name": "John Doe", "age": 25, "teams": ["Marketing", "Sales"]}
        response = client.post("/create_employee", json=data)
        # vérifier que la réponse est bien un code 200 (succès)
        self.assertEqual(response.status_code, 200)
        # vérifier que la collection contient maintenant un document avec les mêmes données
        self.assertEqual(self.collection.count_documents(data), 1)
    
    def test_get_all_employees(self):
        # ajouter des données à la collection de test
        data = {"name": "John Doe", "age": 25, "teams": ["Marketing", "Sales"]}
        self.collection.insert_one(data)
        # envoyer une requête GET pour obtenir tous les employés
        response = client.get("/get_all_employees")
        # vérifier que la réponse est bien un code 200 (succès)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_employee(self):
        # ajouter des données à la collection de test
        data = {"name": "John Doe", "age": 25, "teams": ["Marketing", "Sales"]}
        self.collection.insert_one(data)
        # envoyer une requête DELETE pour supprimer l'employé ajouté précédemment
        response = client.delete(f"/delete_employee?name={data['name']}")
        # vérifier que la réponse est bien un code 200 (succès)
        self.assertEqual(response.status_code, 200)
    
    def test_update_employee(self):
        # ajouter des données à la collection de test
        old_data = {"name": "John Doe", "age": 25, "teams": ["Marketing", "Sales"]}
        new_data = {"name": "John Smith", "age": 30, "teams": ["Sales", "Development"]}
        self.collection.insert_one(old_data)
        # envoyer une requête PUT pour mettre à jour les données de l'employé ajouté précédemment
        response = client.put(f"/update_employee?oldname={old_data['name']}", json=new_data)
        # vérifier que la réponse est bien un code 200 (succès)
        self.assertEqual(response.status_code, 200)

