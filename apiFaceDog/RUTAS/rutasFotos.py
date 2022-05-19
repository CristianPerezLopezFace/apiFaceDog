
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from models import UserModel,imgModel,userToken,loginModel
import conexion
import schemas
import gridfs
from voluptuous.error import MultipleInvalid
import my_token

import pymongo

rutasFotos = APIRouter()

@rutasFotos.post(
    '/imag',
    tags=["Fotos"]
)

def create_img(img:imgModel, token_user=Depends(my_token.auth_wrapper)) :
    
    
    try : 
        try : 
            result=conexion.conexion.FOTOS.find().sort("id",pymongo.DESCENDING)
            id_max= result[0].get("id")
        except Exception :
                id_max = 1
        newImg=dict(img)
        newImg.update({
            "id":int(id_max)+1,
            "comentarios":[],
            "likes":[]
        })
        
        conexion.conexion.FOTOS.insert_one(newImg)
      
        return "todo ok"
    except MultipleInvalid as e: 
        raise  HTTPException(status_code=500,detail="error type data: "+str(e))
    except Exception as e: 
        raise HTTPException(status_code=422,detail="unfilled fields "+str(e))

@rutasFotos.get(
    '/users/imagenPrincipal/{nameEmail}',
    response_model=imgModel,
    tags=["Fotos"]
    )

def  getImagePrincipal(nameEmail:str, token_user = Depends(my_token.auth_wrapper)) : 
    
    imagen:imgModel=conexion.conexion.FOTOS.find_one({"email":nameEmail,"principal":1},{"_id":0})
    
    return imagen

@rutasFotos.get(
    '/users/imagen/id/{id}',
    response_model=imgModel,
    tags=["Fotos"]
    )
def  getImage(id:int, token_user = Depends(my_token.auth_wrapper)) : 
    
    imagen:imgModel=conexion.conexion.FOTOS.find_one({"id":id},{"_id":0})
    
    return imagen


@rutasFotos.get(
    '/users/allImagen/{nameEmail}',
    response_model=[],
    tags=["Fotos"]
    )
def  getAllImag(nameEmail:str, token_user=Depends(my_token.auth_wrapper)) : 
    
    imagen=conexion.conexion.FOTOS.find({"email":nameEmail,"tipo":"user"},{"_id":0})
    listaImg=[]
    for img in imagen :
        listaImg.append(img)
    
    
    return listaImg


@rutasFotos.get(
    '/users/allImagen/{nameEmail}',
    response_model=[],
    tags=["Fotos"]
    )
def  getAllImag(nameEmail:str, token_user=Depends(my_token.auth_wrapper)) : 
    
    imagen=conexion.conexion.FOTOS.find({"email":nameEmail,"tipo":"user"},{"_id":0})
    listaImg=[]
    for img in imagen :
        listaImg.append(img)
    
    
    return listaImg


@rutasFotos.get(
    '/users/skip{skip}/limit{limit}/email{email}',
     response_model=[],
    tags=["imagenes paginados"]
)
def find_all_users(skip:int,limit:int,email:str, token_user=Depends(my_token.auth_wrapper)) : 
    try :
        imagenes=conexion.conexion.FOTOS.find({"email":email},{"_id":0}).skip(skip).limit(limit)
        listaImg=[]
        for img in imagenes :
             listaImg.append(img)
    
        total :int = conexion.conexion.FOTOS.count()
        usersAndTotal= {
            'users':listaImg,
            'total': total
        }
    except :
        raise HTTPException(status_code=404,detail="Error whit list")
    else : 
        return usersAndTotal
@rutasFotos.get(
    '/users/ImgVeterinario/',
    response_model=[],
    tags=["Fotos"]
    )
def  getAllImagVeter(token_user=Depends(my_token.auth_wrapper)) : 
    
    imagen=conexion.conexion.FOTOS.find({"tipo":"veterinario"},{"_id":0})
    listaImg=[]
    for img in imagen :
        listaImg.append(img)
    
    return listaImg

@rutasFotos.get(
    '/users/ImgVeterinarioByUser/{email}',
    response_model=[],
    tags=["Fotos"]
    )
def  getAllImagVeterByUser(email:str, token_user=Depends(my_token.auth_wrapper)) : 
    
    imagen=conexion.conexion.FOTOS.find({"tipo":"veterinario","email":email},{"_id":0})
    listaImg=[]
    for img in imagen :
        listaImg.append(img)
    
    return listaImg

@rutasFotos.post(
    '/users/updatePrincipalImagen',
    tags=["Fotos"]
    )
    
def  updateImgPrincipal(foto:imgModel, token_user=Depends(my_token.auth_wrapper)) : 
    
    
    oldImg:imgModel= conexion.conexion.FOTOS.find_one({"email":foto.email,"principal":1},{"_id":0})
    if oldImg :
       oldImg2=dict(oldImg)
      
       conexion.conexion.FOTOS.update_one({"id":oldImg2["id"]}, {"$set": {"principal":0}}) 
   
    conexion.conexion.FOTOS.update_one({"id":foto.id}, {"$set": {"principal":1}})
    conexion.conexion.update_one({"email":foto.email},{"$set": {"foto":foto.foto}})
  
 
    return "ok"

@rutasFotos.post(
    '/users/updateImagen',
    tags=["Fotos"]
    )
    
def  updateImg(foto:imgModel, token_user=Depends(my_token.auth_wrapper)) : 
   
    
    conexion.conexion.FOTOS .update_one({"id":foto.id},{"$set": {"titulo":foto.titulo,"descripcion":foto.descripcion,"fechaModificacion":foto.fechaModificacion}})
    return "ok"
@rutasFotos.post(
    '/users/deleteImagen/byId',
    tags=["Fotos"]
    )
    
def  updateImg(foto:imgModel) : 
   
    
    conexion.conexion.FOTOS .delete_one({"id":foto.id})
    return "ok"

@rutasFotos.get(
    '/users/addLike/{id_foto}/{id_user}',
    tags=["Fotos"]
    )
def  likeFoto(id_foto:int,id_user:int, token_user=Depends(my_token.auth_wrapper)) : 
    
    oldImg:imgModel= conexion.conexion.FOTOS.find_one({"id":id_foto},{"_id":0})
  
    lista=[]
    for like in oldImg["likes"]:
            lista.append(like)
    if not lista.__contains__(id_user) : 
        lista.append(id_user)
    
    conexion.conexion.FOTOS.update_one({"id":id_foto}, {"$set": {"likes":lista}}) 
     
    return True
