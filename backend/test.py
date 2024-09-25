from pymongo import MongoClient

client = MongoClient("mongodb+srv://22z212:TfVGyfVhyjG8hkNJ@cluster0.gbcugd2.mongodb.net/test?retryWrites=true&w=majority&ssl=true&appName=Cluster0")
users_collection = client['ecampus']['users']
for user in users_collection.find():
    print(user['rollNo'],user['notifications']['attendance'],user['notifications']['marks'])

