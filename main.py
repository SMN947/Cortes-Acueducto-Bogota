import os
import csv
import requests
from bs4 import BeautifulSoup


vgm_url = 'https://www.acueducto.com.co/wps/portal/EAB2/Home/atencion-al-usuario/programacion-de-cortes'
html_text = requests.get(vgm_url).text
soup = BeautifulSoup(html_text, 'html.parser')
bgfecha = ["#8eaadb", "#9cc2e5"]
bgtexto = ["#ffffff"]

def getInicio(data):
    p = data.find_all("p")
    return ("Desde las {} y por {}").format(p[0].get_text(), p[1].get_text())

if __name__ == '__main__':

    tablas = soup.find_all('table')

    fName = 'Data.csv'
    f = open(os.path.join(os.getcwd() ,fName), 'w', newline='', encoding='utf-8')
    writer = csv.writer(f, delimiter=",")

    rows = [["fecha", "localidad", "barrios", "lugar", "inicioDuracion", "motivo"]]

    count = 1
    for tabla in tablas:
        if len(tabla.find_all("tr")) > 0:
            filas = tabla.find_all("tr")
            fecha = ""
            localidad = ""
            barrios = ""
            lugar = ""
            inicio = ""
            motivo = ""
            
            for fila in filas:
                
                try:
                    cl = fila.td["bgcolor"]
                except:
                    cl = bgtexto

                if cl in bgfecha or cl in bgtexto:
                    if cl in bgfecha:  
                        fecha = fila.font.get_text()
                    else:
                        cols = fila.find_all("td")
                        localidad = cols[0].font.get_text()
                        barrios = cols[1].font.get_text()
                        lugar = cols[2].font.get_text()
                        inicio = getInicio(cols[3])
                        motivo = cols[4].font.get_text()
                        rows.append([fecha, localidad, barrios, lugar, inicio, motivo])

    writer.writerows(rows)
    f.close()