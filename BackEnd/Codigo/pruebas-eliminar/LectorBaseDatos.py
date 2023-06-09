
import certifi
import pycurl
from io import BytesIO

class LectorBaseDatos:
    
    def __init__ (self, URL):
        self.URL = URL

    def leerBaseDatosJSON (self):
        buffer = BytesIO()
        c = pycurl.Curl()
        #initializing the request URL
        c.setopt(c.URL, self.URL)
        #setting options for cURL transfer  
        c.setopt(c.WRITEDATA, buffer)

        custom_headers = ['User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0/8mqLkJuL-86']
        c.setopt(pycurl.HTTPHEADER, custom_headers)

        #setting the file name holding the certificates
        c.setopt(c.CAINFO, certifi.where())
        # perform file transfer
        c.perform()
        #Ending the session and freeing the resources
        c.close()

        body = buffer.getvalue()
        return body.decode('iso-8859-1')

        