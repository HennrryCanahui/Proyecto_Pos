import flet as ft
from recursos.funciones import *

class RegistroPage:
    def __init__(self, page):
        self.page = page
        self.tb2 = ft.TextField(label="ID", autofocus=True)
        self.tb3 = ft.TextField(label="NOMBRE")
        self.tb4 = ft.TextField(label="PRECIO UNIDAD")
        self.tb5 = ft.TextField(label="PRECIO MAYORISTA")

        self.b_registro = ft.ElevatedButton(
            text="Registrar",
            color="white",
            icon="CHECK",
            bgcolor="black",
            on_click=self.click_Registro
        )

        self.alertaRegistro = ft.AlertDialog(
            title=ft.Text("Registro Exitoso", text_align="CENTER"),
            bgcolor=ft.colors.GREEN,
        )

        self.Registro = ft.Container(
            ft.Row([
                ft.Container(
                    ft.Column(
                        controls=[
                            ft.Container(
                                ft.Text("REGISTRO DE PRODUCTOS", size=35, color="BLACK"),
                                alignment=ft.alignment.center,
                            ),
                            ft.Row(controls=[
                                ft.Container(self.tb2, expand=2),
                                ft.Container(self.b_registro, expand=1),
                            ]),
                            self.tb3, self.tb4, self.tb5,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    gradient=ft.LinearGradient(['blue', 'purple']),
                    width=980,
                    height=650,
                    border_radius=20,
                    margin=15,
                    padding=20
                )
            ])
        )

    def click_Registro(self, e):
        registro(self.tb2.value, self.tb3.value, self.tb4.value, self.tb5.value)
        self.tb2.value = ""
        self.tb3.value = ""
        self.tb4.value = ""
        self.tb5.value = ""
        self.page.dialog = self.alertaRegistro
        self.alertaRegistro.open = True
        self.page.update()




class ConsultaPage:
    def __init__(self, page):
        self.page = page
        self.tb2 = ft.TextField(label="ID", autofocus=True)
        
        self.b_buscar = ft.ElevatedButton(
            text="Buscar",
            color="white",
            icon="SEARCH",
            bgcolor="black",
            on_click=self.click_Buscar
        )

        self.alertaConsulta = ft.AlertDialog(
            title=ft.Text("Consulta Exitosa", bgcolor=ft.colors.GREEN)
        )

        self.Consulta = ft.Container(
            ft.Row([
                ft.Container(
                    ft.Column(
                        controls=[
                            ft.Container(
                                ft.Text("BUSQUEDA DE PRECIOS", size=35, color="BLACK"),
                                alignment=ft.alignment.center,
                            ),
                            ft.Row(controls=[
                                ft.Container(self.tb2, expand=2),
                                ft.Container(self.b_buscar, expand=1),
                            ]),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    gradient=ft.LinearGradient(['blue', 'purple']),
                    width=980,
                    height=650,
                    border_radius=20,
                    margin=15,
                    padding=20
                )
            ])
        )

    def click_Buscar(self, e):
        consulta(self.tb2.value)  # Ahora solo pasa `id`
        self.tb2.value = ""
        self.page.update()











class VentasPage:
    def __init__(self, page):
        self.page = page
        self.tb2 = ft.TextField(label="ID", autofocus=True)

        self.b_registro = ft.ElevatedButton(
            text="Vender",
            color="white",
            icon="SHOPPING_CART",
            bgcolor="black",
            on_click=self.click_Vender
        )

        self.alertaVenta = ft.AlertDialog(
            title=ft.Text("Venta Exitosa", bgcolor=ft.colors.GREEN)
        )

        self.Ventas = ft.Container(
            ft.Row([
                ft.Container(
                    ft.Column(
                        controls=[
                            ft.Container(
                                ft.Text("VENTA", size=35, color="BLACK"),
                                alignment=ft.alignment.center,
                            ),
                            ft.Row(controls=[
                                ft.Container(self.tb2, expand=2),
                                ft.Container(self.b_registro, expand=1),
                            ]),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    gradient=ft.LinearGradient(['blue', 'purple']),
                    width=980,
                    height=650,
                    border_radius=20,
                    margin=15,
                    padding=20
                )
            ])
        )

    def click_Vender(self, e):
        #vender(self.tb2.value)  # Asumiendo que hay una función `vender` definida en `recursos.funciones`
        self.tb2.value = ""
        self.page.update()
