import Dataset as datos
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_ventas=datos.get_df_ventas()
datos.guardar_en_excel(df_ventas)

facturación_total= df_ventas.neto.sum()
cantidad_facturas = df_ventas.comprob.nunique()
cantidad_articulos = df_ventas.articulo.nunique()
resample_meses = datos.get_resample_meses()

estadisticas_generales = pd.Series({
"Facturación Neta en el año" : "$"+"{:,.2f}".format(facturación_total).replace(',','x').replace('.',',').replace('x','.'),
"Promedio de facturación por mes" :"$"+"{:,.2f}".format(facturación_total/12,2).replace(',','x').replace('.',',').replace('x','.'),
"Cantidad de facturas en el año" : cantidad_facturas,
"Promedio de facturas por mes" : round(cantidad_facturas/12,1),
"Valor Medio de Precio Neto/Pedido" :"$"+"{:,.2f}".format(facturación_total/cantidad_facturas).replace(',','x').replace('.',',').replace('x','.'),
"Cantidad de articulos vendidos": cantidad_articulos
})
estadisticas_generales.index.name = "Estadísticas"
estadisticas_generales.name = "Estadisticas Generales"

datos.guardar_en_excel(estadisticas_generales)
print(estadisticas_generales)

plt.figure(figsize=[9,5]).suptitle("Facturación neta por Mes:")
plt.xlabel(resample_meses.index.name)
plt.ylabel(resample_meses.columns[0] + " en $")
f1 = plt.bar(resample_meses.index, resample_meses["Facturacion neta"], width=30,tick_label=resample_meses.index.strftime('%m/%y'))
plt.grid(which="major", axis="y", color="black", alpha=0.15)
plt.axhline(y=resample_meses["Facturacion neta"].mean(),ls="--", label= "Promedio: $" + "{:,}".format(round(df_ventas.neto.sum()/12,2)).replace(',','x').replace('.',',').replace('x','.'))
plt.xticks( rotation=45)
plt.yticks(np.arange(0,resample_meses["Facturacion neta"].max()*1.1,datos.escala_grafico(resample_meses["Facturacion neta"].max())))
plt.ticklabel_format(axis="y",style="plain", useLocale=True,)
plt.legend(loc="upper left")
axes = plt.gca()
axes.set_ylim([0,resample_meses["Facturacion neta"].max()*1.1])

for i in f1:
    x = i.get_x()
    y = i.get_height()
    ancho = i.get_width()
    plt.text(x+ancho/2, 0, str(int(round(y/1000,0)))+"k", fontsize=10, color="black", ha="center")
plt.savefig("Gráficos generales/"+resample_meses.name+".jpg")
plt.show()
