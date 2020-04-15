import requests
import json
import datetime
import pytz
from getDarkSky import getDarkSky
from send_mail import send_mail
def Alerte_Onde_Nord():
  stations=[
    ("Lyon-Bron",45.728337,4.942131,200.),
    ("Nice-Côte d'Azur",43.663041,7.214449,15.)
    ]
  seuil=11.  # Vielle recette de St. Auban : Ecart QNH Lyon-Nice > 11 °hPa
  res=[]
  for station in stations:
    data=getDarkSky(station[1],station[2])
    for day in data["daily"]["data"]:
      #res[str(datetime.datetime.fromtimestamp(day["time"]))].append(([station[0]],day["pressure"]))
      #print (station[0],datetime.datetime.fromtimestamp(day["time"]),day["time"],day["pressure"])
      pression=day["pressure"]
      #pression=pression+station[3]/8.  # réduction sommaire au niveau de la mer
      localeParis = datetime.datetime.utcfromtimestamp(day["time"]).astimezone(pytz.timezone('Europe/Paris'))
      dateParis=localeParis.date()
      res.append({"station":station[0],"date":dateParis.strftime("%a %-d %b %Y"),"pression":pression})
  alerte=False
  message=[]
  message.append("Alerte onde de Nord dans les Alpes du Sud")
  for ligne in res:
    if ligne["station"]==stations[0][0]:
      date=ligne["date"]
      toto=[(x["station"],x["pression"]) for x in res if (x["date"]== ligne["date"] and not x["station"]==ligne["station"])]
      ecart=ligne["pression"]-toto[0][1]
      onde=ecart>seuil
      alerte=alerte or onde
      message.append(str(ligne["date"])+" "+ligne["station"]+" "+str(round(ligne["pression"],1))+" "+str(toto[0][0])+" "+str(round(toto[0][1],1))+" ecart: "+str(round(ecart,1))+" "+str(onde))
  mail=""
  for ligne in message:
    print (ligne)
    mail=mail+ligne+"<br>"
  print (alerte)
  if alerte :   # En cas d'alerte, on prévient par mail
    send_mail("jpmacveigh@gmail.com","Alerte onde de Nord sur les Alpes du Sud",mail)
  
Alerte_Onde_Nord ()