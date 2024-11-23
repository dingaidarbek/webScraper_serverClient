

#############################################################
### use this file to implement the web scrapper in part 1 ###
#############################################################


import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

# Настройка Selenium
driver = webdriver.Chrome()  # Убедитесь, что chromedriver установлен и доступен
url = "https://www.rit.edu/dubai/directory"
driver.get(url)

try:
    cookie_banner = driver.find_element(By.ID, "cookie-consent")
    accept_button = cookie_banner.find_element(By.TAG_NAME, "button")  # Найти кнопку в баннере
    accept_button.click()
    time.sleep(1)  # Подождать, чтобы баннер исчез
except Exception as e:
    print(f"Баннер с cookies не найден или уже закрыт: {e}")

# Нажимаем кнопку "Load More" 5 раз
for _ in range(5):
    try:
        load_more_button = driver.find_element(By.CLASS_NAME, "see-more")  # Класс кнопки (проверьте и уточните при необходимости)
        load_more_button.click()
        print("Load me pressed")
        time.sleep(5)  # Ждем загрузки контента
    except Exception as e:
        print("There is no load me")
        break

# Получаем HTML-код страницы после всех загрузок
html_content = driver.page_source
driver.quit()  # Закрываем браузер

# Используем BeautifulSoup для парсинга данных
soup = BeautifulSoup(html_content, "html.parser")
employees = soup.find_all("article", class_=lambda x: x and "card person-directory" in x)

data = []
for card in employees:
    name_tag = card.find("div", class_="person--info").find("a")
    name = name_tag.text.strip() if name_tag else ""

    # Извлекаем должность (title)
    title_tag = card.find("div", class_="person--info").find("div", class_="pb-2 directory-text-small")
    title = title_tag.text.strip() if title_tag else ""

    # Извлекаем email
    email_tag = card.find("a", href=lambda href: href and "mailto:" in href)
    email = email_tag.text.strip() if email_tag else ""

    # Добавляем данные в список
    data.append({"Name": name, "Title": title, "Email": email})

# Сохраняем данные в CSV с помощью Pandas
df = pd.DataFrame(data)
df.to_csv("directory.csv", index=False)

print("Данные сохранены в файл employees.csv")
