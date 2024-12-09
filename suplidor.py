import decimal
import sys
import pymysql
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QImage, QPixmap, QIcon, QDoubleValidator
from PyQt5.QtWidgets import QTableWidgetItem, QMenu, QAction, QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime

from uisuplidor import *

conexion = pymysql.connect(host="Localhost",
                           user="root",
                           password="elian2003",
                           database="sispos")
cursor = conexion.cursor()

class VentanaSuplidor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.uisup = Ui_Suplidor()
        self.uisup.setupUi(self)

        self.mensaje = QMessageBox()

        self.uisup.nombre.textChanged.connect(self.BuscarSup)

    def IdentificarSuplidor(self):
        try:
            row = self.uisup.tablasup.currentRow()
            columnas = self.uisup.tablasup.columnCount()
            datos = []
            for c in range(columnas):
                celda = self.uisup.tablasup.item(row, c)
                if celda is not None:
                    datos.append(celda.text())

            return datos

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CargarSuplidores(self):
        try:
            cursor.execute("SELECT idsup, nombre, telefono, direccion, correo, web FROM tbsup09")
            data = cursor.fetchall()

            if data:
                self.uisup.tablasup.setRowCount(len(data))

                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        self.uisup.tablasup.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def BuscarSup(self, text):

        for row in range(self.uisup.tablasup.rowCount()):
            item = self.uisup.tablasup.item(row, 1)
            if text.lower() in item.text().lower():
                self.uisup.tablasup.showRow(row)
            else:
                self.uisup.tablasup.hideRow(row)


