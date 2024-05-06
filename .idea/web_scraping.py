import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuração do WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://www.kabum.com.br/produto/235984/placa-de-video-rx-6600-cld-8g-asrock-amd-radeon-8gb-gddr6-90-ga2rzz-00uanf")

wait = WebDriverWait(driver, 10)
ratings = []

try:
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        ratings_div = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.sc-8841b8a3-0.dINqTS')))
        new_ratings = [el.text for el in driver.find_elements(By.CSS_SELECTOR, 'span.sc-8841b8a3-8.hzVyNl')]
        ratings.extend(new_ratings)

        if len(driver.find_elements(By.CSS_SELECTOR, 'li.next a.nextLink')) == 0:
            print("Chegou na última página.")
            break

        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.next a.nextLink')))
        driver.execute_script("arguments[0].click();", next_button)
        wait.until(EC.staleness_of(ratings_div))

except (NoSuchElementException, TimeoutException) as e:
    print(f"Erro durante o scraping: {e}")
finally:
    driver.quit()

# Criando um DataFrame a partir da lista de ratings
df = pd.DataFrame(ratings, columns=['Rating'])

# Salvando o DataFrame em um arquivo CSV
df.to_csv('ratings.csv', index=False)

print("Ratings foram escritos em 'ratings.csv'.")
