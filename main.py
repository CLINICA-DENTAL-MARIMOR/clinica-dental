import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox, QLabel, QTabWidget, QDateTimeEdit)
from PySide6.QtCore import QDateTime
from paciente import Paciente
from paciente_controller import PacienteController
from cita import Cita
from cita_controller import CitaController

class VentanaPrincipalClinica(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión Clínica Sonrisa Perfecta - Sprint 2")
        self.setMinimumSize(1000, 700)

        # Inicialización de controladores con nombres claros
        self.controlador_pacientes = PacienteController()
        self.controlador_citas = CitaController()

        # Contenedor principal de módulos
        self.panel_pestañas_principal = QTabWidget()
        self.setCentralWidget(self.panel_pestañas_principal)

        self._inicializar_modulo_gestion_pacientes()
        self._inicializar_modulo_agenda_citas()

    # --- MÓDULO: GESTIÓN DE PACIENTES ---
    def _inicializar_modulo_gestion_pacientes(self):
        widget_pestaña_pacientes = QWidget()
        layout_vertical_pacientes = QVBoxLayout(widget_pestaña_pacientes)

        layout_vertical_pacientes.addWidget(QLabel("<h2>Registro de Nuevo Paciente</h2>"))

        # Campos de entrada con nombres descriptivos
        self.entrada_documento_paciente = QLineEdit()
        self.entrada_documento_paciente.setPlaceholderText("Ingrese el documento de identidad")

        self.entrada_nombre_paciente = QLineEdit()
        self.entrada_nombre_paciente.setPlaceholderText("Ingrese el nombre completo")

        self.entrada_telefono_paciente = QLineEdit()
        self.entrada_telefono_paciente.setPlaceholderText("Ingrese el número de teléfono")

        self.boton_registrar_paciente = QPushButton("Guardar Datos del Paciente")
        self.boton_registrar_paciente.clicked.connect(self._procesar_registro_paciente)

        # Tabla de visualización
        self.tabla_lista_pacientes = QTableWidget(0, 3)
        self.tabla_lista_pacientes.setHorizontalHeaderLabels(["Documento", "Nombre Completo", "Teléfono"])

        # Agregar elementos al layout de la pestaña
        layout_vertical_pacientes.addWidget(self.entrada_documento_paciente)
        layout_vertical_pacientes.addWidget(self.entrada_nombre_paciente)
        layout_vertical_pacientes.addWidget(self.entrada_telefono_paciente)
        layout_vertical_pacientes.addWidget(self.boton_registrar_paciente)
        layout_vertical_pacientes.addWidget(self.tabla_lista_pacientes)

        self.panel_pestañas_principal.addTab(widget_pestaña_pacientes, "Gestión de Pacientes")
        self._refrescar_datos_tabla_pacientes()

    # --- MÓDULO: AGENDA DE CITAS ---
    def _inicializar_modulo_agenda_citas(self):
        widget_pestaña_citas = QWidget()
        layout_vertical_citas = QVBoxLayout(widget_pestaña_citas)

        layout_vertical_citas.addWidget(QLabel("<h2>Agendamiento de Citas Médicas</h2>"))

        self.entrada_documento_busqueda_cita = QLineEdit()
        self.entrada_documento_busqueda_cita.setPlaceholderText("Documento del paciente para la cita")

        self.entrada_fecha_hora_cita = QDateTimeEdit(QDateTime.currentDateTime())
        self.entrada_fecha_hora_cita.setCalendarPopup(True)

        self.entrada_motivo_consulta = QLineEdit()
        self.entrada_motivo_consulta.setPlaceholderText("Motivo de la consulta (ej. Limpieza, Calza)")

        self.boton_confirmar_cita = QPushButton("Confirmar y Agendar Cita")
        self.boton_confirmar_cita.clicked.connect(self._procesar_agendamiento_cita)

        self.tabla_lista_citas = QTableWidget(0, 4)
        self.tabla_lista_citas.setHorizontalHeaderLabels(["Paciente", "Fecha y Hora", "Motivo", "Estado"])

        # Agregar elementos al layout
        layout_vertical_citas.addWidget(QLabel("Documento del Paciente:"))
        layout_vertical_citas.addWidget(self.entrada_documento_busqueda_cita)
        layout_vertical_citas.addWidget(QLabel("Fecha Seleccionada:"))
        layout_vertical_citas.addWidget(self.entrada_fecha_hora_cita)
        layout_vertical_citas.addWidget(self.entrada_motivo_consulta)
        layout_vertical_citas.addWidget(self.boton_confirmar_cita)
        layout_vertical_citas.addWidget(self.tabla_lista_citas)

        self.panel_pestañas_principal.addTab(widget_pestaña_citas, "Agenda de Citas")
        self._refrescar_datos_tabla_citas()

    # --- LÓGICA DE PROCESAMIENTO ---

    def _procesar_registro_paciente(self):
        documento = self.entrada_documento_paciente.text()
        nombre = self.entrada_nombre_paciente.text()
        telefono = self.entrada_telefono_paciente.text()

        if documento and nombre:
            objeto_paciente = Paciente(documento, nombre, telefono)
            self.controlador_pacientes.registrar_paciente(objeto_paciente)
            self._refrescar_datos_tabla_pacientes()

            # Limpiar campos después de guardar
            self.entrada_documento_paciente.clear()
            self.entrada_nombre_paciente.clear()
            self.entrada_telefono_paciente.clear()

            QMessageBox.information(self, "Registro Exitoso", "El paciente ha sido guardado en la base de datos.")
        else:
            QMessageBox.warning(self, "Campos Requeridos", "Por favor complete Documento y Nombre.")

    def _procesar_agendamiento_cita(self):
        documento_buscado = self.entrada_documento_busqueda_cita.text()
        fecha_texto = self.entrada_fecha_hora_cita.dateTime().toString("dd/MM/yyyy HH:mm")
        motivo_texto = self.entrada_motivo_consulta.text()

        # Obtenemos la lista actual de pacientes para la validación de seguridad
        lista_pacientes_actuales = self.controlador_pacientes.obtener_todos()
        nueva_cita_medica = Cita(documento_buscado, fecha_texto, motivo_texto)

        resultado_operacion, mensaje_respuesta = self.controlador_citas.agendar_cita(
            nueva_cita_medica,
            lista_pacientes_actuales
        )

        if resultado_operacion:
            self._refrescar_datos_tabla_citas()
            self.entrada_documento_busqueda_cita.clear()
            self.entrada_motivo_consulta.clear()
            QMessageBox.information(self, "Cita Agendada", mensaje_respuesta)
        else:
            QMessageBox.critical(self, "Error de Validación", mensaje_respuesta)

    def _refrescar_datos_tabla_pacientes(self):
        datos_recuperados = self.controlador_pacientes.obtener_todos()
        self.tabla_lista_pacientes.setRowCount(len(datos_recuperados))
        for indice, paciente_dict in enumerate(datos_recuperados):
            self.tabla_lista_pacientes.setItem(indice, 0, QTableWidgetItem(paciente_dict['documento']))
            self.tabla_lista_pacientes.setItem(indice, 1, QTableWidgetItem(paciente_dict['nombre']))
            self.tabla_lista_pacientes.setItem(indice, 2, QTableWidgetItem(paciente_dict['telefono']))

    def _refrescar_datos_tabla_citas(self):
        citas_recuperadas = self.controlador_citas.listar_todas()
        self.tabla_lista_citas.setRowCount(len(citas_recuperadas))
        for indice, cita_dict in enumerate(citas_recuperadas):
            self.tabla_lista_citas.setItem(indice, 0, QTableWidgetItem(cita_dict['doc_paciente']))
            self.tabla_lista_citas.setItem(indice, 1, QTableWidgetItem(cita_dict['fecha']))
            self.tabla_lista_citas.setItem(indice, 2, QTableWidgetItem(cita_dict['motivo']))
            self.tabla_lista_citas.setItem(indice, 3, QTableWidgetItem(cita_dict['estado']))

if __name__ == "__main__":
    aplicacion = QApplication(sys.argv)
    ventana_principal = VentanaPrincipalClinica()
    ventana_principal.show()
    sys.exit(aplicacion.exec())
