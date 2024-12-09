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

from uiproducto import *

conexion = pymysql.connect(host="Localhost",
                           user="root",
                           password="elian2003",
                           database="sispos")
cursor = conexion.cursor()


class VentanaProducto(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.uipro = Ui_Producto()
        self.uipro.setupUi(self)

        self.mensaje = QMessageBox()

        self.uipro.busnombre.textChanged.connect(self.FiltrarNombre)
        self.uipro.busprecio.textChanged.connect(self.FiltrarPrecio)
        self.uipro.busespec.textChanged.connect(self.FiltrarEspecificacion)



    def IdentificarProducto(self):
        try:
            row = self.uipro.tablaproducto.currentRow()
            columnas = self.uipro.tablaproducto.columnCount()
            datos = []
            for c in range(columnas):
                celda = self.uipro.tablaproducto.item(row, c)
                if celda is not None:
                    datos.append(celda.text())

            return datos
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CargarProductos(self):
        try:
            cursor.execute("SELECT idpro, nompro, punret, canexis, precio, especificaciones FROM tbpro10")
            data = cursor.fetchall()

            if data:
                self.uipro.tablaproducto.setRowCount(len(data))

                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        self.uipro.tablaproducto.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def FiltrarEspecificacion(self, text):

        for row in range(self.uipro.tablaproducto.rowCount()):
            item = self.uipro.tablaproducto.item(row, 5)
            if text.lower() in item.text().lower():
                self.uipro.tablaproducto.showRow(row)
            else:
                self.uipro.tablaproducto.hideRow(row)



    def FiltrarPrecio(self, text):

        for row in range(self.uipro.tablaproducto.rowCount()):
            item = self.uipro.tablaproducto.item(row, 4)
            if text.lower() in item.text().lower():
                self.uipro.tablaproducto.showRow(row)
            else:
                self.uipro.tablaproducto.hideRow(row)

    def FiltrarNombre(self, text):
        # Filtrar los datos en el QTableWidget según el texto ingresado
        for row in range(self.uipro.tablaproducto.rowCount()):
            item = self.uipro.tablaproducto.item(row, 1)
            if text.lower() in item.text().lower():
                self.uipro.tablaproducto.showRow(row)
            else:
                self.uipro.tablaproducto.hideRow(row)



