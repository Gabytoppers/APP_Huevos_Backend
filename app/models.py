from pymongo import MongoClient

mongo_uri = "mongodb+srv://myAtlasDBUser:FlsztsABiY1luHwL@myatlasclusteredu.jakrico.mongodb.net/?retryWrites=true&w=majority&appName=myAtlasClusterEDU"

# Crear cliente de MongoDB con desactivación de certificados SSL
client = MongoClient(mongo_uri, tlsAllowInvalidCertificates=True)

try:
    db = client["granja_db"]

    huevos_collection = db["huevos"]
    ventas_collection = db["ventas"]
   
    client.admin.command('ismaster')
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"Error de conexión a MongoDB: {e}")
