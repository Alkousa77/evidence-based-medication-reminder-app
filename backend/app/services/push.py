import requests

def send_push_notification(token, title, body):
    message={
        "to":token,
        "sound":"default",
        "title":title,
        "body":body,
    }
    #send notification request to expo server
    response = requests.post(
        "https://exp.host/--/api/v2/push/send", #contact expo notificaiton servers to forward notification (json) to device
        json=message 
    )
    
    return response.json() # return the reponse from expo (ok, error)