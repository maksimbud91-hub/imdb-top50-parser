from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import os

driver = webdriver.Chrome()
driver.get("https://www.imdb.com/chart/top/")
sleep(5)

element = driver.find_elements(By.CLASS_NAME, "sc-ebbca8d2-0")

movies = []

for el in element[:50]:
    try:
        el1 = el.find_element(By.CLASS_NAME, "ipc-signpost__text")
        number = el1.text.replace("#", "")
        
        el2 = el.find_element(By.CSS_SELECTOR, "h4.ipc-title__text")
        title = el2.text
        
        el3 = el.find_element(By.CLASS_NAME, "sc-ebbca8d2-5")
        lis = el3.find_elements(By.TAG_NAME, "li")
        data = [li.text for li in lis]
        
        el4 = el.find_element(By.CLASS_NAME, "ipc-rating-star--rating")
        rating = el4.text
        
        movies.append({
            "Номер": number,
            "Название": title,
            "Год": data[0] if len(data) > 0 else "",
            "Длительность": data[1] if len(data) > 1 else "",
            "Возраст": data[2] if len(data) > 2 else "",
            "Рейтинг": rating
        })
        
        print(f"{number}. {title} ({data[0] if len(data) > 0 else 'N/A'}) - {rating}")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        continue

driver.quit()

df = pd.DataFrame(movies)

filename = "imdb_top50.xlsx"

df.to_excel(filename, index=False)
print(f"\nSokhraneno {len(movies)} filmov v {filename}")