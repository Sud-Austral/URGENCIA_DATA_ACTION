from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os



if __name__ == '__main__':
    url = "https://repositoriodeis.minsal.cl/SistemaAtencionesUrgencia/AtencionesUrgencia2024.zip"
    options = Options()
    os.environ['PATH'] += os.pathsep + "/usr/local/bin"
    #options.add_argument('-headless')
    geckodriver_path = "/usr/local/bin/geckodriver"
    # Iniciar el navegador Firefox
    driver = webdriver.Firefox(options=options)
    #driver.implicitly_wait(3000000)
    # Abrir la página web
    try:
        driver.get(url)
    except:
        print("No se pero llego aca")