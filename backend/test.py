from pymongo import MongoClient

client = MongoClient("mongodb+srv://22z212:TfVGyfVhyjG8hkNJ@cluster0.gbcugd2.mongodb.net/test?retryWrites=true&w=majority&ssl=true&appName=Cluster0")
db = client.test
print(db.list_collection_names())

