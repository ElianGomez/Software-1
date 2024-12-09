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

from uidetallefactura import *


conexion = pymysql.connect(host="Localhost",
                           user="root",
                           password="elian2003",
                           database="sispos")
cursor = conexion.cursor()

class DetalleFactura(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.det = Ui_Detalle()
        self.det.setupUi(self)

        self.mensaje = QMessageBox()


    def CargarOrdCompra(self, ord):
        try:
            sql = "SELECT b.numord, c.nompro, b.cantidad, b.precio, b.itebis " \
                  "FROM tbordcommae01 a, tbordcomdet02 b, tbpro10 c " \
                  "WHERE a.numord=%s AND a.numord=b.numord AND c.idpro=b.idpro"
            valores = (ord)
            cursor.execute(sql, valores)
            data = cursor.fetchall()

            if data:
                self.det.tabladet.setRowCount(len(data))

                for i, row in enumerate(data):
                    cantidad = float(row[2])
                    precio = float(row[3])
                    itebis = float(row[4])
                    total = (cantidad * precio) + itebis
                    for j, value in enumerate(row):
                        self.det.tabladet.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
                        self.det.tabladet.setItem(i, 5, QtWidgets.QTableWidgetItem(str(total)))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CargarRecepcion(self, norecep, idsup):
        try:
            sql = "SELECT b.norecep, c.nompro, b.cantidad, b.precio, b.itebis " \
                  "FROM tbrecmae18 a, tbrecdet19 b, tbpro10 c " \
                  "WHERE a.norecep=%s AND a.norecep=b.norecep AND a.idsup=%s AND c.idpro=b.idpro"
            valores = (norecep, idsup)
            cursor.execute(sql, valores)
            data = cursor.fetchall()

            if data:
                self.det.tabladet.setRowCount(len(data))

                for i, row in enumerate(data):
                    cantidad = float(row[2])
                    precio = float(row[3])
                    itebis = float(row[4])
                    total = (cantidad * precio) + itebis
                    for j, value in enumerate(row):
                        self.det.tabladet.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
                        self.det.tabladet.setItem(i, 5, QtWidgets.QTableWidgetItem(str(total)))


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CargarFacturas(self, nofac, idcli):
        try:
            sql = "SELECT b.nofac, c.nompro, b.cantipro, b.prepro, b.itebis " \
                  "FROM tbfacmae20 a, tbfacdet21 b, tbpro10 c " \
                  "WHERE a.nofac=%s AND a.nofac=b.nofac AND a.idcli=%s AND c.idpro=b.idpro"
            valores = (nofac, idcli)
            cursor.execute(sql, valores)
            data = cursor.fetchall()

            if data:
                self.det.tabladet.setRowCount(len(data))

                for i, row in enumerate(data):
                    cantidad = float(row[2])
                    precio = float(row[3])
                    itebis = float(row[4])
                    total = (cantidad * precio) + itebis
                    for j, value in enumerate(row):
                        self.det.tabladet.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
                        self.det.tabladet.setItem(i, 5, QtWidgets.QTableWidgetItem(str(total)))


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()




