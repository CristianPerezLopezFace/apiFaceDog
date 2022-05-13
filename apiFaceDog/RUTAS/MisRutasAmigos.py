import base64
import email
from tokenize import String
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter

from models import notificacion
import conexion
from voluptuous.error import MultipleInvalid
import my_token
import pymongo


rutasAmigos = APIRouter()


@rutasAmigos.get(
    '/amigos/{email}',
    tags=["Amigos"],
    response_model = []
)
def getAll(email :str) : 
   
    email = email.replace(" ", "")
    user=conexion.conexion.find_one({"email":email})
    userDict=dict(user)
    amigos=[]
    for id in userDict["amigos"] :
        amigo=conexion.conexion.find_one({"id":id},{"_id":0,"amigos":0,"surName":0,"password":0,"roles":0,"email":0})
        amigos.append(amigo)
    return amigos

@rutasAmigos.post(
    '/crearNotificacion',
    tags=["Amigos"]
)
def crearNotificacion(notifi : notificacion) :

    newNoti:notificacion={
        "idUser":notifi.idUser,
        "tipo":notifi.tipo,
        "idDestino":notifi.idDestino,
        "fecha":notifi.fecha,
        "name":notifi.name,
        "idObj":notifi.idObj
    }
    conexion.conexion.Notificacion.insert_one(newNoti)
    print("insertadaCorrectamente")

@rutasAmigos.get(
    '/notificacion/{email}',
    tags=["Amigos"],
    response_model=[]
)
def getNotificacion(email:str) :
      lista=[]
      user=conexion.conexion.find_one({'email':email})
      respuesta=conexion.conexion.Notificacion.find({'idDestino':user["email"]},{"_id":0})
      for i in respuesta:
          lista.append(i)
      
      return lista

@rutasAmigos.post(
    '/aceptarAmigo',
    tags=["Amigos"]
)
def aceptarAmigo(notifi:notificacion) :
      user=conexion.conexion.find_one({'email':notifi.idDestino})
      userAmigo=conexion.conexion.find_one({'email':notifi.idUser})

      print(user)
      print(userAmigo)
      #añadimos el amigo al destinatario
      lista=[]
      for amigo in user["amigos"]:
         lista.append(amigo)
     
      if not lista.__contains__(userAmigo["id"]):
          lista.append(userAmigo["id"])

         
      print(lista)
      conexion.conexion.update_one({"id":user["id"]}, {"$set": {"amigos":lista}}) 
      
      #añadmos al destinatario a la lista de amigos
      lista=[]
      for amigo in userAmigo["amigos"]:
          lista.append(amigo)
     
      if not lista.__contains__(user["id"]):
          lista.append(user["id"])
      print(lista)
      conexion.conexion.update_one({"id":userAmigo["id"]}, {"$set": {"amigos":lista}}) 
      conexion.conexion.Notificacion.delete_one({'fecha':notifi.fecha})
      
      return "ok"

