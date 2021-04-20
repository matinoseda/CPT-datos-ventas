import Dataset as datos
import matplotlib.pyplot as plt
import numpy as np
import os

df_ventas = datos.get_df_ventas()
resample_meses = datos.get_resample_meses()

facturacion_por_juego = datos.get_facturacion_por_juego()
cantidad_ventas_por_juego = datos.get_cantidad_ventas_por_juego()
#----------------------------------------------------------------------------------------------------------------- guardo los datos en Excel
datos.guardar_en_excel(datos.get_facturacion_por_juego())
datos.guardar_en_excel(datos.get_cantidad_ventas_por_juego())
#----------------------------------------------------------------------------------------------------------------- imprimo datos en consola de python
print(facturacion_por_juego)
print(cantidad_ventas_por_juego)
#----------------------------------------------------------------------------------------------------------------- agrego descripcion de los juegos
a = datos.get_facturacion_por_juego().reset_index()
a.set_index("descripcion", inplace=True)
a.name = "Comparación de la facturación de cada juego "
#----------------------------------------------------------------------------------------------------grafico comparación facturacion de los juegos
plt.figure(figsize=[11,6]).suptitle("Comparación facturación (neta) de cada juego:")
plt.subplots_adjust(bottom=0.34, right=0.99, left=0.1, top=0.95)
plt.ylabel(a.columns[1] + " en $")
f1 = plt.bar(a.index, a["facturacion neta"], tick_label=a.index)
plt.grid(which="major", axis="y", color="black", alpha=0.15)
plt.axhline(y=a["facturacion neta"].mean(),ls="--", label= "Promedio: $" +
        "{:,}".format(round(a["facturacion neta"].mean(),2)).replace(',','x').replace('.',',').replace('x','.')+
        " (no muy útil porque se comparan \n todos los juegos, que son muy distintos)")
plt.xticks( rotation=90)
plt.yticks(np.arange(0,a["facturacion neta"].max()*1.1,datos.escala_grafico(a["facturacion neta"].max())))
plt.ticklabel_format(axis="y",style="plain", useLocale=True,)
plt.legend(loc="upper right")
axes = plt.gca()
axes.set_ylim([0,a["facturacion neta"].max()*1.1])

plt.savefig("Gráficos generales/"+a.name+".jpg")
plt.show()
plt.close()
#--------------------------------------------------------------------------------------- grafico de juegos vendidos por mes, de todos los juegos
contador=1
for juego in df_ventas.articulo.unique():
    juego = datos.get_tabla_juegos(juego)
    plt.figure().suptitle(juego)
    plt.xlabel(resample_meses.index.name)
    plt.ylabel("Número de juegos vendidos")
    f1 = plt.bar(resample_meses.index, resample_meses[juego], width=30, tick_label=resample_meses.index.strftime('%m/%y'))
    plt.grid(which="major", axis="y", color="black", alpha=0.15)
    plt.axhline(y=resample_meses[juego].mean(), ls="--",label="Promedio: $" +
     "{:,}".format(round(resample_meses[juego].mean(), 2)).replace(',', 'x').replace('.', ',').replace('x', '.'))
    plt.xticks(rotation=45)
    plt.yticks(np.arange(0, resample_meses[juego].max() * 1.1, datos.escala_grafico(resample_meses[juego].max())))
    plt.ticklabel_format(axis="y", style="plain", useLocale=True, )
    plt.legend(loc="upper right")
    axes = plt.gca()
    axes.set_ylim([0, resample_meses[juego].max() * 1.1])

    for i in f1:
        x = i.get_x()
        y = i.get_height()
        ancho = i.get_width()
        plt.text(x + ancho / 2, 0, y, fontsize=10, color="black", ha="center")
    print(contador," Se guardó " + juego+".jpg" )
    contador+=1
    plt.savefig("Gráfico de cada juego/"+juego+".jpg")
    plt.close()
del contador

#-------------------------------------------------------------------------------------------------------------------------------- GUI image viewer
from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title('CIENCIAS PARA TODOS - Estadísticas')

image_list = []
for foto in os.listdir("Gráfico de cada juego/"):
    aux = ImageTk.PhotoImage(Image.open("Gráfico de cada juego/"+foto))
    image_list.append(aux)


my_label = Label(image=image_list[0])
my_label.grid(row=0, column=0, columnspan=3)

def forward(image_number):
    global my_label
    global button_forward
    global button_back

    my_label.grid_forget()
    my_label = Label(image=image_list[image_number - 1])
    button_forward = Button(root, text=">>", command=lambda: forward(image_number + 1))
    button_back = Button(root, text="<<", command=lambda: back(image_number - 1))

    if image_number == len(image_list):
        button_forward = Button(root, text=">>", state=DISABLED)

    my_label.grid(row=0, column=0, columnspan=3)
    button_back.grid(row=1, column=0)
    button_forward.grid(row=1, column=2)


def back(image_number):
    global my_label
    global button_forward
    global button_back

    my_label.grid_forget()
    my_label = Label(image=image_list[image_number - 1])
    button_forward = Button(root, text=">>", command=lambda: forward(image_number + 1))
    button_back = Button(root, text="<<", command=lambda: back(image_number - 1))

    if image_number == 1:
        button_back = Button(root, text="<<", state=DISABLED)

    my_label.grid(row=0, column=0, columnspan=3)
    button_back.grid(row=1, column=0)
    button_forward.grid(row=1, column=2)


button_back = Button(root, text="<<", command=back, state=DISABLED)
button_exit = Button(root, text="Exit Program", command=root.quit)
button_forward = Button(root, text=">>", command=lambda: forward(2))

button_back.grid(row=1, column=0)
button_exit.grid(row=1, column=1)
button_forward.grid(row=1, column=2)

root.mainloop()