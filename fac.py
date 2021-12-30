#facapoc.txt
#bajar archivo zip (http://www.afip.gob.ar/genericos/facturasApocrifas/)
#unzip
#truncate primeras 3 lineas
#,, = 500 espacios ,          ,
import urllib.request as urllib
import zipfile
import urllib.error as urlerr
import mailing
import traceback
import logging




logging.basicConfig(filename='facacop.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)


space = ',                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    ,'
base_filename = 'facapoc.txt'
url = 'https://servicioscf.afip.gob.ar/Facturacion/facturasApocrifas/DownloadFile.aspx'
try:
    filehandle, _ = urllib.urlretrieve(url)
    zip_file_object = zipfile.ZipFile(filehandle, 'r')
    first_file = zip_file_object.namelist()[0]
    file = zip_file_object.open(first_file)
    content = file.read()


    outfile = open(base_filename, 'wb')
    outfile.write(content)
    outfile.close()

    with open(base_filename, "r") as f:
        lines = f.readlines()
        f.close()

    del lines[2]
    del lines[1]
    del lines[0]

    with open(base_filename, "w+") as f:
        for line in lines:
            f.write(line.replace(',,',space))
    #outfile.replace(',,',space)
    f.close()

    with open(base_filename) as f_input:
        data = f_input.read().rstrip('\n')

    with open(base_filename, 'w') as f_output:    
        f_output.write(data)

except urlerr.HTTPError as e:
    logging.error(traceback.format_exc())
    mailing.sendMailTo("-")   
except Exception as e:
    logging.error(traceback.format_exc())
    mailing.sendMailTo("-")     
 








