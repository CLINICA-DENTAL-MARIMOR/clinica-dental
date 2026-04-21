import json
import os

class PacienteController:
    """ Maneja la persistencia y reglas de negocio de los pacientes. """

    def __init__(self, ruta_db="data/pacientes.json"):
        self.ruta_db = ruta_db
        # Crea la carpeta data si no existe
        if not os.path.exists("data"):
            os.makedirs("data")

    def registrar_paciente(self, paciente_obj):
        """ Guarda un objeto Paciente en el archivo JSON. """
        datos = self.listar_todos()
        datos.append(paciente_obj.to_dict())
        with open(self.ruta_db, "w", encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    def listar_todos(self):
        """ Recupera la lista de pacientes desde el JSON. """
        if not os.path.exists(self.ruta_db):
            return []
        try:
            with open(self.ruta_db, "r", encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
