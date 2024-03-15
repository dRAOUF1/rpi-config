from flask import Flask, render_template,request
import subprocess

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

    # Execute the command
    process = subprocess.Popen('nmcli con delete localnet', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the command to finish and get the return code
    return_code = process.wait()

    process = subprocess.Popen(f"sudo nmcli con add type wifi ifname 'wlan0' ssid '{ssid}' \
    con-name 'localnet' -- wifi-sec.key-mgmt 'wpa-psk' \
    wifi-sec.psk '{password}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    return_code = process.wait()
    if return_code != 0:
        return render_template('./erreur.html',erreur="Erreur lors de la connexion au réseau wifi")
    with open('/home/pi/Desktop/PFE/.env','w') as f:
        f.write(f"ROOM_NAME={roomName}\nURL_BACKEND={appURL}\nROTATION={rotation}")


    return render_template('./configurationTermine.html')

if __name__ == '__main__':
    app.run(debug=True)
