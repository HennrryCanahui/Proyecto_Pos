import flet as ft
from recursos.funciones import *

def click_Registro(e):
    registro(tb2.value, tb3.value, tb4.value, tb5.value)

    tb2.value = ""
    tb3.value = ""
    tb4.value = ""
    tb5.value = ""
    #print("datos registrados")

###                     ###
##  Apartado de registro ##
#                         #

tb2 = ft.TextField(label="ID") # ID  DE LA ROPA
tb3 = ft.TextField(label="NOMBRE") # NOMBRENDE LA PRENDA
tb4 = ft.TextField(label="PRECIO UNIDAD") #PRECIO EN UNIDAD u/C
tb5 = ft.TextField(label="PRECIO MAYORISTA") # PRECIO MAYOR d/C

b_registro = ft.ElevatedButton(text="Registrar", color="white", icon="CHECK", bgcolor="black", on_click = click_Registro)




Registro = ft.Container(
    ft.Row([
        ft.Container(
            ft.Column(controls= [
                ft.Container(
                   ft.Text("REGISTRO DE PRODUCTOS", size=35, color="BLACK"),
                    alignment=ft.alignment.center,
                ),
                ft.Row(controls=[ft.Container(
                                    tb2,
                                    expand=2,
                                ),
                                ft.Container(
                                    b_registro,
                                    expand=1,
                                ),
                                    ]),
               tb3, tb4, tb5, 
            
            ], 
            alignment = ft.MainAxisAlignment.START,       
            ),

            # caracteristicas del contenedor
            gradient= ft.LinearGradient(['blue', 'purple']),     
            width=980,
            height =650,
            border_radius=20,
            margin =15,
            padding= 20
        )
    ])
)


Consulta = ft.Container(
    ft.Row([
        ft.Container(
            ft.Column(controls= [
                ft.Container(
                    ft.Text("BUSQUEDA DE PRECIOS", size=35, color="BLACK"),
                    alignment=ft.alignment.center,
                ),
                ft.Row(controls=[ft.Container(
                                    tb2,
                                    expand=2,
                                ),
                                ft.Container(
                                    b_registro,
                                    expand=1,
                                ),
                                    ]),
                
            ], 
            alignment = ft.MainAxisAlignment.START,       
            ),

            # caracteristicas del contenedor
            gradient= ft.LinearGradient(['blue', 'purple']),     
            #bgcolor= "GRAY",
            width=980,
            height =650,
            border_radius=20,
            margin =15,
            padding= 20
        )
    ])
)

Ventas = ft.Container(
    ft.Row([
        ft.Container(
            ft.Column(controls= [
                ft.Container(
                   ft.Text("VENTA", size=35, color="BLACK"),
                    alignment=ft.alignment.center,
                ),
                ft.Row(controls=[ft.Container(
                                    tb2,
                                    expand=2,
                                ),
                                ft.Container(
                                    b_registro,
                                    expand=1,
                                ),
                                    ]),
               
                
            ], 
            alignment = ft.MainAxisAlignment.START,       
            ),

            # caracteristicas del contenedor
            gradient= ft.LinearGradient(['blue', 'purple']),     
            width=980,
            height =650,
            border_radius=20,
            margin =15,
            padding= 20
        )
    ])
)