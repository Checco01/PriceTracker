from dotenv import load_dotenv
from bs4 import BeautifulSoup
load_dotenv()

import os
import requests
import time
import datetime
from telebot import TeleBot

app = TeleBot(__name__)
TOKEN = '<BOT_TOKEN>'
HEADER = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7', 'accept-encoding': 'gzip, deflate, br, Cookie', 'Connection': 'keep-alive', 'Referer': 'https://www.google.com/'}
x = datetime.datetime.now()

@app.route('/start')
def start_command(message):
  chat_dest = message['chat']['id']
  app.send_message(
    chat_dest,
       '👋 Benvenuto Utente 👋\n' +
       'questo bot ogni volta \n' +
       'che cliccherai /send \n' + 
       'ti invierà una serie di prodotti. \n' +
       'con i relativi prezzi \n' + 
       'e da quali shop gli ha presi. \n\n' + 
       '💰Grazie a me e alle mie offerte \n' +
       'risparmierai MOLTI soldi 💰' 
  )

@app.route('/send')
def start_command(message):
  chat_dest = message['chat']['id']
  app.send_message(
    chat_dest,
       '🔽🔽🔽🔽🔽🔽🔽🔽🔽🔽🔽🔽🔽🔽' +
       '\n🚨Ciao Utente oggi è il ' + x.strftime("%x") + ' 🚨' + '\n🚨Ecco un riepilogo dei prezzi che hai inserito🚨' 
  )
  print('\n*******************\n' + str(message) + '\n*******************\n')
  main(chat_dest)


def trovaprezzzi(c):
    items = [
        '/Fprezzo_processori_intel_core_i5_10600k.aspx',
        '/Fprezzo_processori_intel_core_i7_10700k.aspx',
        '/prezzo_processori_i9_10900k.aspx',
        '/schede-madri/prezzi-scheda-prodotto/msi_mpg_z490_gaming_plus-v',
        '/prezzo_ram_ddr4_16gb_kit_2x8gb_pc_3600_corsair_vengeance_rgb_pro_cmw16gx4m2d3600c18.aspx',
        '/Fprezzo_case-alimentatori_cooler_master_masterbox_mb511_argb.aspx',
        '/Fprezzo_case-alimentatori_corsair_rm750x.aspx',
        '/prezzo_hard-disk_ssd_crucial_p2_pcie_m.2_nvme_500gb.aspx'
    ]
    for item in items:
        BASE_URL = 'https://www.trovaprezzi.it'
        url = BASE_URL + items[c]
        r = requests.get(url, headers=HEADER)
        soup = BeautifulSoup(r.text, 'html.parser')

        price = soup.find('div', class_='item_basic_price').text
        price = price.replace('€&nbsp;','').replace('€','').replace(',','.').strip()
        link_s_t = soup.find('a', class_='listing_item_button cta_button')['href']
        link_s_t = BASE_URL + link_s_t

        return link_s_t,price

def idealo(c):
    items = [
        '/confronta-prezzi/200332059/intel-core-i5-10600k.html',
        '/confronta-prezzi/200331878/intel-core-i7-10700k.html',
        '/confronta-prezzi/7043697/intel-core-i9-10900x.html',
        '/confronta-prezzi/200295282/msi-mpg-z490-gaming-plus.html',
        '/confronta-prezzi/6844731/corsair-vengeance-rgb-pro-16gb-kit-ddr4-3600-cl18-cmw16gx4m2d3600c18.html',
        '/confronta-prezzi/7074513/coolermaster-masterbox-mb511-argb.html',
        '/confronta-prezzi/6052663/corsair-rm750x-2018-750w-black.html',
        '/confronta-prezzi/200241235/crucial-p2-500gb-m-2.html'
    ]
    for item in items:
        BASE_URL = 'https://www.idealo.it'
        url = BASE_URL + items[c]
        r = requests.get(url, headers=HEADER)
        soup = BeautifulSoup(r.text, 'html.parser')

        price = soup.find('a', class_='productOffers-listItemOfferPrice').text
        price = price.replace('€&nbsp;','').replace('€','').replace(',','.').strip()
        link_s_i = soup.find('a', class_='productOffers-listItemOfferCtaLeadout button button--leadout')['href']
        link_s_i = BASE_URL + link_s_i

        return link_s_i,price

        


def main(chat_id, event={}, context={}):
    c = -1
    dati_idealo = []
    dati_trovaprezzi = []
    miglior_prezzo = 0.0
    ultimo_prezzo = 0.0
    link_acquisto_conveniente = ""
    shop_conveniente = ""

    items = [
        'I5 10600K',
        'I7 10700K',
        'I9 10900K',
        'MSI MPG Z490 GAMING PLUS',
        'RAM Corsair Vengeance 16GB 3600Mhz',
        'CoolerMaster MasterBox MB611 ARGB',
        'Corsair RM750X',
        'Ssd Crucial P2 M.2 Nvme 500 GB'
    ]

    for item in items:
        c += 1

        dati_trovaprezzi = trovaprezzzi(c)
        dati_idealo = idealo(c)


        prezzo_t = dati_trovaprezzi[1]
        prezzo_i = dati_idealo[1]
        link_s_t = dati_trovaprezzi[0]
        link_s_i = dati_idealo[0]


        if float(prezzo_t) > float(prezzo_i) : 
            miglior_prezzo = prezzo_i
            link_acquisto_conveniente = link_s_i
            shop_conveniente = 'Idealo'
        else:
            miglior_prezzo = prezzo_t
            link_acquisto_conveniente = link_s_t
            shop_conveniente = 'Trovaprezzi'
        if float(prezzo_t) == float(prezzo_i) :
            miglior_prezzo = prezzo_i #cambiare prezzo_t con prezzo_i
            link_acquisto_conveniente = link_s_i #cambiare link_s_t con link_s_i
            shop_conveniente = 'entrambi'


        miglior_prezzo = miglior_prezzo.replace('.', ',')
        testo = ('Lo shop ' + f'*{shop_conveniente}*' + ' ha ' + f'*{item}* a ' + f'*{miglior_prezzo}*' + '€' + '\nCompra: ' + f'[Vai allo shop]({link_acquisto_conveniente})')
        r = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={testo}&disable_web_page_preview=True')

    #messaggio finale
    testo = ('🔼🔼🔼🔼🔼🔼🔼🔼🔼🔼🔼🔼🔼🔼')
    x = datetime.datetime.now()
    r = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={testo}')
    #fine messaggio finale
        

    
if __name__ == '__main__':
    app.config['api_key'] = '<BOT_TOKEN>'
    app.poll(debug=True)
