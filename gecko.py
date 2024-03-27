from selenium import webdriver
from selenium.webdriver.firefox.options import Options




if __name__ == '__main__':
    url = "https://repositoriodeis.minsal.cl/SistemaAtencionesUrgencia/AtencionesUrgencia2024.zip"
    options = Options()
    options.add_argument('-headless')

    # Iniciar el navegador Firefox
    driver = webdriver.Firefox(options=options)
    #driver.implicitly_wait(3000000)
    # Abrir la página web
    try:
        driver.get(url)
    except:
        print("No se pero llego aca")