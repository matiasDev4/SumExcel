import pandas as pd
import flet as ft
from flet import *


def main(page: ft.Page):
    #Configurando ventana 
    page.window.width=500
    page.window.height=500
    page.window.center()
    page.window.icon = "/assets/favicon.ico"
    page.title = "MYM"
    
    #Widgets para mostrar datos
    dir = Text("", size=15)
    total_ventas = Text("", size=20)
    total_grabado = Text("", size=20)
    total_iva21 = Text("", size=20)
    total_iva10 = Text("", size=20)
    #Titulo
    page.add(ft.Container(
        content=ft.Text("Gestion de ventas", size=30, text_align=TextAlign.CENTER),
        width=1500))
    #Funcion para cerrar dialogo
    def close(e):
        page.close(dlg_modal)
        
    #Dialogo
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Ocurrio un error ❌"),
        content=ft.Text("Solo se permiten archivos de tipo xlsx o xls, intente con otro", color="red", size=16),
        actions=[
            ft.TextButton("Cerrar", on_click=close),
        ]
    )
    #Funcion para cargar archivos
    def on_dialog_result(e: ft.FilePickerResultEvent):
        #Itero sobre el archivo para obtener sus propiedades
        for x in e.files:
            #Le paso el valor nuevo al widget
            dir.value = f"Archivo actual: {x.name}"
            dir.update()
            try:
                #obtengo el tipo de extension del archivo
                extension = x.path.split(".")[1]
                if extension == "xlsx" or extension == "xls":
                    try: 
                        datos = pd.read_excel(f"{x.path}")
                        ventas = datos["Total"].sum()
                        grabado = datos["IInterno"].sum()
                        iva21 = datos["IVA21"].sum()
                        iva10 = datos["IVA105"].sum()  
                        #Creo formato de numeros
                        formato_total = "{:0,.0f}".format(ventas)
                        formato_grabado = "{:0,.0f}".format(grabado)
                        formato_iva21 = "{:0,.0f}".format(iva21)
                        formato_iva10 = "{:0,.0f}".format(iva10)
                        #Le paso los nuevos valores a los widget
                        total_ventas.value = f"Total de ventas: ${formato_total}"
                        total_ventas.update()
                        total_grabado.value = f"Total Inpuesto Interno: ${formato_grabado}"
                        total_grabado.update()
                        total_iva21.value = f"Total IVA 21: ${formato_iva21}"
                        total_iva21.update()        
                        total_iva10.value = f"Total IVA 10,5: ${formato_iva10}"
                        total_iva10.update()
                    except Exception as e:
                        pass
                else:
                    page.open(dlg_modal)
                    page.update()  
            except Exception as e:
                pass
    #Abrir explorador de archivos
    file_picker = ft.FilePicker(on_result=on_dialog_result)
    select_file = ft.Row(
        wrap=True,
        spacing=15,
        run_spacing=10,
        controls=[(ft.ElevatedButton("Selecciona un archivo...",
    on_click=lambda _: file_picker.pick_files(allow_multiple=False))  
    ),
    dir],
        width=page.window.width,
    )
    #Muestra los resulados
    results = ft.SafeArea(
        ft.Container(
            ft.Column(spacing=25, controls=[total_ventas, total_grabado, total_iva21, total_iva10]),
            alignment=ft.alignment.center
        )
    )
    #Añado todo
    page.add(select_file)
    page.add(results)
    page.overlay.append(file_picker)
    page.add(Text(""))
    page.add()
    page.update()


ft.app(main)

