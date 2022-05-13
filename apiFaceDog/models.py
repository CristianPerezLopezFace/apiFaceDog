from dataclasses import dataclass
from datetime import date
from xmlrpc.client import DateTime
from pydantic import BaseModel 


def users_Entity(entidad) -> list:
    return [UserModel(item) for item in entidad]

class UserModel(BaseModel) : 
    id:int
    password:str
    name : str
    surName : str
    ciudad:str
    email : str
    roles : str
    descripcion:str

class comentario(BaseModel):
    id:int
    idFoto:int
    emailUsuario:str
    nameUsuario:str
    texto:str
    fecha:str 
    likes=[]

    

class imgModel(BaseModel):
    id:int
    titulo:str
    descripcion:str
    foto:str
    email:str
    principal:int
    fechaModificacion:str
    tipo:str
    likes=[]
    comentarios=[]
    
class userToken(BaseModel):
    roles: str
    name: str
    surName : str
    ciudad:str
    email: str
    id_fotos:str

class loginModel(BaseModel):
    email:str
    password:str

class amigo(BaseModel):
    id :str
    name:str
    descripcion:str
    foto:str
    ciudad:str
    id_fotos:str

class notificacion(BaseModel):
    idUser:str
    name:str
    tipo:str
    idDestino:str
    fecha:str
    idObj:int


