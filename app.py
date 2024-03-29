from flask import Flask, render_template,request
import subprocess
import requests
import socket

app = Flask(__name__)

@app.route('/')
def index():
    # Rendre le fichier HTML index.html
    return render_template('./index.html')



@app.route('/connexion', methods=['POST'])
def connexion():
    # Récupérer les données du formulaire
    roomName = request.form['roomName']
    ssid = request.form['ssid']
    password = request.form['password']
    appURL = request.form['appURL']
    rotation = request.form['rotation']
    print(f"roomName: {roomName}, ssid: {ssid}, password: {password}, appURL: {appURL}, rotation: {rotation}")
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    
    r = requests.post(f"{appURL}/addRaspberryPi",json={"salle":roomName,"addressIp":IPAddr})
    # Execute the command
    process = subprocess.Popen('nmcli con delete localnet', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the command to finish and get the return code
    return_code = process.wait()

    process = subprocess.Popen(f"sudo nmcli con add type wifi ifname 'wlan0' ssid '{ssid}' \
    con-name 'localnet' -- wifi-sec.key-mgmt 'wpa-psk' \
    wifi-sec.psk '{password}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    return_code = process.wait()
    if return_code != 0:
        return render_template('./erreur.html',erreur="Erreur lors de la création de la connexion au réseau wifi")
    
    try:
        with open('/home/pi/Desktop/PFE/.env','w') as f:
            f.write(f"ROOM_NAME={roomName}\nURL_BACKEND={appURL}\nROTATION={rotation}")
    except FileNotFoundError:
        return render_template('./erreur.html',erreur="Fichier de configuration introuvable")

    process = subprocess.Popen('sleep 10 && sudo reboot', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return render_template('./configurationTermine.html')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999,debug=True)
