import decimal
import sys
import pymysql
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QImage, QPixmap, QIcon, QDoubleValidator
from PyQt5.QtWidgets import QTableWidgetItem, QMenu, QAction, QFileDialog, QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime

from uiprovincia import *

conexion = pymysql.connect(host="Localhost",
                           user="root",
                           password="elian2003",
                           database="sispos")
cursor = conexion.cursor()

class VentanaProvincia(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.uiprov = Ui_Provincia()
        self.uiprov.setupUi(self)

        self.mensaje = QMessageBox()

        self.uiprov.busnombre.textChanged.connect(self.FiltrarNombre)

    def IdentificarProvincia(self):
        try:
            row = self.uiprov.tablaprovincia.currentRow()
            columnas = self.uiprov.tablaprovincia.columnCount()
            datos = []
            for c in range(columnas):
                celda = self.uiprov.tablaprovincia.item(row, c)
                if celda is not None:
                    datos.append(celda.text())

            return datos

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    

    def CargarProvincia(self):
        try:
            cursor.execute("SELECT idprov, nombre, creacion FROM tbprov25")
            data = cursor.fetchall()

            if data:
                self.uiprov.tablaprovincia.setRowCount(len(data))

                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        self.uiprov.tablaprovincia.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def FiltrarNombre(self, text):
        # Filtrar los datos en el QTableWidget según el texto ingresado
        for row in range(self.uiprov.tablaprovincia.rowCount()):
            item = self.uiprov.tablaprovincia.item(row, 1)
            if text.lower() in item.text().lower():
                self.uiprov.tablaprovincia.showRow(row)
            else:
                self.uiprov.tablaprovincia.hideRow(row)