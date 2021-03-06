
from fastapi import FastAPI
import pymongo
import tags
from fastapi import HTTPException
from RUTAS.misRutasUser import rutas
from RUTAS.MisRutasAmigos import rutasAmigos
from RUTAS.rutasFotos import rutasFotos
from fastapi.middleware.cors import CORSMiddleware
from RUTAS.comentarios import rutasComentarios
from RUTAS.emails import rutasEmails
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

try :

    mongo_client_nube = "mongodb+srv://Practica:DAM@cluster0.fkixc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    mongo_client_local = "mongodb+srv://Cristian:root@cluster0.1wun7.mongodb.net/test"
    client = pymongo.MongoClient(mongo_client_local)   
    # database = client["FACEDOG"]
    database = client["FaceDog2"]
    conexion = database["USERS"]  
    
   

except pymongo.errors.ServerSelectionTimeoutError as errorEx:
    raise HTTPException(status_code=422,detail="unfilled fields"+errorEx)


app = FastAPI(
    title=tags.title,
    description=tags.description,
    contact=tags.contact,
   
)

app.include_router(rutas)
app.include_router(rutasAmigos)
app.include_router(rutasFotos)
app.include_router(rutasComentarios)
app.include_router(rutasEmails)


    # "https://facedog-933a5.web.app/",
    # "http://localhost:4200"
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    # HTTPSRedirectMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

