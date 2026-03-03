import flet as ft
from database import Database
from logic import TaskLogic
from datetime import datetime

def main(page: ft.Page):
    page.title = "Gestor de Tareas"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 850
    page.window_height = 600
    
    db = Database()

    # --- CAMPOS DE FORMULARIO ---
    txt_titulo = ft.TextField(label="Título", border_color="blue400")
    txt_desc = ft.TextField(label="Descripción", multiline=True, min_lines=2, max_lines=3)
    
    drop_prio = ft.Dropdown(
        label="Prioridad",
        options=[
            ft.dropdown.Option("1", "1 - Alta"),
            ft.dropdown.Option("2", "2 - Media"),
            ft.dropdown.Option("3", "3 - Baja"),
        ],
        value="1"
    )

    def cambio_fecha(e):
        if date_picker.value:
            btn_fecha.text = date_picker.value.strftime("%Y-%m-%d")
            page.update()

    # Componente de fecha
    date_picker = ft.DatePicker(on_change=cambio_fecha)
    page.overlay.append(date_picker)
    
    # Abrir calendario correctamente en versiones nuevas
    def abrir_calendario(e):
        date_picker.open = True
        page.update()

    btn_fecha = ft.OutlinedButton(
        "Seleccionar Fecha", 
        icon=ft.Icons.CALENDAR_MONTH, 
        on_click=abrir_calendario
    )

    # --- LISTA DE TAREAS ---
    lista_tareas = ft.ListView(expand=True, spacing=10, padding=10)

    def refrescar_lista():
        lista_tareas.controls.clear()
        for t in db.obtener_tareas():
            color_urgencia = TaskLogic.calcular_urgencia(t[4])
            color_prio = TaskLogic.obtener_color_prioridad(t[3])
            
            card = ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(t[1], size=16, weight="bold"),
                        ft.Text(t[2] if t[2] else "Sin descripción", size=12, color="grey400"),
                        ft.Row([
                            ft.Container(
                                content=ft.Text(" PRIORIDAD ", size=10, weight="bold", color="white"),
                                bgcolor=color_prio,
                                border_radius=4,
                                padding=3
                            ),
                            ft.Text(f"Fecha: {t[4]}", size=11, italic=True)
                        ])
                    ], expand=True),
                    # CORRECCIÓN DEFINITIVA DEL BOTÓN: Usando ft.Icons
                    ft.IconButton(
                        icon=ft.Icons.CHECK_CIRCLE_OUTLINE, 
                        icon_color="greenaccent400",
                        tooltip="Marcar como completada",
                        on_click=lambda e, id_t=t[0]: completar(id_t)
                    )
                ]),
                border=ft.border.all(2, color_urgencia),
                border_radius=10,
                padding=10
            )
            lista_tareas.controls.append(card)
        page.update()

    def completar(id_tarea):
        db.marcar_completada(id_tarea)
        refrescar_lista()

    def guardar(e):
        if TaskLogic.validar_datos(txt_titulo.value)[0]:
            fecha_val = date_picker.value.strftime("%Y-%m-%d") if date_picker.value else datetime.now().strftime("%Y-%m-%d")
            db.insertar_tarea(txt_titulo.value, txt_desc.value, int(drop_prio.value), fecha_val)
            txt_titulo.value = ""
            txt_desc.value = ""
            refrescar_lista()

    # --- LAYOUT ---
    page.add(
        ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("Nueva Tarea", size=20, weight="bold"),
                    txt_titulo,
                    txt_desc,
                    drop_prio,
                    btn_fecha,
                    ft.FilledButton("Guardar", on_click=guardar, width=280)
                ], spacing=15),
                width=280,
                padding=20,
                bgcolor="surfaceContainerHighest",
                border_radius=10
            ),
            ft.Container(content=lista_tareas, expand=True)
        ], expand=True)
    )

    refrescar_lista()

if __name__ == "__main__":
    ft.app(target=main)