# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uilogin.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(996, 660)
        Login.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(Login)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_principal = QtWidgets.QFrame(self.centralwidget)
        self.frame_principal.setStyleSheet("\n"
"*{\n"
"    font-family: century gothic;\n"
"    font-size: 24px;\n"
"    color: white;\n"
"    background-image: url(:/pantalla/pantalla/photo-1519681393784-d120267933ba.jpg);\n"
"    background-repeat: no-repeat;\n"
"    border-radius: 30px;\n"
"}")
        self.frame_principal.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_principal.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_principal.setObjectName("frame_principal")
        self.frame_2 = QtWidgets.QFrame(self.frame_principal)
        self.frame_2.setGeometry(QtCore.QRect(12, 12, 263, 79))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.frame_4)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout.addWidget(self.frame_4, 0, QtCore.Qt.AlignTop)
        self.frame_3 = QtWidgets.QFrame(self.frame_principal)
        self.frame_3.setGeometry(QtCore.QRect(160, 140, 691, 481))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setStyleSheet("*{\n"
"    background: transparent;\n"
"    background-color: rgba(0, 0, 0, 0.6);\n"
"    border-radius: 20px;\n"
"}\n"
"\n"
"QLabel{\n"
"    background: transparent;\n"
"}\n"
"\n"
"QLineEdit{\n"
"    background: transparent;\n"
"    border-radius: 15px;\n"
"    border-bottom: 2px solid rgb(100, 100, 100);\n"
"    color: rgb(150, 150, 150);\n"
"}\n"
"\n"
"QPushButton{\n"
"    border-radius: 15px;\n"
"    background: red;\n"
"}\n"
"\n"
"#login::hover{\n"
"    background-color: rgba(0, 0, 0, 0.7);\n"
"}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setGeometry(QtCore.QRect(180, 50, 331, 61))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.usuario = QtWidgets.QLineEdit(self.frame_3)
        self.usuario.setGeometry(QtCore.QRect(190, 150, 311, 41))
        self.usuario.setInputMask("")
        self.usuario.setText("")
        self.usuario.setMaxLength(30)
        self.usuario.setClearButtonEnabled(True)
        self.usuario.setObjectName("usuario")
        self.clave = QtWidgets.QLineEdit(self.frame_3)
        self.clave.setGeometry(QtCore.QRect(190, 300, 321, 32))
        self.clave.setEchoMode(QtWidgets.QLineEdit.Password)
        self.clave.setClearButtonEnabled(True)
        self.clave.setObjectName("clave")
        self.login = QtWidgets.QPushButton(self.frame_3)
        self.login.setGeometry(QtCore.QRect(160, 420, 371, 41))
        self.login.setObjectName("login")
        self.nombrecompleto = QtWidgets.QLineEdit(self.frame_3)
        self.nombrecompleto.setGeometry(QtCore.QRect(190, 220, 311, 41))
        self.nombrecompleto.setInputMask("")
        self.nombrecompleto.setText("")
        self.nombrecompleto.setMaxLength(1000)
        self.nombrecompleto.setReadOnly(True)
        self.nombrecompleto.setPlaceholderText("")
        self.nombrecompleto.setClearButtonEnabled(False)
        self.nombrecompleto.setObjectName("nombrecompleto")
        self.visual = QtWidgets.QPushButton(self.frame_3)
        self.visual.setGeometry(QtCore.QRect(520, 310, 41, 31))
        self.visual.setStyleSheet("*{\n"
"    background: transparent;\n"
"}")
        self.visual.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/blanco/iconos_blancos/eye-off.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.visual.setIcon(icon)
        self.visual.setIconSize(QtCore.QSize(25, 25))
        self.visual.setCheckable(True)
        self.visual.setChecked(False)
        self.visual.setObjectName("visual")
        self.btnrecuperar = QtWidgets.QPushButton(self.frame_3)
        self.btnrecuperar.setGeometry(QtCore.QRect(200, 360, 281, 41))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.btnrecuperar.setFont(font)
        self.btnrecuperar.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.btnrecuperar.setAutoFillBackground(False)
        self.btnrecuperar.setStyleSheet("*{\n"
"    background-color: none;\n"
"    font: 12pt \"MS Shell Dlg 2\";\n"
"    color: rgba(255, 255, 255, 0.7)\n"
"    \n"
"}\n"
"\n"
"*:hover{\n"
"    background-color: rgb(0, 0, 0);\n"
"}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/blanco/iconos_blancos/arrow-right-circle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnrecuperar.setIcon(icon1)
        self.btnrecuperar.setAutoRepeat(False)
        self.btnrecuperar.setObjectName("btnrecuperar")
        self.frame_5 = QtWidgets.QFrame(self.frame_principal)
        self.frame_5.setGeometry(QtCore.QRect(807, 30, 171, 61))
        self.frame_5.setStyleSheet("*{\n"
"    border: none;\n"
"    background: transparent;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"    background-color: rgba(0, 0, 0 , 0.7);\n"
"    border-radius: 10px;\n"
"    \n"
"}")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.minimizar = QtWidgets.QPushButton(self.frame_5)
        self.minimizar.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/blanco/iconos_blancos/minus.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.minimizar.setIcon(icon2)
        self.minimizar.setIconSize(QtCore.QSize(30, 30))
        self.minimizar.setObjectName("minimizar")
        self.horizontalLayout_2.addWidget(self.minimizar)
        self.cerrar = QtWidgets.QPushButton(self.frame_5)
        self.cerrar.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/blanco/iconos_blancos/x.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cerrar.setIcon(icon3)
        self.cerrar.setIconSize(QtCore.QSize(30, 30))
        self.cerrar.setObjectName("cerrar")
        self.horizontalLayout_2.addWidget(self.cerrar)
        self.inicio = QtWidgets.QPushButton(self.frame_principal)
        self.inicio.setGeometry(QtCore.QRect(450, 80, 111, 101))
        self.inicio.setStyleSheet("*{\n"
"    border-radius: 40px;\n"
"    background: red;\n"
"    icon: url(:/blanco/iconos_blancos/user.svg);\n"
"}\n"
"")
        self.inicio.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/negro/iconos_negros/users.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.inicio.setIcon(icon4)
        self.inicio.setIconSize(QtCore.QSize(50, 50))
        self.inicio.setObjectName("inicio")
        self.verticalLayout.addWidget(self.frame_principal)
        Login.setCentralWidget(self.centralwidget)

        self.retranslateUi(Login)
        self.usuario.returnPressed.connect(self.clave.setFocus) # type: ignore
        self.clave.returnPressed.connect(self.login.setFocus) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "MainWindow"))
        self.label.setText(_translate("Login", "<html><head/><body><p>My <span style=\" font-weight:600;\">SisPos </span></p></body></html>"))
        self.label_2.setText(_translate("Login", "Log <strong> In </strong>"))
        self.usuario.setPlaceholderText(_translate("Login", "User..."))
        self.clave.setPlaceholderText(_translate("Login", "Password..."))
        self.login.setText(_translate("Login", "Log In"))
        self.btnrecuperar.setText(_translate("Login", "Recuperar clave"))
import iconos
