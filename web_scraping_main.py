import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd

from fastapi import FastAPI,HTTPException

app = FastAPI()

#Paso 2
file_name = 'data_out/dataMunicipios_api.txt'

def write_headers(data_list, file_name):
    with open(file_name, 'w',encoding='utf-8') as file:
        headers = data_list
        file.write(', '.join(headers) + '\n')

    
def write_headers_and_append(data_list, file_name):
    # Abrir el archivo en modo de escritura (write mode) para escribir los encabezados    
    # Abrir el archivo en modo de anexar (append mode) para agregar los registros
    with open(file_name, 'a',encoding='utf-8') as file:
        for data in data_list:
            line = ', '.join([str(value) for value in data.values()])
            file.write(line + '\n')



@app.get("/municipios_de_estados")
def scraping_municipios_inegi():
    """_summary_
        Obtiene los municipios de cada entidad federativa
    Args:
        Este método no recibe parámetros

    Returns:
        str: Un mensaje de terminación de proceso
    """
    respuesta=''
    try:
        header=["estado_id","estado","municipio","latitud","longitud","altitud"]
        write_headers(header,file_name)
        #estado=["Aguascalientes","Baja California","Baja California Sur","Campeche","Coahuila de Zaragoza","Colima","Chiapas","Chihuaua","Durango","Guanajuato","Guerrero","Hidalgo","Jalisco","México","Michoacán de Ocampo","Morelos","Nayarit","Nuevo León","Oaxaca","Puebla","Querétaro","Quintana Roo","San Luis Potosí","Sinaloa","Sonora","Tabasco","Tamaulipas","Tlaxcala","Veracruz de Ignacio de la LLave","Yucatán","Zacatecas"]
        estado=["Aguascalientes","Baja California","Baja California Sur"]
        for i,edo in enumerate(estado):
            # Configuración del WebDriver (ajusta el path según tu sistema)
            #service = Service(executable_path='D:/Home/Cursos/Henry/WEB_scraping/chromedriver-win64/chromedriver.exe')
            service = Service(executable_path='D:/Home/Mis_proyectos/web_scraping_inegi/chrome/chromedriver.exe')
            
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(service=service, options=options)
            # Abre la página web
            driver.get('https://www.inegi.org.mx/app/cuadroentidad/CDMX/2023/01/1_2')

            # Espera a que la página se cargue
            time.sleep(2)

            # Encuentra y hace clic en el botón que maneja el data-target  por class: btn btn-default dropdown-toggle
            button = driver.find_element(By.CSS_SELECTOR, 'button[data-target="#seleccion_entidad"]')
            button.click()

            # Espera a que los dropdowns sean visibles
            wait = WebDriverWait(driver, 10)
            dropdown1 = wait.until(EC.visibility_of_element_located((By.ID, 'id_entidad')))

            # Selecciona valores en los dropdowns
            select1 = Select(dropdown1)
            #select1.select_by_visible_text('Aguascalientes')
            select1.select_by_visible_text(edo)

            wait = WebDriverWait(driver, 50)
            time.sleep(10)
            dropdown2 = wait.until(EC.element_to_be_clickable((By.ID, 'cuadro_temas')))
            select2 = Select(dropdown2)

            select2.select_by_visible_text('División geoestadística municipal, coordenadas geográficas y altitud de las cabeceras municipales / Al 31 de diciembre de 2023')

            # Espera un momento para ver los cambios (opcional)
            time.sleep(2)

            div_cuerpo = driver.find_element(By.ID, 'cuerpo')
            table = div_cuerpo.find_element(By.CSS_SELECTOR, 'table.Ancho100')

            rows = table.find_elements(By.TAG_NAME, 'tr')
            data=[]
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                if len(cells)==5 and cells[0].text != '' and cells[4].text!='':
                    data.append([cell.text for cell in cells if cell.text!=''])
            driver.quit()
            print(data)
            mun=dict()
            lista=[]
            municipios=pd.Series()
            for item in data:
                mun={"estado_id":i+1,"estado":edo,"municipio":item[0],"latitud":item[1],"longitud":item[2],"altitud":item[3]}
                lista.append(mun)
            write_headers_and_append(lista, file_name)
    
        msj="Se ha generado el archivo con los municipios"
        
        respuesta = msj
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        
    return respuesta