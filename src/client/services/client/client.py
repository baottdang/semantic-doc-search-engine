import requests

class Client():
    def __init__(self):
        self.query_port = "http://127.0.0.1:8000/query_vector/"
        self.db_paths_port = "http://127.0.0.1:8000/database_paths/"
        
    def query_on_server(self, embedding, db_path, num_result):
        payload = {
            "embedding" : embedding.flatten().tolist(),
            "db_path" : db_path,
            "num_result" : num_result
            }
        try:
            response = requests.post(self.query_port, json=payload)
            if response.status_code == 200:
                result = response.json()
                return result["results"]
            else:
                return []
        except Exception as e:
            return []
    
    def request_db_paths(self):
        try:
            response = requests.get(self.db_paths_port)
            if response.status_code == 200:
                result = response.json()
                return result["database_paths"]
            else:
                return []
        except Exception as e:
            return []

_client = Client()

def get_client():
    return _client
