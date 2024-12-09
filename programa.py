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

from uiprograma import *

conexion = pymysql.connect(host="Localhost",
                           user="root",
                           password="elian2003",
                           database="sispos")
cursor = conexion.cursor()

class VentanaPrograma(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.uiprg = Ui_Programa()
        self.uiprg.setupUi(self)

        self.mensaje = QMessageBox()

        self.uiprg.busnombre.textChanged.connect(self.FiltrarNombre)
        self.uiprg.busdesc.textChanged.connect(self.FiltrarDescr)

    def IdentificarPrograma(self):
        try:
            row = self.uiprg.tablaprograma.currentRow()
            columnas = self.uiprg.tablaprograma.columnCount()
            datos = []
            for c in range(columnas):
                celda = self.uiprg.tablaprograma.item(row, c)
                if celda is not None:
                    datos.append(celda.text())

            return datos

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CargarPrograma(self):
        try:
            cursor.execute("SELECT idprg, nombre, descripcion, creacion FROM tbprg23")
            data = cursor.fetchall()

            if data:
                self.uiprg.tablaprograma.setRowCount(len(data))

                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        self.uiprg.tablaprograma.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def FiltrarDescr(self, text):

        for row in range(self.uiprg.tablaprograma.rowCount()):
            item = self.uiprg.tablaprograma.item(row, 2)
            if text.lower() in item.text().lower():
                self.uiprg.tablaprograma.showRow(row)
            else:
                self.uiprg.tablaprograma.hideRow(row)

    def FiltrarNombre(self, text):
        # Filtrar los datos en el QTableWidget según el texto ingresado
        for row in range(self.uiprg.tablaprograma.rowCount()):
            item = self.uiprg.tablaprograma.item(row, 1)
            if text.lower() in item.text().lower():
                self.uiprg.tablaprograma.showRow(row)
            else:
                self.uiprg.tablaprograma.hideRow(row)