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

from uiusuario import *

conexion = pymysql.connect(host="Localhost",
                           user="root",
                           password="elian2003",
                           database="sispos")
cursor = conexion.cursor()


class VentanaUsuario(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.uiusu = Ui_Usuario()
        self.uiusu.setupUi(self)

        self.mensaje = QMessageBox()

        self.uiusu.busnombre.textChanged.connect(self.FiltrarNombre)
        self.uiusu.busapellido.textChanged.connect(self.FiltrarApellido)
        self.uiusu.busidusu.textChanged.connect(self.FiltrarIDUsuario)

    def IdentificarUsuario(self):
        try:
            row = self.uiusu.tablausuario.currentRow()
            columnas = self.uiusu.tablausuario.columnCount()
            datos = []
            for c in range(columnas):
                celda = self.uiusu.tablausuario.item(row, c)
                if celda is not None:
                    datos.append(celda.text())

            return datos

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CargarUsuario(self):
        try:
            cursor.execute("SELECT a.iduse, a.cedula, b.nombre, a.nombre, a.apellido, a.correo, a.telefono "
                           "FROM tbusu08 a, tbsuc26 b "
                           "WHERE a.idsuc=b.idsuc")
            data = cursor.fetchall()

            if data:
                self.uiusu.tablausuario.setRowCount(len(data))

                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        self.uiusu.tablausuario.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def FiltrarApellido(self, text):

        for row in range(self.uiusu.tablausuario.rowCount()):
            item = self.uiusu.tablausuario.item(row, 4)
            if text.lower() in item.text().lower():
                self.uiusu.tablausuario.showRow(row)
            else:
                self.uiusu.tablausuario.hideRow(row)

    def FiltrarIDUsuario(self, text):

        for row in range(self.uiusu.tablausuario.rowCount()):
            item = self.uiusu.tablausuario.item(row, 0)
            if text.lower() in item.text().lower():
                self.uiusu.tablausuario.showRow(row)
            else:
                self.uiusu.tablausuario.hideRow(row)

    def FiltrarNombre(self, text):
        # Filtrar los datos en el QTableWidget según el texto ingresado
        for row in range(self.uiusu.tablausuario.rowCount()):
            item = self.uiusu.tablausuario.item(row, 3)
            if text.lower() in item.text().lower():
                self.uiusu.tablausuario.showRow(row)
            else:
                self.uiusu.tablausuario.hideRow(row)