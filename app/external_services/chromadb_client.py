import chromadb
import os

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db'))
client = chromadb.PersistentClient(path=db_path)
collection = client.get_collection(name="jurisprudencia_peruana")
