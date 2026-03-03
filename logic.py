from datetime import datetime

class TaskLogic:
    @staticmethod
    def calcular_urgencia(fecha_limite_str):
        try:
            fecha_limite = datetime.strptime(fecha_limite_str, "%Y-%m-%d").date()
            hoy = datetime.now().date()
            dias_restantes = (fecha_limite - hoy).days

            if dias_restantes <= 0:
                return "red600"
            elif dias_restantes == 1:
                return "orange600"
            else:
                return "green600"
        except ValueError:
            return "grey400"

    @staticmethod
    def obtener_color_prioridad(nivel):
        colores = {1: "red600", 2: "orange600", 3: "green600"}
        return colores.get(nivel, "grey400")

    @staticmethod
    def validar_datos(tarea):
        if not tarea or not tarea.strip():
            return False, "Escribe un título."
        return True, "OK"