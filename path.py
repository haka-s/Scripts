import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import mailing
import traceback
import logging



logging.basicConfig(filename='dolar.log', level=logging.DEBUG, 
                   format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)


try:
    with urllib.request.urlopen('https://www.bna.com.ar/Personas') as \
        url:
        s = url.read()
    soup = BeautifulSoup(s, "html.parser")
    table = soup.find_all('table')
    df = pd.read_html(str(table))[0]
    BilleteDC = df.loc[0,'Venta']
    BilleteEV = df.loc[1,'Venta']
    dff = pd.read_html(str(table))[1]
    DivisasDC = dff.at[0,'Compra']
    DivisasDV = dff.at[0,'Venta']
    DivisasEC = dff.at[2,'Compra']
    DivisasEV = dff.at[2,'Venta']
    print(df)
    print(dff)

    strdol = str(BilleteDC)
    leng = len(strdol) - 4
    a_string = strdol[:leng] + "." + strdol[leng:]
    BilleteDC = float(a_string)

        
    streuro = str(BilleteEV)
    lengt = len(strdol) - 4
    as_string = streuro[:lengt] + "." + streuro[lengt:]
    BilleteEV = float(as_string)

    print(BilleteDC,BilleteEV,DivisasDC,DivisasDV,DivisasEC,DivisasEV)
    diasig = datetime.date.today() + datetime.timedelta(days=1)
    diasig = diasig.strftime('%Y%m%d')

    path = 'Parametros.csv'

    df = pd.DataFrame({
        'diasig': [diasig],
        'dolarBillete': [BilleteDC],
        'dolarDivisaC': [DivisasDC],
        'dolarDivisaV': [DivisasDV],
        'euroBillete': [BilleteEV],
        'euroDivisasC': [DivisasEC],
        'euroDivisasV': [DivisasEV],
        })
        
    df['dolarBillete'] = df['dolarBillete'].apply(lambda x: '{:012.4f}'.format(x))
    df['dolarDivisaC'] = df['dolarDivisaC'].apply(lambda x: '{:012.4f}'.format(x))
    df['dolarDivisaV'] = df['dolarDivisaV'].apply(lambda x: '{:012.4f}'.format(x))
    df['euroBillete'] = df['euroBillete'].apply(lambda x: '{:012.4f}'.format(x))
    df['euroDivisasC'] = df['euroDivisasC'].apply(lambda x: '{:012.4f}'.format(x))
    df['euroDivisasV'] = df['euroDivisasV'].apply(lambda x: '{:012.4f}'.format(x))
    
    df.to_csv(path, index=False, header=False,
                encoding='utf-8')

    print(datetime.datetime.now())
except Exception:
    logging.error(traceback.format_exc())
    mailing.sendMailTo("-")