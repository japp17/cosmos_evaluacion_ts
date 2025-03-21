from fastapi import FastAPI, HTTPException, Query, Path
from typing import List, Optional
from models import Usuario, Proyecto
from azure.cosmos import exceptions
from datetime import datetime
from database import container_usu, container_pry

app = FastAPI(title='API de Gestion de Usuarios y Proyectos - Examen Final Juan Peña')

### Endpoint de Eventos

@app.get("/")
def home():
    return "Hola Mundo"

###USUARIOS###
#Crear usuario POST
@app.post("/usuarios/", response_model=Usuario, status_code=201)
def create_usuario(event: Usuario):
    try:
        container_usu.create_item(body=event.dict())
        return event
    except exceptions.CosmosResourceExistsError:
        raise HTTPException(status_code=400, detail="El usuario con este ID ya existe")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))    
    
#Listar usuario GET
@app.get("/usuarios/", response_model=List[Usuario])
def List_event():
    query = "SELECT * FROM c WHERE 1=1"
    items = list(container_usu.query_items(query=query, enable_cross_partition_query=True))
    return items
    
#Actualizar usuario PUT
@app.put("/usuarios/{usuario_id}", response_model=Usuario)
def update_usuario(usuario_id:str, updated_usuario: Usuario):
    try:
        existing_usuario = container_usu.read_item(item=usuario_id, partition_key=usuario_id)
        existing_usuario.update(updated_usuario.dict(exclude_unset=True))
        container_usu.replace_item(item=usuario_id, body=existing_usuario)

        return existing_usuario
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Usuario no encotrado')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Eliminar usuario DELETE
@app.delete("/usuarios/{usuario_id}", status_code=204)
def delete_usuario(usuario_id: str):
    try:
        container_usu.delete_item(item=usuario_id, partition_key=usuario_id)
        return
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))