from flask import Flask, render_template,request
import subprocess
import requests
import socket, os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
@app.route('/')
def index():
    default_values = {
        'mode': os.getenv('MODE', 'reseau'),
        'room_name': os.getenv('ROOM_NAME', ''),
        'app_url': os.getenv('URL_BACKEND', ''),
        'rotation': os.getenv('ROTATION', '0'),
        'detection_threshold': os.getenv('DETECTION_THRESHOLD', '0.65'),
        'recognition_threshold': os.getenv('RECOGNITION_THRESHOLD', '0.45'),
        'tracker_max_distance': os.getenv('TRACKER_MAX_DISTANCE', '90'),
        'tracker_max_frame_loss': os.getenv('TRACKER_MAX_FRAME_LOSS', '4')
    }
    # Rendre le fichier HTML index.html
    return render_template('index.html', default_values=default_values)



@app.route('/connexion', methods=['POST'])
def connexion():
    # Récupérer les données du formulaire
    roomName = request.form['roomName']
    ssid = request.form['ssid']
    password = request.form['password']
    appURL = request.form['appURL']
    rotation = request.form['rotation']
    detection_threshold = request.form['detection_threshold']
    recognition_threshold = request.form['recognition_threshold']
    tracker_max_distance = request.form['tracker_max_distance']
    tracker_max_frame_loss = request.form['tracker_max_frame_loss']
    mode = request.form["mode"]
    print(f"roomName: {roomName}, ssid: {ssid}, password: {password}, appURL: {appURL}, rotation: {rotation}, detection_threshold: {detection_threshold}, recognition_threshold: {recognition_threshold}, tracker_max_distance: {tracker_max_distance}, tracker_max_frame_loss: {tracker_max_frame_loss}")
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    
    if mode=="reseau":
        #r = requests.post(f"{appURL}/addRaspberryPi",json={"salle":roomName,"addressIp":IPAddr})
        # Execute the command
        process = subprocess.Popen('nmcli con delete localnet', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the command to finish and get the return code
        return_code = process.wait()

        process = subprocess.Popen(f"sudo nmcli con add type wifi ifname 'wlan0' ssid '{ssid}' \
        con-name 'localnet' -- wifi-sec.key-mgmt 'wpa-psk' \
        wifi-sec.psk '{password}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        return_code = process.wait()
        # if return_code != 0:
        #     return render_template('./erreur.html',erreur="Erreur lors de la création de la connexion au réseau wifi")
    

    
    
    try:
        with open('/home/pi/Desktop/PFE/.env','w') as f:
            f.write(f"MODE={mode}\nROOM_NAME={roomName}\nURL_BACKEND={appURL}\nROTATION={rotation}\n DETECTION_THRESHOLD={detection_threshold/100}\nRECOGNITION_THRESHOLD={recognition_threshold}\nTRACKER_MAX_DISTANCE={tracker_max_distance}\nTRACKER_MAX_FRAME_LOSS={tracker_max_frame_loss}")
        with open('.env','w') as f:
            f.write(f"MODE={mode}\nROOM_NAME={roomName}\nURL_BACKEND={appURL}\nROTATION={rotation}\n DETECTION_THRESHOLD={detection_threshold/100}\nRECOGNITION_THRESHOLD={recognition_threshold}\nTRACKER_MAX_DISTANCE={tracker_max_distance}\nTRACKER_MAX_FRAME_LOSS={tracker_max_frame_loss}")
    except FileNotFoundError:
        return render_template('./erreur.html',erreur="Fichier de configuration introuvable")

    if mode=="reseau":
        process = subprocess.Popen('sleep 10 && sudo reboot', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return render_template('./configurationTermine.html')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999,debug=True)
