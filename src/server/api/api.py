from fastapi import FastAPI
from services.index.index_construct_utils import path_to_dbname
from services.db_interface.db_manager import get_db_manager
from pgvector import Vector
from pydantic import BaseModel
from typing import List
from resources.strings.string_resource import host, server_port
import uvicorn

app = FastAPI()

class VectorMsg(BaseModel):
    embedding: List[float]
    db_path: str
    num_result : int

@app.post("/query_vector/")
def query_vector(msg: VectorMsg):
    db_manager = get_db_manager()
    db = db_manager.get_table(path_to_dbname(msg.db_path))
    results = db.query_embedding(Vector(msg.embedding), num_result=msg.num_result)
    final_result = [(result[0], result[1], 1) for result in results]
    return {
        "results" : final_result
    }

@app.get("/database_paths/")
def get_db_paths():
    db_manager = get_db_manager()
    db_paths = db_manager.get_db_paths()
    return {
        "database_paths" : db_paths
    }

def run_api():
    uvicorn.run(app, host=host, port=server_port)