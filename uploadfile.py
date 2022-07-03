import requests
import os
url = 'http://127.0.0.1:8000/upload'
path=input("Enter file path")
file = {'file': open(path, 'rb')}
resp = requests.post(url=url, files=file) 
filename=resp.headers.get("Content-Disposition").split("filename=")[1].replace('"',"")
resp.raise_for_status()
with open(filename, 'wb') as f:
    for chunk in resp.iter_content(): 
        f.write(chunk)