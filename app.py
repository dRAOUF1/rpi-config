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
    print(f"roomName: {roomName}, ssid: {ssid}, password: {password}, appURL: {appURL}")

    # Execute the command
    process = subprocess.Popen('nmcli con delete localnet', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the command to finish and get the return code
    return_code = process.wait()

    process = subprocess.Popen(f"sudo nmcli con add type wifi ifname 'wlan0' ssid 'D-Link1' \ncon-name 'localnet' -- wifi-sec.key-mgmt 'wpa-psk' \nwifi-sec.psk '%Fortress123&'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    return render_template('./connexion.html')

if __name__ == '__main__':
    app.run(debug=True)
