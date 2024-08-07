import flet as ft
from recursos.funciones import *


class RegistroPage:
    def __init__(self, page):
        self.page = page
        self.tb2 = ft.TextField(label="ID", autofocus=True)
        self.tb3 = ft.TextField(label="NOMBRE")
        self.tb4 = ft.TextField(label="PRECIO UNIDAD")
        self.tb5 = ft.TextField(label="PRECIO MAYORISTA")
        self.contador = 0
        self.list_id = []
        self.cont = ft.Text(f"Registro para imprimir: {self.contador}")
        
        self.print = ft.IconButton(
            icon=ft.icons.LOCAL_PRINT_SHOP_ROUNDED,
            icon_color="BLACK",
            on_click=self.click_imprimir_dialog
        )
        
        self.registro = ft.ElevatedButton(
            text="Registrar",
            color="white",
            icon="CHECK",
            bgcolor="black",
            on_click=self.click_Registro
        )

        self.alertaRegistro = ft.AlertDialog(
            title=ft.Text("Registro Exitoso", text_align="CENTER"),
            bgcolor=ft.colors.GREEN
        )
        
        self.alertaError = ft.AlertDialog(
            title=ft.Text("Error de Registro", text_align="CENTER"),
            bgcolor=ft.colors.RED
        )
        
        self.alertaCamposVacios = ft.AlertDialog(
            title=ft.Text("Campos Vacíos", text_align="CENTER"),
            bgcolor=ft.colors.ORANGE
        )

        self.alertaPrecios = ft.AlertDialog(
            title=ft.Text("Error de Precios", text_align="CENTER"),
            bgcolor=ft.colors.RED
        )

        self.alertaImpresion = ft.AlertDialog(
            title=ft.Text("Seleccione la cantidad de copias por ID"),
            content=ft.Container(),
            actions=[
                ft.TextButton("Imprimir", on_click=self.click_imprimir)
            ]
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
                                ft.Container(self.registro, expand=1),
                            ]),
                            self.tb3, self.tb4, self.tb5,

                            ft.Container(height=30),
                            ft.Divider(color="WHITE"),

                            ft.Row(controls=[
                                ft.Container(self.print, expand=1),
                                ft.Container(self.cont, expand=4),
                            ]),
                            ft.Divider(color="WHITE"),
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

    def click_imprimir_dialog(self, e):
        list_view_content = []
        self.id_copias_fields = {}
        for id in self.list_id:
            field = ft.TextField(label="Cant", value="", width=100)
            self.id_copias_fields[id] = field
            list_view_content.append(ft.Row([ft.Text(f"ID: {id}"), field]))
        
        self.alertaImpresion.content = ft.ListView(controls=list_view_content)
        self.alertaImpresion.open = True
        self.page.dialog = self.alertaImpresion
        self.page.update()

    def click_imprimir(self, e):
        id_copias_list = []
        for id, field in self.id_copias_fields.items():
            copias = int(field.value)
            id_copias_list.append((id, copias))
    
        if id_copias_list:
            generar_codigos_barras_pdf(id_copias_list)
            self.list_id = []
            self.contador = 0
            self.cont.value = f"Registro para imprimir: {self.contador}"
            self.alertaImpresion.open = False
            self.page.dialog = ft.AlertDialog(
                title=ft.Text("Impresión Exitosa"),
                content=ft.Text("Registros mandados a imprimir exitosamente."),
                bgcolor=ft.colors.GREEN
            )
            self.page.dialog.open = True
        print("id:",self.list_id)
        print("Cant:",id_copias_list)
        self.page.update()






    def click_Registro(self, e):
        id = self.tb2.value
        nombre = self.tb3.value
        precio_unidad = self.tb4.value
        precio_mayor = self.tb5.value
        
        campos_validos, id, mensaje_campos = verificar_campos(id, nombre, precio_unidad, precio_mayor)
        if not campos_validos:
            self.alertaCamposVacios.content = ft.Text(mensaje_campos)
            self.page.dialog = self.alertaCamposVacios
            self.page.dialog.open = True
            self.page.update()
            return

        precios_validos, mensaje_precios = verificar_precios(precio_unidad, precio_mayor)
        if not precios_validos:
            self.alertaPrecios.content = ft.Text(mensaje_precios)
            self.page.dialog = self.alertaPrecios
            self.page.dialog.open = True
            self.page.update()
            return

        success, message = registro(id, nombre, precio_unidad, precio_mayor)
        if success:
            self.tb2.value = ""
            self.tb3.value = ""
            self.tb4.value = ""
            self.tb5.value = ""
            self.list_id.append(id)
            self.contador += 1
            self.cont.value = f"Registro para imprimir: {self.contador}"
            self.page.dialog = self.alertaRegistro
        else:
            self.alertaError.content = ft.Text(message)
            self.page.dialog = self.alertaError
        
        self.page.dialog.open = True
        self.page.update()





class ConsultaPage:
    def __init__(self, page):
        self.page = page
        self.tb2 = ft.TextField(label="ID", autofocus=True)
        
        self.buscar = ft.ElevatedButton(
            text="Buscar",
            color="white",
            icon="SEARCH",
            bgcolor="black",
            on_click=self.click_Buscar
        )

        self.alertaConsulta = ft.AlertDialog(
            title=ft.Text("Consulta Exitosa",size=35,text_align="CENTER"),
            bgcolor=ft.colors.GREEN
        )

        self.alertaError = ft.AlertDialog(
            title=ft.Text("Error en la Consulta",size=35, text_align="CENTER"),
            bgcolor=ft.colors.RED
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
                                ft.Container(self.buscar, expand=1),
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
        id = self.tb2.value
        resultado = consulta(id)

        if resultado is not None:
            mensaje = f"Precio Unidad: Q{resultado[2]}\nPrecio Mayorista: Q{resultado[3]}"
            self.alertaConsulta.content = ft.Text(mensaje, size= 30, text_align="CENTER")
            self.page.dialog = self.alertaConsulta
        else:
            self.alertaError.content = ft.Text("No se encontró el producto con el id dado.", size=30, text_align="CENTER")
            self.page.dialog = self.alertaError

        self.page.dialog.open = True
        self.tb2.value = ""
        self.page.update()


class VentasPage:
    def __init__(self, page):
        self.page = page
        self.tb2 = ft.TextField(label="ID", autofocus=True)

        self.venta = ft.ElevatedButton(
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
                                ft.Container(self.venta, expand=1),
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


class RecibosPage:
    def __init__(self,page):
        self.page = page

        self.imprimir = ft.IconButton(
            icon=ft.icons.LOCAL_PRINTSHOP_ROUNDED,
            icon_size=150,
            on_click=self.on_click_imprimir,
            padding= 50,
            icon_color = "black"
        )

        self.Recibos = ft.Container(
            ft.Row([
                ft.Container(
                    ft.Column(
                        controls=[
                            ft.Container(
                                ft.Text("RECIBOS", size=35, color="BLACK"),
                                alignment=ft.alignment.center,
                            ),
                            ft.Row(controls=[
                                ft.Container(self.imprimir)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,)
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
    def on_click_imprimir(self, e):
        Facturacion()