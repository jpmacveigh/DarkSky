import requests
import json
def getDarkSky(lati,longi):  
  path="https://api.darksky.net/forecast/65c59c85e831f6ce989aa0b9c612c444/"+str(lati)+","+str(longi)+"?lang=fr&units=ca"
  print(path)
  status=-1
  r=None
  while status != 200:
      r=requests.get(path)
      status=r.status_code
  res=r.content
  data = json.loads(res)    #   le resultat de la requête est mis dans un dictionnaire Python
  return(data)