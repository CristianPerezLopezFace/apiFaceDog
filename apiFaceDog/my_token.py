
from bson.objectid import ObjectId
from fastapi.exceptions import HTTPException
from fastapi import Security
import jwt
from models import userToken
from datetime import datetime, timedelta
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

secret ="contraseña"

security = HTTPBearer()

def decryptToken(token) : 
        user:userToken
        try : 
            user = jwt.decode(token,secret,algorithms =["HS256"])
            return user
            
        except jwt.ExpiredSignatureError :
            raise HTTPException(status_code = 401, detail = 'Signature has expired')

        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code = 401, detail = 'Invalid token')
      
def generateToken(user:userToken) :
    payload = {
        'exp' : datetime.utcnow() + timedelta(days=0, minutes=30),
        'iat' : datetime.utcnow(),
        'sub' : {          
            "email" : user["email"],
            "name" : user["name"],
            "roles" : user["roles"],
            "id_fotos":user["id_fotos"],
            "surName":user["surName"],
            "ciudad":user["ciudad"],
            "id":user["id"]
        }
    }
    token = jwt.encode(payload,secret,algorithm ="HS256")
    return token

def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(security)) :    
    return decryptToken(auth.credentials)