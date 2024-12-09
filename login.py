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


from uilogin import *
from reset import *
from main import *

conexion = pymysql.connect(host="Localhost",
                           user="root",
                           password="elian2003",
                           database="sispos")
cursor = conexion.cursor()



class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.log = Ui_Login()
        self.log.setupUi(self)

        # Instancias de Clases
        validadorint = QIntValidator()


        # Creacion de Instancias
        self.mensaje = QMessageBox()
        self.recuperacion = Reset(self)

        # Botones de control
        self.log.minimizar.clicked.connect(lambda: self.showMinimized())
        self.log.cerrar.clicked.connect(lambda: self.close())

        # Botones de Formulario
        self.log.login.clicked.connect(self.Login)
        self.log.clave.returnPressed.connect(self.Login)
        self.log.usuario.returnPressed.connect(self.VerificacionUsuario)
        self.log.visual.clicked.connect(self.Visual)
        self.log.btnrecuperar.clicked.connect(lambda: self.recuperacion.show())

        # Validaciones de Datos Enteros
        self.log.clave.setValidator(validadorint)



    def Login(self):
        try:
            idusuario = self.log.usuario.text()
            clave = self.log.clave.text()
            cursor.execute("SELECT * FROM tbusu08 WHERE iduse='"+idusuario+"' AND clave='"+clave+"'")
            data = cursor.fetchall()

            if data:
                for i in data:
                    usuario = i[0]
                    sucursal = i[2]

                    self.principal = MainApp(usuario, sucursal, self)
                    self.principal.show()

                self.close()
                self.log.usuario.clear()
                self.log.clave.clear()
                self.log.nombrecompleto.clear()

            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"Las credenciales no son correctas")
                self.mensaje.show()
                self.log.clave.setFocus()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def Visual(self):
        try:
            if self.log.visual.isChecked():
                icono = QIcon("iconos_blancos/eye.svg")
                self.log.clave.setEchoMode(QLineEdit.Normal)
            else:
                icono = QIcon("iconos_blancos/eye-off.svg")
                self.log.clave.setEchoMode(QLineEdit.Password)

            self.log.visual.setIcon(icono)

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def VerificacionUsuario(self):
        try:

            cursor.execute("SELECT nombre, apellido FROM tbusu08 WHERE iduse='"+self.log.usuario.text()+"'")
            data = cursor.fetchall()

            if data:
                for i in data:
                    nombre = i[0]
                    apellido = i[1]

                    self.log.nombrecompleto.setText(str(self.Concatenacion(nombre, apellido)))

            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"El nombre del usuario es incorrecto")
                self.mensaje.show()

                self.log.usuario.setFocus()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def Concatenacion(self, nom, ape):
        try:
            concatenacion = str(nom) + " " + str(ape)
            return concatenacion
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Login()
    window.setWindowFlag(Qt.FramelessWindowHint)
    window.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    window.show()
    sys.exit(app.exec_())
