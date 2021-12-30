from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import logging
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import mailing
import traceback
import logging




logging.basicConfig(filename='Grandes-e.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)


base_filename = 'grandesc.txt'
binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')

driver = webdriver.Firefox(firefox_binary=binary,executable_path=r'C:\geko\geckodriver.exe')
driver.get('https://servicioscf.afip.gob.ar/facturadecreditoelectronica/Listado-RFCE-Mi-PyMe.asp#content')
delay = 30 
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'empresasGrandes_length')))
    print ("Cargo correctamente")
    select = Select(driver.find_element_by_name('empresasGrandes_length'))
    select.select_by_value('-1')

    #numbers='//*[@id="empresasGrandes_info"]/b[3]'
    table = driver.find_element_by_xpath('//*[@id="empresasGrandes"]/tbody')
    #table_id = driver.find_element("id":'empresasGrandes')
    rows = table.find_elements( 'tag name',"tr") # get all of the rows in the table
    outfile = open(base_filename, 'a')
    #outfile.truncate(0) #borra el contenido del archivo
    for row in rows: # Itera sobre todas las files  
        col = row.find_elements( 'tag name',"td")[0] #index 0 marca la primer columa (CUIT)
        print(col.text)
        outfile.write(f"{col.text}\n")


    outfile.close()
            

    driver.close()
except TimeoutException:
    logging.error(traceback.format_exc())
    mailing.sendMailTo("-")
    driver.close()
except Exception:
    logging.error(traceback.format_exc())
    mailing.sendMailTo("-")
    driver.close()

