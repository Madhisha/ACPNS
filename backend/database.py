from pymongo import MongoClient

MONGO_URI = "mongodb+srv://22z212:TfVGyfVhyjG8hkNJ@cluster0.gbcugd2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI, connectTimeoutMS=30000, socketTimeoutMS=30000)
db = client['ecampus']
user_collection = db['new_users']