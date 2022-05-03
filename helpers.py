import requests
from lxml import html
import string
import random
import uiautomator2 as u2
import hcaptcha
import time
import traceback
import dict

def get_email(token):
    for i in range(15):
        try:
            r = requests.get(f'http://api.kopeechka.store/mailbox-get-email?token={token}&site=discord.com&mail_type=REAL&sender=noreply%40discord.com&soft=7&type=JSON&api=2.0').json()
            return (r['mail'], r['id'])
        except:
            time.sleep(1)

def get_code(id, token):
    for i in range(30):
        try:
            r = requests.get(f'http://api.kopeechka.store/mailbox-get-message?id={id}&token={token}&full=1&type=JSON&api=2.0').json()
            print(r)
            if r['status'] == 'OK':
                return r['value']

        except:
            print('Письмо Не найдено')
        time.sleep(2)
    raise ('Письмо не найдено')



def get_username():
    r = requests.get('https://www.fakepersongenerator.com/?new=fresh')
    t = html.fromstring(r.content)
    return t.xpath('//div[./div[@class="info-title"]/span[text()="Username"]]/div[2]/p/text()')[0]

def get_password():
    char_set = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.sample(char_set * 10, 10))


def get_number(token, country):
    while True:
        r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={token}&action=getNumber&service=ds&country={country}').text
        print(r)
        if 'ACCESS_NUMBER' in r:
            return (r.split(':')[2],r.split(':')[1])
        time.sleep(2)


def get_sms(token, id):
    for i in range(15):
        r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={token}&action=getStatus&id={id}').text
        print(r)
        if 'STATUS_OK' in r:
            return r.split(':')[1]
        time.sleep(2)
    time.sleep(2)
    raise('Долго жду смс')
def set_status_number(token, id, status):
    r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={token}action=setStatus&status={status}&id={id}').text
