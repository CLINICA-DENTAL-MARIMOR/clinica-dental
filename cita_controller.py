import json
import os

class CitaController:
    """ Maneja la lógica de agendamiento y validación de citas. """

    def __init__(self, ruta_db="data/citas.json"):
        self.ruta_db = ruta_db
        if not os.path.exists("data"):
            os.makedirs("data")

    def agendar_cita(self, cita_obj, lista_pacientes_registrados):
        """
        Valida si el paciente existe y guarda la cita.
        lista_pacientes_registrados: Lista de diccionarios de pacientes.
        """
        # Validación de seguridad: ¿Existe el paciente?
        documentos_validos = [p['documento'] for p in lista_pacientes_registrados]

        if cita_obj.doc_paciente not in documentos_validos:
            return False, "Error: El paciente no está registrado en el sistema."

        citas = self.listar_todas()
        citas.append(cita_obj.to_dict())

        with open(self.ruta_db, "w", encoding='utf-8') as f:
            json.dump(citas, f, indent=4, ensure_ascii=False)

        return True, "Cita agendada exitosamente."

    def listar_todas(self):
        if not os.path.exists(self.ruta_db):
            return []
        try:
            with open(self.ruta_db, "r", encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
