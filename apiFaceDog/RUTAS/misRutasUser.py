
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from numpy import int_
import pymongo

from models import UserModel, imgModel, userToken, loginModel
import conexion
import schemas
from voluptuous.error import MultipleInvalid
import my_token
from RUTAS.emails import rutasEmails

rutas = APIRouter()


@rutas.post(
    '/userLogin',
    tags=['Users']
)
def login_user(login: loginModel):

    user: userToken
    try:
        user = conexion.conexion.find_one(
            {"email": login.email, "password": login.password}, {'password': 0, "_id": 0})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Email o contraseña incorrectos"+e)

    if not user:
        raise HTTPException(status_code=404, detail="Email o contraseña incorrectos")
    else:
        
        if( user["habilitado"] == 1) : 
                
            return my_token.generateToken((user))

        else : 
             raise HTTPException(status_code=404, detail="Confirme su cuenta" )
            
        
@rutas.post(
    '/create/users',
    tags=["Users"]
)
def create_user(user: UserModel):


    # try:
        userExits = conexion.conexion.find_one({"email": user.email})
        if not userExits:
            try : 
                result = conexion.conexion.find().sort("id", pymongo.DESCENDING)
                id_max = result[0].get("id")
            
            except Exception :
                id_max = 1
            newUser = dict(user)
            newUser.update({'id_fotos': user.email})
            newUser.update({'id': (int(id_max)+1)})
            newUser.update({'foto': ""})
            newUser.update({'habilitado': 0})
            newUser.update({'amigos': []})
            conexion.conexion.insert_one(newUser)
            menssage = "User: " + user.name + "solo falta confirmar tu cuenta"
            
            enviarEmail(user.email)
        else:
            menssage = "La cuenta ya esta regitrada"

        return menssage
    # except:
    #     raise HTTPException(
    #         status_code=422, detail="A user object is required")


@rutas.get(
    '/users/{email}',
    tags=["Users"],
    response_model=UserModel
)
def get_one_user(email: str, token_user=Depends(my_token.auth_wrapper)):
    email = email.replace(" ", "")
    try:
        schemas.schema_Get_User({
            "email": email
        })
        user: UserModel
        user = conexion.conexion.find_one(
            {"email": email}, {"amigos": 0, "foto": 0})
        if not user:
            raise HTTPException(
                status_code=404, detail="email incorrecto")
        else:
            return user
    except MultipleInvalid as e:
        raise HTTPException(status_code=400, detail=str(e))
   


@rutas.get(
    '/users/id/{id}',
    tags=["Users"],
    response_model=UserModel
)
def get_one_user_by_id(id: int, token_user=Depends(my_token.auth_wrapper)):

    try:

        user: UserModel
        user = conexion.conexion.find_one({"id": id}, {"amigos": 0, "foto": 0})
     
        return user

    except MultipleInvalid as e:
        raise HTTPException(status_code=400, detail=str(e))
    except:
        raise HTTPException(
            status_code=500, detail="The id entered is not wrong")

@rutas.get(
    '/Allusers',
    tags=["Users"],
    response_model = []
)
def getAllUsers(token_user=Depends(my_token.auth_wrapper)) :
    amigosList=[]
    amigos=conexion.conexion.find({},{"_id":0,"amigos":0,"surName":0,"password":0,"roles":0,"email":0})
    for amigo in amigos :
        amigosList.append(amigo)
    return amigosList


@rutas.get(
    '/users/skip{skip}/limit{limit}/rol{rol}',
    tags=["All_Users"],
    response_model={}
)
def find_all_users(skip: int, limit: int, rol: str, token_user=Depends(my_token.auth_wrapper)):
    try:
        lista = []
        users = conexion.conexion.find(
            {"roles": rol}, {"_id": 0}).skip(skip).limit(limit)
        for user in users:
            lista.append(user)
        total: int = conexion.conexion.count()
        usersAndTotal = {
            'users': lista,
            'total': total
        }
    except:
        raise HTTPException(status_code=404, detail="Error whit list")
    else:
        return usersAndTotal


@rutas.put(
    '/users/{id}',
    tags=["Update_One_User"]

)
def update_user(id: int, user: UserModel, token_user=Depends(my_token.auth_wrapper)):
    oldUser: UserModel
    try:
        oldUser = conexion.conexion.find_one({"id": id})
        newUser = {
            "$set": dict(user)
        }
    except:
        raise HTTPException(
            status_code=404, detail="The id entered is not wrong")

    try:
        conexion.conexion.update_one(oldUser, newUser)
        return "User " + user.name + " was updated"
    except:
        raise HTTPException(status_code=500, detail="Unable to update user")


@rutas.delete(
    '/users/{id}',
    tags=["Delete_One_User"]

)
def delete_user(id: int,  token_user=Depends(my_token.auth_wrapper)):
    try:
        conexion.conexion.find_one_and_delete({"id": id})
        return "Delete correctly"
    except:
        raise HTTPException(
            status_code=404, detail="the id entered is not correct")


@rutas.get(
    '/Allveterinarios',
    tags=["Users"],
    response_model=[]
)
def getAllUsers( token_user=Depends(my_token.auth_wrapper)):
    veterinarioList = []
    amigos = conexion.conexion.find({"roles": "Veterinario"}, {
                                    "_id": 0, "amigos": 0, "surName": 0, "password": 0, "roles": 0})

    for amigo in amigos:

        veterinarioList.append(amigo)
    print(veterinarioList)
    return veterinarioList


def enviarEmail(email:str) : 
    html = """
         <html>
                <body style="padding: 3rem; background-color:orange;">
                    <div style="background-color: white; padding: 2.5rem;">
                        <center>
                            <hi>Face Dog Confirmacion</h1>
                            <img src="https://getwallpapers.com/wallpaper/full/6/1/d/1385810-vertical-cute-dog-wallpaper-2560x1600-picture.jpg" style="height: 100px;"/>
                        </center>
                        <h2 style="text-align:center; margin-button:3.5rem">Confirma tu cuenta de face dog</h2>
                        <center>
                            
                            <a href="https://facedogapirest.herokuapp.com/confirmarEmail/?email="""+email+"""" >Pincha aqui para confirmar tu cuenta</a>
                           
                        
                        </center>
                        </center>
                    </div>
                </body>
            
            </html>"""

    

    mensaje = MIMEMultipart('alternative')
    mensaje['Subject'] = "Confirmar cuenta FaceDog "
    mensaje.attach(MIMEText(html,'html'))

    with  smtplib.SMTP_SSL("smtp.gmail.com",465, context=ssl.create_default_context()) as server :
        server.login('faceDogAPP@gmail.com',"gxgztpeclklvnvaq")
        server.sendmail('faceDogAPP@gmail.com',email,mensaje.as_string() )