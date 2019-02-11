#coding: utf8
import requests
import json
import sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
sys.path.insert(0,'/home/jpmvjvmh/public_html/DarkSky/Utils')  # insérer dans sys.path le dossier contenant le/les modules
#sys.path.insert(0, '/home/ubuntu/workspace/Utils') # insérer dans sys.path le dossier contenant le/les modules
sys.path.insert(0, '../Utils') # insérer dans sys.path le dossier contenant le/les modules
from Utils import chaineUTCFromTs 
lon=3.06
lat=50.6
XMLFileName="darksky.json"
path="https://api.darksky.net/forecast/65c59c85e831f6ce989aa0b9c612c444/"+str(lat)+","+str(lon)+"?lang=fr&units=ca"
status=-1
r=None
while status != 200:
    r=requests.get(path)
    status=r.status_code
fichier = open(XMLFileName,"w")
print >> fichier,r.content  # le résultat de la requête est un json qui l'on écrite dans un fichier
fichier.close()
data = json.loads(r.content)    #   le resultat de la requête est mis dans un dictionnaire Python
#print(json.dumps(data, indent=4,sort_keys=True))
mes=''   #  message d'alerte
heure=data["hourly"]["data"][0]["time"]  #  Affichage des données du jour à 0600 UTC
if ((heure-21600)%86400)==0:  # il est 0600 UTC:
    today=data["daily"]["data"][0]
    mes=mes+"Il est 0600 UTC. Aujourd'hui : "+today["summary"]+"\n"
    mes=mes+"Tmin: "+str(today["temperatureMin"])+"  Tmax: "+str(today["temperatureMax"])+"\n"
    mes=mes+"% precipitation: "+str(today["precipProbability"]) +"  type: "+today["precipType"]+"\n"
currently=data["currently"]   # détection d'orage à proximité
if "nearestStormDistance" in currently :
    mes=mes+"nearestStormDistance : "+str(currently["nearestStormDistance"])+" bearing : "+str(currently["nearestStormBearing"])+" degres \n"
for i in range(len(data["hourly"]["data"])):   #  boucle sur les blocs horaires du résultat
    hourly=data["hourly"]["data"][i]
    ch=chaineUTCFromTs(hourly["time"])
    raf=hourly["windGust"]
    t=hourly["temperature"]
    if raf>=60 :
        mes=mes+ch+" rafale = "+str(raf)+" km/h"+"\n"            #  alerte sur les rafales
    if not(-3<=t<=28) :
        mes=mes+ch+" température = "+str(t)+" °C"+"\n"           #  alerte sur la température
    if (("precipIntensity" in hourly) and (hourly['precipIntensity']>=2)) :     #  alerte sur l'intensité des précipitations
        mes=mes+ch+" intensity of precipitation = "+str(hourly['precipIntensity'])+" mm/h"+"\n"
    
    if (("precipType" in hourly) and ((hourly['precipType']=="snow")or(hourly['precipType']=="sleet"))) :     #  alerte sur la neige
        mes=mes+ch+" type de précipitation = "+str(hourly['precipType'])+"\n"
        
    print ch,hourly["temperature"],hourly["windGust"],hourly['precipProbability'],hourly["precipIntensity"],hourly['cloudCover'],hourly['summary']

print "message d'alerte = \n" + mes

if not(mes==""):
    def sendMailToMe (sujet,message):
        import smtplib
        fromaddr="jpmacveigh@gmail.com"
        toaddr="jpmacveigh@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = sujet
        msg.attach(MIMEText(message, 'plain'))
        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        user="jpmacveigh@gmail.com"
        password="fury8675"
        server.login(user,password)
        server.sendmail(fromaddr,toaddr ,text)
        server.quit()
    sendMailToMe("Alerte Darksky",mes)