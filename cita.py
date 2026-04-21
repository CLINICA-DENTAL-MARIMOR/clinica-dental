class Cita:
    """ Representa una cita médica en el sistema con encapsulamiento. """

    def __init__(self, doc_paciente, fecha, motivo, odontologo="Dr. Pérez"):
        self.__doc_paciente = doc_paciente
        self.__fecha = fecha
        self.__motivo = motivo
        self.__odontologo = odontologo
        self.__estado = "Activa"

    @property
    def doc_paciente(self): return self.__doc_paciente

    @property
    def fecha(self): return self.__fecha

    @property
    def motivo(self): return self.__motivo

    @property
    def odontologo(self): return self.__odontologo

    @property
    def estado(self): return self.__estado

    @estado.setter
    def estado(self, valor): self.__estado = valor

    def to_dict(self):
        """ Convierte el objeto a diccionario para persistencia JSON. """
        return {
            "doc_paciente": self.__doc_paciente,
            "fecha": self.__fecha,
            "motivo": self.__motivo,
            "odontologo": self.__odontologo,
            "estado": self.__estado
        }
