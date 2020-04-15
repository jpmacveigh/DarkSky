''' Alerte basée sur les données hoaraires de Darksky '''
#coding: utf8
import requests
import json
import sys
from getDarkSky import getDarkSky
from send_mail import send_mail
sys.path.insert(0, '../WCS_MF') # insérer dans sys.path le dossier contenant le/les modules
from Utils import chaineUTCFromTs
destinataire="jpmacveigh@gmail.com"    # destinataire des alertes
lon=3.06   # coordonées de Lille
lat=50.6
seuil_rafale=60.              # seuil des rafales en km/h
seuil_tmin=-3.                # borne mini des températures (°C)
seuil_tmax=28.                # borne maxi des températures (°C)
seuil_intensite_precip=2.     # seuil intensité horaire des précipitations (mm)
data = getDarkSky(lat,lon)    #   le resultat de la requête Darksky est renvoyé dans un dictionnaire Python
#print(json.dumps(data, indent=4,sort_keys=True))
mes=""   #  potentiel message d'alerte
heure=data["hourly"]["data"][0]["time"]  #  Affichage des données du jour à 0600 UTC
if ((heure-21600)%86400)==0:  # il est 0600 UTC:
    today=data["daily"]["data"][0]
    mes=mes+"Il est 0600 UTC. Aujourd'hui : "+today["summary"].encode('utf8')+"\n"
    mes=mes+"Tmin: "+str(today["temperatureMin"])+"  Tmax: "+str(today["temperatureMax"])+"\n"
    mes=mes+"% precipitation: "+str(today["precipProbability"])
    if ("precipType" in data) :
        mes = mes +"  type: "+today["precipType"]+"\n"
    else:
        mes=mes+"\n"
currently=data["currently"]   # détection d'orage à proximité
if "nearestStormDistance" in currently :
    mes=mes+"nearestStormDistance : "+str(currently["nearestStormDistance"])+" bearing : "+str(currently["nearestStormBearing"])+" degres \n"
for i in range(len(data["hourly"]["data"])):   #  boucle sur les blocs horaires du résultat
    hourly=data["hourly"]["data"][i]
    ch=chaineUTCFromTs(hourly["time"])
    raf=hourly["windGust"]
    t=hourly["temperature"]
    if raf>=seuil_rafale :
        mes=mes+ch+" rafale = "+str(raf)+" km/h"+"\n"            #  alerte sur les rafales
    if not(seuil_tmin<=t<=seuil_tmax) :
        mes=mes+ch+" température = "+str(t)+" °C"+"\n"           #  alerte sur la température
    if (("precipIntensity" in hourly) and (hourly['precipIntensity']>=seuil_intensite_precip)) :     #  alerte sur l'intensité des précipitations
        mes=mes+ch+" intensity of precipitation = "+str(hourly['precipIntensity'])+" mm/h"+"\n"
    
    if (("precipType" in hourly) and ((hourly['precipType']=="snow")or(hourly['precipType']=="sleet"))) :     #  alerte sur la neige
        mes=mes+ch+" type de précipitation = "+str(hourly['precipType'])+"\n"
        
    #print (ch,hourly["temperature"],hourly["windGust"],hourly['precipProbability'],hourly["precipIntensity"],hourly['cloudCover'],hourly['summary'])

print ("message d'alerte : \n" + mes)

if (mes==""):
    print("Pas d'alerte")
else:
    print("Alerte")
    mes=mes.replace("\n","<br>")
    send_mail(destinataire,"Alerte Darksky pour Lille",mes)