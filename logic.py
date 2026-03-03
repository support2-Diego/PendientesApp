from datetime import datetime

class TaskLogic:
    @staticmethod
    def calcular_urgencia(fecha_limite_str):
        try:
            fecha_limite = datetime.strptime(fecha_limite_str, "%Y-%m-%d").date()
            hoy = datetime.now().date()
            dias_restantes = (fecha_limite - hoy).days

            if dias_restantes <= 0:
                return "HOY/VENCIDO", "#FF4444" # Rojo (Hoy o pasado)
            elif dias_restantes == 1:
                return "MAÑANA", "#FF8C00"      # Naranja (Mañana)
            else:
                return "A TIEMPO", "#4CAF50"    # Verde (2 días o más)
        except ValueError:
            return "ERROR", "#808080"

    @staticmethod
    def obtener_color_prioridad(nivel):
        # 1: Alto (Rojo), 2: Medio (Naranja), 3: Bajo (Verde)
        colores = {
            1: "#FF4444", 
            2: "#FF8C00", 
            3: "#4CAF50"  
        }
        return colores.get(nivel, "#808080")

    @staticmethod
    def validar_datos(tarea):
        if not tarea.strip():
            return False, "Escribe un título."
        return True, "OK"