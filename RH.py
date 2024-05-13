"""""
Objetivo:   Automatizar la Extracción de Data proveniente de Facturas en formato XML
Fecha:      Mayo 2024
Realizó:    Lic. Sánchez Santana Ángel  
"""
import xmltodict
import pandas as pd
 
def xml_to_dataframe(xml_file):

    #XML a un DataFrame de Pandas

    with open(xml_file) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    df = pd.json_normalize(data_dict)
    df.insert(0, 'fuente' ,xml_file.name)
    return df
 
def dataframe_to_excel(df, excel_file):
 
   #guardar el DataFrame en un archivo Excel

    df.to_excel(excel_file, index=False)
 
if __name__ == "__main__":
    xml_file = [
    "Facturas Gasolina RRHH/1.xml",
    "Facturas Gasolina RRHH/2.xml",
    "Facturas Gasolina RRHH/3.xml",
    "Facturas Gasolina RRHH/4.xml",
                 ]
    
    #Nombramos el Excel de salida

    excel_file = "combinados.xlsx"
 
    # Convertir los XML a DataFrame

    dfs = [xml_to_dataframe(xml_file) for xml_file in xml_file]
    df = pd.concat(dfs, ignore_index=True)
 
    # Guardar el DataFrame en archivo Excel

    dataframe_to_excel(df, excel_file)
