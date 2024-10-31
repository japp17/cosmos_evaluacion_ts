from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class Usuario(BaseModel):
    id: str = Field(..., example='u1')
    nombre: str = Field(..., example='Juan')
    email: str = Field(..., example='juan.perez@example.com')
    edad: int = Field(..., ge =1, example=31)

class Proyecto(BaseModel):
    id: str = Field(..., example='p1')
    nombre: str= Field(..., example='Proyecto XYZ')
    descripcion: str= Field(..., example='Descripcion del Proyecto XYZ')
    id_usuario: str = Field(..., example='u1')