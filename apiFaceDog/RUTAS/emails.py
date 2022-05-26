
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from ssl import create_default_context
import ssl
from fastapi.routing import APIRouter
import smtplib
import conexion


rutasEmails = APIRouter()


@rutasEmails.get(
    '/email/{email}',
    tags=["Fotos"]
)

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
                       
                            <a href="https://facedogapirest.herokuapp.com/confirmarEmail/?email="""+email+"""">Pincha aqui para confirmar tu cuenta</a>                       
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
    return True


@rutasEmails.get('/confirmarEmail/',
            response_description='Get one user',
            summary='',
            tags=['users']
            )
def confirmarEmail(email:str):
    html = """
                <html>
                    <head>
                        <title>Civi-cancelaciones :(</title>
                    </head>
                    <body>
                            <h1>Cuenta confirmada</h1>
                            <script>
                                window.location.replace("https://facedog-933a5.web.app/")
                            </script>
                    </body>
                </html>
            """

    try:
        print(email)
        oldUser = conexion.conexion.find_one({"email": email})
        
        user =  dict(oldUser)
        user.update({'habilitado': 1})
        newUser = {
            "$set": dict(user)
        }
        conexion.conexion.update_one(oldUser, newUser)

    except:
        raise HTTPException(
            status_code=404, detail="The id entered is not wrong")
    return HTMLResponse(html, status_code=200)



