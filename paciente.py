class Paciente:
    """ Clase que representa la entidad Paciente con encapsulamiento. """

    def __init__(self, documento, nombre, telefono):
        # Atributos privados según requerimiento
        self.__documento = documento
        self.__nombre = nombre
        self.__telefono = telefono
        self.__historial = []

    # --- GETTERS (Propiedades) ---
    @property
    def documento(self):
        return self.__documento

    @property
    def nombre(self):
        return self.__nombre

    @property
    def telefono(self):
        return self.__telefono

    # --- SETTERS ---
    @nombre.setter
    def nombre(self, valor):
        self.__nombre = valor

    @telefono.setter
    def telefono(self, valor):
        self.__telefono = valor

    def to_dict(self):
        """ Convierte el objeto a diccionario para persistencia en JSON. """
        return {
            "documento": self.__documento,
            "nombre": self.__nombre,
            "telefono": self.__telefono,
            "historial": self.__historial
        }
