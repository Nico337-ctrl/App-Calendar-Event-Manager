# from os import path
from notifypy import Notify



def notificacion(mensaje, titulo):
    notificacion = Notify()
    notificacion.title = titulo
    notificacion.message = mensaje
    notificacion.send()
    #notificacion.icon = "D:/Workspace/Nicolas/App-Calendar-Event-Manager/calendeventmanager/static/src/images/sena-azul.png"
    # icono = "logo-del-sena-01.png"
    # ruta = path.abspath(path.dirname(__file__))
    # notificacion.icon = path.join(ruta, icono)


#ejemplo de envio de notificacion    
# enviarNotificacion('Este es una notificacion push ', 'Notificacion emergente')