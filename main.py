import flet as ft 
from recursos.secciones import *

def main(page:ft.Page):
    

    nav = ft.Container(
        ft.Row([
            ft.Container(
                ft.Column(controls= [
                    ft.Text(
                        'OPCIONES',
                        width=360,
                        size=30,
                        weight ='w900',
                        text_align = 'center'
                    ),
                    ft.Container(
                        ft.IconButton(
                            icon=ft.icons.ADD,
                            icon_color="BLACK",
                            icon_size=40,
                            tooltip="AÑADIR",
                            on_click=lambda _: page.go("/nav_uno")  
                        ),
                        padding = ft.padding.only(65)
                    ),
                    ft.Container(
                        ft.IconButton(
                            icon=ft.icons.SEARCH,
                            icon_color="BLACK",
                            icon_size=40,
                            tooltip="BUSQUEDA",
                            on_click=lambda _: page.go("/nav_dos")  
                        ),
                        padding = ft.padding.only(65)
                    ),
                    ft.Container(
                        ft.IconButton(
                            icon=ft.icons.POINT_OF_SALE_OUTLINED,
                            icon_color="BLACK",
                            icon_size=40,
                            tooltip="VENTA",
                            on_click=lambda _: page.go("/nav_tres")  
                        ),
                        padding = ft.padding.only(65),
                    )
                ], 
                alignment = ft.MainAxisAlignment.SPACE_EVENLY,       
                ),
                gradient= ft.LinearGradient(['purple', 'blue']),     
                width=180,
                height =650,
                border_radius=20,
                margin =15,
            ),
        ],
        ),   
    )
    page.window_width =1250
    page.window_min_width =1250
    page.window_min_height = 720
    page.padding = 0
    page.theme_mode = ft.ThemeMode.SYSTEM
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [ft.Row([nav, 
                        ft.Image(
                            src=r"recursos/Comercial_Glendy.png",
                            width=980,
                            height=650,
                            fit=ft.ImageFit.CONTAIN,
                            border_radius=ft.border_radius.all(15),
                        )

                    ])]
            )
        )
        if page.route == "/nav_uno":
            page.views.append(
                ft.View(
                    "/nav_uno",
                    [
                        ft.Row([
                            nav,
                            Registro,
                           
                        ])
                    ],
                )
            )
        elif page.route == "/nav_dos":
            page.views.append(
                ft.View(
                    "/nav_dos",
                    [

                        ft.Row([
                            nav,
                            Consulta,
                        ])
                    ],
                )
            )
        elif page.route == "/nav_tres":
            page.views.append(
                ft.View(
                    "/nav_tres",
                    [
                        ft.Row([
                            nav,
                            Ventas,
                        ])
                    ],
                )
            )
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)