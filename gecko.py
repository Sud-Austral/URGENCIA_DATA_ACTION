from selenium import webdriver
from selenium.webdriver.firefox.options import Options




if __name__ == '__main__':
    url = "https://repositoriodeis.minsal.cl/SistemaAtencionesUrgencia/AtencionesUrgencia2024.zip"
    download_path = '/ruta' 
    options = Options()
    options.add_argument('-headless')
    options.set_preference('browser.download.dir', download_path)
    options.set_preference('browser.download.folderList', 2)  # Configurar para que use la carpeta personalizada
    options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')  # Evitar diálogos de descarga

    # Iniciar el navegador Firefox
    driver = webdriver.Firefox(options=options)
    #driver.implicitly_wait(3000000)
    # Abrir la página web
    try:
        driver.get(url)
    except:
        print("No se pero llego aca")