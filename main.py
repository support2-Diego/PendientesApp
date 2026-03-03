import flet as ft
from database import Database
from logic import TaskLogic
from datetime import datetime

def main(page: ft.Page):
    page.title = "Gestor de Tareas Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 900
    page.window_height = 700
    
    db = Database()

    # --- ELEMENTOS DE UI ---
    txt_titulo = ft.TextField(label="Título", border_color="blue400")
    txt_desc = ft.TextField(label="Descripción", multiline=True, min_lines=2)
    
    drop_prio = ft.Dropdown(
        label="Prioridad",
        options=[
            ft.dropdown.Option("1", "1 - Alta"),
            ft.dropdown.Option("2", "2 - Media"),
            ft.dropdown.Option("3", "3 - Baja"),
        ],
        value="1"
    )

    # Barra de búsqueda mejorada
    search_field = ft.TextField(
        label="Buscar tarea...",
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: refrescar_lista(e.control.value),
        expand=True
    )

    # Notificaciones (SnackBars)
    def mostrar_mensaje(texto, color="blue"):
        page.snack_bar = ft.SnackBar(ft.Text(texto), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    # Manejo de Fecha
    def cambio_fecha(e):
        if date_picker.value:
            btn_fecha.text = date_picker.value.strftime("%Y-%m-%d")
            page.update()

    date_picker = ft.DatePicker(on_change=cambio_fecha)
    page.overlay.append(date_picker)
    
    btn_fecha = ft.OutlinedButton(
        "Seleccionar Fecha", 
        icon=ft.Icons.CALENDAR_MONTH, 
        on_click=lambda _: setattr(date_picker, "open", True) or page.update()
    )

    # --- LISTA DE TAREAS ---
    lista_tareas = ft.ListView(expand=True, spacing=10, padding=10)

    def refrescar_lista(filtro=""):
        lista_tareas.controls.clear()
        tareas = db.obtener_tareas()
        
        for t in tareas:
            # Filtrar por título (búsqueda)
            if filtro.lower() not in t[1].lower():
                continue

            color_urgencia = TaskLogic.calcular_urgencia(t[4])
            color_prio = TaskLogic.obtener_color_prioridad(t[3])
            
            # Tarjeta con Animación de entrada
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
                    ft.IconButton(
                        icon=ft.Icons.CHECK_CIRCLE_OUTLINE, 
                        icon_color="greenaccent400",
                        on_click=lambda e, id_t=t[0]: completar(id_t)
                    )
                ]),
                border=ft.border.all(2, color_urgencia),
                border_radius=10,
                padding=10,
                # Animación suave al aparecer
                animate_opacity=300,
                opacity=1
            )
            lista_tareas.controls.append(card)
        page.update()

    def completar(id_tarea):
        db.marcar_completada(id_tarea)
        mostrar_mensaje("¡Tarea completada!", "green800")
        refrescar_lista(search_field.value)

    def guardar(e):
        # Validación de campos
        valido, msg = TaskLogic.validar_datos(txt_titulo.value)
        if not valido:
            mostrar_mensaje(msg, "red800")
            return

        fecha_val = date_picker.value.strftime("%Y-%m-%d") if date_picker.value else datetime.now().strftime("%Y-%m-%d")
        db.insertar_tarea(txt_titulo.value, txt_desc.value, int(drop_prio.value), fecha_val)
        
        # Limpieza y feedback
        txt_titulo.value = ""
        txt_desc.value = ""
        mostrar_mensaje("Tarea guardada con éxito")
        refrescar_lista()

    # --- DISEÑO (LAYOUT) ---
    page.add(
        ft.Row([
            # Panel Izquierdo: Formulario
            ft.Container(
                content=ft.Column([
                    ft.Text("Nueva Tarea", size=22, weight="bold"),
                    txt_titulo,
                    txt_desc,
                    drop_prio,
                    btn_fecha,
                    ft.FilledButton("Guardar Tarea", on_click=guardar, icon=ft.Icons.ADD, width=280),
                ], spacing=20),
                width=300,
                padding=20,
                bgcolor="surfaceContainerHighest",
                border_radius=10
            ),
            # Panel Derecho: Búsqueda + Lista
            ft.Column([
                ft.Row([search_field]),
                ft.Divider(height=1, color="grey800"),
                lista_tareas
            ], expand=True)
        ], expand=True)
    )

    refrescar_lista()

if __name__ == "__main__":
    ft.app(target=main)