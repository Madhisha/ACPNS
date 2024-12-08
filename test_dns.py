import dns.resolver
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# MongoDB connection URI
MONGO_URI = "mongodb+srv://22z212:TfVGyfVhyjG8hkNJ@cluster0.gbcugd2.mongodb.net/?retryWrites=true&w=majority"

def check_srv_dns():
    """Check DNS SRV records for MongoDB cluster."""
    try:
        srv_records = dns.resolver.resolve('_mongodb._tcp.cluster0.gbcugd2.mongodb.net', 'SRV')
        print("SRV Records:")
        for record in srv_records:
            print(f" - Target: {record.target}, Port: {record.port}")
    except Exception as e:
        print(f"DNS SRV resolution failed: {e}")

def check_mongodb_connection():
    """Test MongoDB connection."""
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')  # Pinging the server
        print("MongoDB connection successful!")
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    print("Checking DNS SRV records...")
    check_srv_dns()
    print("\nTesting MongoDB connection...")
    check_mongodb_connection()
