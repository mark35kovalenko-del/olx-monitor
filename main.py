import requests
from bs4 import BeautifulSoup
import time

# Сюди вставляємо дані з Кроку 1
TOKEN = "8989679922:AAFOy8CF37jF5tboPtK_XB_4T_uBFbgy69s"
CHAT_ID = "8206438924"

# Посилання на OLX (Краків, оренда квартир, сортування від найновіших)
URL = "https://olx.pl"

last_checked_link = None

def check_olx():
    global last_checked_link
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        print("Сайт заблокував запит або лежить")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Знаходимо першу картку оголошення
    first_ad = soup.find('div', {'data-cy': 'l-card'})
    if not first_ad:
        return

    link_element = first_ad.find('a')
    if link_element:
        # Формуємо повне посилання
        href = link_element['href']
        ad_link = href if href.startswith('http') else "https://olx.pl" + href
        
        # Знаходимо заголовок
        title = first_ad.find('h6').text if first_ad.find('h6') else "Нова квартира"
        
        # Перевірка на новизну
        if ad_link != last_checked_link:
            last_checked_link = ad_link
            message = f"🏢 Нова квартира в Кракові!\n\n📌 {title}\n🔗 {ad_link}"
            
            # Відправка в телеграм
            send_url = f"https://telegram.org{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
            requests.get(send_url)

# Перевірка кожні 10 хвилин (600 секунд)
while True:
    try:
        check_olx()
    except Exception as e:
        print(f"Помилка: {e}")
    time.sleep(600)
