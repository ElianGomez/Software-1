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

from uibanco import *

conexion = pymysql.connect(host="Localhost",
                           user="root",
                           password="elian2003",
                           database="sispos")
cursor = conexion.cursor()

class VentanaBanco(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.uiban = Ui_Banco()
        self.uiban.setupUi(self)

        self.mensaje = QMessageBox()

        self.uiban.busnombre.textChanged.connect(self.FiltrarNombre)

    def IdentificarBanco(self):
        try:
            row = self.uiban.tablabanco.currentRow()
            columnas = self.uiban.tablabanco.columnCount()
            datos = []
            for c in range(columnas):
                celda = self.uiban.tablabanco.item(row, c)
                if celda is not None:
                    datos.append(celda.text())

            return datos

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def CargarBanco(self):
        try:
            cursor.execute("SELECT idbanco, nombre FROM tbban06")
            data = cursor.fetchall()

            if data:
                self.uiban.tablabanco.setRowCount(len(data))

                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        self.uiban.tablabanco.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def FiltrarNombre(self, text):
        # Filtrar los datos en el QTableWidget según el texto ingresado
        for row in range(self.uiban.tablabanco.rowCount()):
            item = self.uiban.tablabanco.item(row, 1)
            if text.lower() in item.text().lower():
                self.uiban.tablabanco.showRow(row)
            else:
                self.uiban.tablabanco.hideRow(row)




