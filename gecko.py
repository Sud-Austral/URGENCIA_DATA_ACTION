from selenium import webdriver
from selenium.webdriver.firefox.options import Options




if __name__ == '__main__':
    url = "https://repositoriodeis.minsal.cl/SistemaAtencionesUrgencia/AtencionesUrgencia2024.zip"
    options = Options()
    #options.add_argument('-headless')
    geckodriver_path = "/usr/local/bin/geckodriver"
    # Iniciar el navegador Firefox
    driver = webdriver.Firefox(options=options, executable_path=geckodriver_path)
    #driver.implicitly_wait(3000000)
    # Abrir la página web
    try:
        driver.get(url)
    except:
        print("No se pero llego aca")