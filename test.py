import pandas as pd
import http.client
import zipfile
import time
import requests
import os
import datetime

def getZIP():
    #url = "https://repositoriodeis.minsal.cl/SistemaAtencionesUrgencia/AtencionesUrgencia2024.zip"
    #log = pd.read_excel("log_descarga.xlsx")
    fechaActual = datetime.datetime.now().strftime("%d%m%Y")
    # Definir los parámetros de la solicitud
    host = "repositoriodeis.minsal.cl"
    path = f"/SistemaAtencionesUrgencia/AtencionesUrgencia2024.zip"
    #path = f"/DatosAbiertos/VITALES/DEFUNCIONES_FUENTE_DEIS_2021_2024_12032024.zip"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "TE": "trailers",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }
    timeout = 10000
    flag = True
    for _ in range(30):
        try:
            # Realizar la solicitud GET con timeout
            #response = requests.get(f"https://{host}{path}", headers=headers, timeout=timeout, proxies=proxy)
            response = requests.get(f"https://{host}{path}", headers=headers, timeout=timeout)

            # Verificar el código de estado de la respuesta
            if response.status_code == 200:
                with open("descarga.zip", "wb") as f:
                    f.write(response.content)
                log.loc[len(log)] = {"fecha":datetime.datetime.now(),"descarga":"Descargado"}
                flag = False
                print("Archivo descargado exitosamente.")
                break  # Si la descarga es exitosa, sal del bucle
            else:
                print("Error al descargar el archivo:", response.status_code)
        except requests.Timeout:
            print("Se ha agotado el tiempo de espera durante la solicitud.")
        except requests.RequestException as e:
            print("Error durante la solicitud:", e)
    return fechaActual



        
def descomprimir():
    # Ruta del archivo ZIP
    archivo_zip = "descarga.zip"
    # Abre el archivo ZIP en modo lectura
    with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
        # Lista los contenidos del archivo ZIP
        contenidos = zip_ref.namelist()
        # Extrae todos los archivos del ZIP en la carpeta actual
        zip_ref.extractall()
        return contenidos

if __name__ == '__main__':
    
    fechaActual = getZIP()
    contenidos = descomprimir()
    ref2 = pd.read_excel("referencia.xlsx")
    del ref2["glosacausa"]
    try:
        df = pd.read_csv(f"AtencionesUrgencia2024.csv", encoding='latin-1',sep=";", header=None)
        del df['Menores_1']
        del df['De_1_a_4']
        del df['De_5_a_14']
        del df['De_15_a_64']
        del df['De_65_y_mas']
        df['semana'] = df["semana"].apply(lambda x: f"Semana {x}")
        dfGroup = df.groupby(['IdEstablecimiento', 'NEstablecimiento', 'IdCausa', 'GlosaCausa',
            'GLOSATIPOESTABLECIMIENTO',
            'GLOSATIPOATENCION', 'GlosaTipoCampana', 'CodigoRegion', 'NombreRegion',
            'CodigoDependencia', 'NombreDependencia', 'CodigoComuna',
            'NombreComuna','semana']).sum().reset_index()  

        dfPivot = dfGroup.drop_duplicates().pivot(index=['IdEstablecimiento', 'NEstablecimiento', 'IdCausa', 'GlosaCausa',
            'GLOSATIPOESTABLECIMIENTO',
            'GLOSATIPOATENCION', 'GlosaTipoCampana', 'CodigoRegion', 'NombreRegion',
            'CodigoDependencia', 'NombreDependencia', 'CodigoComuna',
            'NombreComuna'], columns='semana', values='Total').reset_index()  #.to_excel("realidad2.xlsx",index=False)
        #del dfPivot["semana"]
        dfPivot.columns.name = None
        dfPivot["Año"] = 2024
        diccionarioColumnas = {
            'IdEstablecimiento':'idestablecimiento', 
            'NEstablecimiento':'nestablecimiento', 
            'IdCausa':'Idcausa',
            'GlosaCausa':'glosacausa'}
        dfRename = dfPivot.rename(columns=diccionarioColumnas)
        dfMerge = dfRename.merge(ref2)
        dfMerge['Unnamed: 0'] = range(len(dfMerge))
        columnas_a_eliminar = [ 'CodigoRegion', 'NombreRegion', 'CodigoDependencia',
                            'NombreDependencia', 'CodigoComuna', 'NombreComuna']
        dfMerge.drop(columns=columnas_a_eliminar).to_excel("data_urgencia_2024.xlsx")
        dfMerge.to_excel("data_urgencia_2024_(conComunasYDependencias).xlsx")
        for file in contenidos:
            print(file)
            if os.path.exists(file):
                # Borra el archivo
                os.remove(file)
                print(f"El archivo '{file}' ha sido borrado exitosamente.")
            else:
                print(f"El archivo '{file}' no existe.")
        df = df[df["Año"] == 2024]
        df.to_excel("difuntos.xlsx",index=False)
        print("Termino correctamente")
    except:
        print("Error de archivo")