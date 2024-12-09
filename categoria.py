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

from uicategoria import *

conexion = pymysql.connect(host="Localhost",
                           user="root",
                           password="elian2003",
                           database="sispos")
cursor = conexion.cursor()

class VentanaCategoria(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.uicat = Ui_Categoria()
        self.uicat.setupUi(self)

        self.mensaje = QMessageBox()

        self.uicat.busnombre.textChanged.connect(self.FiltrarNombre)

    def IdentificarCategoria(self):
        try:
            row = self.uicat.tablacategoria.currentRow()
            columnas = self.uicat.tablacategoria.columnCount()
            datos = []
            for c in range(columnas):
                celda = self.uicat.tablacategoria.item(row, c)
                if celda is not None:
                    datos.append(celda.text())

            return datos

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def CargarCategoria(self):
        try:
            cursor.execute("SELECT idcategoria, descripcion FROM tbcat00")
            data = cursor.fetchall()

            if data:
                self.uicat.tablacategoria.setRowCount(len(data))

                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        self.uicat.tablacategoria.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def FiltrarNombre(self, text):
        # Filtrar los datos en el QTableWidget según el texto ingresado
        for row in range(self.uicat.tablacategoria.rowCount()):
            item = self.uicat.tablacategoria.item(row, 1)
            if text.lower() in item.text().lower():
                self.uicat.tablacategoria.showRow(row)
            else:
                self.uicat.tablacategoria.hideRow(row)