from azure.cosmos import CosmosClient, exceptions
from dotenv import load_dotenv
import os


# Obtener las variables de entorno
COSMOS_ENDPOINT = 'https://acdbjppdev.documents.azure.com:443/'
COSMOS_KEY = 'vq8ptSADKHMefzt7WKWAEIY533or0gF1P0RsqSnbGsnosxkBttJUMUAhGozoFaSOqZj0B6D5NVGSACDbG7jJgw=='
DATABASE_NAME = 'GestorProyectosDB'

# Inicializar el cliente de Cosmos DB
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
USUARIO_CONTAINER = client.get_database_client(DATABASE_NAME).get_container_client("usuarios")
PROYECTOS_CONTAINER = client.get_database_client(DATABASE_NAME).get_container_client("proyectos")

# Crear o obtener la base de datos
try:
    database = client.create_database_if_not_exists(id=DATABASE_NAME)
except exceptions.CosmosResourceExistsError:
    database = client.get_database_client(DATABASE_NAME)

# Crear o obtener el contenedor Usuario
try:
    container_usu = database.create_container_if_not_exists(
        id=USUARIO_CONTAINER,
        partition_key={'paths': ['/id'], 'kind': 'Hash'},
        offer_throughput=400
    )
except exceptions.CosmosResourceExistsError:
    container_usu = database.get_container_client(USUARIO_CONTAINER)

# Crear o obtener el contenedor Proyectos
try:
    container_pry = database.create_container_if_not_exists(
        id=PROYECTOS_CONTAINER,
        partition_key={'paths': ['/id'], 'kind': 'Hash'},
        offer_throughput=400
    )
except exceptions.CosmosResourceExistsError:
    container_pry = database.get_container_client(PROYECTOS_CONTAINER) 