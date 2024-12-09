import decimal
import smtplib
import sys
import pymysql
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from uipassword import *

conexion = pymysql.connect(host="Localhost",
                           user="root",
                           password="elian2003",
                           database="sispos")
cursor = conexion.cursor()


class Reset(QtWidgets.QMainWindow):
    def __init__(self, instancia):
        super().__init__()
        self.reset = Ui_MainWindow()
        self.reset.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)

        validadorint = QIntValidator()
        self.mensaje = QMessageBox()

        self.reset.cerrar.clicked.connect(lambda: self.close())
        self.reset.minimizar.clicked.connect(lambda: self.showMinimized())

        self.instant = instancia

        self.reset.btnrecuperar.clicked.connect(self.ConfirmarCuenta)
        self.reset.lineusuario.returnPressed.connect(self.ConfirmarCuenta)

        self.reset.btnrestablecer.clicked.connect(self.Verificacion)
        self.reset.digito6.textChanged.connect(self.Verificacion)

        self.reset.btnfinalizar.clicked.connect(self.Restablecimiento)
        self.reset.nuevaclave2.returnPressed.connect(self.Restablecimiento)

        self.reset.digito1.setValidator(validadorint)
        self.reset.digito2.setValidator(validadorint)
        self.reset.digito3.setValidator(validadorint)
        self.reset.digito4.setValidator(validadorint)
        self.reset.digito5.setValidator(validadorint)
        self.reset.digito6.setValidator(validadorint)
        self.reset.nuevaclave1.setValidator(validadorint)
        self.reset.nuevaclave2.setValidator(validadorint)

    def Restablecimiento(self):

        if self.reset.nuevaclave1.text() == self.reset.nuevaclave2.text():
            try:

                sql = "UPDATE tbusu08 SET clave=%s WHERE iduse=%s"
                valor = (self.reset.nuevaclave1.text(), self.valores)

                cursor.execute(sql, valor)
                conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText("La clave se ha cambiado correctamente")
                self.mensaje.show()


                self.instant.show()
                self.close()

            except Exception as ex:
                self.mensaje.setIcon(QMessageBox.Critical)
                self.mensaje.setText(f"Ha ocurrido un error {ex}")
                self.mensaje.show()
        else:
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.setText("Las credenciales no coinciden")
            self.mensaje.show()


    def Verificacion(self):
        try:
            self.dig1 = self.reset.digito1.text()
            self.dig2 = self.reset.digito2.text()
            self.dig3 = self.reset.digito3.text()
            self.dig4 = self.reset.digito4.text()
            self.dig5 = self.reset.digito5.text()
            self.dig6 = self.reset.digito6.text()

            self.concatenacion = (str(self.dig1) + str(self.dig2) + str(self.dig3) +
                                  str(self.dig4) + str(self.dig5) + str(self.dig6))

            if int(self.concatenacion) == int(self.num):
                self.reset.paginas.setCurrentWidget(self.reset.pagina3)
            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("El codigo que se ha insertado es invalido")
                self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def EnviarCorreo(self, correo_destino):
        try:
            self.num = random.randint(100_000, 999_999)

            cursor.execute("SELECT correo, clave FROM tbemp32")
            info = cursor.fetchone()
            sender_email = info[0]
            sender_password = info[1]


            # Crear el objeto de mensaje MIME
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = correo_destino
            msg['Subject'] = "Recuperación de clave"  # Asunto del correo

            # Cuerpo del mensaje
            mensaje = f"Este es el código de combinación para recuperar la clave: {self.num}"
            msg.attach(MIMEText(mensaje, 'plain'))

            # Configurar la conexión con el servidor SMTP
            server = smtplib.SMTP("smtp.office365.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)

            # Enviar el correo electrónico
            server.sendmail(sender_email, correo_destino, msg.as_string())

            self.mensaje.setIcon(QMessageBox.Information)
            self.mensaje.setText("Se ha enviado una clave de confirmacion de 6 digitos a su correo")
            self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def ConfirmarCuenta(self):

        try:
            self.sql = "SELECT correo FROM tbusu08 WHERE iduse=%s"
            self.valores = (self.reset.lineusuario.text())

            cursor.execute(self.sql, self.valores)
            self.data = cursor.fetchall()

            if self.data:
                for i in self.data:
                    self.EnviarCorreo(i[0])
                    self.reset.paginas.setCurrentWidget(self.reset.pagina2)
            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("No existe un correo en este usuario o el usuario no existe")
                self.mensaje.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



