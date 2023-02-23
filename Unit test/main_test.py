import unittest
import requests

class mainTest(unittest.TestCase):
    def test_get_employee(self):
        reponse = requests.get('http://localhost:8000/employee')
        self.assertEqual(reponse.status_code, 200)

    def test_create_employee(self):
        employee = {'name': 'Michel Dufour', 'age': '63', 'teams': '["Technologies"]'}
        response = requests.post('http://localhost:8000/employee', json=employee)
        self.assertEqual(response.status_code, 200)

    def test_update_employee(self):
        employee = {'task': 'Updated Test Task', 'importance': 'high', 'completed': True}
        response = requests.put('http://localhost:8000/employee', json=employee)
        self.assertEqual(response.status_code, 200)

    def test_delete_task(self):
        response = requests.delete('http://localhost:8000/employee')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()