import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import pandasgui

def get_df_ventas():
    df_ventas = pd.read_excel("Ventas 2020.xls")
    df_ventas.name = "Ventas 2020 limpio"
    # Elimino columnas que no necesito
    df_ventas.drop(["otros", "retencion", "neto_nog", "anulada", "sumatori", "descduma",
                    "imprime", "cuit", "calc", "total", "iva_rn", "ubicacion"], axis=1, inplace=True)

    # Pongo como indice fecha y cambio a formato datetime
    df_ventas.set_index("fecha", inplace=True)
    df_ventas.index = pd.to_datetime(df_ventas.index)
    df_ventas.sort_index(ascending=True)
    # Relleno nombres de clientes y cuit
    df_ventas["cliente"].fillna(method='ffill', inplace=True)
    #df_ventas["cuit"].fillna(method='ffill', inplace=True)
    return df_ventas

#Preparacion de los diferentes datasets ******************************************************************************************
#MESES
def get_resample_meses():
    df_ventas = get_df_ventas()
    resample_meses = df_ventas["neto"].resample("MS", closed='left', label='left').sum().to_frame()
    resample_meses.name = "Facturación (neta) total por mes"
    resample_meses.index.name = "Meses"
    resample_meses.columns=["Facturacion neta"]
    resample_meses["Cantidad de juegos vendidos"] = df_ventas["cantidad"].resample("MS", closed='left', label='left').sum()

    for art in df_ventas.articulo.unique():
        resample_meses[get_tabla_juegos(art)]=df_ventas[df_ventas.articulo==art]["cantidad"].resample("MS", closed='left', label='left').sum()
        resample_meses[get_tabla_juegos(art)].fillna(0,inplace=True)
    return resample_meses

def get_resample_meses_transpuesta():
    aux = get_resample_meses().T
    aux.name = "resample meses"
    return aux

#JUEGOS
def get_facturacion_por_juego():
    df_ventas = get_df_ventas()
    lista =[]

    for art in df_ventas.articulo.unique():
        lista.append((art,
                      get_tabla_juegos(art),
                      round(df_ventas[df_ventas.articulo==art]["neto"].resample("MS", closed='left', label='left').sum().sum(),2),
                      df_ventas[df_ventas.articulo==art]["cantidad"].resample("MS", closed='left', label='left').sum().sum()
                      ))
    facturacion_por_juego=pd.DataFrame(lista, columns=["articulo","descripcion","facturacion neta","cantidad"])
    facturacion_por_juego.name ="Ventas juegos ordenados por facturación"
    facturacion_por_juego.set_index("articulo",inplace=True)
    facturacion_por_juego.sort_values(by="facturacion neta",ascending=False,inplace=True)

    return facturacion_por_juego

def get_cantidad_ventas_por_juego():
    facturacion_por_juego = get_facturacion_por_juego()
    cantidad_ventas_por_juego = facturacion_por_juego.sort_values(by="cantidad", ascending=False)
    cantidad_ventas_por_juego.name = "Ventas juegos ordenados por cantidad"
    return cantidad_ventas_por_juego

def get_ventas_por_vendedor_por_mes():
    df_ventas = get_df_ventas()[["neto","vendedor"]].reset_index()
    table = pd.pivot_table(df_ventas, values='neto', index="fecha", columns=['vendedor']  ,fill_value=0)#.resample("MS", closed='left', label='left').sum()
    pandasgui.show(table.astype("int32"), settings={'block': True})
    return table


def escala_grafico(valor_maximo):
    return int(str(int(valor_maximo))[0])*(10**(len(str(int(valor_maximo)))-2))

def guardar_en_excel(dataframe):
    print(dataframe.name)
    dataframe.to_excel("Estadísticas en Excel/" + dataframe.name + ".xlsx")

def get_tabla_juegos(key):
    tabla_juegos = {9:"Varios",
                    200:"CUBIEXP Exhibidor Pack x36,",
                    201:"CUBIEXP Astronauta (vio)X6",
                    202:"CUBIEXP Detective (ama)X6",
                    203:"CUBIEXP Matematico (ver)X6",
                    204:"CUBIEXP Paleontologo (nar)X6",
                    205:"CUBIEXP Meteorologo (roj)X6",
                    206:"CUBIEXP Medico (azu)X6",
                    1023:"CELUSCOPIO",
                    1024:"ESPEJOS EN ACCION",
                    1025:"KIT MOTOR ELECTRICO",
                    1026:"ATRAPA TU ADN",
                    1027:"KIT DE ELECTRONICA",
                    1028:"ESTACION METEOROLOGICA",
                    1029:"EXPLORANDO COLORES",
                    1031:"CIENCIA PARA DETECTIVES",
                    1032:"QUIMICA DIVERTIDA",
                    1034:"TELESCOPIO SHILBA 5050t",
                    1035:"EFECTOS ESPECIALES",
                    1038:"TELESCOPIO SHILBA 50600T",
                    1039:"TELESCOPIO ECLIPSE 60700",
                    1041:"BINOCULAR PASSPORT 8x21",
                    1046:"Pesca TELE-SET-JUNIOR",
                    1047:"Pesca TELE-SET-PRO",
                    1048:"FISHING SET",
                    1055:"Brujula DC352A",
                    1065:"Brujula H4-1",
                    1075:"Brujula H5-1",
                    1100:"Kit Solar 6 en 1",
                    1200:"Kit Solar Pegasus",
                    2025:"LUPA EN ACCION",
                    2027:"BRUJULA EN ACCION",
                    2028:"TERMOMETRO EN ACCION",
                    4002:"DESTREZA MENTAL",
                    5001:"ABRECOCOS - PIRAMIDE",
                    5002:"ABRECOCOS - CRUZ",
                    5003:"ABRECOCOS - ESTRELLA",
                    5004:"ABRECOCOS - CAJA RUSA",
                    5005:"ABRECOCOS - CUBO",
                    5006:"ABRECOCOS - CRYSTAL",
                    6006:"Atrapados Bolonki",
                    6007:"Atrapados Equis",
                    6008:"Atrapados DUO",
                    7001:"AVENTURA QUIMICA",
                    7002:"ACCION Y REACCION ",
                    8010:"Caja Experimento Siemens",
                    8100:"Valijas Baylab",
                    9994:"Cursos_Capacitación",
                    99999:"Descuento omitido"
                    }
    return tabla_juegos[key]