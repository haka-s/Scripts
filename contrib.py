import zipfile
import os
import mailing
import traceback
import logging
import requests


#
#

logging.basicConfig(filename='contrib.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)
url = 'https://www.afip.gob.ar/genericos/cInscripcion/archivos/SINapellidoNombreDenominacion.zip'

#
base_filename = "contrib.tmp"

try:
    #filename = mktemp('.zip')
    filehandle =requests.get(url,allow_redirects=True) 
    open('zipe.zip', 'wb').write(filehandle.content)

except Exception:
    logging.error(traceback.format_exc())

try:       
    zipefile = zipfile.ZipFile("zipe.zip")

    for member in zipefile.namelist():
        filename = os.path.basename(member)

        if not filename:
            continue
        source = zipefile.open(member)
        content = source.read()
        source.close()
    zipefile.close()


    outfile = open(base_filename, 'wb')
    outfile.write(content)
    outfile.close()
    os.remove("zipe.zip")

except Exception:
    logging.error(traceback.format_exc())
    mailing.sendMailTo("-")









