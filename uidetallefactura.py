# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uidetallefactura.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Detalle(object):
    def setupUi(self, Detalle):
        Detalle.setObjectName("Detalle")
        Detalle.resize(1038, 429)
        Detalle.setMinimumSize(QtCore.QSize(1038, 429))
        Detalle.setMaximumSize(QtCore.QSize(1038, 429))
        self.centralwidget = QtWidgets.QWidget(Detalle)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabladet = QtWidgets.QTableWidget(self.centralwidget)
        self.tabladet.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabladet.sizePolicy().hasHeightForWidth())
        self.tabladet.setSizePolicy(sizePolicy)
        self.tabladet.setMinimumSize(QtCore.QSize(1025, 500))
        self.tabladet.setMaximumSize(QtCore.QSize(1025, 500))
        self.tabladet.setSizeIncrement(QtCore.QSize(1016, 407))
        self.tabladet.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tabladet.setObjectName("tabladet")
        self.tabladet.setColumnCount(6)
        self.tabladet.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tabladet.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tabladet.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tabladet.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tabladet.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tabladet.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tabladet.setHorizontalHeaderItem(5, item)
        self.tabladet.horizontalHeader().setDefaultSectionSize(169)
        self.tabladet.horizontalHeader().setMinimumSectionSize(120)
        self.verticalLayout.addWidget(self.tabladet)
        Detalle.setCentralWidget(self.centralwidget)

        self.retranslateUi(Detalle)
        QtCore.QMetaObject.connectSlotsByName(Detalle)

    def retranslateUi(self, Detalle):
        _translate = QtCore.QCoreApplication.translate
        Detalle.setWindowTitle(_translate("Detalle", "Detalles"))
        item = self.tabladet.horizontalHeaderItem(0)
        item.setText(_translate("Detalle", "Numero de factura"))
        item = self.tabladet.horizontalHeaderItem(1)
        item.setText(_translate("Detalle", "Nombre del producto"))
        item = self.tabladet.horizontalHeaderItem(2)
        item.setText(_translate("Detalle", "Cantidad de producto"))
        item = self.tabladet.horizontalHeaderItem(3)
        item.setText(_translate("Detalle", "Precio"))
        item = self.tabladet.horizontalHeaderItem(4)
        item.setText(_translate("Detalle", "ITEBIS"))
        item = self.tabladet.horizontalHeaderItem(5)
        item.setText(_translate("Detalle", "Importe Neto"))
