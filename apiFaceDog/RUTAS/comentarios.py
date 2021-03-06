

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from models import UserModel
from models import imgModel,comentario
from models import comentario
import my_token
from models import notificacion
import conexion



rutasComentarios = APIRouter()


@rutasComentarios.post(
    '/crearComentario',
    tags=["Comentarios"]
)
def crearComentario(comen : comentario, token_user=Depends(my_token.auth_wrapper)) :
    imagen:imgModel=conexion.conexion.FOTOS.find({"id":comen.idFoto},{"_id":0})
    
    comentUser=[]
    for coment in imagen[0]["comentarios"] : 
        comentUser.append(coment)
    newComen:comentario={
        "id":len(imagen[0]["comentarios"]),
        "idFoto":comen.idFoto,
        "emailUsuario":comen.emailUsuario,
        "nameUsuario":comen.nameUsuario,      
        "texto":comen.texto,
        "fecha":comen.fecha,
        "likes":[]
    }
    comentUser.append(newComen)
    conexion.conexion.FOTOS.update_one({"id":comen.idFoto}, {"$set": {"comentarios":comentUser}})
  
@rutasComentarios.get(
    '/comentarios/{id}',
    tags=["Comentarios"],
    response_model = []
)
def getAll(id:str, token_user=Depends(my_token.auth_wrapper)) : 
    imagen=conexion.conexion.FOTOS.find({"id":id},{"_id":0}) 
    listaComentarios=[]
    for comen in imagen[0]["comentarios"] :    
        listaComentarios.append(comen)
    return listaComentarios

@rutasComentarios.get(
    '/comentarios_one/{id}/{id_comentario}',
    tags=["Comentarios"],
    response_model = []
)
def get_one(id:str,id_cometario:int, token_user=Depends(my_token.auth_wrapper)) : 
    imagen=conexion.conexion.FOTOS.find({"id":id},{"_id":0}) 
    
    for comen in imagen[0]["comentarios"] :    
        if comen.id == id_cometario : 
             return comen
        else:
            return False







@rutasComentarios.get(
    '/actualeNotices/{email}',
    tags=["Comentarios"]
)   
def getFotosAmigos(email:str, token_user=Depends(my_token.auth_wrapper)):
    listaTodo=[]  
    listaInd=conexion.conexion.Fotos.find({'email':email})
    for foto in listaInd:

        listaTodo.append(foto)
    
    return listaTodo


@rutasComentarios.post(
    '/borrarNotificacionComentario/',
    tags=["Comentarios"]
)
def borrarNotificacion(notifi:notificacion, token_user=Depends(my_token.auth_wrapper)) :
     
      conexion.conexion.Notificacion.delete_one({'fecha':notifi.fecha,'tipo':notifi.tipo,'idUser':notifi.idUser})

      return "ok"



        
@rutasComentarios.get(
    '/users/addLikeComentario/{id_foto}/{id_user}/{posicion}',
    tags=["Comentarios"]
    )
def  likeComentario(id_foto:int,id_user:int,posicion:int) : 

    oldImg:imgModel= conexion.conexion.FOTOS.find_one({"id":id_foto},{"_id":0})

    comentarios=oldImg["comentarios"]

    oldcoment:comentario=comentarios[posicion]
    
    likes=oldcoment["likes"]

    if not likes.__contains__(id_user) : 
        likes.append(id_user)
        
    
    newComent=dict(oldcoment)
    newComent.update({'likes':likes})  
    comentarios.remove(oldcoment)
    comentarios.insert(posicion,newComent)
    conexion.conexion.FOTOS.update_one({"id":id_foto}, {"$set": {"comentarios":comentarios}}) 
      
   #a??admos al destinatario a la lista de amigos
    return "ok"