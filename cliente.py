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

from uicliente import *


conexion = pymysql.connect(host="Localhost",
                           user="root",
                           password="elian2003",
                           database="sispos")
cursor = conexion.cursor()

class VentanaCliente(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.uicli = Ui_Cliente()
        self.uicli.setupUi(self)

        self.mensaje = QMessageBox()

        self.uicli.busnombre.textChanged.connect(self.FiltrarNombre)
        self.uicli.busapellido.textChanged.connect(self.FiltrarApellido)


    def IdentificarCliente(self):
        try:
            row = self.uicli.tablacliente.currentRow()
            columnas = self.uicli.tablacliente.columnCount()
            datos = []
            for c in range(columnas):
                celda = self.uicli.tablacliente.item(row, c)
                if celda is not None:
                    datos.append(celda.text())

            return datos

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CargarClienteFactura(self):
        try:
            estatus = "A"
            cursor.execute("SELECT a.idcli, a.nombre, a.apellido, a.telefono, a.correo, a.direccion "
                           "FROM tbcli03 a, tbfacmae20 b "
                           "WHERE b.balance > 0 AND b.condicion > 0 AND b.estatus='"+estatus+"' AND a.idcli=b.idcli")
            data = cursor.fetchall()

            if data:
                self.uicli.tablacliente.setRowCount(len(data))

                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        self.uicli.tablacliente.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CargarCliente(self):
        try:
            cursor.execute("SELECT idcli, nombre, apellido, telefono, correo, direccion FROM tbcli03")
            data = cursor.fetchall()

            if data:
                self.uicli.tablacliente.setRowCount(len(data))

                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        self.uicli.tablacliente.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def FiltrarApellido(self, text):

        for row in range(self.uicli.tablacliente.rowCount()):
            item = self.uicli.tablacliente.item(row, 2)
            if text.lower() in item.text().lower():
                self.uicli.tablacliente.showRow(row)
            else:
                self.uicli.tablacliente.hideRow(row)

    def FiltrarNombre(self, text):
        # Filtrar los datos en el QTableWidget según el texto ingresado
        for row in range(self.uicli.tablacliente.rowCount()):
            item = self.uicli.tablacliente.item(row, 1)
            if text.lower() in item.text().lower():
                self.uicli.tablacliente.showRow(row)
            else:
                self.uicli.tablacliente.hideRow(row)






