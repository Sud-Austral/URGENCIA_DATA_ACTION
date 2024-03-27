import pandas as pd
import http.client
import zipfile
import time
import requests
import os
import datetime

def getZIP():
    url = "https://repositoriodeis.minsal.cl/SistemaAtencionesUrgencia/AtencionesUrgencia2024.zip"
    #log = pd.read_excel("log_descarga.xlsx")
    file = requests.get(url, allow_redirects=True)
    open('descarga.zip', 'wb').write(file.content)
    fechaActual = datetime.datetime.now().strftime("%d%m%Y")
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