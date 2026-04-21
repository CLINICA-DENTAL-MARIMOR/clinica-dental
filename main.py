import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QLabel)
from paciente import Paciente
from paciente_controller import PacienteController

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clínica Sonrisa Perfecta - Sprint 1")
        self.setMinimumSize(700, 500)
        self.controlador = PacienteController()
        self._configurar_ui()

    def _configurar_ui(self):
        # Widget central y layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)

        # Formulario
        self.layout.addWidget(QLabel("### Registro de Pacientes ###"))
        self.in_doc = QLineEdit(); self.in_doc.setPlaceholderText("Documento de Identidad")
        self.in_nom = QLineEdit(); self.in_nom.setPlaceholderText("Nombre Completo")
        self.in_tel = QLineEdit(); self.in_tel.setPlaceholderText("Teléfono de Contacto")

        btn_add = QPushButton("Guardar Paciente")
        btn_add.clicked.connect(self._evento_guardar)

        # Tabla
        self.tabla = QTableWidget(0, 3)
        self.tabla.setHorizontalHeaderLabels(["Documento", "Nombre", "Teléfono"])

        # Agregar al layout
        for w in [self.in_doc, self.in_nom, self.in_tel, btn_add, self.tabla]:
            self.layout.addWidget(w)

        self.setCentralWidget(self.central_widget)
        self._refrescar_tabla()

    def _evento_guardar(self):
        doc, nom, tel = self.in_doc.text(), self.in_nom.text(), self.in_tel.text()

        if doc and nom:
            nuevo = Paciente(doc, nom, tel)
            self.controlador.registrar_paciente(nuevo)
            self._refrescar_tabla()
            self.in_doc.clear(); self.in_nom.clear(); self.in_tel.clear()
            QMessageBox.information(self, "Éxito", "Paciente guardado exitosamente.")
        else:
            QMessageBox.warning(self, "Error", "Por favor completa Documento y Nombre.")

    def _refrescar_tabla(self):
        pacientes = self.controlador.listar_todos()
        self.tabla.setRowCount(len(pacientes))
        for i, p in enumerate(pacientes):
            self.tabla.setItem(i, 0, QTableWidgetItem(p["documento"]))
            self.tabla.setItem(i, 1, QTableWidgetItem(p["nombre"]))
            self.tabla.setItem(i, 2, QTableWidgetItem(p["telefono"]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
