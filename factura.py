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

from uifactura import *

conexion = pymysql.connect(host="Localhost",
                           user="root",
                           password="elian2003",
                           database="sispos")
cursor = conexion.cursor()

class Factura(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.fac = Ui_Factura()
        self.fac.setupUi(self)

        self.mensaje = QMessageBox()

    def CargarFacturas(self, nofac):
        try:
            sql = "CALL spfaccntcob(%s)"
            valores = (nofac)
            cursor.execute(sql, valores)
            data = cursor.fetchall()

            if data:
                self.fac.tablafac.setRowCount(len(data))

                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        self.fac.tablafac.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CargarRecepcion(self, norecep):
        try:
            sql = "CALL spfaccntpag(%s)"
            valores = (norecep)
            cursor.execute(sql, valores)
            data = cursor.fetchall()

            if data:
                self.fac.tablafac.setRowCount(len(data))

                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        self.fac.tablafac.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()