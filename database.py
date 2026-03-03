import sqlite3

class Database:
    def __init__(self, db_name="pendientes.db"):
        self.conexion = sqlite3.connect(db_name)
        self.cursor = self.conexion.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        query = '''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarea TEXT NOT NULL,
            descripcion TEXT, 
            prioridad INTEGER NOT NULL,
            fecha_limite TEXT NOT NULL,
            estado TEXT DEFAULT 'Pendiente'
        )
        '''
        self.cursor.execute(query)
        self.conexion.commit()

    def insertar_tarea(self, tarea, descripcion, prioridad, fecha):
        query = "INSERT INTO tareas (tarea, descripcion, prioridad, fecha_limite) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (tarea, descripcion, prioridad, fecha))
        self.conexion.commit()

    def obtener_tareas(self):
        # --- CAMBIO CLAVE: Ordenar primero por FECHA y luego por PRIORIDAD ---
        query = "SELECT * FROM tareas WHERE estado != 'Completado' ORDER BY fecha_limite ASC, prioridad ASC"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def marcar_completada(self, id_tarea):
        query = "UPDATE tareas SET estado = 'Completado' WHERE id = ?"
        self.cursor.execute(query, (id_tarea,))
        self.conexion.commit()

    def cerrar_conexion(self):
        self.conexion.close()