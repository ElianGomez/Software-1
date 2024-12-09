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

from uisucursal import *

conexion = pymysql.connect(host="Localhost",
                           user="root",
                           password="elian2003",
                           database="sispos")
cursor = conexion.cursor()

class VentanaSucursal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.uisuc = Ui_Sucursal()
        self.uisuc.setupUi(self)

        self.mensaje = QMessageBox()

        self.uisuc.busnombre.textChanged.connect(self.FiltrarNombre)
        self.uisuc.busprovincia.textChanged.connect(self.FiltrarProvincia)

    def IdentificarSucursal(self):
        try:
            row = self.uisuc.tablasucursal.currentRow()
            columnas = self.uisuc.tablasucursal.columnCount()
            datos = []
            for c in range(columnas):
                celda = self.uisuc.tablasucursal.item(row, c)
                if celda is not None:
                    datos.append(celda.text())

            return datos

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def CargarSucursal(self):
        try:
            cursor.execute("SELECT a.idsuc,  a.nombre, a.idprov, b.nombre, a.creacion "
                           "FROM tbsuc26 a, tbprov25 b "
                           "WHERE a.idprov=b.idprov")
            data = cursor.fetchall()

            if data:
                self.uisuc.tablasucursal.setRowCount(len(data))

                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        self.uisuc.tablasucursal.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def FiltrarProvincia(self, text):

        for row in range(self.uisuc.tablasucursal.rowCount()):
            item = self.uisuc.tablasucursal.item(row, 3)
            if text.lower() in item.text().lower():
                self.uisuc.tablasucursal.showRow(row)
            else:
                self.uisuc.tablasucursal.hideRow(row)

    def FiltrarNombre(self, text):
        # Filtrar los datos en el QTableWidget según el texto ingresado
        for row in range(self.uisuc.tablasucursal.rowCount()):
            item = self.uisuc.tablasucursal.item(row, 1)
            if text.lower() in item.text().lower():
                self.uisuc.tablasucursal.showRow(row)
            else:
                self.uisuc.tablasucursal.hideRow(row)