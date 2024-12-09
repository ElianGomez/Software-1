import decimal
import os
import sys
import pymysql
from PyQt5.QtCore import Qt, QBuffer
from PyQt5.QtCore import QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QIntValidator, QImage, QPixmap, QIcon, QDoubleValidator, QKeySequence
from PyQt5.QtWidgets import QTableWidgetItem, QMenu, QAction, QFileDialog, QShortcut, QCheckBox, QDesktopWidget, QDoubleSpinBox
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate
from plyer import notification
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.mime.application import MIMEApplication
import numpy as np
from twilio.rest import Client

import datetime

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks
import mplcursors

from past.types import basestring

from suplidor import *
from cliente import *
from interface import *
from producto import *
from detalle import *
from factura import *
from banco import *
from usuario import *
from categoria import *
from provincia import *
from sucursal import *
from programa import *
from reporte import *
from server import FacturaProcessorApp
#from Predict import *
from keras.models import load_model


conexion = pymysql.connect(host="Localhost",
                           user="root",
                           password="elian2003",
                           database="sispos")
cursor = conexion.cursor()


class MainApp(QtWidgets.QMainWindow):
    def __init__(self, code, suc, instancia):
        super().__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)

        self.suc = suc
        self.codeusu = code
        self.instancia = instancia
        self.cliente = ""

        self.ui.salir.setText(self.codeusu)

        self.CargarImagen(False)

        self.account_sid = 'AC7a5644af32ee1be07e46a506fe684c3f'
        self.auth_token = '40124f254f2c1e06a8690d9954121f83'
        # Instancias de Clases
        validadorint = QIntValidator()
        validadorfloat = QDoubleValidator()

        self.mensaje = QMessageBox()

        self.reporte = ImprimirFac()

        #self.Prediccion = Recomendacion()

        self.cliente = VentanaCliente()
        self.cliente.uicli.tablacliente.itemDoubleClicked.connect(self.PresentarDatosTablaCliente)

        self.suplidor = VentanaSuplidor()
        self.suplidor.uisup.tablasup.itemDoubleClicked.connect(self.PresentarDatosTablaSuplidor)

        self.producto = VentanaProducto()
        self.producto.uipro.tablaproducto.itemDoubleClicked.connect(self.PresentarDatosTablaProducto)

        self.banco = VentanaBanco()
        self.banco.uiban.tablabanco.itemDoubleClicked.connect(self.PresentarDatosTablaBanco)

        self.usuario = VentanaUsuario()
        self.usuario.uiusu.tablausuario.itemDoubleClicked.connect(self.PresentarDatosTablaUsuario)

        self.categoria = VentanaCategoria()
        self.categoria.uicat.tablacategoria.itemDoubleClicked.connect(self.PresentarDatosTablaCategoria)

        self.provincia = VentanaProvincia()
        self.provincia.uiprov.tablaprovincia.itemDoubleClicked.connect(self.PresentarDatosTablaProvincias)

        self.sucursal = VentanaSucursal()
        self.sucursal.uisuc.tablasucursal.itemDoubleClicked.connect(self.PresentarDatosTablaSucursales)

        self.programa = VentanaPrograma()
        self.programa.uiprg.tablaprograma.itemDoubleClicked.connect(self.PresentarDatosTablaProgramas)

        self.detalle = DetalleFactura()

        self.factura = Factura()


        # Botones de control
        self.ui.cerrar_sesion.clicked.connect(self.CerrarSesion)
        self.ui.cerrar_sistema.clicked.connect(self.Salir)

        self.ui.cambia_imagen.clicked.connect(lambda: self.SeleccionarImagen("configuracion"))
        self.ui.salir.clicked.connect(self.Sesion)

        self.ui.slide.clicked.connect(self.Menu)
        self.ui.mant.clicked.connect(self.Mantenimiento)
        self.ui.mov.clicked.connect(self.Movimiento)
        self.ui.cons.clicked.connect(self.Consultas)


        # Boton de Inicio
        self.ui.inicio.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.fndini))


        # Botones de los mantenimientos
        self.ui.btnpro.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmntpro10))
        self.ui.btncli.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmntcli03))
        self.ui.btnimp.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmntimp07))
        self.ui.btnban.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmntban06))
        self.ui.btnusu.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmntusu08))
        self.ui.btnsup.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmntsup09))
        self.ui.btncat.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmntcat00))
        self.ui.btnprg.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmntprg23))
        self.ui.btnrol.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmntrol24))
        self.ui.btnprov.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmntprov25))
        self.ui.btnsuc.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmntsuc26))
        self.ui.btnbon.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmntbon28))
        self.ui.btnraz.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmntraz31))
        self.ui.btnsec.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmntncf05))
        self.ui.btnconv.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmntconv11))
        self.ui.btnemp.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmntemp32))


        # Botones de los movimientos
        self.ui.btnordcom.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmovordcomp0102))
        self.ui.btncob.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmovcob2930))
        self.ui.btnfac.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmovfac2021))
        self.ui.btnpag.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmovpag1617))
        self.ui.btnrec.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmovrec1819))
        self.ui.btndevcli.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmovdevcli1213))
        self.ui.btndevsup.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmovdevsup1415))
        self.ui.btnnotcli.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagnoticli))
        self.ui.btnvalsup.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagvalsup))
        self.ui.btnmejsup.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagmjsupli))


        # Botones de consultas
        self.ui.btnfaccli.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagconfaccli))
        self.ui.btnrecsup.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagconrecsup))
        self.ui.btnord.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagconordcom))
        self.ui.btnconpag.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagconpag))
        self.ui.btnconcob.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagconcob))
        self.ui.btnexissuc.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagconexissuc))
        self.ui.btnmejpre.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagconmjpre))
        self.ui.btnexisgen.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagconexisgen))
        self.ui.btnvent.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagconvent))
        self.ui.btncomp.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.pagconcomp))


        # Botones Formulario de suplidor
        self.ui.idsup09.returnPressed.connect(self.RellenarInfoSuplidor)
        self.ui.btnguardarsup09.clicked.connect(self.GuardarSuplidor)
        self.ui.btnnuevosup09.clicked.connect(self.NuevoSuplidor)
        self.ui.btneliminarsup09.clicked.connect(self.EliminarSuplidor)
        self.ui.btnbussup09.clicked.connect(self.VentanaBusSupMnt)

        self.GenerarIDSuplidor()


        # Botones Formulario de usuario
        self.ui.btnguardarusu08.clicked.connect(self.GuardarUsuario)
        self.ui.btnnuevousu08.clicked.connect(self.NuevoUsuario)
        self.ui.btneliminarusu08.clicked.connect(self.EliminarUsuario)
        self.ui.btnvisualusu08.clicked.connect(self.VisualUsuario)
        self.ui.idusu08.returnPressed.connect(self.RellenarInfoUsuario)
        self.ui.btnimgusu08.clicked.connect(lambda: self.SeleccionarImagen("usuario"))
        self.ui.btnbususu08.clicked.connect(self.VentanaBusUsuMnt)

        self.RellenarSucursalUsu()


        # Botones Formulario de banco
        self.ui.btnguardarban06.clicked.connect(self.GuardarBanco)
        self.ui.btneliminarban06.clicked.connect(self.EliminarBanco)
        self.ui.btnnuevoban06.clicked.connect(self.NuevoBanco)
        self.ui.btnbusban06.clicked.connect(self.VentanaBusBanMnt)

        self.ui.idban06.returnPressed.connect(self.RellenarInfoBanco)

        self.GenerarIDBanco()


        # Botones Formulario de cliente
        self.ui.btnguardarcli03.clicked.connect(self.GuardarCliente)
        self.ui.btneliminarcli03.clicked.connect(self.EliminarCliente)
        self.ui.btnnuevocli03.clicked.connect(self.NuevoCliente)
        self.ui.btnbuscli03.clicked.connect(self.VentanaBusCliMnt)

        self.ui.idcli03.returnPressed.connect(self.RellenarInfoCliente)

        self.GenerarIDCliente()


        # Botones Formulario de impuestos
        self.ui.btnguardarimp07.clicked.connect(self.GuardarImpuesto)
        self.ui.btneliminarimp07.clicked.connect(self.EliminarImpuesto)
        self.ui.btnnuevoimp07.clicked.connect(self.NuevoImpuesto)

        self.ui.idimp07.returnPressed.connect(self.RellenarImpuesto)
        self.ui.fecimp07.setText(str(self.GenerarFechaActual()))

        self.GenerarImpuesto()


        # Botones Formulario de categoria
        self.ui.btnguardarcat00.clicked.connect(self.GuardarCategoria)
        self.ui.btnnuevocat00.clicked.connect(self.NuevaCategoria)
        self.ui.btneliminarcat00.clicked.connect(self.EliminarCategoria)
        self.ui.idcat00.returnPressed.connect(self.RellenarCategoria)
        self.ui.btnbuscat00.clicked.connect(self.VentanaBusCatMnt)

        self.GenerarIDCategoria()

        # Botones Formulario de producto
        self.ui.btnguardarpro10.clicked.connect(self.GuardarProducto)
        self.ui.btneliminarpro10.clicked.connect(self.EliminarProducto)
        self.ui.btnnuevopro10.clicked.connect(self.NuevoProducto)
        self.ui.idpro10.returnPressed.connect(self.RellenarProducto)
        self.ui.btnbuspro10.clicked.connect(self.VentanaBusProMnt)

        self.GenerarIDProducto()
        self.LlenarComboCategoriaPro()


        # Botones Formulario Programa
        self.ui.btnguardarprg23.clicked.connect(self.GuardarPrograma)
        self.ui.btneliminarprg23.clicked.connect(self.EliminarPrograma)
        self.ui.btnnuevoprg23.clicked.connect(self.NuevoPrograma)
        self.ui.btnbusprg23.clicked.connect(self.VentanaBusPrgMnt)

        self.ui.idprg23.returnPressed.connect(self.RellenarPrograma)
        self.GenerarIDPrograma()


        # Botones Formulario Rol
        self.ui.btnguardarrol24.clicked.connect(self.GuardarRol)
        self.ui.btnmarcarrol24.clicked.connect(self.MarcarTodo)
        self.ui.btndesmarcarrol24.clicked.connect(self.DesmarcarTodo)
        self.ui.btnnuevorol24.clicked.connect(self.NuevoRol)

        self.ui.idusu24.returnPressed.connect(self.CargarDatos)
        self.ui.idusu24.returnPressed.connect(self.RellenarCampos)

        self.Verificacion()


        # Botones Formulario Provincia
        self.ui.btnnuevoprov25.clicked.connect(self.NuevoProv)
        self.ui.btneliminarprov25.clicked.connect(self.EliminarProv)
        self.ui.btnguardarprov25.clicked.connect(self.GuardarProv)
        self.ui.btnbusprov25.clicked.connect(self.VentanaBusProvMnt)

        self.ui.idprov25.returnPressed.connect(self.RellenarProv)

        self.GenerarIDProv()


        # Botones Formulario Sucursal
        self.ui.btnguardarsuc26.clicked.connect(self.GuardarSucursal)
        self.ui.btneliminarsuc26.clicked.connect(self.EliminarSucursal)
        self.ui.btnnuevosuc26.clicked.connect(self.NuevoSucursal)
        self.ui.btnbussuc26.clicked.connect(self.VentanaBusSucMnt)

        self.ui.idsuc26.returnPressed.connect(self.RellenarSucursal)

        self.GenerarIDSucursal()
        self.LlenarComboSucursal()


        # Botones Formulario Bono
        self.ui.btncargarbon28.clicked.connect(self.VerificarCliBono)
        self.ui.btnnuevobon28.clicked.connect(self.NuevoBono)
        self.ui.btnenviarbon28.clicked.connect(self.GuardarBono)
        self.ui.cancli28.editingFinished.connect(lambda: self.VerificacionCantiCli(self.ui.cancli28.text()))

        self.GenerarIDBono()


        # Botones Formulario Razones
        self.ui.btnguardarraz31.clicked.connect(self.GuardarRazon)
        self.ui.btnnuevoraz31.clicked.connect(self.NuevaRazon)
        self.ui.btneliminarraz31.clicked.connect(self.EliminarRazon)

        self.ui.idraz31.returnPressed.connect(self.RellenarRazon)

        self.GenerarIDRazon()


        # Botones Formulario SecNCF
        self.ui.btnnuevoncf05.clicked.connect(self.NuevoNCF)
        self.ui.btnguardarsncf05.clicked.connect(self.GuardarNCF)
        self.ui.btneliminarncf05.clicked.connect(self.EliminarNCF)

        self.ui.idncf05.returnPressed.connect(self.RellenarNCF)


        # Botones Formulario Factor Conversion
        self.ui.btnguardarconv11.clicked.connect(self.GuardarConversion)
        self.ui.btnnuevoconv11.clicked.connect(self.NuevoConversion)
        self.ui.btneliminarconv11.clicked.connect(self.EliminarConversion)
        self.ui.univenconv11.returnPressed.connect(self.RellenarConversion)
        self.ui.btnbuspro11.clicked.connect(self.VentanaProConv)


        # Botones Formulario Empresa
        self.ui.btnguardaremp32.clicked.connect(self.GuardarEmpresa)
        self.ui.btnnuevoemp32.clicked.connect(self.NuevaEmpresa)
        self.ui.btneliminaremp32.clicked.connect(self.EliminarEmpresa)
        self.ui.btnvisualemp32.clicked.connect(self.VisualEmpresa)
        self.ui.btnelegirlog32.clicked.connect(lambda: self.SeleccionarImagen("empresa"))

        self.ui.nomemp32.returnPressed.connect(self.RellenarEmpresa)


        # Botones Formulario de Factura
        self.ui.btnagregarfac20.clicked.connect(self.AgregarFacturaTabla)
        self.ui.btnnuevofac20.clicked.connect(self.NuevaFactura)
        self.ui.btneliminarprofac20.clicked.connect(self.EliminarFacturaTabla)
        self.ui.btnsalvarfac20.clicked.connect(self.SalvarFactura)
        self.ui.btnimprimirfac20.clicked.connect(self.ImprimirFactura)
        self.ui.btnbuscli20.clicked.connect(self.VentanaClienteFac)
        self.ui.btnbuspro20.clicked.connect(self.VentanaProductoFac)

        self.ui.idclifac20.returnPressed.connect(self.MostrarInfoCliente)
        self.ui.numprofac20.returnPressed.connect(self.MostrarInfoProducto)

        self.ui.fechfac20.setText(str(self.GenerarFechaActual()))

        self.ui.cantiprofac20.textChanged.connect(self.CalcularImporteFactura)
        self.ui.cantiprofac20.textChanged.connect(lambda: self.CalcularImpuesto(self.ui.iptfac20.text()))

        self.GenerarIDFactura()


        # Botones de Formulario de Pagos
        self.ui.btnsalvarpag16.clicked.connect(self.SalvarPago)
        self.ui.btnguardarcambpag16.clicked.connect(self.GuardarCambiosPago)
        self.ui.btnimprimirpag16.clicked.connect(self.ImprimirPago)
        self.ui.btnnuevopag16.clicked.connect(self.NuevoPago)
        self.ui.btnbuscli16.clicked.connect(self.VentanaClientePag)
        self.ui.tbpag16.doubleClicked.connect(self.RellenarFormPago)

        self.ui.forpag16.currentIndexChanged.connect(self.VerificacionDocu)
        self.ui.idclipag16.returnPressed.connect(self.MostrarInfoClientePago)
        self.ui.numpromo16.returnPressed.connect(self.VerificacionBono)

        self.ui.numpromo16.setDisabled(True)
        self.ui.monpromo16.setDisabled(True)


        self.LlenarComboBanco()
        self.GenerarIDPago()
        self.ui.fecpag16.setText(str(self.GenerarFechaActual()))


        # Botones de Formulario de Recepcion
        self.ui.btnsalvarrec18.clicked.connect(self.SalvarRecepcion)
        self.ui.btnimprimirrec18.clicked.connect(self.ImprimirRecepcion)
        self.ui.btnnuevorec18.clicked.connect(self.NuevoRecepcion)
        self.ui.btnsuprec18.clicked.connect(self.VentanaSuplidorRec)
        self.ui.tbrec18.doubleClicked.connect(self.EditarRecepcion)
        self.ui.cantirec18.textChanged.connect(self.ActualizarImporteRecepcion)
        self.ui.btnagregarrec18.clicked.connect(self.AgregarElementoRecepcion)
        self.ui.btnlimparrec18.clicked.connect(self.LimpiarCampos)

        self.ui.numord18.returnPressed.connect(self.CargarOrdRec)
        self.ui.idprorec18.returnPressed.connect(self.MostrarProductoRecepcion)

        self.ui.cantirec18.textChanged.connect(self.CalcularImporteRecepcion)
        self.ui.cantirec18.textChanged.connect(lambda: self.CalcularImpuestoRecepcion(self.ui.imprec18.text()))

        self.ui.fecrec18.setText(str(self.GenerarFechaActual()))
        self.GenerarIDRecepcion()


        # Botones Formulario Devolucion Cliente
        self.ui.tbclidev12.doubleClicked.connect(self.CargarDatosGridDevCli)
        self.ui.btnguardardevcli12.clicked.connect(self.GuardarDevolucionCliente)
        self.ui.btnnuevodevcli12.clicked.connect(self.NuevoDevolucionCliente)
        self.ui.btneliminardevcli12.clicked.connect(self.EliminarDevolucionCliente)
        self.ui.btnsalvardevcli12.clicked.connect(self.SalvarDevolucionCliente)
        self.ui.btndevtotal1213.clicked.connect(self.DevTotalCli)
        self.ui.btnimprimirdevcli12.clicked.connect(self.ImprimirDevoluionCliente)

        self.ui.numfacclidev12.returnPressed.connect(self.CargarDetallesFacturaDevCli)

        self.ui.fecdevcli12.setText(str(self.GenerarFechaActual()))

        self.GenerarIDDevolucionCliente()
        self.RellenarComboRazCli()


        # Botones Formulario Devolucion Suplidor
        self.ui.btnnuevosupdev15.clicked.connect(self.NuevoDevolucionSuplidor)
        self.ui.tbsupdev15.doubleClicked.connect(self.CargarDatosGridDevSup)
        self.ui.btndevtotalsupdev15.clicked.connect(self.DevTotalSup)
        self.ui.btnsalvarsupdev15.clicked.connect(self.SalvarDevolucionSuplidor)
        self.ui.btnimprimirsupdev15.clicked.connect(self.ImprimirDevolucionSuplidor)
        self.ui.btneliminardevsup15.clicked.connect(self.EliminarDevolucionSuplidor)
        self.ui.numrecdev15.returnPressed.connect(self.CargarDetallesRecepcionDevSup)
        self.ui.btneliminardevsup15.clicked.connect(self.CalcularImporteDevSup)
        self.ui.btnguardarsupdev15.clicked.connect(self.GuardarDevolucionSuplidor)

        self.RellenarComboRazSup()
        self.GenerarIDDevolucionSuplidor()
        self.ui.fecsupdev15.setText(str(self.GenerarFechaActual()))


        # Botones Formulario Cobros
        self.ui.btnguardarcob29.clicked.connect(self.SalvarCobro)
        self.ui.btnnuevocob29.clicked.connect(self.NuevoCobro)
        self.ui.btnimprimircob29.clicked.connect(self.ImprimirCobro)
        self.ui.btnbuscli16.clicked.connect(self.VentanaSuplidorCob)
        self.ui.btnguardarcamcob29.clicked.connect(self.GuardarCambiosCob)
        self.ui.tbcob29.doubleClicked.connect(self.RellenarFormCobro)

        self.ui.idsupcob29.returnPressed.connect(self.MostrarInfoSuplidorCob)
        self.ui.forpagcob29.currentIndexChanged.connect(self.VerificacionDocuCob)

        self.LlenarComboBancoCobro()
        self.GenerarIDCobro()
        self.ui.feccob29.setText(str(self.GenerarFechaActual()))


        # Botones Formulario de Orden De Compra
        self.ui.btnguardarord01.clicked.connect(self.AgregarOrd)
        self.ui.btneliminarord01.clicked.connect(self.EliminarOrd)
        self.ui.btnnuevoord01.clicked.connect(self.NuevoOrd)
        self.ui.btnsalvarord01.clicked.connect(self.SalvarOrd)
        self.ui.btnimprimirord01.clicked.connect(self.ImprimirOrd)
        self.ui.brnenviarord01.clicked.connect(self.EnviarOrd)

        self.ui.idsupord01.returnPressed.connect(self.MostrarInfoSuplidorOrd)
        self.ui.idproord01.returnPressed.connect(self.MostrarInfoProductoOrd)

        self.ui.cantiord01.textChanged.connect(self.CalcularImporteOrd)
        self.ui.cantiord01.textChanged.connect(lambda: self.CalcularImpuestoOrd(self.ui.impord01.text()))

        self.GenerarIDOrdenCompra()
        self.LlenarComboSucOrd()
        self.ui.fecord01.setText(str(self.GenerarFechaActual()))


        # Botones de Verificacion

        # Botones de Consulta Factura-Cliente
        self.ui.btncargarfaccli.clicked.connect(self.CargarFacturas)
        self.ui.btnnuevofaccli.clicked.connect(self.NuevoConcli)
        self.ui.tbconfaccli.doubleClicked.connect(self.DetalleConFacCli)


        # Botones de Consulta Factura-Suplidor
        self.ui.btncargarrecsup.clicked.connect(self.CargarRecSup)
        self.ui.btnnuevorecsup.clicked.connect(self.NuevoRecSup)
        self.ui.tbconrecsup.doubleClicked.connect(self.DetalleConRecsup)


        # Botones de Consulta Orden De Compra
        self.ui.btncargarord.clicked.connect(self.CargarConOrd)
        self.ui.btnnuevoord.clicked.connect(self.NuevoConOrd)
        self.ui.tbconordcom.doubleClicked.connect(self.DetalleConOrd)


        # Botones de Consulta Cuentas Por Cobrar
        self.ui.btnconpag.clicked.connect(self.CargarDatosConCntCob)
        self.ui.tbconpag.doubleClicked.connect(self.DetalleConCntCob)


        # Botones de Consulta Cuentas Por Pagar
        self.ui.btnconcob.clicked.connect(self.CargarDatosConCntPag)
        self.ui.tbconcob.doubleClicked.connect(self.DetalleConCntPag)


        # Botones de Consulta Existencia-Sucursal
        self.ui.btncargarpro.clicked.connect(self.CargarConExisSuc)
        self.ui.btnnuevaexiscons.clicked.connect(self.NuevoConExisSuc)

        self.RellenarCombConExisSuc()


        # Botones de Consulta Existencia General
        self.ui.btnexisgen.clicked.connect(self.CargarDatosExGeneral)


        # Botones de Consulta de Ventas
        self.ui.btncargarvent.clicked.connect(self.CargarDatosVent)
        self.ui.btnnuevacons.clicked.connect(self.NuevaConsVent)


        # Botones de Consulta de Compras
        self.ui.btncargarconscomp.clicked.connect(self.CargarDatosComp)
        self.ui.btnnuevaconscom.clicked.connect(self.NuevaConsComp)

        # Botones de Consulta De Mejor Precio
        self.ui.btnmejpre.clicked.connect(self.CargarDatosMejPre)
        self.ui.tbmejpre.doubleClicked.connect(self.OtrosSuplidoresMejPre)

        # Proceso Estrategico
        self.ui.btnenviar.clicked.connect(self.NotificarCliente)
        self.ui.btnrecargacliente.clicked.connect(self.LlenarTablaCliente)

        self.LlenarTablaCliente()


        # Validaciones de Entradas Enteras
        self.ui.idncf05.setValidator(validadorint)
        self.ui.secinincf05.setValidator(validadorint)
        self.ui.secfinncf05.setValidator(validadorint)
        self.ui.idproconv11.setValidator(validadorint)
        self.ui.numbon28.setValidator(validadorint)
        self.ui.idprg23.setValidator(validadorint)
        self.ui.idprov25.setValidator(validadorint)
        self.ui.idsuc26.setValidator(validadorint)
        self.ui.idsup09.setValidator(validadorint)
        self.ui.rncsup09.setValidator(validadorint)
        self.ui.clavusu08.setValidator(validadorint)
        self.ui.idpro10.setValidator(validadorint)
        self.ui.ultsuppro10.setValidator(validadorint)
        self.ui.idcat00.setValidator(validadorint)
        self.ui.idban06.setValidator(validadorint)
        self.ui.idcli03.setValidator(validadorint)
        self.ui.rnccli03.setValidator(validadorint)
        self.ui.idimp07.setValidator(validadorint)
        self.ui.idclifac20.setValidator(validadorint)
        self.ui.numprofac20.setValidator(validadorint)
        self.ui.idclipag16.setValidator(validadorint)
        self.ui.nodocupag16.setValidator(validadorint)
        self.ui.idsupord01.setValidator(validadorint)
        self.ui.idproord01.setValidator(validadorint)
        self.ui.obscob29.setValidator(validadorint)
        self.ui.idsupcob29.setValidator(validadorint)
        self.ui.nodocmob29.setValidator(validadorint)
        self.ui.norecibcob29.setValidator(validadorint)
        self.ui.noreccob29.setValidator(validadorint)
        self.ui.norec18.setValidator(validadorint)
        self.ui.idsuprec18.setValidator(validadorint)
        self.ui.idprorec18.setValidator(validadorint)
        self.ui.norecdevclimae12.setValidator(validadorint)
        self.ui.idclidev12.setValidator(validadorint)
        self.ui.numfacclidev12.setValidator(validadorint)
        self.ui.idproclidev12.setValidator(validadorint)
        self.ui.numrecdev15.setValidator(validadorint)
        self.ui.idsupdev15.setValidator(validadorint)
        self.ui.norecsupdev15.setValidator(validadorint)
        self.ui.idprosupdev15.setValidator(validadorint)
        self.ui.idraz31.setValidator(validadorint)
        self.ui.idclifaccli.setValidator(validadorint)
        self.ui.conidsup.setValidator(validadorint)


        # Validaciones de Entradas Flotantes
        self.ui.punretpro10.setValidator(validadorfloat)
        self.ui.exipro10.setValidator(validadorfloat)
        self.ui.prepro10.setValidator(validadorfloat)
        self.ui.cospro10.setValidator(validadorfloat)

        self.LlenarTablaGeneral()
        self.LlenarCombo()
        self.LLenarComboDeCalidad()
        self.ui.idsuplido.returnPressed.connect(self.RellenarComboProduto_Suplidor)
        self.ui.guardarvaloracion_2.clicked.connect(self.RecogerInformacion)

        #self.ui.btnanterior.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page))
        #self.ui.btnsiguieinte.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))

        self.ui.rdnivelgeneral.setChecked(True)

        self.ui.rdcriterios.toggled.connect(self.RDCriterios)
        self.ui.rdcalidad.toggled.connect(self.RDCalidad)
        self.ui.rdproducto.toggled.connect(self.RDProducto)
        self.ui.rdtiempo.toggled.connect(self.RDTiempo)

        self.ui.nompro.textChanged.connect(self.FiltrarProducto)

        self.ui.combocalidad.currentIndexChanged.connect(self.FiltrarCalidad)
        self.ui.categorias.currentIndexChanged.connect(self.FiltrarCriterio)
        self.ui.tiempcobro.currentIndexChanged.connect(self.FiltrarTiempoCobro)
        self.ui.codpro.returnPressed.connect(self.FiltrarProductoEspecifico)


    def setup_ui_connections(self):
        # Conectar el radiobutton de Filtros Combinados a la función de control
        self.ui.rdcombinado.toggled.connect(self.on_filtros_combinados_toggled)


    def on_filtros_combinados_toggled(self, checked):
        # Ejecutar la función solo si el radiobutton está seleccionado
        if checked:  # Si el radiobutton está activo
            self.FiltrarCombinado()


    def FiltrarCombinado(self):
        try:
            # Valores seleccionados en la interfaz
            self.ui.tbconsup.showColumn(1)
            self.ui.tbconsup.showColumn(2)

            nivel_general = self.ui.rdnivelgeneral.isChecked()
            id_criterio = self.ui.categorias.currentData() if self.ui.rdcriterios.isChecked() else None
            id_calidad = self.ui.combocalidad.currentData() if self.ui.rdcalidad.isChecked() else None
            id_producto = self.ui.codpro.text() if self.ui.rdproducto.isChecked() else None
            tiempo_cobro = self.ui.tiempcobro.text() if self.ui.rdtiempo.isChecked() else None

            # self.ui.codpro.setDisabled(True)
            # Base de la consulta
            sql = """
                    SELECT 
                        (SELECT nombre FROM tbsup09 WHERE idsup = te.idsup) AS NombreSuplidor,
                        (SELECT nompro FROM tbpro10 WHERE idpro = te.idpro) AS Articulo,
                        sc.caligeneral AS Puntaje,
                        (SELECT timecredito FROM tbsup09 WHERE idsup = te.idsup) AS Tiempo,
                        (SELECT nombre FROM tbcriteval33 WHERE idcrit = te.idcrit) AS Criterio,
                        (SELECT nombre 
                         FROM tbcalifi36 
                         WHERE idcalifi = (SELECT idcalifi 
                                           FROM tbevalcalifi37 
                                           WHERE sc.caligeneral BETWEEN valorminimo AND valormaximo)) AS Categoria
                    FROM 
                        tbevalsup34 te
                    LEFT JOIN 
                        tbsupcalifi39 sc ON te.idsup = sc.idsup
                    WHERE 
                        1 = 1
                    """

            # Agregar filtros dinámicamente
            if id_criterio:
                sql += f" AND te.idcrit = {id_criterio}"
            if id_calidad:
                sql += f"""
                        AND (SELECT idcalifi 
                             FROM tbevalcalifi37 
                             WHERE sc.caligeneral BETWEEN valorminimo AND valormaximo) = {id_calidad}
                        """
            if id_producto:
                sql += f" AND te.idpro = {id_producto}"
            if tiempo_cobro:
                sql += f" AND te.tiempo_cobro = {tiempo_cobro}"  # Cambiar por la columna real en la base de datos

            # Ordenar resultados
            sql += " GROUP BY te.idsup ORDER BY sc.caligeneral DESC;"

            self.EjecutarSQL(sql)

        except Exception as ex:
            pass
            # self.mensaje.setIcon(QMessageBox.Critical)
            # self.mensaje.setText(f"Ha ocurrido un error {ex}")
            # self.mensaje.show()


    def FiltrarTiempoCobro(self):
        try:

            if self.ui.tiempcobro.currentIndex() == 1:
                sql = """
                        SELECT 
            (SELECT nombre FROM tbsup09 WHERE idsup = te.idsup) AS NombreSuplidor,
            (SELECT nompro FROM tbpro10 WHERE idpro = te.idpro) AS Articulo,
            (SELECT precio FROM tbpro10 WHERE idpro = te.idpro) AS Precio,
            sc.caligeneral AS Puntaje, -- Puntaje desde tbsupcalifi39
            (SELECT nombre FROM tbcriteval33 WHERE idcrit = te.idcrit) AS Criterio,
            ts.timecredito AS TiempoCredito, -- Tiempo de crédito desde tbsup09
            (SELECT nombre 
             FROM tbcalifi36 
             WHERE idcalifi = (SELECT idcalifi 
                               FROM tbevalcalifi37 
                               WHERE sc.caligeneral BETWEEN valorminimo AND valormaximo)) AS Categoria
        FROM 
            tbevalsup34 te
        JOIN 
            tbsupcalifi39 sc ON te.idsup = sc.idsup -- Relación con puntaje
        JOIN 
            tbsup09 ts ON te.idsup = ts.idsup -- Relación con tiempo de crédito
        GROUP BY 
            te.idsup -- Agrupar por suplidor
        ORDER BY 
            ts.timecredito ASC; -- Ordenar por tiempo de crédito en forma ascendente
    
                        """
            elif self.ui.tiempcobro.currentIndex() == 2:
                sql = """SELECT 
            (SELECT nombre FROM tbsup09 WHERE idsup = te.idsup) AS NombreSuplidor,
            (SELECT nompro FROM tbpro10 WHERE idpro = te.idpro) AS Articulo,
            (SELECT precio FROM tbpro10 WHERE idpro = te.idpro) AS Precio,
            sc.caligeneral AS Puntaje, -- Puntaje desde tbsupcalifi39
            (SELECT nombre FROM tbcriteval33 WHERE idcrit = te.idcrit) AS Criterio,
            ts.timecredito AS TiempoCredito, -- Tiempo de crédito desde tbsup09
            (SELECT nombre 
             FROM tbcalifi36 
             WHERE idcalifi = (SELECT idcalifi 
                               FROM tbevalcalifi37 
                               WHERE sc.caligeneral BETWEEN valorminimo AND valormaximo)) AS Categoria
        FROM 
            tbevalsup34 te
        JOIN 
            tbsupcalifi39 sc ON te.idsup = sc.idsup -- Relación con puntaje
        JOIN 
            tbsup09 ts ON te.idsup = ts.idsup -- Relación con tiempo de crédito
        GROUP BY 
            te.idsup -- Agrupar por suplidor
        ORDER BY 
            ts.timecredito DESC; -- Ordenar por tiempo de crédito en forma ascendente
    
                                        """

            self.EjecutarSQL(sql)
        except Exception as ex:
            pass
            # self.mensaje.setIcon(QMessageBox.Critical)
            # self.mensaje.setText(f"Ha ocurrido un error {ex}")
            # self.mensaje.show()


    def FiltrarProducto(self, text):
        try:
            for row in range(self.ui.tbconsup.rowCount()):
                item = self.ui.tbconsup.item(row, 1)
                if text.lower() in item.text().lower():
                    self.ui.tbconsup.showRow(row)
                else:
                    self.ui.tbconsup.hideRow(row)
        except Exception as ex:
            pass
            # self.mensaje.setIcon(QMessageBox.Critical)
            # self.mensaje.setText(f"Ha ocurrido un error {ex}")
            # self.mensaje.show()


    def FiltrarProductoEspecifico(self):
        try:
            identificador = self.ui.codpro.text()
            # Ocultar la columna con índice 2
            self.ui.tbconsup.hideColumn(1)
            self.ui.tbconsup.hideColumn(2)

            sql = f"""
                            SELECT 
            (SELECT nombre FROM tbsup09 WHERE idsup = te.idsup) AS NombreSuplidor,
            (SELECT nompro FROM tbpro10 WHERE idpro = te.idpro) AS Articulo,
            (SELECT precio FROM tbpro10 WHERE idpro = te.idpro) AS Precio, -- Selección del precio del producto]
            (SELECT nombre FROM tbcriteval33 WHERE idcrit = te.idcrit) AS Criterio,
            sc.caligeneral AS Puntaje, -- Tomar el puntaje de tbsupcalifi39
            (SELECT timecredito FROM tbsup09 WHERE idsup = te.idsup) AS Tiempo,
            (SELECT nombre 
             FROM tbcalifi36 
             WHERE idcalifi = (SELECT idcalifi 
                               FROM tbevalcalifi37 
                               WHERE sc.caligeneral BETWEEN valorminimo AND valormaximo)) AS Categoria
        FROM 
            tbevalsup34 te
        JOIN 
            tbsupcalifi39 sc ON te.idsup = sc.idsup -- Relación con puntaje
        WHERE 
            te.idpro = {identificador} -- Filtrar por el producto seleccionado
        GROUP BY 
            te.idsup -- Agrupar por suplidor
        ORDER BY 
            sc.caligeneral DESC; -- Ordenar por el puntaje
    
                            """

            self.EjecutarSQL(sql)
        except Exception as ex:
            pass
            # self.mensaje.setIcon(QMessageBox.Critical)
            # self.mensaje.setText(f"Ha ocurrido un error {ex}")
            # self.mensaje.show()


    def FiltrarCalidad(self):
        try:

            identificador = self.ui.combocalidad.currentData()

            sql = f"""
                    SELECT 
            (SELECT nombre FROM tbsup09 WHERE idsup = te.idsup) AS NombreSuplidor,
            (SELECT nompro FROM tbpro10 WHERE idpro = te.idpro) AS Articulo,
            te.valor AS Precio,
            (SELECT nombre FROM tbcriteval33 WHERE idcrit = te.idcrit) AS Criterio,
            te.valor AS Puntaje,
            (SELECT timecredito FROM tbsup09 WHERE idsup = te.idsup) AS Tiempo,
            (SELECT nombre 
             FROM tbcalifi36 
             WHERE idcalifi = (SELECT idcalifi 
                               FROM tbevalcalifi37 
                               WHERE te.valor BETWEEN valorminimo AND valormaximo)) AS Categoria
        FROM 
            tbevalsup34 te
        WHERE 
            (SELECT idcalifi 
             FROM tbevalcalifi37 
             WHERE te.valor BETWEEN valorminimo AND valormaximo) = {identificador} -- Cambiar por el ID de categoría elegido
        ORDER BY 
            Puntaje DESC;
    
                    """

            self.EjecutarSQL(sql)
        except Exception as ex:
            pass
            # self.mensaje.setIcon(QMessageBox.Critical)
            # self.mensaje.setText(f"Ha ocurrido un error {ex}")
            # self.mensaje.show()


    def FiltrarCriterio(self):
        try:

            identificador = self.ui.categorias.currentData()

            sql = f"""
                                SELECT 
            (SELECT nombre FROM tbsup09 WHERE idsup = te.idsup) AS NombreSuplidor,
            (SELECT nompro FROM tbpro10 WHERE idpro = te.idpro) AS Articulo,
            te.valor AS Precio,
            (SELECT nombre FROM tbcriteval33 WHERE idcrit = te.idcrit) AS Criterio,
            te.valor AS Puntaje,
            (SELECT timecredito FROM tbsup09 WHERE idsup = te.idsup) AS Tiempo,
            (SELECT nombre 
             FROM tbcalifi36 
             WHERE idcalifi = (SELECT idcalifi 
                               FROM tbevalcalifi37 
                               WHERE te.valor BETWEEN valorminimo AND valormaximo)) AS Categoria
        FROM 
            tbevalsup34 te
        WHERE 
            te.idcrit = {identificador}
        ORDER BY 
            Puntaje DESC;
    
    
                                """

            self.EjecutarSQL(sql)
        except Exception as ex:
            pass
            # self.mensaje.setIcon(QMessageBox.Critical)
            # self.mensaje.setText(f"Ha ocurrido un error {ex}")
            # self.mensaje.show()


    def RDTiempo(self):
        try:
            self.ui.tbconsup.showColumn(1)
            self.ui.tbconsup.showColumn(2)

            self.ui.combocalidad.setDisabled(True)
            self.ui.categorias.setDisabled(True)
            self.ui.codpro.setDisabled(True)
            self.ui.tiempcobro.setEnabled(True)

            self.ui.combocalidad.setCurrentIndex(-1)
            self.ui.categorias.setCurrentIndex(-1)
            self.ui.codpro.clear()

        except Exception as ex:
            pass
            #self.mensaje.setIcon(QMessageBox.Critical)
            #self.mensaje.setText(f"Ha ocurrido un error {ex}")
            #self.mensaje.show()


    def RDProducto(self):
        try:
            self.ui.tbconsup.hideColumn(1)
            self.ui.tbconsup.hideColumn(2)

            self.ui.codpro.setText(str("0"))

            self.ui.combocalidad.setDisabled(True)
            self.ui.categorias.setDisabled(True)
            self.ui.tiempcobro.setDisabled(True)
            self.ui.codpro.setEnabled(True)

            self.ui.combocalidad.setCurrentIndex(-1)
            self.ui.categorias.setCurrentIndex(-1)
            self.ui.tiempcobro.setCurrentIndex(-1)
        except Exception as ex:
            pass
            #self.mensaje.setIcon(QMessageBox.Critical)
            #self.mensaje.setText(f"Ha ocurrido un error {ex}")
            #self.mensaje.show()


    def RDCriterios(self):
        try:
            self.ui.tbconsup.showColumn(1)
            self.ui.tbconsup.showColumn(2)

            self.ui.combocalidad.setDisabled(True)
            self.ui.codpro.setDisabled(True)
            self.ui.tiempcobro.setDisabled(True)
            self.ui.categorias.setEnabled(True)

            self.ui.combocalidad.setCurrentIndex(-1)
            self.ui.codpro.clear()
            self.ui.tiempcobro.setCurrentIndex(-1)
        except Exception as ex:
            pass
            #self.mensaje.setIcon(QMessageBox.Critical)
            #self.mensaje.setText(f"Ha ocurrido un error {ex}")
            #self.mensaje.show()


    def RDCalidad(self):
        try:
            self.ui.tbconsup.showColumn(1)
            self.ui.tbconsup.showColumn(2)

            self.ui.categorias.setDisabled(True)
            self.ui.codpro.setDisabled(True)
            self.ui.tiempcobro.setDisabled(True)
            self.ui.combocalidad.setEnabled(True)

            self.ui.categorias.setCurrentIndex(-1)
            self.ui.codpro.clear()
            self.ui.tiempcobro.setCurrentIndex(-1)
        except Exception as ex:
            pass
            #self.mensaje.setIcon(QMessageBox.Critical)
            #self.mensaje.setText(f"Ha ocurrido un error {ex}")
            #self.mensaje.show()


    def RecogerInformacion(self):
        try:
            fila = self.ui.tbvalsupli.rowCount()
            columna = self.ui.tbvalsupli.columnCount()
            datos = []
            suma = 0
            cont = 0

            idsuplidor = self.ui.idsuplido.text()
            idproducto = self.ui.proxsupli.currentText()[0]

            for f in range(fila):
                tupla = []
                for c in range(columna):
                    # Verificar si la celda contiene un widget (como QDoubleSpinBox)
                    widget = self.ui.tbvalsupli.cellWidget(f, c)
                    if widget and isinstance(widget, QDoubleSpinBox):
                        tupla.append(widget.value())  # Obtener el valor del QDoubleSpinBox
                    else:
                        celda = self.ui.tbvalsupli.item(f, c)
                        if celda is not None:
                            tupla.append(celda.text())  # Obtener el texto del QTableWidgetItem
                        else:
                            tupla.append("")  # Agregar un valor vacío si no hay datos
                datos.append(tupla)

            for i in datos:
                # Consulta SQL con ON DUPLICATE KEY UPDATE
                sql = """
                        INSERT INTO tbevalsup34 (idsup, idpro, idcrit, valor, fecha)
                        VALUES (%s, %s, %s, %s, NOW())
                        ON DUPLICATE KEY UPDATE
                            valor = VALUES(valor),
                            fecha = NOW()
                        """
                # Formatear y redondear el valor a 2 decimales
                valorformateado = f"{i[2]:.2f}"
                valores = (idsuplidor, idproducto, i[0], valorformateado)

                # Ejecutar la consulta
                cursor.execute(sql, valores)
                cont += 1
                suma += float(i[2])

            equivalencia = (float(suma) / float(cont))
            equivalencia_formateada = f"{equivalencia:.2f}"

            sql = "INSERT INTO tbsupcalifi39(idsup, caligeneral) VALUES(%s, %s) ON DUPLICATE KEY UPDATE caligeneral = VALUES(caligeneral)"
            valores = (idsuplidor, equivalencia_formateada)
            cursor.execute(sql, valores)


        except Exception as ex:
            pass
            #self.mensaje.setIcon(QMessageBox.Critical)
            #self.mensaje.setText(f"Ha ocurrido un error {ex}")
            #self.mensaje.show()


    def CargarInformacionSuplidor(self, codsup):
        try:
            sql = "SELECT nombre, telefono, correo, web, telefonocontact FROM tbsup09 WHERE idsup='" + codsup + "'"
            cursor.execute(sql)

            data = cursor.fetchall()

            if data:
                for i in data:
                    self.ui.nombresupli.setText(str(i[0]))
                    self.ui.telsupli.setText(str(i[1]))
                    self.ui.corrsupli.setText(str(i[2]))
                    self.ui.websupli.setText(str(i[3]))
                    self.ui.telcontactsup.setText(str(i[4]))

        except Exception as ex:
            pass
            # self.mensaje.setIcon(QMessageBox.Critical)
            # self.mensaje.setText(f"Ha ocurrido un error {ex}")
            # self.mensaje.show()


    def RellenarComboProduto_Suplidor(self):
        try:

            sql = """
                    SELECT b.idpro, b.nompro
                FROM tbsup09 a, tbpro10 b, tbproxsup38 c
                WHERE a.idsup=c.idsup AND b.idpro=c.idpro AND a.idsup=%s;
    
                    """
            valor = (self.ui.idsuplido.text())
            self.CargarInformacionSuplidor(valor)
            cursor.execute(sql, valor)
            data = cursor.fetchall()

            if data:
                for i in data:
                    formato = f"{i[0]} - {i[1]}"
                    self.ui.proxsupli.addItem(str(formato))

                self.RellenarTabla()

        except Exception as ex:
            pass
            # self.mensaje.setIcon(QMessageBox.Critical)
            # self.mensaje.setText(f"Ha ocurrido un error {ex}")
            # self.mensaje.show()


    def update_calificacion(self, row, value):
        """Actualiza la calificación según el valor ingresado."""
        if value >= 4.5:
            calificacion = "Excelente"
        elif value >= 4.0:
            calificacion = "Muy Bueno"
        elif value >= 3.0:
            calificacion = "Bueno"
        elif value >= 2.0:
            calificacion = "Regular"
        elif value >= 1.0:
            calificacion = "Malo"
        else:
            calificacion = "Muy Malo"

        self.ui.tbvalsupli.setItem(row, 3, QTableWidgetItem(calificacion))


    def RellenarTabla(self):
        try:
            # Consulta para obtener los criterios desde la base de datos
            cursor.execute("SELECT idcrit, nombre FROM tbcriteval33")
            criterios = cursor.fetchall()

            # Configurar el número de filas según los criterios
            self.ui.tbvalsupli.setRowCount(len(criterios))

            for row, (idcrit, nombre) in enumerate(criterios):
                # Configurar la columna "ID Criterio"
                self.ui.tbvalsupli.setItem(row, 0, QTableWidgetItem(str(idcrit)))

                # Configurar la columna "Criterio"
                self.ui.tbvalsupli.setItem(row, 1, QTableWidgetItem(nombre))

                # Configurar la columna "Calificación (0-5)" con QDoubleSpinBox
                spin_box = QDoubleSpinBox()
                spin_box.setRange(0, 5)
                spin_box.setSingleStep(0.1)
                spin_box.valueChanged.connect(
                    lambda value, r=row: self.update_calificacion(r, value)
                )
                self.ui.tbvalsupli.setCellWidget(row, 2, spin_box)

                # Configurar la columna "Calificación" (texto inicial como "Sin Calificación")
                self.ui.tbvalsupli.setItem(row, 3, QTableWidgetItem("Sin Calificación"))

                # Configurar una nueva columna adicional (placeholder o lógica específica)

        except Exception as ex:
            pass
            # self.mensaje.setIcon(QMessageBox.Critical)
            # self.mensaje.setText(f"Ha ocurrido un error {ex}")
            # self.mensaje.show()


    def EjecutarSQL(self, sql):
        try:
            cursor.execute(sql)
            data = cursor.fetchall()

            if data:
                self.ui.tbconsup.setRowCount(len(data))
                for i, row in enumerate(data):
                    for j, values in enumerate(row):
                        self.ui.tbconsup.setItem(i, j, QTableWidgetItem(str(values)))
            else:
                self.ui.tbconsup.setRowCount(0)
                self.ui.tbconsup.clearContents()

        except Exception as ex:
            pass
            # self.mensaje.setIcon(QMessageBox.Critical)
            # self.mensaje.setText(f"Ha ocurrido un error {ex}")
            # self.mensaje.show()


    def LlenarTablaGeneral(self):
        try:
            sql = """
                    SELECT 
            (SELECT nombre FROM tbsup09 WHERE idsup = te.idsup) AS NombreSuplidor,
            (SELECT nompro FROM tbpro10 WHERE idpro = te.idpro) AS Articulo,
            te.valor AS Precio,
            (SELECT nombre FROM tbcriteval33 WHERE idcrit = te.idcrit) AS Criterio,
            te.valor AS Puntaje,
            (SELECT timecredito FROM tbsup09 WHERE idsup = te.idsup) AS Tiempo,
            (SELECT nombre 
             FROM tbcalifi36 
             WHERE idcalifi = (SELECT idcalifi 
                               FROM tbevalcalifi37 
                               WHERE te.valor BETWEEN valorminimo AND valormaximo)) AS Categoria
        FROM 
            tbevalsup34 te
        ORDER BY 
            Puntaje DESC;
                    """
            self.EjecutarSQL(sql)

        except Exception as ex:
            pass
            # self.mensaje.setIcon(QMessageBox.Critical)
            # self.mensaje.setText(f"Ha ocurrido un error {ex}")
            # self.mensaje.show()


    def LLenarComboDeCalidad(self):
        try:
            sql = "SELECT idcalifi, nombre FROM tbcalifi36"
            cursor.execute(sql)
            data = cursor.fetchall()
            if data:
                for i in data:
                    formato = f"{i[1]}"
                    self.ui.combocalidad.addItem(str(formato), i[0])
        except Exception as ex:
            pass
            # self.mensaje.setIcon(QMessageBox.Critical)
            # self.mensaje.setText(f"Ha ocurrido un error {ex}")
            # self.mensaje.show()


    def LlenarCombo(self):
        try:
            sql = "SELECT idcrit, nombre FROM tbcriteval33"
            cursor.execute(sql)
            data = cursor.fetchall()
            if data:
                for i in data:
                    formato = f"{i[1]}"
                    self.ui.categorias.addItem(str(formato), i[0])
        except Exception as ex:
            pass
            # self.mensaje.setIcon(QMessageBox.Critical)
            # self.mensaje.setText(f"Ha ocurrido un error {ex}")
            # self.mensaje.show()
########################################################################################################################
###################################### Proceso estrategico #############################################################
########################################################################################################################


    def EnviarEmail(self, cliente_email, servidor_url, idcliente):
        # Obtener los productos desde la base de datos
        productos = self.ObtenerProductos(idcliente)

        # Generar la tabla HTML con los productos
        tabla_html = self.GenerarTablaHTML(productos, idcliente, self.suc)

        # Configurar el mensaje
        asunto = "Ranking Productos Mas Comprados"
        remitente = "elian3734@gmail.com"
        destinatario = cliente_email

        sql = "SELECT CONCAT(nombre, ' ', apellido) FROM tbcli03 WHERE idcli=%s"
        valor = idcliente
        cursor.execute(sql, valor)
        data = cursor.fetchone()

        # Crear el contenido HTML del correo
        mensaje_html = f"""
        <html>
            <body>
                <h3>Productos disponibles en nuestra tienda</h3>
                <p> {idcliente}-{data[0]}
                <p>A continuación, te mostramos los productos que puedes adquirir:</p>
                {tabla_html}
                <p>¿Te gustaría comprar algún producto? <a href="{servidor_url}/respuesta?cliente={cliente_email}">Haz clic aquí</a>.</p>
            </body>
        </html>
        """

        # Crear el mensaje
        mensaje = MIMEMultipart("alternative")
        mensaje["Subject"] = asunto
        mensaje["From"] = remitente
        mensaje["To"] = destinatario

        # Adjuntar el contenido HTML
        parte_html = MIMEText(mensaje_html, "html")
        mensaje.attach(parte_html)


        # Configurar y enviar el correo
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login("elian3734@gmail.com", "symn baba mjbf fddz")  # Reemplaza con tu contraseña de aplicación
            servidor.sendmail(remitente, destinatario, mensaje.as_string())

        #Servidor = FacturaProcessorApp()


    def GenerarTablaHTML(self, productos, idcliente, idsucursal):
        tabla = """
        <form action="http://localhost:5000/respuesta" method="post" onsubmit="return validarFormulario()">
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <thead>
                    <tr style="background-color: #f2f2f2;">
                        <th>Seleccionar</th>
                        <th>ID Producto</th>
                        <th>Descripción</th>
                        <th>Cantidad</th>
                        <th>Precio Unitario</th>
                    </tr>
                </thead>
                <tbody>
        """
        for producto in productos:
            idpro, descripcion, precio_unitario = producto
            cantidad = 1  # Valor por defecto
            tabla += f"""
            <tr>
                <td><input type="checkbox" name="productos[]" value="{idpro}"></td>
                <td>{idpro}<input type="hidden" name="id_{idpro}" value="{idpro}"></td>
                <td>{descripcion}<input type="hidden" name="descripcion_{idpro}" value="{descripcion}"></td>
                <td><input type="number" name="cantidad_{idpro}" value="{cantidad}" min="1" style="width: 50px;" required></td>
                <td>${precio_unitario:.2f}<input type="hidden" name="precio_{idpro}" value="{precio_unitario:.2f}"></td>
                <!-- Columna oculta para ID Cliente -->
                <td style="display: none;"><input type="hidden" name="id_cliente" value="{idcliente}"></td>
                <!-- Columna oculta para ID Sucursal -->
                <td style="display: none;"><input type="hidden" name="id_sucursal" value="{idsucursal}"></td>
            </tr>
            """
        tabla += """
                </tbody>
            </table>
            <br><br>
            <button type="submit">Realizar compra</button>
            <h3>Si no necesita nada de lo presentado en este correo, haga caso omiso al mismo</h3>
        </form>
        """
        return tabla

    def ObtenerProductos(self, idcliente):
        sql = "CALL spprocestrat(%s)"
        valor = idcliente
        cursor.execute(sql, valor)
        productos = cursor.fetchall()
        return productos

    def NotificarCliente(self):
        try:

            filas = self.ui.tbnoticli.rowCount()

            for f in range(filas):
                correo = self.ui.tbnoticli.item(f, 3)
                idcliente = self.ui.tbnoticli.item(f, 0)

                if correo is not None:
                    correotxt = correo.text()
                    idcli = int(idcliente.text())

                    self.EnviarEmail(correotxt, "http://localhost:5000", idcli)



        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def LlenarTablaCliente(self):
        try:
            cursor.execute("SELECT * FROM vwprocestrat")
            data = cursor.fetchall()

            if data:
                self.ui.tbnoticli.setRowCount(len(data))

                for i, row in enumerate(data):
                    for j, values in enumerate(row):
                        self.ui.tbnoticli.setItem(i, j, QTableWidgetItem(str(values)))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

########################################################################################################################
################################## Verificacion de Reorden #############################################################
########################################################################################################################


    def Notificacion(self, idpro, nombre, idsup, suplidor, contacto, cantidad):
        try:

            titulo = "Compra de productos"
            mensaje = f"Queda poca cantidad({cantidad}, del producto {idpro}({nombre}) El mejor suplidor es el {idsup}({suplidor})." \
                      f"Este es el numero de contacto del suplidor {contacto}"
            duracion = 10

            icon_path = os.path.join(os.getcwd(), 'bell.ico')
            notification.notify(
                title=titulo,
                message=mensaje,
                timeout=duracion,
                app_icon=icon_path
            )


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def VerificacionReorden(self):
        try:

            global idpro, nombre, idsup, suplidor, numero, cantidad

            sql = "SELECT a.idpro, a.nompro, d.idsup, d.nombre, d.telefonocontact, b.cantidad " \
                  "FROM tbpro10 a, tbproxsuc27 b, tbsuc26 c, tbsup09 d " \
                  "WHERE b.cantidad<=a.punret AND a.idpro=b.idpro AND c.idsuc=b.idsuc AND b.idsuc=%s;"
            valor = (self.suc)
            cursor.execute(sql, valor)
            data = cursor.fetchall()

            if data:
                for i in data:
                    idpro = str(i[0])
                    nombre = str(i[1])
                    idsup = str(i[2])
                    suplidor = str(i[3])
                    numero = str(i[4])
                    cantidad = str(i[5])

                    self.Notificacion(idpro, nombre, idsup, suplidor, numero, cantidad)
            else:
                pass
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

########################################################################################################################
######################################## Consulta de Mejor precio ######################################################
########################################################################################################################

    def CargarDatosMejPre(self):
        try:
            cursor.execute("SELECT * FROM vwmejpre")
            data = cursor.fetchall()

            if data:
                self.ui.tbmejpre.setRowCount(len(data))

                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        self.ui.tbmejpre.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"No hay registros hasta la actualidad")
                self.mensaje.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def OtrosSuplidoresMejPre(self):
        pass



########################################################################################################################
######################################## Consulta de Compras ###########################################################
########################################################################################################################

    def CargarDatosComp(self):

        try:
            ini = self.ui.fecdesdecomp.text()
            fin = self.ui.fechastacomp.text()

            if not ini or not fin:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Los campos son obligatorios")
                self.mensaje.show()
            else:
                sql = "CALL spcomp(%s, %s)"
                valores = (ini, fin)
                cursor.execute(sql, valores)
                data = cursor.fetchall()

                if data:
                    self.ui.tbcomp.setRowCount(len(data))

                    for i, row in enumerate(data):
                        for j, value in enumerate(row):
                            self.ui.tbcomp.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
                else:
                    self.mensaje.setIcon(QMessageBox.Warning)
                    self.mensaje.setText(f"No hay ventas dentro de estas dos fechas")
                    self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def NuevaConsComp(self):
        try:
            fecha = QDate.currentDate()

            self.ui.fecdesdecomp.setDate(fecha)
            self.ui.fechastacomp.setDate(fecha)

            self.ui.tbcomp.setRowCount(0)
            self.ui.tbcomp.clearContents()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

########################################################################################################################
######################################## Consulta de Ventas ############################################################
########################################################################################################################

    def CargarDatosVent(self):
        try:
            ini = self.ui.fecdesdevent.text()
            fin = self.ui.fechastavent.text()


            if not ini or not fin:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"Los campos son obligatorios")
                self.mensaje.show()
            else:
                sql = "CALL spvent(%s, %s)"
                valores = (ini, fin)
                cursor.execute(sql, valores)
                data = cursor.fetchall()

                if data:
                    self.ui.tbvent.setRowCount(len(data))

                    for i, row in enumerate(data):
                        for j, value in enumerate(row):
                            self.ui.tbvent.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
                else:
                    self.mensaje.setIcon(QMessageBox.Warning)
                    self.mensaje.setText(f"No hay ventas dentro de estas dos fechas")
                    self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevaConsVent(self):
        try:
            fecha = QDate.currentDate()
            self.ui.fecdesdevent.setDate(fecha)
            self.ui.fechastavent.setDate(fecha)

            self.ui.tbvent.clearContents()
            self.ui.tbvent.setRowCount(0)

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

########################################################################################################################
##################################### Consulta Existencia General ######################################################
########################################################################################################################

    def CargarDatosExGeneral(self):
        try:
            cursor.execute("SELECT * FROM vwexgen")
            data = cursor.fetchall()

            if data:
                self.ui.tbexisgen.setRowCount(len(data))

                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        self.ui.tbexisgen.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

########################################################################################################################
##################################### Consulta Existencia-Sucursal  ####################################################
########################################################################################################################

    def CargarConExisSuc(self):
        try:
            idsuc = self.ui.idsuccon.currentText()[0] + "" + \
                    self.ui.idsuccon.currentText()[1] + "" + \
                    self.ui.idsuccon.currentText()[2]

            sql = "CALL spexsuc(%s)"
            valores = (idsuc)
            cursor.execute(sql, valores)
            data = cursor.fetchall()

            if data:
                self.ui.tbexissuc.setRowCount(len(data))

                for i, row in enumerate(data):
                    self.ui.nomsuccons.setText(str(row[6]))
                    self.ui.provsuccons.setText(str(row[7]))
                    for j, value in enumerate(row):
                        self.ui.tbexissuc.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"No hay productos en esta sucursal")
                self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevoConExisSuc(self):
        try:
            self.ui.idsuccon.setCurrentIndex(0)

            self.ui.tbexissuc.clearContents()
            self.ui.tbexissuc.setRowCount(0)

            self.ui.nomsuccons.clear()
            self.ui.provsuccons.clear()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def RellenarCombConExisSuc(self):
        try:
            cursor.execute("SELECT idsuc, nombre FROM tbsuc26")
            data = cursor.fetchall()

            if data:
                for i in data:
                    formato = f"{i[0]}   - {i[1]}"

                    self.ui.idsuccon.addItem(formato)

            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("No hay ninguna sucursal")
                self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


########################################################################################################################
##################################### Consulta Cuentas Por Pagar #######################################################
########################################################################################################################

    def DetalleConCntPag(self):
        try:
            seleccion = self.ui.tbconcob.currentRow()  # Obtiene el índice de la fila seleccionada

            if seleccion >= 0:
                idsup = self.ui.tbconcob.item(seleccion, 0).text()

                self.factura.CargarRecepcion(idsup)
                self.factura.show()

            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"No hay ninguna fila seleccionada")
                self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CargarDatosConCntPag(self):
        try:
            cursor.execute("SELECT * "
                           "FROM vwcntpag")
            data = cursor.fetchall()

            if data:
                self.ui.tbconcob.setRowCount(len(data))

                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        self.ui.tbconcob.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

########################################################################################################################
##################################### Consulta Cuentas Por Cobrar ######################################################
########################################################################################################################

    def DetalleConCntCob(self):
        try:
            seleccion = self.ui.tbconpag.currentRow()  # Obtiene el índice de la fila seleccionada

            if seleccion >= 0:
                idcli = self.ui.tbconpag.item(seleccion, 0).text()
                self.factura.CargarFacturas(idcli)
                self.factura.show()

            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"No hay ninguna fila seleccionada")
                self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CargarDatosConCntCob(self):
        try:
            cursor.execute("SELECT * "
                           "FROM vwcntcob")
            data = cursor.fetchall()

            if data:
                self.ui.tbconpag.setRowCount(len(data))

                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        self.ui.tbconpag.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

########################################################################################################################
##################################### Consulta Orden De Compra #########################################################
########################################################################################################################

    def DetalleConOrd(self):
        try:
            seleccion = self.ui.tbconordcom.currentRow()  # Obtiene el índice de la fila seleccionada

            if seleccion >= 0:
                numord = self.ui.tbconordcom.item(seleccion, 0).text()

                self.detalle.CargarOrdCompra(numord)
                self.detalle.show()

            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"No hay ninguna fila seleccionada")
                self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CargarDatosConOrd(self, tupla):
        try:
            if tupla:
                self.ui.tbconordcom.setRowCount(len(tupla))

                for i, row in enumerate(tupla):
                    for j, value in enumerate(row):
                        self.ui.tbconordcom.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CargarConOrd(self):
        try:
            desde = self.ui.conorddesde.text()
            hasta = self.ui.conordhasta.text()

            if not desde or not hasta:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Todos los campos son obligatorios")
                self.mensaje.show()
            else:
                sql = "CALL spordcom(%s, %s)"
                valores = (desde, hasta)
                cursor.execute(sql, valores)
                data = cursor.fetchall()

                if data:
                    self.CargarDatosConOrd(data)
                else:
                    self.mensaje.setIcon(QMessageBox.Warning)
                    self.mensaje.setText("No hay ordenes de compra entre estas dos fechas")
                    self.mensaje.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevoConOrd(self):
        try:
            fecha = QDate.currentDate()

            self.ui.conorddesde.setDate(fecha)
            self.ui.conordhasta.setDate(fecha)

            self.ui.tbconordcom.setRowCount(0)
            self.ui.tbconordcom.clearContents()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


########################################################################################################################
##################################### Consulta Recepcion-Suplidor ######################################################
########################################################################################################################

    def DetalleConRecsup(self):
        try:

            seleccion = self.ui.tbconrecsup.currentRow()  # Obtiene el índice de la fila seleccionada
            if seleccion >= 0:
                idsup = self.ui.conidsup.text()
                norecep = self.ui.tbconrecsup.item(seleccion, 0).text()

                self.detalle.CargarRecepcion(norecep, idsup)
                self.detalle.show()

            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"No hay ninguna fila seleccionada")
                self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CargarDatosRecSup(self, tupla):
        try:
            if tupla:
                self.ui.tbconrecsup.setRowCount(len(tupla))

                for i, row in enumerate(tupla):
                    for j, value in enumerate(row):
                        self.ui.tbconrecsup.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CargarRecSup(self):
        try:
            idsuplidor = self.ui.conidsup.text()
            desde = self.ui.recdesde.text()
            hasta = self.ui.rechasta.text()

            if not idsuplidor or not desde or not hasta:
                self.mensaje.setIcon(QMessageBox.Critical)
                self.mensaje.setText("Todos los campos son obligatorios")
                self.mensaje.show()
            else:
                sql = "CALL sprecsup(%s, %s, %s)"
                valores = (idsuplidor, desde, hasta)
                cursor.execute(sql, valores)
                data = cursor.fetchall()

                if data:
                    self.CargarDatosRecSup(data)
                else:
                    self.mensaje.setIcon(QMessageBox.Warning)
                    self.mensaje.setText(f"Este suplidor no tiene recepcion entre estas fechas")
                    self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevoRecSup(self):
        try:
            fecha = QDate.currentDate()

            self.ui.conidsup.clear()
            self.ui.recdesde.setDate(fecha)
            self.ui.rechasta.setDate(fecha)

            self.ui.tbconrecsup.setRowCount(0)
            self.ui.tbconrecsup.clearContents()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


########################################################################################################################
##################################### Consulta Factura-Cliente #########################################################
########################################################################################################################

    def DetalleConFacCli(self):
        try:

            seleccion = self.ui.tbconfaccli.currentRow()  # Obtiene el índice de la fila seleccionada
            idcli = self.ui.idclifaccli.text()
            if seleccion >= 0:
                nofac = self.ui.tbconfaccli.item(seleccion, 0).text()

                self.detalle.CargarFacturas(nofac, idcli)
                self.detalle.show()

            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"No hay ninguna fila seleccionada")
                self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevoConcli(self):
        try:
            fecha = QDate.currentDate()

            self.ui.idclifaccli.clear()
            self.ui.facclidesde.setDate(fecha)
            self.ui.facclihasta.setDate(fecha)

            self.ui.tbconfaccli.setRowCount(0)
            self.ui.tbconfaccli.clearContents()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CargarDatosFacCli(self, tupla):
        try:
            if tupla:
                self.ui.tbconfaccli.setRowCount(len(tupla))

                for i, row in enumerate(tupla):
                    for j, value in enumerate(row):
                        self.ui.tbconfaccli.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CargarFacturas(self):
        try:
            idcli = self.ui.idclifaccli.text()
            desde = self.ui.facclidesde.text()
            hasta = self.ui.facclihasta.text()

            if not idcli or not desde or not hasta:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes llenar todos los campos")
                self.mensaje.show()
            else:
                sql = "CALL spfaccli(%s, %s, %s)"
                valores = (idcli, desde, hasta)
                cursor.execute(sql, valores)
                data = cursor.fetchall()

                if data:
                    self.CargarDatosFacCli(data)
                else:
                    self.mensaje.setIcon(QMessageBox.Warning)
                    self.mensaje.setText("El cliente no tienen ninguna factura")
                    self.mensaje.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


########################################################################################################################
############################################## Proceso de Bono #########################################################
########################################################################################################################
    def NuevoBono(self):
        try:
            self.ui.numbon28.clear()
            self.ui.monbon28.setValue(0.00)
            self.ui.cancli28.setValue(1)

            self.GenerarIDBono()

            self.ui.tbbon28.setRowCount(0)
            self.ui.tbbon28.clearContents()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GuardarBono(self):
        try:

            verificacion = self.ui.tbbon28.item(0, 0)

            if verificacion is None:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes generar los clientes para la aplicacion de bono")
                self.mensaje.show()
            else:
                estatus = 1
                numbon = self.ui.numbon28.text()

                filas = self.ui.tbbon28.rowCount()
                columnas = self.ui.tbbon28.columnCount()
                tupla = []

                for f in range(filas):
                    datos = []
                    for c in range(columnas):
                        celda = self.ui.tbbon28.item(f, c)
                        if celda is not None:
                            datos.append(celda.text())
                        else:
                            datos.append("")

                    tupla.append(datos)


                for i in tupla:
                    sql = "INSERT INTO tbbon28(numbon, idcli, monto, fecha, vencimiento, estatus) VALUES(%s, %s, %s, %s, %s, %s)"
                    valores = (numbon, i[0], i[2], i[3], i[4], estatus)
                    cursor.execute(sql, valores)
                    conexion.commit()

                    self.EnviarBono(numbon, i[0], i[2], i[3], i[4])


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def EnviarBono(self, numbono, idcli, monto, inicio, vencimiento):
        try:
            cursor.execute("SELECT correo, clave FROM tbemp32")
            info = cursor.fetchone()
            sender_email = info[0]
            sender_password = info[1]

            cursor.execute("SELECT correo FROM tbcli03 WHERE idcli='"+idcli+"'")
            correo = cursor.fetchone()

            if correo:
                numbono = "00000" + str(numbono)
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = correo[0]
                msg['Subject'] = "Bono de recompensa"

                mensaje = f"De parte de nuestra empresa, hemos decidido darte un bono de compra disponible desde {inicio} hasta {vencimiento} " \
                          f"El monto de este bono es de {monto} pesos. El codigo del bono es {numbono}"
                msg.attach(MIMEText(mensaje, 'plain'))

                server = smtplib.SMTP("smtp.office365.com", 587)
                server.starttls()
                server.login(sender_email, sender_password)

                server.sendmail(sender_email, correo[0], msg.as_string())

            self.mensaje.setIcon(QMessageBox.Information)
            self.mensaje.setText("El correo se ha enviado correctamente a cada cliente")
            self.mensaje.show()

            self.NuevoBono()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def CargarClientesBono(self, data):
        try:
            self.ui.tbbon28.setRowCount(len(data))
            monto = self.ui.monbon28.text()

            fecha = datetime.datetime.today()
            vencimiento = fecha + datetime.timedelta(days=30)

            for i, row in enumerate(data):
                for j, value in enumerate(row):
                    self.ui.tbbon28.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
                    self.ui.tbbon28.setItem(i, 2, QtWidgets.QTableWidgetItem(str(monto)))
                    self.ui.tbbon28.setItem(i, 3, QtWidgets.QTableWidgetItem(str(fecha.strftime("%Y-%m-%d"))))
                    self.ui.tbbon28.setItem(i, 4, QtWidgets.QTableWidgetItem(str(vencimiento.strftime("%Y-%m-%d"))))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def VerificacionCantiCli(self, cantidad):
        try:
            cursor.execute("SELECT COUNT(idcli) FROM tbcli03")
            data = cursor.fetchone()

            if data:
                if int(data[0]) == int(0):
                    self.mensaje.setIcon(QMessageBox.Warning)
                    self.mensaje.setText("No hay clientes para hacer este proceso")
                    self.mensaje.show()
                elif int(data[0]) < int(cantidad):
                    self.mensaje.setIcon(QMessageBox.Warning)
                    self.mensaje.setText("No hay suficientes clientes para hacer el proceso con esta cantidad")
                    self.mensaje.show()

                    self.ui.cancli28.setValue(1)
                    self.ui.tbbon28.setRowCount(0)
                    self.ui.tbbon28.clearContents()
                else:
                    pass

            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("No hay clientes para hacer este proceso")
                self.mensaje.show()

            return data[0]

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def VerificarCliBono(self):
        try:
            bono = self.ui.numbon28.text()
            monto = self.ui.monbon28.text()
            cantidad = self.ui.cancli28.text()

            canticli = self.VerificacionCantiCli(cantidad)

            if canticli:
                if int(canticli) == int(0):
                    self.mensaje.setIcon(QMessageBox.Warning)
                    self.mensaje.setText("No hay clientes para hacer este proceso")
                    self.mensaje.show()
                elif int(canticli) < int(cantidad):
                    self.mensaje.setIcon(QMessageBox.Warning)
                    self.mensaje.setText("No hay suficientes clientes para hacer el proceso con esta cantidad")
                    self.mensaje.show()

                    self.ui.cancli28.setValue(1)

                    self.ui.tbbon28.setRowCount(0)
                    self.ui.tbbon28.clearContents()
                else:
                    pass

            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("No hay clientes para hacer este proceso")
                self.mensaje.show()

            if not bono or not monto or not cantidad:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"Debes llenar los campos")
                self.mensaje.show()
            elif float(monto) == 0.00:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"El monto del bono no puede ser 0")
                self.mensaje.show()
            else:
                sql = "CALL spclibon(%s)"
                valores = (cantidad)
                cursor.execute(sql, valores)

                data = cursor.fetchall()

                if data:
                    self.CargarClientesBono(data)
                else:
                    self.mensaje.setIcon(QMessageBox.Critical)
                    self.mensaje.setText(f"No hay suficientes clientes para generar bonos")
                    self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setIcon(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GenerarIDBono(self):
        try:
            global numero
            cont = "1"

            cursor.execute("SELECT MAX(numbon + 1) FROM tbbon28")
            data = cursor.fetchall()

            for i in data:
                numero = str(i[0])

            if numero == "None":
                self.ui.numbon28.setText(cont)
            else:
                self.ui.numbon28.setText(str(numero))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

########################################################################################################################
################################## Grafico de los productos ############################################################
########################################################################################################################

    def CalcularImpuestoOrdAux(self):
        try:
            filas = self.ui.tbord01.rowCount()
            total = 0

            for f in range(filas):
                datos = self.ui.tbord01.item(f, 4)
                if datos is not None:
                    total += float(datos.text())
                else:
                    pass

            return total
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def EnviarOrd(self):
        try:
            nomsup = self.ui.nomsupord01.text()
            telsup = self.ui.telsupord01.text()
            numord = self.ui.numord01.text()
            fecha = self.ui.fecord01.text()
            monto = self.ui.montotord01.text()
            idsup = self.ui.idsupord01.text()
            idsuc = self.ui.idsucord01.currentText()
            filas = self.ui.tbord01.rowCount()
            columna = self.ui.tbord01.columnCount()

            tabla = self.ui.tbord01.item(0, 0)

            if not tabla:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes agregar elementos en la tabla")
                self.mensaje.show()
            else:

                tupla = []
                for f in range(filas):
                    datos = []
                    for c in range(columna):
                        celda = self.ui.tbord01.item(f, c)
                        if celda is not None:
                            datos.append(celda.text())
                        else:
                            datos.append("")
                    tupla.append(datos)

                impuesto = self.CalcularImpuestoOrdAux()

                self.reporte.GenerarPDF(tupla, nomsup, telsup, numord, fecha, monto, impuesto, idsup, idsuc)

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def ImprimirOrd(self):
        try:
            numord = self.ui.numord01.text()
            fecha = self.ui.fecord01.text()
            nomsup = self.ui.nomsupord01.text()
            telsup = self.ui.telsupord01.text()
            monto = self.ui.montotord01.text()
            idsuc = self.ui.idsucord01.currentText()

            filas = self.ui.tbord01.rowCount()
            columnas = self.ui.tbord01.columnCount()
            tupla = []

            tabla = self.ui.tbord01.item(0, 0)
            if tabla is None:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("No hay elementos en la tabla")
                self.mensaje.show()
            else:
                for f in range(filas):
                    datos = []
                    for c in range(columnas):
                        item = self.ui.tbord01.item(f, c)
                        if item is not None:
                            datos.append(item.text())
                        else:
                            datos.append("")
                    tupla.append(datos)
                sumimp = self.CalcularImpuestoOrdAux()
                self.reporte.ImprimirOrd(sumimp, monto, numord, fecha, nomsup, telsup, idsuc, tupla)

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CalcularMontoOrd(self):
        try:
            total = 0
            rows = self.ui.tbord01.rowCount()

            for row in range(rows):
                importe = self.ui.tbord01.item(row, 5)
                itebis = self.ui.tbord01.item(row, 4)

                if importe and itebis is not None:
                    impor = float(importe.text())
                    iteb = float(itebis.text())
                    suma = float(impor) + float(iteb)

                    total += suma
            self.ui.montotord01.setText(str(total))

        except Exception as ex:
                self.mensaje.setIcon(QMessageBox.Critical)
                self.mensaje.setText(f"Ha ocurrido un error {ex}")
                self.mensaje.show()

    def GenerarIDOrdenCompra(self):
        try:
            global numero
            cont = "1"

            cursor.execute("SELECT MAX(numord + 1) FROM tbordcommae01")
            data = cursor.fetchall()

            for i in data:
                numero = str(i[0])

            if numero == "None":
                self.ui.numord01.setText(cont)
            else:
                self.ui.numord01.setText(str(numero))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def LlenarComboSucOrd(self):
        try:
            cursor.execute("SELECT idsuc, nombre FROM tbsuc26")
            data = cursor.fetchall()

            if data:
                for i in data:
                    formato = f"{i[0]}   - {i[1]}"
                    self.ui.idsucord01.addItem(formato)
            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"No hay sucursales creadas")
                self.mensaje.show()


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def MostrarInfoSuplidorOrd(self):
        try:
            idsup = self.ui.idsupord01.text()
            verificacion = self.VerificacionSuplidor(idsup)

            if verificacion is False:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("El suplidor ingresado no existe")
                self.mensaje.show()


            else:
                for i in verificacion:
                    self.ui.idsupord01.setText(str(i[0]))
                    self.ui.nomsupord01.setText(str(i[2]))
                    self.ui.dirsupord01.setText(str(i[3]))
                    self.ui.telsupord01.setText(str(i[4]))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def MostrarInfoProductoOrd(self):
        try:
            idpro = self.ui.idproord01.text()
            verificacion = self.VerificacionProducto(idpro)

            if verificacion is False:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("El producto ingresado no existe")
                self.mensaje.show()


            else:
                for i in verificacion:
                    self.ui.preord01.setValue(float(i[7]))


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CalcularImpuestoOrd(self, valor):
        try:
            cursor.execute("SELECT MAX(porcentaje) FROM tbimp07")
            data = cursor.fetchone()

            if data:
                porciento = float(data[0])
                impuesto = (porciento * float(valor)) / 100

                self.ui.itbord01.setText(str(impuesto))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CalcularImporteOrd(self):
        try:

            cantidad = self.ui.cantiord01.text()
            precio = self.ui.preord01.text()

            importe = float(cantidad) * float(precio)

            self.ui.impord01.setValue(float(importe))
            self.ui.canpenord01.setValue(float(cantidad))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def AgregarOrd(self):
        try:
            suplidor = self.ui.idsupord01.text()
            orden = self.ui.numord01.text()
            idpro = self.ui.idproord01.text()
            precio = self.ui.preord01.text()
            cantidad = self.ui.cantiord01.text()
            importe = self.ui.impord01.text()
            itebis = self.ui.itbord01.text()
            pendiente = self.ui.canpenord01.text()

            if not orden or not suplidor or not idpro or not cantidad or not pendiente or not precio or not importe:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes llenar todos los campos antes de agregar el producto")
                self.mensaje.show()

            else:
                try:

                    filas = self.ui.tbord01.rowCount()
                    self.ui.tbord01.insertRow(filas)
                    self.ui.tbord01.setItem(filas, 0, QTableWidgetItem(str(orden)))
                    self.ui.tbord01.setItem(filas, 1, QTableWidgetItem(str(idpro)))
                    self.ui.tbord01.setItem(filas, 2, QTableWidgetItem(str(cantidad)))
                    self.ui.tbord01.setItem(filas, 3, QTableWidgetItem(str(precio)))
                    self.ui.tbord01.setItem(filas, 4, QTableWidgetItem(str(itebis)))
                    self.ui.tbord01.setItem(filas, 5, QTableWidgetItem(str(importe)))
                    self.ui.tbord01.setItem(filas, 6, QTableWidgetItem(str(pendiente)))

                    self.CalcularMontoOrd()
                    self.LimpiarCamposOrd()
                except Exception as ex:
                    self.mensaje.setIcon(QMessageBox.Critical)
                    self.mensaje.setText(f"Ha ocurrido un error {ex}")
                    self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def SalvarDetalleOrd(self):
        filas = self.ui.tbord01.rowCount()
        columnas = self.ui.tbord01.columnCount()
        tupla = []

        for f in range(filas):
            datos = []
            for c in range(columnas):
                celda = self.ui.tbord01.item(f, c)
                if celda is not None:
                    datos.append(celda.text())
                else:
                    datos.append("")

            tupla.append(datos)

        for i in tupla:
            sql = "INSERT INTO tbordcomdet02(numord, idpro, cantidad, precio, itebis, cantipen) VALUES(%s, %s, %s, %s, %s, %s)"
            valores = (i[0], i[1], i[2], i[3], i[4], i[6])

            cursor.execute(sql, valores)
            conexion.commit()



    def SalvarOrd(self):
        try:

            orden = self.ui.numord01.text()
            suplidor = self.ui.idsupord01.text()
            sucursal = self.ui.idsucord01.currentText()[0] + "" + \
                       self.ui.idsucord01.currentText()[1] + "" + \
                       self.ui.idsucord01.currentText()[2]
            observacion = self.ui.obsord01.text()
            tabla = self.ui.tbord01.item(0, 0)


            if not orden or not suplidor or not tabla:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("El campo de numero de orden y suplidor son obligatorios y recuerda agregar elementos a la tabla")
                self.mensaje.show()
            else:
                sql = "INSERT INTO tbordcommae01(numord, idsup, idsuc, iduse, fecha, observacion) VALUES(%s, %s, %s, %s, now(), %s)"
                valores = (orden, suplidor, sucursal, self.codeusu, observacion)

                cursor.execute(sql, valores)
                conexion.commit()

                self.SalvarDetalleOrd()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText(f"La orden de compra se ha guardado correctamente")
                self.mensaje.show()

                self.NuevoOrd()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def EliminarOrd(self):
        try:

            filas = self.ui.tbord01.selectionModel().selectedRows()

            if not filas:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"Debes seleccionar elemento")
                self.mensaje.show()
            else:
                for i in filas:
                    self.ui.tbord01.removeRow(i.row())

            self.CalcularMontoOrd()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def LimpiarCamposOrd(self):
        try:
            self.ui.idproord01.clear()
            self.ui.preord01.setValue(0.00)
            self.ui.cantiord01.setValue(0.00)
            self.ui.impord01.setValue(0.00)
            self.ui.itbord01.clear()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def NuevoOrd(self):
        try:
            self.ui.idsupord01.clear()
            self.ui.nomsupord01.clear()
            self.ui.dirsupord01.clear()
            self.ui.telsupord01.clear()
            self.ui.numord01.clear()
            self.ui.idproord01.clear()
            self.ui.preord01.setValue(0.00)
            self.ui.cantiord01.setValue(0.00)
            self.ui.impord01.setValue(0.00)
            self.ui.itbord01.clear()
            self.ui.idsucord01.setCurrentIndex(0)
            self.ui.fecord01.clear()
            self.ui.canpenord01.setValue(0.00)
            self.ui.montotord01.clear()
            self.ui.obsord01.clear()

            self.GenerarIDOrdenCompra()
            self.ui.tbord01.clearContents()
            self.ui.tbord01.setRowCount(0)

            self.ui.fecord01.setText(str(self.GenerarFechaActual()))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



########################################################################################################################
################################## Grafico de los productos ############################################################
########################################################################################################################

    def CalcularRestante(self, monto, balance):
        try:

            if float(monto) > float(balance):
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("El balance a pagar no puede ser mayor a el monto")
                self.mensaje.show()
            else:

                resto = float(balance) - float(monto)

                return resto

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

########################################################################################################################
############################################## Movimiento de Cobros ####################################################
########################################################################################################################

    def RellenarFormCobro(self):
        try:
            seleccion = self.ui.tbcob29.currentRow()

            norecibo = self.ui.tbcob29.item(seleccion, 0)
            balance = self.ui.tbcob29.item(seleccion, 3)

            if balance or norecibo is not None:
                self.ui.noreccob29.setText(str(norecibo.text()))
                self.ui.balcob29.setValue(float(balance.text()))
                self.ui.moncob29.setMaximum(float(balance.text()))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def VentanaSuplidorCob(self):
        try:
            self.modo = "cobros"
            self.suplidor.CargarSuplidores()
            self.cliente.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GenerarIDCobro(self):
        try:
            global numero
            cont = "1"

            cursor.execute("SELECT MAX(numrecibo + 1) FROM tbcobmae29")
            data = cursor.fetchall()

            for i in data:
                numero = str(i[0])

            if numero == "None":
                self.ui.norecibcob29.setText(cont)
            else:
                self.ui.norecibcob29.setText(str(numero))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CargarRecepcionCob(self):
        try:
            idsup = self.ui.idsupcob29.text()
            cursor.execute("SELECT norecep, fecha, monto, balance, condicion FROM tbrecmae18 "
                           "WHERE idsup='" + idsup + "' AND condicion > 0 AND balance > 0")
            data = cursor.fetchall()

            if data:
                self.ui.tbcob29.setRowCount(len(data))

                for i, row in enumerate(data):
                    vencimiento = row[1] + datetime.timedelta(days=int(row[4]))
                    for j, value in enumerate(row):
                        self.ui.tbcob29.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
                        self.ui.tbcob29.setItem(i, 4, QtWidgets.QTableWidgetItem(str(vencimiento)))
                        self.ui.tbcob29.setItem(i, 5, QtWidgets.QTableWidgetItem(str("0.00")))

            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Este cliente no debe pagar ninguna factura")
                self.mensaje.show()

                self.NuevoPago()


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def LlenarComboBancoCobro(self):
        try:
            cursor.execute("SELECT * FROM tbban06")
            data = cursor.fetchall()

            if data:
                for i in data:
                    banco = f"{i[0]}  - {i[1]}"
                    self.ui.bancob29.addItem(str(banco))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def MostrarInfoSuplidorCob(self):
        try:
            idsup = self.ui.idsupcob29.text()
            verificacion = self.VerificacionSuplidor(idsup)

            if verificacion is False:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("El suplidor ingresado no existe")
                self.mensaje.show()

                self.NuevoCobro()

            else:
                for i in verificacion:
                    self.ui.idsupcob29.setText(str(i[0]))
                    self.ui.nomsupcob29.setText(str(i[2]))
                    self.ui.dirsupcob29.setText(str(i[3]))
                    self.ui.telsupcob29.setText(str(i[4]))

                    self.CargarRecepcionCob()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def VerificacionDocuCob(self):
        try:
            indice = self.ui.forpagcob29.currentIndex()

            if int(indice) == 0:
                self.ui.nodocmob29.setText("0")
                self.ui.nodocmob29.setDisabled(True)

                self.ui.bancob29.setCurrentIndex(0)
                self.ui.bancob29.setDisabled(True)
            else:
                self.ui.nodocmob29.setEnabled(True)
                self.ui.nodocmob29.setEnabled(True)
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrdio un error {ex}")
            self.mensaje.show()

    def ImprimirCobro(self):
        try:
            idsup = self.ui.idsupcob29.text()
            nomsup = self.ui.nomsupcob29.text()
            telsup = self.ui.telsupcob29.text()
            numrec = self.ui.norecibcob29.text()
            formpag = self.ui.forpagcob29.currentText()
            numdocu = self.ui.nodocmob29.text()
            banco = self.ui.bancob29.currentText()
            fecha = self.ui.feccob29.text()

            filas = self.ui.tbcob29.rowCount()
            columnas = self.ui.tbcob29.columnCount()
            tupla = []

            tabla = self.ui.tbcob29.item(0, 0)
            if tabla is None:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("No hay elementos en la tabla")
                self.mensaje.show()
            else:
                for f in range(filas):
                    datos = []
                    for c in range(columnas):
                        item = self.ui.tbcob29.item(f, c)
                        if item is not None:
                            datos.append(item.text())
                        else:
                            datos.append("")
                    tupla.append(datos)

                total = self.CalcularTotalPagoCob()
                self.reporte.ImprimirCob(idsup, nomsup, telsup, numrec, formpag, numdocu, banco, fecha, total, tupla)
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CalcularTotalPagoCob(self):
        try:
            filas = self.ui.tbcob29.rowCount()
            total = 0

            for f in range(filas):
                monto = self.ui.tbcob29.item(f, 5)
                if monto is not None:
                    total += float(monto.text())
                else:
                    pass

            return total

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def GuardarCambiosCob(self):
        try:
            norece = self.ui.noreccob29.text()
            balance = float(self.ui.balcob29.text())
            monto = float(self.ui.moncob29.text())

            filas = self.ui.tbcob29.rowCount()

            if not norece:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes seleccionar una factura")
                self.mensaje.show()
            else:
                for f in range(filas):
                    celda = self.ui.tbcob29.item(f, 0)
                    if celda is not None:
                        if int(celda.text()) == int(norece):
                            restante = self.CalcularRestante(monto, balance)

                            self.ui.tbcob29.setItem(f, 5, QTableWidgetItem(str(monto)))
                            self.ui.tbcob29.setItem(f, 3, QTableWidgetItem(str(restante)))

                            break
                        else:
                            continue

                self.ui.moncob29.setValue(0.00)
                self.ui.balcob29.setValue(0.00)

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def SalvarCobro(self):
        try:
            idsup = self.ui.idsupcob29.text()
            recibo = self.ui.norecibcob29.text()
            recepcion = self.ui.noreccob29.text()
            formpag = self.ui.forpagcob29.currentText()[0]
            banco = self.ui.bancob29.currentText()[0] + "" + \
                    self.ui.bancob29.currentText()[1] + "" + \
                    self.ui.bancob29.currentText()[2]
            docu = self.ui.nodocmob29.text()
            obsevacion = self.ui.obscob29.text()

            filas = self.ui.tbcob29.rowCount()
            columnas = self.ui.tbcob29.columnCount()
            tupla = []



            if not recepcion or not formpag or not banco:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("No hay ninguna factura seleccionada, asegurate de seleccionar la factura con doble click y recuerda llenar los campos en blanco")
                self.mensaje.show()
            else:

                sql = "INSERT INTO tbcobmae29(numrecibo, idsup, iduse, idbanco, fecha, formpag, nodocu, observacion) " \
                      "VALUES(%s, %s, %s, %s, now(), %s, %s, %s)"
                valores = (recibo, idsup, self.codeusu, banco, formpag, docu, obsevacion)

                cursor.execute(sql, valores)
                conexion.commit()

                for f in range(filas):
                    datos = []
                    for c in range(columnas):
                        celda = self.ui.tbcob29.item(f, c)
                        if celda is not None:
                            datos.append(celda.text())
                        else:
                            datos.append("")
                    tupla.append(datos)

                for i in tupla:
                    sql = "INSERT INTO tbcobdet30(numrecibo, norecep, montopag) VALUES(%s, %s, %s)"
                    valores = (recibo, i[0], i[5])

                    cursor.execute(sql, valores)
                    conexion.commit()

                    sql = "UPDATE tbrecmae18 SET balance=%s WHERE idsup=%s AND norecep=%s"
                    valores = (i[3], idsup, i[0])

                    cursor.execute(sql, valores)
                    conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText(f"El pago se ha realizado correctamente")
                self.mensaje.show()

                self.NuevoCobro()
                self.ui.tbcob29.setRowCount(0)
                self.ui.tbcob29.clearContents()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevoCobro(self):
        try:
            self.ui.idsupcob29.clear()
            self.ui.nomsupcob29.clear()
            self.ui.dirsupcob29.clear()
            self.ui.telsupcob29.clear()
            self.ui.norecibcob29.clear()
            self.ui.noreccob29.clear()
            self.ui.forpagcob29.setCurrentIndex(-1)
            self.ui.nodocmob29.clear()
            self.ui.feccob29.setText(str(self.GenerarFechaActual()))
            self.ui.bancob29.setCurrentIndex(0)
            self.ui.moncob29.setValue(0.00)
            self.ui.obscob29.clear()

            self.ui.tbcob29.setRowCount(0)
            self.ui.tbcob29.clearContents()

            self.ui.bancob29.setEnabled(True)
            self.ui.nodocmob29.setEnabled(True)


            self.GenerarIDCobro()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

########################################################################################################################
################################## Movimiento De Devolucion Suplidor  ##################################################
########################################################################################################################

    def RellenarComboRazSup(self):
        try:
            cursor.execute("SELECT idrazon, descripcion FROM tbraz31")
            data = cursor.fetchall()

            if data:
                for i in data:
                    formato = f"{i[0]}  - {i[1]}"
                    self.ui.razsupdev15.addItem(str(formato))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def AgregarDevTotalSup(self, tupla):
        try:
            self.ui.tbsupdevsec15.setRowCount(len(tupla))
            for i, filas in enumerate(tupla):
                for j, value in enumerate(filas):
                    self.ui.tbsupdev15.setItem(i, 3, QTableWidgetItem(str("0.00")))

                    self.ui.tbsupdevsec15.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

            self.CalcularImporteDevSup()
            self.CalcularImporteDevSupSec()
            self.CalcularBalanceDevSup()
            self.CalcularMontoDevSup()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def DevTotalSup(self):
        try:
            filas = self.ui.tbsupdev15.rowCount()
            columnas = self.ui.tbsupdev15.columnCount()
            tupla = []

            if not filas:
                self.mensaje.setIcon(QMessageBox.Critical)
                self.mensaje.setText("Debes seleccionar un elemento en la tabla")
                self.mensaje.show()
            else:
                for f in range(filas):
                    datos = []
                    for c in range(columnas):
                        celda = self.ui.tbsupdev15.item(f, c)
                        if celda is not None:
                            datos.append(celda.text())
                        else:
                            datos.append("")

                    tupla.append(datos)

            self.AgregarDevTotalSup(tupla)

            self.CalcularImporteDevSup()
            self.CalcularImporteDevSupSec()
            self.CalcularBalanceDevSup()
            self.CalcularMontoDevSup()


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CalcularBalanceDevSup(self):
        try:
            filas = self.ui.tbsupdev15.rowCount()
            total = 0

            for f in range(filas):
                importe = self.ui.tbsupdev15.item(f, 5)
                if importe is not None:
                    total += float(importe.text())

            self.ui.balsupdev15.setText(str(total))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CalcularMontoDevSup(self):
        try:
            filas = self.ui.tbsupdevsec15.rowCount()
            total = 0

            for f in range(filas):
                importe = self.ui.tbsupdevsec15.item(f, 5)
                if importe is not None:
                    total += float(importe.text())

            self.ui.monsupdev15.setText(str(total))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevoDevolucionSuplidor(self):
        try:
            self.ui.idsupdev15.clear()
            self.ui.nomsupdev15.clear()
            self.ui.dirsupdev15.clear()
            self.ui.telsupdev15.clear()
            self.ui.numrecdev15.clear()
            self.ui.idprosupdev15.clear()
            self.ui.nomprosupdev15.clear()
            self.ui.norecsupdev15.clear()
            self.ui.fecsupdev15.clear()
            self.ui.balsupdev15.clear()
            self.ui.monsupdev15.clear()
            self.ui.cansupdev15.setValue(0.00)
            self.ui.presupdev15.setValue(0.00)
            self.ui.ncfdevsup15.clear()

            self.ui.fecsupdev15.setText(str(self.GenerarFechaActual()))
            self.GenerarIDDevolucionSuplidor()

            self.ui.tbsupdev15.setRowCount(0)
            self.ui.tbsupdev15.clearContents()

            self.ui.tbsupdevsec15.setRowCount(0)
            self.ui.tbsupdevsec15.clearContents()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def GenerarIDDevolucionSuplidor(self):
        try:
            global numero

            cont = "1"

            cursor.execute("SELECT MAX(numdev + 1) FROM tbdevsupmae14")
            data = cursor.fetchall()

            for i in data:
                numero = str(i[0])

            if numero == "None":
                self.ui.norecsupdev15.setText(cont)
            else:
                self.ui.norecsupdev15.setText(str(numero))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def RestablecerDevolucionSuplidor(self, codigo, devuelta):
        try:

            fila = self.ui.tbsupdev15.rowCount()

            for f in range(fila):
                producto = self.ui.tbsupdev15.item(f, 1)
                cantidad = self.ui.tbsupdev15.item(f, 3)
                if producto and cantidad is not None:
                    if int(codigo) == int(producto.text()):
                        suma = float(cantidad.text()) + float(devuelta)
                        self.ui.tbsupdev15.setItem(f, 3, QTableWidgetItem(str(suma)))


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def EliminarDevolucionSuplidor(self):
        try:

            fila = self.ui.tbsupdevsec15.currentRow()

            if not fila:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes seleccionar un elemento")
                self.mensaje.show()
            else:
                producto = self.ui.tbsupdevsec15.item(fila, 1).text()
                devuelta = self.ui.tbsupdevsec15.item(fila, 3).text()

                self.RestablecerDevolucionSuplidor(producto, devuelta)

                filas = self.ui.tbsupdevsec15.selectionModel().selectedRows()
                for i in filas:
                    self.ui.tbsupdevsec15.removeRow(i.row())

            self.CalcularImporteDevSup()
            self.CalcularImporteDevSupSec()
            self.CalcularBalanceDevSup()
            self.CalcularMontoDevSup()



        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CargarDatosGridDevSup(self):
        try:
            self.seleccion = self.ui.tbsupdev15.currentRow()

            if self.seleccion >= 0:
                codigo = self.ui.tbsupdev15.item(self.seleccion, 1).text()
                nombre = self.ui.tbsupdev15.item(self.seleccion, 2).text()
                precio = self.ui.tbsupdev15.item(self.seleccion, 4).text()

                self.cantidadlimite = self.ui.tbsupdev15.item(self.seleccion, 3).text()

                self.ui.cansupdev15.setMaximum(float(self.cantidadlimite))
                self.ui.cansupdev15.setValue(float(self.cantidadlimite))

                self.ui.idprosupdev15.setText(str(codigo))
                self.ui.nomprosupdev15.setText(str(nombre))
                self.ui.presupdev15.setValue(float(precio))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CalcularImporteDevSupSec(self):
        try:
            global importe

            filas = self.ui.tbsupdevsec15.rowCount()
            for f in range(filas):
                cantidad = self.ui.tbsupdevsec15.item(f, 3)
                precio = self.ui.tbsupdevsec15.item(f, 4)

                if precio and cantidad is not None:
                    importe = float(cantidad.text()) * float(precio.text())
                    self.ui.tbsupdevsec15.setItem(f, 5, QTableWidgetItem(str(importe)))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GuardarDevolucionSuplidor(self):
        try:
            recepcion = self.ui.numrecdev15.text()
            norecibo = self.ui.norecsupdev15.text()
            codigo = self.ui.idprosupdev15.text()
            nombre = self.ui.nomprosupdev15.text()
            cantidad = self.ui.cansupdev15.text()
            precio = self.ui.presupdev15.text()


            if not norecibo or not codigo or not nombre or not cantidad or not recepcion:

                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes llenar todos los campos antes de agregar el producto")
                self.mensaje.show()

            else:
                try:
                    if float(cantidad) <= 0.00:
                        self.mensaje.setIcon(QMessageBox.Warning)
                        self.mensaje.setText("No puedes devolver una cantidad nula del producto")
                        self.mensaje.show()
                    else:
                        filas = self.ui.tbsupdevsec15.rowCount()
                        self.ui.tbsupdevsec15.insertRow(filas)
                        self.ui.tbsupdevsec15.setItem(filas, 0, QTableWidgetItem(norecibo))
                        self.ui.tbsupdevsec15.setItem(filas, 1, QTableWidgetItem(codigo))
                        self.ui.tbsupdevsec15.setItem(filas, 2, QTableWidgetItem(nombre))
                        self.ui.tbsupdevsec15.setItem(filas, 3, QTableWidgetItem(cantidad))
                        self.ui.tbsupdevsec15.setItem(filas, 4, QTableWidgetItem(str(precio)))

                        rectificacion = float(self.cantidadlimite) - float(self.ui.cansupdev15.text())
                        self.ui.tbsupdev15.setItem(self.seleccion, 3, QTableWidgetItem(str(rectificacion)))

                        self.CalcularImporteDevSup()
                        self.CalcularImporteDevSupSec()
                        self.CalcularBalanceDevSup()
                        self.CalcularMontoDevSup()

                        self.ui.idprosupdev15.clear()
                        self.ui.nomprosupdev15.clear()
                        self.ui.presupdev15.setValue(0.00)
                        self.ui.cansupdev15.setValue(0.00)

                except Exception as ex:
                    self.mensaje.setIcon(QMessageBox.Critical)
                    self.mensaje.setText(f"Ha ocurrido un error {ex}")
                    self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CargarDetallesRecepcionDevSup(self):
        try:
            idrec = self.ui.numrecdev15.text()
            recibo = self.ui.norecsupdev15.text()

            cursor.execute("SELECT a.idpro, d.nompro, a.cantidad-a.cantidaddev as cantidad, a.precio, c.idsup, c.nombre, c.direccion, c.telefono "
                           "FROM tbrecdet19 a, tbrecmae18 b, tbsup09 c, tbpro10 d "
                           "WHERE a.norecep='"+idrec+"' AND a.norecep=b.norecep AND b.idsup=c.idsup AND a.idpro=d.idpro AND a.cantidad > a.cantidaddev")

            data = cursor.fetchall()

            if data:
                self.ui.tbsupdev15.setRowCount(len(data))

                for i, row in enumerate(data):
                    self.ui.idsupdev15.setText(str(row[4]))
                    self.ui.nomsupdev15.setText(str(row[5]))
                    self.ui.dirsupdev15.setText(str(row[6]))
                    self.ui.telsupdev15.setText(str(row[7]))

                    self.ui.tbsupdev15.setItem(i, 0, QTableWidgetItem(str(recibo)))
                    self.ui.tbsupdev15.setItem(i, 1, QTableWidgetItem(str(row[0])))
                    self.ui.tbsupdev15.setItem(i, 2, QTableWidgetItem(str(row[1])))
                    self.ui.tbsupdev15.setItem(i, 3, QTableWidgetItem(str(row[2])))
                    self.ui.tbsupdev15.setItem(i, 4, QTableWidgetItem(str(row[3])))

                    self.CalcularImporteDevSup()
                    self.CalcularImporteDevSupSec()
                    self.CalcularBalanceDevSup()
                    self.CalcularMontoDevSup()


            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"Esta factura no existe")
                self.mensaje.show()

                self.NuevoDevolucionSuplidor()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()




    def CalcularImporteDevSup(self):
        try:
            fila = self.ui.tbsupdev15.rowCount()

            for f in range(fila):
                cantidad = self.ui.tbsupdev15.item(f, 3)
                precio = self.ui.tbsupdev15.item(f, 4)

                if cantidad and precio is not None:
                    importe = float(cantidad.text()) * float(precio.text())
                    self.ui.tbsupdev15.setItem(f, 5, QTableWidgetItem(str(importe)))
                else:
                    pass

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def RestarExistenciaProDevSup(self, idpro, cantidaddev):
        try:
            sql = "UPDATE tbproxsuc27 SET cantidad=cantidad - %s WHERE idpro=%s AND idsuc=%s"
            valores = (cantidaddev, idpro, self.suc)
            cursor.execute(sql, valores)
            conexion.commit()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def InsertarDetalleDevSup(self):
        try:
            norecep = self.ui.numrecdev15.text()
            filas = self.ui.tbsupdevsec15.rowCount()
            columnas = self.ui.tbsupdevsec15.columnCount()
            tupla = []

            for f in range(filas):
                datos = []
                for c in range(columnas):
                    celda = self.ui.tbsupdevsec15.item(f, c)
                    if celda is not None:
                        datos.append(celda.text())
                    else:
                        datos.append("")
                tupla.append(datos)

            for i in tupla:
                sql = "INSERT INTO tbdevsupdet15(numdev, idpro, cantidaddev) VALUES(%s, %s, %s)"
                valores = (i[0], i[1], i[3])
                cursor.execute(sql, valores)
                conexion.commit()

                sql = "UPDATE tbrecdet19 SET cantidaddev=cantidaddev + %s WHERE norecep=%s AND idpro=%s"
                valores = (i[3], norecep, i[1])
                cursor.execute(sql, valores)
                conexion.commit()

                self.RestarExistenciaProDevSup(i[1], i[3])
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def SalvarDevolucionSuplidor(self):
        try:
            main = self.ui.tbsupdev15.item(0, 0)
            sec = self.ui.tbsupdev15.item(0, 0)
            numrecep = self.ui.numrecdev15.text()
            balance = self.ui.balsupdev15.text()

            devolucion = self.ui.norecsupdev15.text()
            suplidor = self.ui.idsupdev15.text()
            idsuc = self.suc
            recepcion = self.ui.numrecdev15.text()
            razon = self.ui.razsupdev15.currentText()[0] + "" + \
                    self.ui.razsupdev15.currentText()[1]
            ncf = self.ui.ncfdevsup15.text()


            if not main:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes cargar una factura antes de guardar")
                self.mensaje.show()
            elif not sec:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes agregar una elementos para devolver")
                self.mensaje.show()

            else:
                sql = "INSERT INTO tbdevsupmae14(numdev, idsup, norecep, iduse, idsuc, idrazon, fecha, ncf) " \
                      "VALUES(%s, %s, %s, %s, %s, %s, now(), %s)"
                valores = (devolucion, suplidor, recepcion, self.codeusu, idsuc, razon, ncf)
                cursor.execute(sql, valores)
                conexion.commit()

                sql = "UPDATE tbrecmae18 SET balance=%s WHERE norecep=%s"
                valores = (balance, numrecep)
                cursor.execute(sql, valores)
                conexion.commit()

                self.InsertarDetalleDevSup()

                self.NuevoDevolucionSuplidor()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText(f"La devolucion se ha completado correctamente")
                self.mensaje.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def ImprimirDevolucionSuplidor(self):
        try:
            idsup = self.ui.idsupdev15.text()
            numrec = self.ui.numrecdev15.text()
            numrecibo = self.ui.norecsupdev15.text()
            fecha = self.ui.fecsupdev15.text()
            nomsup = self.ui.nomsupdev15.text()
            telsup = self.ui.telsupdev15.text()
            monto = self.ui.monsupdev15.text()
            balance = self.ui.balsupdev15.text()

            filas = self.ui.tbsupdevsec15.rowCount()
            columnas = self.ui.tbsupdevsec15.columnCount()
            tupla = []

            tabla = self.ui.tbsupdevsec15.item(0, 0)
            if tabla is None:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("No hay elementos en la tabla")
                self.mensaje.show()
            else:
                for f in range(filas):
                    datos = []
                    for c in range(columnas):
                        item = self.ui.tbsupdevsec15.item(f, c)
                        if item is not None:
                            datos.append(item.text())
                        else:
                            datos.append("")
                    tupla.append(datos)
                self.reporte.ImprimirDevSup(idsup, numrec, numrecibo, fecha, nomsup, telsup, monto, balance, tupla)

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


########################################################################################################################
################################## Movimiento De Devolucion Cliente  ###################################################
########################################################################################################################


    def RellenarComboRazCli(self):
        try:
            cursor.execute("SELECT idrazon, descripcion FROM tbraz31")
            data = cursor.fetchall()

            if data:
                for i in data:
                    formato = f"{i[0]}  - {i[1]}"
                    self.ui.razdevcli12.addItem(str(formato))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def SumarExistenciaProDevCli(self, idpro, cantidaddev):
        try:
            sql = "UPDATE tbproxsuc27 SET cantidad=cantidad + %s WHERE idpro=%s AND idsuc=%s"
            valores = (cantidaddev, idpro, self.suc)
            cursor.execute(sql, valores)
            conexion.commit()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def InsertarDetalleDevCli(self):
        try:
            factura = self.ui.numfacclidev12.text()
            filas = self.ui.tbclidevsec12.rowCount()
            columnas = self.ui.tbclidevsec12.columnCount()
            tupla = []

            for f in range(filas):
                datos = []
                for c in range(columnas):
                    celda = self.ui.tbclidevsec12.item(f, c)
                    if celda is not None:
                        datos.append(celda.text())
                    else:
                        datos.append("")
                tupla.append(datos)

            for i in tupla:
                sql = "INSERT INTO tbdevclidet13(numdev, idpro, cantidaddev) VALUES(%s, %s, %s)"
                valores = (i[0], i[1], i[3])
                cursor.execute(sql, valores)
                conexion.commit()

                sql = "UPDATE tbfacdet21 SET cantidaddev=cantidaddev + %s WHERE nofac=%s AND idpro=%s"
                valores = (i[3], factura, i[1])
                cursor.execute(sql, valores)
                conexion.commit()

                self.SumarExistenciaProDevCli(i[1], i[3])


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def SalvarDevolucionCliente(self):
        try:
            main = self.ui.tbclidev12.item(0, 0)
            sec = self.ui.tbclidevsec12.item(0, 0)
            estatus = "I"

            devolucion = self.ui.norecdevclimae12.text()
            cliente = self.ui.idclidev12.text()
            idsuc = self.suc
            factura = self.ui.numfacclidev12.text()
            razon = self.ui.razdevcli12.currentText()[0] + "" + \
                    self.ui.razdevcli12.currentText()[1]
            balance = self.ui.balclidev12.text()



            if not main:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes cargar una factura antes de guardar")
                self.mensaje.show()
            elif not sec:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes agregar una elementos para devolver")
                self.mensaje.show()

            else:
                sql = "INSERT INTO tbdevclimae12(numdev, idcli, iduse, idsuc, idrazon, factura, fecha) " \
                      "VALUES(%s, %s, %s, %s, %s, %s, now())"
                valores = (devolucion, cliente, self.codeusu, idsuc, factura, razon)
                cursor.execute(sql, valores)
                conexion.commit()

                sql = "UPDATE tbfacmae20 SET balance=%s, estatus=%s WHERE nofac=%s"
                valores = (balance, estatus, factura)
                cursor.execute(sql, valores)
                conexion.commit()

                self.InsertarDetalleDevCli()

                self.NuevoDevolucionCliente()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText(f"La devolucion se ha completado correctamente")
                self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def AgregarDevTotal(self, tupla):
        try:
            self.ui.tbclidevsec12.setRowCount(len(tupla))
            for i, filas in enumerate(tupla):
                for j, value in enumerate(filas):
                    self.ui.tbclidev12.setItem(i, 3, QTableWidgetItem(str("0.00")))

                    self.ui.tbclidevsec12.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

            self.CalcularImporte()
            self.CalcularImporteDevCliSec()
            self.CalcularBalanceDevCliMain()
            self.CalcularBalanceDevCliSec()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def DevTotalCli(self):
        try:

            main = self.ui.tbclidev12.item(0, 0)

            filas = self.ui.tbclidev12.rowCount()
            columnas = self.ui.tbclidev12.columnCount()
            tupla = []

            if not main:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"No hay elementos para devolver")
                self.mensaje.show()

            else:
                for f in range(filas):
                    datos = []
                    for c in range(columnas):
                        celda = self.ui.tbclidev12.item(f, c)
                        if celda is not None:
                            datos.append(celda.text())
                        else:
                            datos.append("")

                    tupla.append(datos)

                self.AgregarDevTotal(tupla)
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def NuevoDevolucionCliente(self):
        try:
            self.ui.idclidev12.clear()
            self.ui.nomclidev12.clear()
            self.ui.apeclidev12.clear()
            self.ui.telclidev12.clear()
            self.ui.numfacclidev12.clear()
            self.ui.idproclidev12.clear()
            self.ui.nomproclidev12.clear()
            self.ui.preclidev12.setValue(0.00)
            self.ui.canclidev12.setValue(0.00)

            self.ui.fecdevcli12.setText(str(self.GenerarFechaActual()))
            self.GenerarIDDevolucionCliente()

            self.ui.tbclidev12.setRowCount(0)
            self.ui.tbclidev12.clearContents()

            self.ui.tbclidevsec12.setRowCount(0)
            self.ui.tbclidevsec12.clearContents()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GuardarDevolucionCliente(self):
        try:
            factura = self.ui.numfacclidev12.text()
            norecibo = self.ui.norecdevclimae12.text()
            codigo = self.ui.idproclidev12.text()
            nombre = self.ui.nomproclidev12.text()
            cantidad = self.ui.canclidev12.text()
            precio = self.ui.preclidev12.text()


            if not norecibo or not codigo or not nombre or not cantidad or not factura:

                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes llenar todos los campos antes de agregar el producto")
                self.mensaje.show()

            else:
                try:
                    if float(cantidad) <= 0.00:
                        self.mensaje.setIcon(QMessageBox.Warning)
                        self.mensaje.setText("No puedes devolver una cantidad nula del producto")
                        self.mensaje.show()
                    else:
                        filas = self.ui.tbclidevsec12.rowCount()
                        self.ui.tbclidevsec12.insertRow(filas)
                        self.ui.tbclidevsec12.setItem(filas, 0, QTableWidgetItem(norecibo))
                        self.ui.tbclidevsec12.setItem(filas, 1, QTableWidgetItem(codigo))
                        self.ui.tbclidevsec12.setItem(filas, 2, QTableWidgetItem(nombre))
                        self.ui.tbclidevsec12.setItem(filas, 3, QTableWidgetItem(cantidad))
                        self.ui.tbclidevsec12.setItem(filas, 4, QTableWidgetItem(str(precio)))

                        rectificacion = float(self.cantidadlimite) - float(self.ui.canclidev12.text())
                        self.ui.tbclidev12.setItem(self.seleccion, 3, QTableWidgetItem(str(rectificacion)))

                        self.CalcularImporte()
                        self.CalcularImporteDevCliSec()
                        self.CalcularBalanceDevCliMain()
                        self.CalcularBalanceDevCliSec()

                        self.ui.idproclidev12.clear()
                        self.ui.nomproclidev12.clear()
                        self.ui.preclidev12.setValue(0.00)
                        self.ui.canclidev12.setValue(0.00)

                except Exception as ex:
                    self.mensaje.setIcon(QMessageBox.Critical)
                    self.mensaje.setText(f"Ha ocurrido un error {ex}")
                    self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CalcularBalanceDevCliSec(self):
        try:
            filas = self.ui.tbclidevsec12.rowCount()
            total = 0

            for f in range(filas):
                monto = self.ui.tbclidevsec12.item(f, 5)
                if monto is not None:
                    total += float(monto.text())

            self.ui.monclidev12.setText(str(total))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CalcularImporteDevCliSec(self):
        try:
            global importe

            filas = self.ui.tbclidevsec12.rowCount()
            for f in range(filas):
                cantidad = self.ui.tbclidevsec12.item(f, 3)
                precio = self.ui.tbclidevsec12.item(f, 4)

                if precio and cantidad is not None:
                    importe = float(cantidad.text()) * float(precio.text())
                    self.ui.tbclidevsec12.setItem(f, 5, QTableWidgetItem(str(importe)))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CalcularBalanceDevCliMain(self):
        try:
            filas = self.ui.tbclidev12.rowCount()
            total = 0

            for f in range(filas):
                monto = self.ui.tbclidev12.item(f, 5)
                if monto is not None:
                    total += float(monto.text())

            self.ui.balclidev12.setText(str(total))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CalcularImporte(self):
        try:
            fila = self.ui.tbclidev12.rowCount()

            for f in range(fila):
                cantidad = self.ui.tbclidev12.item(f, 3)
                precio = self.ui.tbclidev12.item(f, 4)

                if cantidad and precio is not None:
                    importe = float(cantidad.text()) * float(precio.text())
                    self.ui.tbclidev12.setItem(f, 5, QTableWidgetItem(str(importe)))
                else:
                    pass

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def RestablecerDevolucion(self, codigo, devuelta):
        try:

            fila = self.ui.tbclidev12.rowCount()

            for f in range(fila):
                producto = self.ui.tbclidev12.item(f, 1)
                cantidad = self.ui.tbclidev12.item(f, 3)
                if producto and cantidad is not None:
                    if int(codigo) == int(producto.text()):
                        suma = float(cantidad.text()) + float(devuelta)
                        self.ui.tbclidev12.setItem(f, 3, QTableWidgetItem(str(suma)))


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def EliminarDevolucionCliente(self):
        try:

            fila = self.ui.tbclidevsec12.currentRow()

            producto = self.ui.tbclidevsec12.item(fila, 1).text()
            devuelta = self.ui.tbclidevsec12.item(fila, 3).text()

            self.RestablecerDevolucion(producto, devuelta)

            filas = self.ui.tbclidevsec12.selectionModel().selectedRows()
            for i in filas:
                self.ui.tbclidevsec12.removeRow(i.row())

            self.CalcularImporte()
            self.CalcularImporteDevCliSec()
            self.CalcularBalanceDevCliMain()
            self.CalcularBalanceDevCliSec()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CargarDetallesFacturaDevCli(self):
        try:
            factura = self.ui.numfacclidev12.text()
            recibo = self.ui.norecdevclimae12.text()

            cursor.execute("SELECT a.idpro, d.nompro, a.cantipro-a.cantidaddev as cantidad, a.prepro, c.idcli, c.nombre, c.apellido, c.telefono "
                           "FROM tbfacdet21 a, tbfacmae20 b, tbcli03 c, tbpro10 d "
                           "WHERE a.nofac='"+factura+"' AND a.nofac=b.nofac AND b.idcli=c.idcli AND a.idpro=d.idpro AND a.cantipro > a.cantidaddev")

            data = cursor.fetchall()

            if data:
                self.ui.tbclidev12.setRowCount(len(data))

                for i, row in enumerate(data):
                    self.ui.idclidev12.setText(str(row[4]))
                    self.ui.nomclidev12.setText(str(row[5]))
                    self.ui.apeclidev12.setText(str(row[6]))
                    self.ui.telclidev12.setText(str(row[7]))

                    self.ui.tbclidev12.setItem(i, 0, QTableWidgetItem(str(recibo)))
                    self.ui.tbclidev12.setItem(i, 1, QTableWidgetItem(str(row[0])))
                    self.ui.tbclidev12.setItem(i, 2, QTableWidgetItem(str(row[1])))
                    self.ui.tbclidev12.setItem(i, 3, QTableWidgetItem(str(row[2])))
                    self.ui.tbclidev12.setItem(i, 4, QTableWidgetItem(str(row[3])))

                    self.CalcularImporte()
            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"Esta factura no existe")
                self.mensaje.show()

                self.NuevoDevolucionCliente()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def ImprimirDevoluionCliente(self):

        try:
            idcli = self.ui.idclidev12.text()
            nofac = self.ui.numfacclidev12.text()
            numrecibo = self.ui.norecdevclimae12.text()
            fecha = self.ui.fecdevcli12.text()
            nomcli = self.ui.nomclidev12.text()
            apecli = self.ui.apeclidev12.text()
            telcli = self.ui.telclidev12.text()
            monto = self.ui.monclidev12.text()
            balance = self.ui.balclidev12.text()

            filas = self.ui.tbclidevsec12.rowCount()
            columnas = self.ui.tbclidevsec12.columnCount()
            tupla = []

            tabla = self.ui.tbclidevsec12.item(0, 0)
            if tabla is None:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("No hay elementos en la tabla")
                self.mensaje.show()
            else:
                for f in range(filas):
                    datos = []
                    for c in range(columnas):
                        item = self.ui.tbclidevsec12.item(f, c)
                        if item is not None:
                            datos.append(item.text())
                        else:
                            datos.append("")
                    tupla.append(datos)
                self.reporte.ImprimirDevCli(balance, idcli, nofac, numrecibo, fecha, nomcli, apecli, telcli, monto, tupla)

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def GenerarIDDevolucionCliente(self):
        try:
            global numero

            cont = "1"

            cursor.execute("SELECT MAX(numdev + 1) FROM tbdevclimae12")
            data = cursor.fetchall()

            for i in data:
                numero = str(i[0])

            if numero == "None":
                self.ui.norecdevclimae12.setText(cont)
            else:
                self.ui.norecdevclimae12.setText(str(numero))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CargarDatosGridDevCli(self):
        try:
            self.seleccion = self.ui.tbclidev12.currentRow()

            if self.seleccion >= 0:
                codigo = self.ui.tbclidev12.item(self.seleccion, 1).text()
                nombre = self.ui.tbclidev12.item(self.seleccion, 2).text()
                precio = self.ui.tbclidev12.item(self.seleccion, 4).text()

                self.cantidadlimite = self.ui.tbclidev12.item(self.seleccion, 3).text()

                self.ui.canclidev12.setMaximum(float(self.cantidadlimite))
                self.ui.canclidev12.setValue(float(self.cantidadlimite))

                self.ui.idproclidev12.setText(str(codigo))
                self.ui.nomproclidev12.setText(str(nombre))
                self.ui.preclidev12.setValue(float(precio))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



########################################################################################################################
###################################### Presentar Info De Secundarias ###################################################
########################################################################################################################

    def PresentarDatosTablaBanco(self):
        try:
            datos = self.banco.IdentificarBanco()

            id = datos[0]
            self.ui.idban06.setText(str(id))

            self.banco.close()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def PresentarDatosTablaUsuario(self):
        try:
            datos = self.usuario.IdentificarUsuario()

            id = datos[0]
            self.ui.idusu08.setText(str(id))

            self.usuario.close()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def PresentarDatosTablaCategoria(self):
        try:
            datos = self.categoria.IdentificarCategoria()

            id = datos[0]
            self.ui.idcat00.setText(str(id))

            self.categoria.close()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def PresentarDatosTablaProvincias(self):
        try:
            datos = self.provincia.IdentificarProvincia()

            id = datos[0]
            self.ui.idprov25.setText(str(id))

            self.provincia.close()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def PresentarDatosTablaSucursales(self):
        try:
            datos = self.sucursal.IdentificarSucursal()

            id = datos[0]
            self.ui.idsuc26.setText(str(id))

            self.sucursal.close()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def PresentarDatosTablaProgramas(self):
        try:
            datos = self.programa.IdentificarPrograma()

            id = datos[0]
            self.ui.idprg23.setText(str(id))

            self.programa.close()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def PresentarDatosTablaProducto(self):
        try:
            datos = self.producto.IdentificarProducto()

            id = datos[0]
            existencia = datos[3]
            precio = datos[4]

            if self.modo == "factura":
                self.ui.numprofac20.setText(str(id))
                self.ui.canprofac20.setText(str(existencia))
                self.ui.prefac20.setValue(float(precio))

            elif self.modo == "recepcion":
                self.ui.idprorec18.setText(str(id))
                self.ui.prerec18.setValue(float(precio))

            elif self.modo == "conversion":
                self.ui.idproconv11.setText(str(id))

            elif self.modo == "producto":
                self.ui.idpro10.setText(str(id))

            self.producto.close()


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def PresentarDatosTablaSuplidor(self):

        try:
            datos = self.suplidor.IdentificarSuplidor()

            id = datos[0]
            nombre = datos[1]
            telefono = datos[2]
            direccion = datos[3]

            if self.modo == "recepcion":
                self.ui.idsuprec18.setText(str(id))
                self.ui.nomsup18.setText(str(nombre))
                self.ui.telsup18.setText(str(telefono))
                self.ui.dirsup18.setText(str(direccion))

            elif self.modo == "suplidor":
                self.ui.idsup09.setText(str(id))

            self.suplidor.close()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def PresentarDatosTablaCliente(self):
        try:
            datos = self.cliente.IdentificarCliente()

            id = datos[0]
            nombre = datos[1]
            apellido = datos[2]
            telefono = datos[3]

            if self.modo == "factura":
                self.ui.idclifac20.setText(str(id))
                self.ui.nomclifac20.setText(str(nombre))
                self.ui.apeclifac20.setText(str(apellido))
                self.ui.telclifac20.setText(str(telefono))

            elif self.modo == "pago":
                self.ui.idclipag16.setText(str(id))
                self.ui.nomclipag16.setText(str(nombre))
                self.ui.apeclipag16.setText(str(apellido))
                self.ui.telclipag16.setText(str(telefono))

            elif self.modo == "cliente":
                self.ui.idcli03.setText(str(id))

            self.cliente.close()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


########################################################################################################################
############################################## Movimiento de Recepcion #################################################
########################################################################################################################

    def VentanaProductoRec(self):
        try:
            self.modo = "recepcion"
            self.producto.CargarProductos()
            self.producto.show()


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def VentanaSuplidorRec(self):
        try:
            self.modo = "recepcion"
            self.suplidor.CargarSuplidores()
            self.suplidor.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CalcularImpuestoRecepcion(self, valor):
        try:
            cursor.execute("SELECT MAX(porcentaje) FROM tbimp07")
            data = cursor.fetchone()

            if data:
                porciento = float(data[0])
                impuesto = (porciento * float(valor)) / 100

                self.ui.itbrec18.setText(str(impuesto))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def MostrarProductoRecepcion(self):
        try:
            idpro = self.ui.idprorec18.text()
            resultado = self.VerificacionProducto(idpro)

            if resultado is False:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"El producto no existe")
                self.mensaje.show()

            else:
                for i in resultado:
                    self.ui.prerec18.setValue(float(i[7]))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def RellenarInfoOrd(self, datos):
        try:
            if datos:
                self.ui.tbrec18.setRowCount(len(datos))

                for i, row in enumerate(datos):

                    for j, value in enumerate(row):
                        total = float(row[2]) * float(row[3]) + float(row[4])
                        self.ui.tbrec18.setItem(i, j, QTableWidgetItem(str(value)))
                        self.ui.tbrec18.setItem(i, 5, QTableWidgetItem(str(total)))
                        self.ui.tbrec18.setItem(i, 6, QTableWidgetItem(str("0")))


                        self.ui.idsuprec18.setText(str(row[5]))
                        self.ui.nomsup18.setText(str(row[6]))
                        self.ui.dirsup18.setText(str(row[7]))
                        self.ui.telsup18.setText(str(row[8]))
                        self.ui.idsuc18.setText(str(row[9]))

                self.CalcularMontoRecepcion()


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CargarOrdRec(self):
        try:
            sql = "SELECT b.idpro, d.nompro, b.cantipen, d.precio, b.itebis, c.idsup, c.nombre, c.direccion, c.telefono, a.idsuc " \
                  "FROM tbordcommae01 a, tbordcomdet02 b, tbsup09 c, tbpro10 d " \
                  "WHERE a.idsup=c.idsup AND a.numord=b.numord AND d.idpro=b.idpro AND b.numord=%s AND b.cantipen > 0;"
            valores = (self.ui.numord18.text())
            cursor.execute(sql, valores)
            data = cursor.fetchall()

            if data:
                self.RellenarInfoOrd(data)

            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"La orden de compra que se ha ingresado ya esta completa o no existe")
                self.mensaje.show()


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def VerificacionSuplidor(self, idsuplidor):
        try:
            cursor.execute("SELECT * FROM tbsup09 WHERE idsup='"+idsuplidor+"'")
            data = cursor.fetchall()

            if data:
                return data
            else:
                return False

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CalcularImporteRecepcion(self):
        try:
            cantidad = self.ui.cantirec18.text()
            precio = self.ui.prerec18.text()

            total = float(cantidad) * float(precio)

            self.ui.imprec18.setValue(float(total))


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CalcularMontoRecepcion(self):

        try:
            total = 0
            rows = self.ui.tbrec18.rowCount()

            for row in range(rows):
                item = self.ui.tbrec18.item(row, 5)

                if item is not None:
                    valor = float(item.text())
                    total += valor

            self.ui.balrec18.setText(str(total))
            self.ui.monrec18.setText(str(total))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def InsertarProXSuC(self, idpro, idsuc, canti):
        try:
            global cantidad

            sql = "SELECT cantidad FROM tbproxsuc27 WHERE idpro=%s AND idsuc=%s"
            valores = (idpro, idsuc)
            cursor.execute(sql, valores)

            data = cursor.fetchall()

            if data:
                for j in data:
                    cantidad = j[0]
                total = float(cantidad) + float(canti)
                sqlsent = "UPDATE tbproxsuc27 SET cantidad=%s WHERE idpro=%s AND idsuc=%s"
                valor = (total, idpro, idsuc)

            else:
                sqlsent = "INSERT INTO tbproxsuc27 VALUES(%s, %s, %s)"
                valor = (idpro, idsuc, canti)

            cursor.execute(sqlsent, valor)
            conexion.commit()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def ActualizarCantiPen(self, idpro, cantidad):

        try:
            idsuc = self.ui.idsuc18.text()
            orden = self.ui.numord18.text()

            sql = "SELECT cantipen FROM tbordcomdet02 WHERE idpro=%s AND numord=%s"
            valores = (idpro, orden)
            cursor.execute(sql, valores)
            data = cursor.fetchone()


            if data:
                sql = "UPDATE tbordcomdet02 SET cantipen=cantipen - %s WHERE idpro=%s AND numord=%s"
                valores = (cantidad, idpro, orden)
                cursor.execute(sql, valores)
                conexion.commit()

                self.InsertarProXSuC(idpro, idsuc, cantidad)

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def ActualizarImporteRecepcion(self):
        try:
            cantidad = float(self.ui.cantirec18.text())
            precio = float(self.ui.prerec18.text())

            importe = cantidad * precio

            self.ui.imprec18.setValue(float(importe))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def AgregarElementoRecepcion(self):
        try:
            idpro = self.ui.idprorec18.text()
            cantidad = self.ui.cantirec18.text()
            importe = self.ui.imprec18.text()
            itebis = self.ui.itbrec18.text()
            devuelta = self.ui.cantidev18.text()

            filas = self.ui.tbrec18.rowCount()

            if not idpro or not cantidad or not importe or not itebis or not devuelta:
                self.mensaje.setIcon(QMessageBox.Critical)
                self.mensaje.setText(f"Todos los campos son obligatorios, debes llenarlos")
                self.mensaje.show()
            else:
                for f in range(filas):
                    celda = self.ui.tbrec18.item(f, 0)

                    if celda is not None:
                        if int(celda.text()) == int(idpro):
                            self.ui.tbrec18.setItem(f, 0, QTableWidgetItem(str(idpro)))
                            self.ui.tbrec18.setItem(f, 2, QTableWidgetItem(str(cantidad)))
                            self.ui.tbrec18.setItem(f, 4, QTableWidgetItem(str(itebis)))
                            self.ui.tbrec18.setItem(f, 5, QTableWidgetItem(str(importe)))
                            self.ui.tbrec18.setItem(f, 6, QTableWidgetItem(str(devuelta)))

                self.CalcularMontoRecepcion()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def EditarRecepcion(self):
        try:

            fila = self.ui.tbrec18.currentRow()
            columna = self.ui.tbrec18.columnCount()

            for c in range(columna):
                idpro = self.ui.tbrec18.item(fila, 0)
                cantidad = self.ui.tbrec18.item(fila, 2)
                precio = self.ui.tbrec18.item(fila, 3)
                itebis = self.ui.tbrec18.item(fila, 4)

                if idpro or cantidad or precio is not None:
                    self.ui.prerec18.setValue(float(precio.text()))
                    self.ui.cantirec18.setValue(float(cantidad.text()))
                    self.ui.idprorec18.setText(str(idpro.text()))
                    self.ui.itbrec18.setText(str(itebis.text()))


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def SalvarDetalleRecepcion(self):
        idsup = self.ui.idsuprec18.text()
        recibo = self.ui.norec18.text()
        filas = self.ui.tbrec18.rowCount()
        columnas = self.ui.tbrec18.columnCount()
        tupla = []

        for i in range(filas):
            datos = []
            for j in range(columnas):
                elemento = self.ui.tbrec18.item(i, j)
                if elemento is not None:
                    datos.append(elemento.text())
                else:
                    datos.append("")
            tupla.append(datos)


        for i in tupla:
            sql = "INSERT INTO tbrecdet19(norecep, idpro, cantidad, precio, itebis, cantidaddev) " \
                  "VALUES(%s, %s, %s, %s, %s, %s)"
            valores = (recibo, i[0], i[2], i[3], i[4], i[6])
            cursor.execute(sql, valores)
            conexion.commit()

            sql = "UPDATE tbpro10 SET ultsup=%s, costo=%s WHERE idpro=%s"
            valores = (idsup, i[3], i[0])
            cursor.execute(sql, valores)
            conexion.commit()

            self.ActualizarCantiPen(i[0], i[2])


    def LimpiarCampos(self):
        try:
            self.ui.idprorec18.clear()
            self.ui.prerec18.setValue(0.00)
            self.ui.cantirec18.setValue(0.00)
            self.ui.imprec18.setValue(0.00)
            self.ui.itbrec18.clear()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def RellenarMejPre(self):
        suptb = int(self.ui.idsuprec18.text())
        fecha = self.ui.fecrec18.text()

        filas = self.ui.tbrec18.rowCount()

        for f in range(filas):
            idprotb = self.ui.tbrec18.item(f, 0)
            preciotb = self.ui.tbrec18.item(f, 3)
            if idprotb and preciotb is not None:
                    
                sql = "SELECT costo, idsup FROM tbmejpre22 WHERE idpro=%s"
                valores = (idprotb.text())

                cursor.execute(sql, valores)
                data = cursor.fetchone()

                if data:
                    cosbas = float(data[0])
                    idsupbas = int(data[1])

                    if (float(preciotb.text()) < float(cosbas)) and (int(suptb) != int(idsupbas)):
                        sql = "UPDATE tbmejpre22 SET idsup=%s, costo=%s, fecha=%s WHERE idpro=%s"
                        valores = (suptb, float(preciotb.text()), fecha, idprotb.text())

                    elif (float(preciotb.text()) > float(cosbas)) and (int(suptb) == int(idsupbas)):
                        sql = "UPDATE tbmejpre22 SET costo=%s, fecha=%s WHERE idpro=%s"
                        valores = (float(preciotb.text()), fecha, idprotb.text())

                    cursor.execute(sql, valores)
                    conexion.commit()

                else:
                    sql = "INSERT INTO tbmejpre22 VALUES(%s, %s, %s, %s)"
                    valores = (idprotb.text(), suptb, preciotb.text(), fecha)

                    cursor.execute(sql, valores)
                    conexion.commit()



    def SalvarRecepcion(self):
        try:
            numrec = self.ui.norec18.text()
            idsuc = self.ui.idsuc18.text()
            idsup = self.ui.idsuprec18.text()
            nofac = self.ui.numfacrec18.text()
            monto = self.ui.monrec18.text()
            balance = self.ui.balrec18.text()
            condicion = self.ui.condrec18.text()
            ncf = self.ui.ncfrec18.text()
            celda = self.ui.tbrec18.item(0, 0)

            if celda is None:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"Debes agregar elementos a la tabla")
                self.mensaje.show()

            elif not numrec or not idsuc or not idsup or not nofac or not monto or not balance or not condicion or not ncf:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"Debes llenar todos los campos")
                self.mensaje.show()
            else:

                if int(condicion) == 0:
                    balance = 0
                else:
                    pass

                sql = "INSERT INTO tbrecmae18 VALUES(%s, %s, %s, %s, now(), %s, %s, %s, %s, %s)"
                valores = (numrec, self.codeusu, idsuc, idsup, nofac, monto, balance, condicion, ncf)
                cursor.execute(sql, valores)
                conexion.commit()

                self.SalvarDetalleRecepcion()
                self.RellenarMejPre()


                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText(f"La recepcion se ha completado correctamente")
                self.mensaje.show()

                self.NuevoRecepcion()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def ImprimirRecepcion(self):
        try:
            numord = self.ui.numord18.text()
            fecha = self.ui.fecrec18.text()
            nomsup = self.ui.nomsup18.text()
            telsup = self.ui.telsup18.text()
            monto = self.ui.monrec18.text()
            idsuc = self.ui.idsuc18.text()

            filas = self.ui.tbrec18.rowCount()
            columnas = self.ui.tbrec18.columnCount()
            tupla = []

            tabla = self.ui.tbrec18.item(0, 0)
            if tabla is None:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("No hay elementos en la tabla")
                self.mensaje.show()
            else:
                for f in range(filas):
                    datos = []
                    for c in range(columnas):
                        item = self.ui.tbrec18.item(f, c)
                        if item is not None:
                            datos.append(item.text())
                        else:
                            datos.append("")
                    tupla.append(datos)
                sumimp = self.CalcularImpuestoRecAux()
                self.reporte.ImprimirRec(numord, fecha, nomsup, telsup, monto, idsuc, sumimp, tupla)

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()




    def CalcularImpuestoRecAux(self):
        try:
            filas = self.ui.tbrec18.rowCount()
            total = 0
            for f in range(filas):
                celda = self.ui.tbrec18.item(f, 4)
                if celda is not None:
                    total += float(celda.text())
                else:
                    pass

            return total
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def NuevoRecepcion(self):
        try:
            self.ui.idsuprec18.clear()
            self.ui.nomsup18.clear()
            self.ui.dirsup18.clear()
            self.ui.telsup18.clear()
            self.ui.norec18.clear()
            self.ui.numfacrec18.clear()
            self.ui.idprorec18.clear()
            self.ui.prerec18.setValue(0.00)
            self.ui.cantirec18.setValue(1)
            self.ui.condrec18.setValue(0)
            self.ui.imprec18.setValue(0.00)
            self.ui.balrec18.clear()
            self.ui.itbrec18.clear()
            self.ui.fecrec18.clear()
            self.ui.monrec18.clear()
            self.ui.ncfrec18.clear()
            self.ui.idsuc18.clear()
            self.ui.numord18.clear()

            self.ui.tbrec18.clearContents()
            self.ui.tbrec18.setRowCount(0)

            self.GenerarIDRecepcion()
            self.ui.fecrec18.setText(str(self.GenerarFechaActual()))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GenerarIDRecepcion(self):
        try:

            global numero
            cont = "1"

            cursor.execute("SELECT MAX(norecep + 1) FROM tbrecmae18")
            data = cursor.fetchall()

            for i in data:
                numero = str(i[0])

            if numero == "None":
                self.ui.norec18.setText(cont)
            else:
                self.ui.norec18.setText(str(numero))


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()




########################################################################################################################
############################################## Movimiento de Pagos #####################################################
########################################################################################################################

    def VerificacionDocu(self):
        try:
            indice = self.ui.forpag16.currentIndex()

            if int(indice) == 0:
                self.ui.nodocupag16.setText("0")
                self.ui.nodocupag16.setDisabled(True)

                self.ui.banpag16.setCurrentIndex(0)
                self.ui.banpag16.setDisabled(True)
            else:
                self.ui.nodocupag16.setEnabled(True)
                self.ui.banpag16.setEnabled(True)
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrdio un error {ex}")
            self.mensaje.show()


    def VentanaClientePag(self):
        try:
            self.modo = "pago"
            self.cliente.CargarCliente()
            self.cliente.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GenerarIDPago(self):
        try:
            global numero
            cont = "1"

            cursor.execute("SELECT MAX(norecibo + 1) FROM tbpagmae16")
            data = cursor.fetchall()

            for i in data:
                numero = str(i[0])

            if numero == "None":
                self.ui.norecib16.setText(cont)
            else:
                self.ui.norecib16.setText(str(numero))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CargarFacturaPago(self):
        try:
            idcliente = self.ui.idclipag16.text()
            cursor.execute("SELECT nofac, fecha, monto, balance, condicion FROM tbfacmae20 WHERE "
                           "idcli='"+idcliente+"' AND condicion > 0 AND balance > 0")
            data = cursor.fetchall()

            if data:
                self.ui.tbpag16.setRowCount(len(data))

                for i, row in enumerate(data):
                    vencimiento = row[1] + datetime.timedelta(days=int(row[4]))
                    for j, value in enumerate(row):
                        self.ui.tbpag16.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
                        self.ui.tbpag16.setItem(i, 4, QtWidgets.QTableWidgetItem(str(vencimiento)))
                        self.ui.tbpag16.setItem(i, 5, QtWidgets.QTableWidgetItem(str("0.00")))

            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Este cliente no debe pagar ninguna factura")
                self.mensaje.show()

                self.ui.numpromo16.setDisabled(True)
                self.ui.monpromo16.setDisabled(True)
                self.ui.label_150.hide()
                self.ui.label_151.hide()

                self.NuevoPago()


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def LlenarComboBanco(self):
        try:
            cursor.execute("SELECT * FROM tbban06")
            data = cursor.fetchall()

            if data:
                for i in data:
                    banco = f"{i[0]}  - {i[1]}"
                    self.ui.banpag16.addItem(str(banco))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def VerificacionBono(self):
        try:
            bono = self.ui.numpromo16.text()
            cliente = self.ui.idclipag16.text()

            cursor.execute("SELECT numbon, monto FROM tbbon28 WHERE idcli='"+cliente+"' AND numbon='"+bono+"' AND estatus=1")
            data = cursor.fetchall()

            if data:

                for i in data:
                    self.ui.numpromo16.setText(str(i[0]))
                    self.ui.monpromo16.setValue(float(i[1]))
                    self.temp = float(i[1])

            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("El codigo ingresado no existe o ya fue canjeado")
                self.mensaje.show()

                self.ui.monpromo16.setValue(0.00)

                self.CargarFacturaPago()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def MostrarInfoClientePago(self):
        try:
            idcli = self.ui.idclipag16.text()
            verificacion = self.VerificacionCliente(idcli)

            if verificacion is False:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("El cliente ingresado no existe")
                self.mensaje.show()

                self.ui.numpromo16.setDisabled(True)
                self.ui.monpromo16.setDisabled(True)

                self.NuevoPago()

            else:
                for i in verificacion:
                    self.ui.nomclipag16.setText(str(i[1]))
                    self.ui.apeclipag16.setText(str(i[2]))
                    self.ui.telclipag16.setText(str(i[4]))

                    self.CargarFacturaPago()

                sql = "SELECT numbon, monto, estatus " \
                      "FROM tbbon28 a " \
                      "WHERE idcli=%s AND vencimiento >= current_date() AND fecha <= current_date() AND estatus=1;"

                valores = (idcli)
                cursor.execute(sql, valores)
                data = cursor.fetchone()


                if data and data[2] == 1:
                    self.ui.numpromo16.setEnabled(True)
                    self.ui.monpromo16.setEnabled(True)


                else:
                    self.ui.numpromo16.setDisabled(True)
                    self.ui.monpromo16.setDisabled(True)


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def RellenarFormPago(self):
        try:
            seleccion = self.ui.tbpag16.currentRow()
            bono = self.ui.monpromo16.text()
            factura = self.ui.tbpag16.item(seleccion, 0)
            balance = self.ui.tbpag16.item(seleccion, 3)

            if not factura or balance is not None:

                self.ui.nofacpag16.setText(str(factura.text()))
                self.ui.balpag16.setValue(float(balance.text()))

                if float(bono) >= float(balance.text()):
                    self.ui.monpromo16.setValue(float(balance.text()))
                    self.ui.monpag16.setDisabled(True)
                    self.ui.monpag16.setValue(0.00)
                else:
                    self.ui.monpag16.setEnabled(True)

                if float(bono) < float(balance.text()):
                    restante = float(balance.text()) - float(bono)
                    self.ui.monpag16.setMaximum(float(restante))
                    
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def ImprimirPago(self):
        try:
            idcli = self.ui.idclipag16.text()
            nomcli = self.ui.nomclipag16.text()
            telcli = self.ui.telclipag16.text()
            numrec = self.ui.norecib16.text()
            formpag = self.ui.forpag16.currentText()
            numdocu = self.ui.nodocupag16.text()
            banco = self.ui.banpag16.currentText()
            fecha = self.ui.fecpag16.text()

            filas = self.ui.tbpag16.rowCount()
            columnas = self.ui.tbpag16.columnCount()
            tupla = []

            tabla = self.ui.tbpag16.item(0, 0)
            if tabla is None or not idcli or not numrec or not formpag or not numdocu or not banco or not fecha:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes agregar elementos y recuerda no dejar campos en blanco")
                self.mensaje.show()
            else:
                for f in range(filas):
                    datos = []
                    for c in range(columnas):
                        item = self.ui.tbpag16.item(f, c)
                        if item is not None:
                            datos.append(item.text())
                        else:
                            datos.append("")
                    tupla.append(datos)

                total = self.CalularTotalPagado()
                self.reporte.ImprimirPag(idcli, nomcli, telcli, numrec, formpag, numdocu, banco, fecha, total, tupla)

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CalularTotalPagado(self):
        try:
            filas = self.ui.tbpag16.rowCount()
            total = 0

            for f in range(filas):
                monto = self.ui.tbpag16.item(f, 5)
                if monto is not None:
                    total += float(monto.text())
                else:
                    pass

            return total

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def GuardarCambiosPago(self):
        try:
            nofac = self.ui.nofacpag16.text()
            bono = self.ui.monpromo16.text()
            balance = float(self.ui.balpag16.text())


            filas = self.ui.tbpag16.rowCount()

            if not nofac:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes seleccionar una factura")
                self.mensaje.show()
            else:
                for f in range(filas):
                    celda = self.ui.tbpag16.item(f, 0)
                    if celda is not None:
                        if int(celda.text()) == int(nofac):
                            if float(bono) > 0.00:
                                monto = float(self.ui.monpag16.text()) + float(bono)
                                self.ui.monpromo16.setValue(0.00)

                            else:
                                monto = float(self.ui.monpag16.text())

                            restante = self.CalcularRestante(monto, balance)
                            self.ui.tbpag16.setItem(f, 5, QTableWidgetItem(str(monto)))
                            self.ui.tbpag16.setItem(f, 3, QTableWidgetItem(str(restante)))

                            break
                        else:
                            continue


                self.ui.monpag16.setValue(0.00)
                self.ui.balpag16.setValue(0.00)

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def SalvarPago(self):
        try:
            recibo = self.ui.norecib16.text()
            idcli = self.ui.idclipag16.text()
            idbanco = self.ui.banpag16.currentText()[0] + "" + \
                      self.ui.banpag16.currentText()[1] + "" + \
                      self.ui.banpag16.currentText()[2]
            formapag = self.ui.forpag16.currentText()[0]
            documento = self.ui.nodocupag16.text()
            observacion = self.ui.obspag16.text()
            numbono = self.ui.numpromo16.text()
            factura = self.ui.nofacpag16.text()

            filas = self.ui.tbpag16.rowCount()
            columna = self.ui.tbpag16.columnCount()
            tupla = []



            if not factura or not recibo or not idcli or not idbanco or not formapag or not documento or not observacion:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("No hay ninguna factura seleccionada, asegurate de seleccionar la factura con doble click y rellenando los campos en blanco ")
                self.mensaje.show()
            else:
                sql = "INSERT INTO tbpagmae16(norecibo, idcli, iduse, idbanco, fechapag, formpag, nodocu, observacion) VALUES(%s, %s, %s, %s, now(), %s, %s, %s)"
                valores = (recibo, idcli, self.codeusu, idbanco, formapag, documento, observacion)

                cursor.execute(sql, valores)
                conexion.commit()

                for f in range(filas):
                    datos = []
                    for c in range(columna):
                        celda = self.ui.tbpag16.item(f, c)
                        if celda is not None:
                            datos.append(celda.text())
                        else:
                            datos.append("")
                    tupla.append(datos)

                for i in tupla:
                    sql = "INSERT INTO tbpagdet17(norecibo, numfactura, montopag) VALUES(%s, %s, %s)"
                    valores = (recibo, i[0], i[5])

                    cursor.execute(sql, valores)
                    conexion.commit()

                    sql = "UPDATE tbfacmae20 SET balance=%s WHERE nofac=%s AND idcli=%s"
                    valores = (i[3], i[0], idcli)

                    cursor.execute(sql, valores)
                    conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText("El pago se ha realizado correctamente")
                self.mensaje.show()

                self.ui.numpromo16.setDisabled(True)
                self.ui.monpromo16.setDisabled(True)

                self.ui.numpromo16.clear()
                self.ui.monpromo16.setValue(0.00)

                if numbono:
                    sql = "UPDATE tbbon28 SET estatus=0 WHERE numbon=%s AND idcli=%s"
                    valores = (numbono, idcli)

                    cursor.execute(sql, valores)
                    conexion.commit()
                else:
                    pass

                self.NuevoPago()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevoPago(self):
        try:
            self.ui.monpag16.setEnabled(True)
            self.ui.idclipag16.clear()
            self.ui.nomclipag16.clear()
            self.ui.apeclipag16.clear()
            self.ui.telclipag16.clear()
            self.ui.norecib16.clear()
            self.ui.fecpag16.clear()
            self.ui.nodocupag16.clear()
            self.ui.nofacpag16.clear()
            self.ui.monpag16.setValue(0.00)
            self.ui.obspag16.clear()
            self.ui.tbpag16.setRowCount(0)
            self.ui.tbpag16.clearContents()
            self.ui.balpag16.setValue(0.00)
            self.ui.monpromo16.setValue(0.00)
            self.ui.forpag16.setCurrentIndex(-1)
            self.ui.banpag16.setCurrentIndex(0)

            self.ui.numpromo16.setDisabled(True)
            self.ui.monpromo16.setDisabled(True)
            self.ui.numpromo16.clear()
            self.ui.monpromo16.setValue(0.00)

            self.ui.fecpag16.setText(str(self.GenerarFechaActual()))
            self.GenerarIDPago()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



########################################################################################################################
############################################## Movimiento de Facturacion ###############################################
########################################################################################################################

    def RemplazaProductoDuplicado(self, nofac, idpro):
        global fac, pro, dec
        try:
            dec = False
            fila = self.ui.tbfac20.rowCount()

            for i in range(fila):
                columfac = self.ui.tbfac20.item(i, 0)
                columpro = self.ui.tbfac20.item(i, 1)

                if columfac and columpro is not None:
                    if columfac.text() == nofac and columpro.text() == idpro:
                        self.ui.tbfac20.setItem(i, 2, QTableWidgetItem(self.ui.cantiprofac20.text()))
                        self.ui.tbfac20.setItem(i, 3, QTableWidgetItem(self.ui.canprofac20.text()))
                        self.ui.tbfac20.setItem(i, 4, QTableWidgetItem(self.ui.prefac20.text()))
                        self.ui.tbfac20.setItem(i, 5, QTableWidgetItem(self.ui.iptfac20.text()))
                        self.ui.tbfac20.setItem(i, 6, QTableWidgetItem(self.ui.impfac20.text()))
                        dec = True
                        break
                    else:
                        dec = False

            return dec

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def VentanaProductoFac(self):
        try:
            self.modo = "factura"
            self.producto.CargarProductos()
            self.producto.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def VentanaClienteFac(self):
        try:
            self.modo = "factura"
            self.cliente.CargarCliente()
            self.cliente.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CalcularMontoNetoFac(self):
        try:

            total = 0
            rows = self.ui.tbfac20.rowCount()

            for row in range(rows):
                importe = self.ui.tbfac20.item(row, 5)
                itebis = self.ui.tbfac20.item(row, 4)


                if importe and itebis is not None:
                    impor = float(importe.text())
                    iteb = float(itebis.text())
                    suma = float(impor) + float(iteb)

                    total += suma
            self.ui.balfac20.setText(str(total))
            self.ui.monntfac20.setText(str(total))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def MostrarInfoProducto(self):
        try:
            idproducto = self.ui.numprofac20.text()
            resultado = self.VerificacionProducto(idproducto)

            if resultado is False:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("El producto que has insertado no existe")
                self.mensaje.show()
                self.ui.numprofac20.setFocus()

                self.ui.numprofac20.clear()
                self.ui.canprofac20.clear()
                self.ui.prefac20.setValue(0.00)

            else:
                for i in resultado:

                    self.ui.canprofac20.setText("{:.2f}".format(float(i[7])))
                    self.ui.prefac20.setValue(i[8])
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()
    """
    def MandarSugerencia(self, productos):
        try:
            telefono_real = ""
            telefono = self.ui.telclifac20.text()
            # Crear el cliente de Twilio
            client = Client(self.account_sid, self.auth_token)
            # Enviar el MMS
            for i in telefono:
                if i.isdigit():
                    telefono_real+=i

            mensaje_body = 'De parte de nuestra empresa hemos analizado tus gustos y te recomendamos los siguientes productos\n \n' + '\n'.join([f'• {producto}' for producto in productos])

            client.messages.create(
                body=mensaje_body,
                from_='+16317214409',
                to=f'+1{telefono_real}'
            )

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()
            
        """

    def MostrarInfoCliente(self):
        try:
            idcliente = self.ui.idclifac20.text()
            resultados = self.VerificacionCliente(idcliente)

            if resultados is False:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("El cliente que has insertado no existe")
                self.mensaje.show()
                self.ui.idclifac20.setFocus()

                self.ui.nomclifac20.clear()
                self.ui.apeclifac20.clear()
                self.ui.telclifac20.clear()
            else:

                for i in resultados:
                    self.ui.nomclifac20.setText(str(i[1]))
                    self.ui.apeclifac20.setText(str(i[2]))
                    self.ui.telclifac20.setText(str(i[4]))

                """cursor.execute("SELECT nofac FROM tbfacmae20 WHERE idcli='" + idcliente + "'")
                if cursor.fetchall():
                    productos_recomendados = self.Prediccion.Recomendar(int(idcliente))
                    if productos_recomendados:
                        self.MandarSugerencia(productos_recomendados)

                else:
                    pass
"""




        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def VerificacionProducto(self, producto):
        try:
            cursor.execute("SELECT * FROM tbpro10 WHERE idpro='" + producto + "'")
            data = cursor.fetchall()

            if data:
                return data

            else:
                return False
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def VerificacionCliente(self, cliente):
        try:
            cursor.execute("SELECT * FROM tbcli03 WHERE idcli='"+cliente+"'")
            data = cursor.fetchall()

            if data:
                return data

            else:
                return False
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def GenerarIDFactura(self):
        try:
            global numero
            cont = "1"

            cursor.execute("SELECT MAX(nofac + 1) FROM tbfacmae20")
            data = cursor.fetchall()

            for i in data:
                numero = str(i[0])

            if numero == "None":
                self.ui.nofac20.setText(cont)
            else:
                self.ui.nofac20.setText(str(numero))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def AgregarFacturaTabla(self):

        try:
            nofac = self.ui.nofac20.text()
            idpro = self.ui.numprofac20.text()
            cantidad = self.ui.cantiprofac20.text()
            precio = self.ui.prefac20.text()
            itebis = self.ui.impfac20.text()
            importe = self.ui.iptfac20.text()
            existencia = self.ui.canprofac20.text()


            if not nofac or not idpro or not cantidad or not existencia or not precio \
                    or not importe:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes llenar todos los campos antes de agregar el producto")
                self.mensaje.show()

            else:
                try:

                    resultados = self.RemplazaProductoDuplicado(nofac, idpro)

                    if resultados is False:
                        filas = self.ui.tbfac20.rowCount()
                        self.ui.tbfac20.insertRow(filas)
                        self.ui.tbfac20.setItem(filas, 0, QTableWidgetItem(nofac))
                        self.ui.tbfac20.setItem(filas, 1, QTableWidgetItem(idpro))
                        self.ui.tbfac20.setItem(filas, 2, QTableWidgetItem(cantidad))
                        self.ui.tbfac20.setItem(filas, 3, QTableWidgetItem(precio))
                        self.ui.tbfac20.setItem(filas, 4, QTableWidgetItem(itebis))
                        self.ui.tbfac20.setItem(filas, 5, QTableWidgetItem(importe))
                        self.ui.tbfac20.setItem(filas, 6, QTableWidgetItem(existencia))

                    else:
                        pass

                    self.NuevaFactura()
                    self.CalcularMontoNetoFac()
                    self.ui.numprofac20.clear()
                    self.ui.numprofac20.setFocus()


                except Exception as ex:
                    self.mensaje.setIcon(QMessageBox.Critical)
                    self.mensaje.setText(f"Ha ocurrido un error {ex}")
                    self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def EliminarFacturaTabla(self):
        try:
            seleccion = self.ui.tbfac20.selectionModel().selectedRows()

            if not seleccion:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes seleccionar un elemento")
                self.mensaje.show()
            else:
                for row in seleccion:
                    self.ui.tbfac20.removeRow(row.row())

                self.CalcularMontoNetoFac()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevaFactura(self):
        try:

            self.ui.nofac20.clear()
            self.ui.numprofac20.clear()
            self.ui.canprofac20.clear()
            self.ui.prefac20.setValue(0.00)
            self.ui.fechfac20.clear()
            self.ui.cantiprofac20.setValue(1)
            self.ui.iptfac20.setValue(0.00)
            self.ui.condfac20.setValue(0)
            self.ui.impfac20.clear()
            self.ui.ncffac20.clear()



            self.GenerarIDFactura()
            self.ui.fechfac20.setText(str(self.GenerarFechaActual()))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def RebajarCantidadExistenciaProducto(self, idpro, cantidad, sucursal):

        global canti

        sql = "SELECT cantidad FROM tbproxsuc27 WHERE idpro=%s AND idsuc=%s"
        valores = (idpro, sucursal)
        cursor.execute(sql, valores)
        data = cursor.fetchall()

        if data:
            for i in data:
                canti = i[0]
            sql = "UPDATE tbproxsuc27 SET cantidad=%s WHERE idpro=%s AND idsuc=%s"
            total = float(canti) - float(cantidad)
            valores = (total, idpro, sucursal)

            cursor.execute(sql, valores)
            conexion.commit()



    def SalvarFacturaDetalle(self):
        celda = self.ui.tbfac20.item(0, 0)

        if celda is None:
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.setText("No hay productos agregados")
            self.mensaje.show()
        else:
            filas = self.ui.tbfac20.rowCount()
            columnas = self.ui.tbfac20.columnCount()
            tupla = []

            for i in range(filas):
                dato = []
                for j in range(columnas):
                    celda = self.ui.tbfac20.item(i, j)
                    if celda is not None:
                        dato.append(celda.text())
                    else:
                        dato.append("")
                tupla.append(dato)

            for i in tupla:
                sql = "INSERT INTO tbfacdet21(nofac, idpro, cantipro, prepro, itebis) VALUES(%s, %s, %s, %s, %s)"
                valores = (i[0], i[1], i[2], i[3], i[4])

                cursor.execute(sql, valores)
                conexion.commit()

                self.RebajarCantidadExistenciaProducto(i[1], i[2], self.suc)

            self.mensaje.setIcon(QMessageBox.Information)
            self.mensaje.setText("La factura se ha completado correctamente")
            self.mensaje.show()

            self.NuevaFactura()
            self.ui.tbfac20.setRowCount(0)
            self.ui.tbfac20.clearContents()
            self.ui.balfac20.clear()

            self.ui.idclifac20.clear()
            self.ui.nomclifac20.clear()
            self.ui.apeclifac20.clear()
            self.ui.telclifac20.clear()


    def SalvarFactura(self):
        try:
            tabla = self.ui.tbfac20.item(0, 0)
            numfac = self.ui.nofac20.text()
            idcli = self.ui.idclifac20.text()
            condicion = self.ui.condfac20.text()
            monto = self.ui.monntfac20.text()
            balance = self.ui.balfac20.text()
            ncf = self.ui.ncffac20.text()
            estatus = self.ui.estfac20.currentText()[0]


            if int(condicion) == 0:
                balance = 0.00
            else:
                pass

            if not numfac or not idcli or not monto or not balance or not estatus:
                self.mensaje.setIcon(QMessageBox.Critical)
                self.mensaje.setText(f"Debes llenar en blanco los campos")
                self.mensaje.show()
            else:
                if tabla is None:
                    self.mensaje.setIcon(QMessageBox.Critical)
                    self.mensaje.setText(f"Debes agregar un elemento a la tabla")
                    self.mensaje.show()
                else:
                    sql = "INSERT INTO tbfacmae20(nofac, idcli, iduse, idsuc, fecha, condicion, monto, balance, ncf, estatus)" \
                          "VALUES(%s, %s, %s, %s, now(), %s, %s, %s, %s, %s)"
                    valores = (numfac, idcli, self.codeusu, self.suc, condicion, monto, balance, ncf, estatus)

                    cursor.execute(sql, valores)
                    conexion.commit()

                    self.SalvarFacturaDetalle()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def ImprimirFactura(self):
        try:
            nofac = self.ui.nofac20.text()
            fecha = self.ui.fechfac20.text()
            nomcli = self.ui.nomclifac20.text()
            apecli = self.ui.apeclifac20.text()
            telcli = self.ui.telclifac20.text()
            ncf = self.ui.ncffac20.text()
            monto = self.ui.monntfac20.text()

            filas = self.ui.tbfac20.rowCount()
            columnas = self.ui.tbfac20.columnCount()
            tupla = []

            tabla = self.ui.tbfac20.item(0, 0)
            if tabla is None:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("No hay elementos en la tabla")
                self.mensaje.show()
            else:
                for f in range(filas):
                    datos = []
                    for c in range(columnas):
                        item = self.ui.tbfac20.item(f, c)
                        if item is not None:
                            datos.append(item.text())
                        else:
                            datos.append("")
                    tupla.append(datos)
                sumimp = self.TotalImp()
                self.reporte.ImprimirFac(sumimp, monto, ncf, nofac, fecha, nomcli, apecli, telcli, tupla)

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def TotalImp(self):
        try:
            total = 0
            filas = self.ui.tbfac20.rowCount()

            for f in range(filas):
                itebis = self.ui.tbfac20.item(f, 4)
                if itebis is not None:
                    total += float(itebis.text())
                else:
                    pass

            return total
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CalcularImpuesto(self, valor):
        try:
            cursor.execute("SELECT MAX(porcentaje) FROM tbimp07")
            data = cursor.fetchone()

            if data:
                porciento = float(data[0])
                impuesto = (porciento * float(valor)) / 100

                self.ui.impfac20.setText(str(impuesto))


            else:
                self.mensaje.setIcon(QMessageBox.Critical)
                self.mensaje.setText("No existe ningun impuesto")
                self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def CalcularImporteFactura(self):
        try:
            precio = self.ui.prefac20.text()
            cantidad = self.ui.cantiprofac20.text()

            total = float(precio) * float(cantidad)
            self.ui.iptfac20.setValue(total)


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

########################################################################################################################
######################################## Mantenimiento de Empresa ######################################################
########################################################################################################################


    def VisualEmpresa(self):
        try:
            if self.ui.btnvisualemp32.isChecked():
                icono = QIcon("iconos_negros/eye.svg")
                self.ui.claveemp32.setEchoMode(QLineEdit.Normal)
            else:
                icono = QIcon("iconos_negros/eye-off.svg")
                self.ui.claveemp32.setEchoMode(QLineEdit.Password)

            self.ui.btnvisualemp32.setIcon(icono)

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def GuardarEmpresa(self):
        try:
            idempresa = self.ui.nomemp32.text()
            rnc = self.ui.rncemp32.text()
            eslogan = self.ui.eslemp32.text()
            correo = self.ui.corremp32.text()
            clave = self.ui.claveemp32.text()
            telefono = self.ui.telemp32.text()
            fundacion = self.ui.fechaemp32.text()

            if not idempresa or not correo or not telefono or not fundacion or not rnc or not clave:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"Rellena todos los campos en blanco")
                self.mensaje.show()
            else:
                pixmap = self.ui.imglog32.pixmap()

                if pixmap is not None:
                    with open(self.archivo, 'rb') as image_file:
                        image_blob = image_file.read()

                    cursor.execute("SELECT nombre FROM tbemp32 WHERE nombre='"+idempresa+"'")
                    if cursor.fetchall():

                        sql = "UPDATE tbemp32 SET fundacion=%s, rnc=%s, eslogan=%s, correo=%s, clave=%s, telefono=%s, logo=%s WHERE nombre=%s"
                        valores = (fundacion, rnc, eslogan, correo, clave, telefono, image_blob, idempresa)
                    else:
                        sql = "INSERT INTO tbemp32(nombre, rnc, fundacion, eslogan, correo, clave, telefono, logo) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
                        valores = (idempresa, rnc, fundacion, eslogan, correo, clave, telefono, image_blob)

                    cursor.execute(sql, valores)
                    conexion.commit()

                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.setText(f"El registro se ha guardado correctamente")
                    self.mensaje.show()

                    self.NuevaEmpresa()
                else:
                    self.mensaje.setIcon(QMessageBox.Warning)
                    self.mensaje.setText("El logo es obligatorio")
                    self.mensaje.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def EliminarEmpresa(self):
        try:
            idempresa = self.ui.nomemp32.text()

            if not idempresa:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"Primero inserte un ID para eliminar")
                self.mensaje.show()
            else:
                cursor.execute("DELETE FROM tbemp32 WHERE nombre='"+idempresa+"'")
                conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText(f"El registro se ha eliminado correctamente")
                self.mensaje.show()

                self.NuevaEmpresa()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def RellenarEmpresa(self):
        try:
            idempresa = self.ui.nomemp32.text()

            sql = "SELECT nombre, rnc, fundacion, eslogan, correo, clave, telefono, logo FROM tbemp32 WHERE nombre=%s"
            valor = (idempresa)
            cursor.execute(sql, valor)

            data = cursor.fetchall()

            if data:
                for i in data:
                    imagen = i[7]
                    self.ui.rncemp32.setText(str(i[1]))
                    self.ui.nomemp32.setText(str(i[0]))
                    self.ui.fechaemp32.setDate(i[2])
                    self.ui.eslemp32.setText(str(i[3]))
                    self.ui.corremp32.setText(str(i[4]))
                    self.ui.claveemp32.setText(str(i[5]))
                    self.ui.telemp32.setText(str(i[6]))

                    pixmap = self.BytesPixmap(imagen)
                    self.ui.imglog32.setPixmap(pixmap)
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevaEmpresa(self):
        try:
            self.ui.rncemp32.clear()
            self.ui.nomemp32.clear()
            self.ui.eslemp32.clear()
            self.ui.corremp32.clear()
            self.ui.telemp32.clear()
            self.ui.claveemp32.clear()
            self.ui.imglog32.clear()

            fecha = QDate.currentDate()
            self.ui.fechaemp32.setDate(fecha)

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

########################################################################################################################
######################################## Mantenimiento de Factor Conversion ############################################
########################################################################################################################

    def VentanaProConv(self):
        try:
            self.modo = "conversion"
            self.producto.CargarProductos()
            self.producto.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevoConversion(self):
        try:
            self.ui.idproconv11.clear()
            self.ui.univenconv11.clear()
            self.ui.faccanconv11.setValue(0.00)
            self.ui.facpreconv11.setValue(0.00)


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def EliminarConversion(self):
        try:
            idpro = self.ui.idproconv11.text()
            univent = self.ui.univenconv11.text()

            if not idpro or not univent:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"Antes de rellenar el formulario debes insertar el producto y la unidad de venta")
                self.mensaje.show()
            else:
                cursor.execute("DELETE FROM tbfaccon11 WHERE idpro='"+idpro+"' AND univent='"+univent+"'")
                conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText(f"El registro se ha eliminado correctamente")
                self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GuardarConversion(self):
        try:
            idpro = self.ui.idproconv11.text()
            univent = self.ui.univenconv11.text()
            faccantidad = self.ui.faccanconv11.text()
            facprecio = self.ui.facpreconv11.text()

            if not idpro or not univent or not faccantidad or not facprecio:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes rellenar todos los campos")
                self.mensaje.show()
            else:
                cursor.execute("SELECT idpro, univent FROM tbfaccon11 WHERE idpro='"+idpro+"' AND univent='"+univent+"'")
                if cursor.fetchall():
                    sql = "UPDATE tbfaccon11 SET factorcant=%s, factorprecio=%s WHERE idpro=%s AND univent=%s"
                    valores = (faccantidad, facprecio, idpro, univent)
                else:
                    sql = "INSERT INTO tbfaccon11 VALUES(%s, %s, %s, %s)"
                    valores = (idpro, univent, faccantidad, facprecio)

                cursor.execute(sql, valores)
                conexion.commit()

                self.mensaje.setIcon(QMessageBox.Critical)
                self.mensaje.setText(f"El registro se ha guardado correctamente")
                self.mensaje.show()

                self.NuevoConversion()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def RellenarConversion(self):
        try:
            idpro = self.ui.idproconv11.text()
            univen = self.ui.univenconv11.text()

            if not idpro or not univen:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"Antes de rellenar el formulario debes insertar el producto y la unidad de venta")
                self.mensaje.show()
            else:
                cursor.execute("SELECT factorcant, factorprecio FROM tbfaccon11 WHERE idpro='"+idpro+"' AND univent='"+univen+"'")
                data = cursor.fetchall()

                if data:
                    for i in data:
                        self.ui.faccanconv11.setValue(float(i[0]))
                        self.ui.facpreconv11.setValue(float(i[1]))
                else:
                    pass

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

########################################################################################################################
######################################### Mantenimiento de SecuenciaNCF ################################################
########################################################################################################################

    def NuevoNCF(self):
        try:
            self.ui.tipncf05.clear()
            self.ui.secinincf05.clear()
            self.ui.secfinncf05.clear()
            self.ui.fechaini05.clear()
            self.ui.fechafin05.clear()


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GuardarNCF(self):
        try:
            idsec = self.ui.idncf05.text()
            tipo = self.ui.tipncf05.text()
            secini = self.ui.secinincf05.text()
            secfin = self.ui.secfinncf05.text()
            fechaini = self.ui.fechaini05.text()
            fechafin = self.ui.fechafin05.text()

            if not idsec or not tipo or not secini or not secfin or not fechaini or not fechafin:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes rellenar todos los campos")
                self.mensaje.show()
            else:
                cursor.execute("SELECT secncf FROM tbncf05 WHERE secncf='"+idsec+"'")
                if cursor.fetchall():
                    sql = "UPDATE tbncf05 SET tipncf=%s, secini=%s, secfin=%s, fechaini=%s, fechafin=%s WHERE secncf=%s"
                    valores = (tipo, secini, secfin, fechaini, fechafin, idsec)
                else:
                    sql = "INSERT INTO tbncf05 VALUES(%s, %s, %s, %s, %s, %s)"
                    valores = (idsec, tipo, secini, secfin, fechaini, fechafin)

                cursor.execute(sql, valores)
                conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText(f"El registro se ha guardado correctamente")
                self.mensaje.show()

                self.NuevoNCF()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def EliminarNCF(self):
        try:
            idsecuencia = self.ui.idncf05.text()

            if not idsecuencia:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes ingresar un ID de secuencia")
                self.mensaje.show()
            else:
                cursor.execute("DELETE FROM tbncf05 WHERE secncf='"+idsecuencia+"'")
                conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText(f"El registro se ha eliminado correctamente")
                self.mensaje.show()

                self.NuevoNCF()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def RellenarNCF(self):
        try:
            idsec = self.ui.idncf05.text()
            
            cursor.execute("SELECT tipncf, secini, secfin, fechaini, fechafin FROM tbncf05 WHERE secncf='"+idsec+"'")
            data = cursor.fetchall()

            if data:
                for i in data:
                    self.ui.tipncf05.setText(str(i[0]))
                    self.ui.secinincf05.setText(str(i[1]))
                    self.ui.secfinncf05.setText(str(i[2]))
                    self.ui.fechaini05.setText(str(i[3]))
                    self.ui.fechafin05.setText(str(i[4]))
            else:
                self.NuevoNCF()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


########################################################################################################################
############################################## Mantenimiento de Razones ################################################
########################################################################################################################

    def GuardarRazon(self):
        try:
            idrazon = self.ui.idraz31.text()
            descripcion = self.ui.desraz31.toPlainText()

            if idrazon or not descripcion:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes rellenar los campos en blanco")
                self.mensaje.show()
            else:
                cursor.execute("SELECT idrazon FROM tbraz31 WHERE idrazon='"+idrazon+"'")
                if cursor.fetchall():

                    sql = "UPDATE tbraz31 SET descripcion=%s WHERE idrazon=%s"
                    valores = (descripcion, idrazon)
                else:
                    sql = "INSERT INTO tbraz31 VALUES(%s, %s)"
                    valores = (idrazon, descripcion)

                cursor.execute(sql, valores)
                conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText(f"El registro se ha guardado correctamente")
                self.mensaje.show()

                self.NuevaRazon()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def EliminarRazon(self):
        try:
            idrazon = self.ui.idraz31.text()

            if not idrazon:
                self.mensaje.setIcon(QMessageBox.Critical)
                self.mensaje.setText(f"Ingresa un ID de razon antes de eliminar")
                self.mensaje.show()
            else:
                cursor.execute("DELETE FROM tbraz31 WHERE idrazon='"+idrazon+"'")
                conexion.commit()

                self.mensaje.setText(f"El registro se ha eliminado correctamente")
                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevaRazon(self):
        try:
            self.ui.idraz31.clear()
            self.ui.desraz31.clear()

            self.GenerarIDRazon()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def RellenarRazon(self):
        try:
            idrazon = self.ui.idraz31.text()
            cursor.execute("SELECT idrazon, descripcion FROM tbraz31 WHERE idrazon='"+idrazon+"'")
            data = cursor.fetchall()

            if data:
                for i in data:
                    self.ui.idraz31.setText(str(i[0]))
                    self.ui.desraz31.setText(str(i[1]))
            else:

                self.NuevaRazon()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GenerarIDRazon(self):
        try:
            global numero

            cont = "1"

            cursor.execute("SELECT MAX(idrazon + 1) FROM tbraz31")
            data = cursor.fetchall()

            for i in data:
                numero = str(i[0])

            if numero == "None":
                self.ui.idraz31.setText(cont)
            else:
                self.ui.idraz31.setText(str(numero))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


########################################################################################################################
############################################## Mantenimiento de Sucursal ###############################################
########################################################################################################################

    def VentanaBusSucMnt(self):
        try:
            self.sucursal.CargarSucursal()
            self.sucursal.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GuardarSucursal(self):
        try:
            idsuc = self.ui.idsuc26.text()
            idprov = self.ui.idprov26.currentIndex() + 1
            nomsuc = self.ui.nomsuc26.text()
            direccion = self.ui.dirsuc26.toPlainText()
            telefono = self.ui.telsup26.text()

            if not idsuc or not idprov or not nomsuc or not direccion or not telefono:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes rellenar todos los campos en blanco")
                self.mensaje.show()
            else:

                cursor.execute("SELECT * FROM tbsuc26 WHERE idsuc='"+idsuc+"'")
                data = cursor.fetchall()

                if data:
                    sql = "UPDATE tbsuc26 SET idprov=%s, nombre=%s, direccion=%s, telefono=%s, creacion=now() WHERE idsuc=%s"
                    valores = (idprov, nomsuc, direccion, telefono, idsuc)

                else:
                    sql = "INSERT INTO tbsuc26 VALUES(%s, %s, %s, %s, %s, now())"
                    valores = (idsuc, idprov, nomsuc, direccion, telefono)

                cursor.execute(sql, valores)
                conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText("El registro se ha guardado correctamente")
                self.mensaje.show()

                self.NuevoSucursal()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def EliminarSucursal(self):
        try:
            idsuc = self.ui.idsuc26.text()

            if not idsuc:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes ingresar un ID para poder eliminar el registro")
                self.mensaje.show()
            else:
                cursor.execute("DELETE FROM tbsuc26 WHERE idsuc='"+idsuc+"'")
                conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText("El registro se ha eliminado corretcamente")
                self.mensaje.show()

                self.NuevoSucursal()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def RellenarSucursal(self):
        try:
            idsuc = self.ui.idsuc26.text()

            cursor.execute("SELECT idsuc, idprov, nombre, direccion, telefono FROM tbsuc26 WHERE idsuc='"+idsuc+"'")
            data = cursor.fetchall()

            if data:
                for i in data:
                    self.ui.idsuc26.setText(str(i[0]))
                    self.ui.idprov26.setCurrentIndex(int(i[1]) - 1)
                    self.ui.nomsuc26.setText(str(i[2]))
                    self.ui.dirsuc26.setPlainText(str(i[3]))
                    self.ui.telsup26.setText(str(i[4]))
            else:
                self.NuevoSucursal()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevoSucursal(self):
        try:
            self.ui.idsuc26.clear()
            self.ui.idprov26.setCurrentIndex(0)
            self.ui.nomsuc26.clear()
            self.ui.dirsuc26.clear()
            self.ui.telsup26.clear()

            self.GenerarIDSucursal()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def LlenarComboSucursal(self):
        try:
            cursor.execute("SELECT nombre FROM tbprov25")
            data = cursor.fetchall()

            if data:
                for i in data:
                    self.ui.idprov26.addItem(str(i[0]))
            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"No existe provincias en este sistema")
                self.mensaje.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GenerarIDSucursal(self):
        try:
            global numero

            cont = "1"

            cursor.execute("SELECT MAX(idsuc + 1) FROM tbsuc26")
            data = cursor.fetchall()

            for i in data:
                numero = str(i[0])

            if numero == "None":
                self.ui.idsuc26.setText(cont)
            else:
                self.ui.idsuc26.setText(str(numero))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



########################################################################################################################
############################################## Mantenimiento de Provincia ##############################################
########################################################################################################################

    def VentanaBusProvMnt(self):
        try:
            self.provincia.CargarProvincia()
            self.provincia.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def GuardarProv(self):
        try:
            idprov = self.ui.idprov25.text()
            nombre = self.ui.nomprov25.text()

            if not idprov or not nombre:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes rellenar todos los campos en blanco")
                self.mensaje.show()
            else:
                cursor.execute("SELECT * FROM tbprov25 WHERE idprov='"+idprov+"'")
                data = cursor.fetchall()

                if data:
                    sql = "UPDATE tbprov25 SET nombre=%s, creacion=now() WHERE idprov=%s"
                    valores = (nombre, idprov)

                else:
                    sql = "INSERT INTO tbprov25 VALUES(%s, %s, now())"
                    valores = (idprov, nombre)

                cursor.execute(sql, valores)
                conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText(f"El registro se ha modificado correctamente")
                self.mensaje.show()

                self.ui.idprov26.clear()
                self.LlenarComboSucursal()

                self.NuevoProv()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def EliminarProv(self):
        try:
            idprov = self.ui.idprov25.text()

            if not idprov:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"Debes ingresar un ID para poder eliminar una provincia")
                self.mensaje.show()
            else:
                cursor.execute("DELETE FROM tbprov25 WHERE idprov='"+idprov+"'")
                conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText("El registro se ha eliminado correctamente")
                self.mensaje.show()

                self.ui.idprov26.clear()
                self.LlenarComboSucursal()

                self.NuevoProv()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevoProv(self):
        try:
            self.ui.idprov25.clear()
            self.ui.nomprov25.clear()

            self.GenerarIDProv()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GenerarIDProv(self):
        try:
            global numero
            cont = "1"

            cursor.execute("SELECT MAX(idprov + 1) FROM tbprov25")
            data = cursor.fetchall()

            for i in data:
                numero = str(i[0])

            if numero == "None":
                self.ui.idprov25.setText(cont)
            else:
                self.ui.idprov25.setText(str(numero))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def RellenarProv(self):
        try:

            idprov = self.ui.idprov25.text()

            cursor.execute("SELECT idprov, nombre FROM tbprov25 WHERE idprov='"+idprov+"'")
            data = cursor.fetchall()

            if data:

                for i in data:
                    self.ui.idprov25.setText(str(i[0]))
                    self.ui.nomprov25.setText(str(i[1]))
            else:
                self.NuevoProv()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



########################################################################################################################
############################################## Mantenimiento de Rol-Programa ###########################################
########################################################################################################################

    def DesmarcarTodo(self):
        try:
            filas = self.ui.tablaroles.rowCount()

            for i in range(filas):
                checkbox = QCheckBox()
                checkbox.setCheckState(Qt.Unchecked)
                self.ui.tablaroles.setCellWidget(i, 3, checkbox)
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def MarcarTodo(self):
        try:
            filas = self.ui.tablaroles.rowCount()

            for i in range(filas):
                checkbox = QCheckBox()
                checkbox.setCheckState(Qt.Checked)
                self.ui.tablaroles.setCellWidget(i, 3, checkbox)

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GuardarRol(self):
        try:

            global valor, modo

            filas = self.ui.tablaroles.rowCount()

            for f in range(filas):
                programa = self.ui.tablaroles.item(f, 0)
                item = self.ui.tablaroles.cellWidget(f, 3)

                cursor.execute("SELECT a.iduse, a.idprg "
                               "FROM tbprgxusu24 a, tbusu08 b, tbprg23 c "
                               "WHERE a.iduse='"+self.ui.idusu24.text()+"' AND a.iduse=b.iduse AND a.idprg='"+programa.text()+"' AND a.idprg=c.idprg;")

                if cursor.fetchall():
                    modo = "modificar"
                else:
                    modo = "guardar"""

                if programa is not None:
                    if isinstance(item, QCheckBox):
                        if item.isChecked():
                            valor = 1
                        else:
                            valor = 0

                    if modo == "modificar":

                        sql = "UPDATE tbprgxusu24 SET acceso=%s WHERE iduse=%s AND idprg=%s"
                        valores = (valor, self.ui.idusu24.text(), programa.text())
                        cursor.execute(sql, valores)
                        conexion.commit()
                    else:
                        sql = "INSERT INTO tbprgxusu24 VALUES(%s, %s, %s)"
                        valores = (self.ui.idusu24.text(), programa.text(), valor)
                        cursor.execute(sql, valores)
                        conexion.commit()

            self.mensaje.setIcon(QMessageBox.Information)
            self.mensaje.setText(f"Se ha modificado correctamente los permisos")
            self.mensaje.show()

            self.ui.tablaroles.setRowCount(0)
            self.ui.tablaroles.clearContents()

            self.CargarDatos()
            self.ui.idusu24.clear()
            self.Verificacion()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def Verificacion(self):
        try:
            sql = "SELECT b.iduse, a.nombre, b.acceso " \
                  "FROM tbprg23 a, tbprgxusu24 b, tbusu08 c " \
                  "WHERE c.iduse=%s AND b.iduse=c.iduse AND b.idprg=a.idprg AND b.acceso=0;"
            valores = (self.codeusu)

            cursor.execute(sql, valores)

            data = cursor.fetchall()
            if data:
                for i in data:
                    concatenacion = "self.ui."+i[1]+".hide()"
                    exec(concatenacion)

            sql = "SELECT b.iduse, a.nombre, b.acceso " \
                  "FROM tbprg23 a, tbprgxusu24 b, tbusu08 c " \
                  "WHERE c.iduse=%s AND b.iduse=c.iduse AND b.idprg=a.idprg AND b.acceso=1;"
            valores = (self.codeusu)

            cursor.execute(sql, valores)

            data = cursor.fetchall()
            if data:
                for i in data:
                    concatenacion = "self.ui." + i[1] + ".show()"
                    exec(concatenacion)

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def RellenarCampos(self):
        try:
            usuario = self.ui.idusu24.text()
            filas = self.ui.tablaroles.rowCount()

            sql = "SELECT a.nombre, a.descripcion, b.acceso " \
                  "FROM tbprg23 a, tbprgxusu24 b, tbusu08 c " \
                  "WHERE c.iduse=%s AND b.iduse=c.iduse AND b.idprg=a.idprg"

            valor = (usuario)
            cursor.execute(sql, valor)

            data = cursor.fetchall()

            if data:
                for i in data:
                    programa = i[0]
                    acceso = int(i[2])

                    for f in range(filas):
                        celda = self.ui.tablaroles.item(f, 1)
                        if celda is not None and celda.text() == programa and acceso == 1:

                            checkbox = self.ui.tablaroles.cellWidget(f, 3)
                            if isinstance(checkbox, QCheckBox):
                                checkbox.setCheckState(Qt.Checked)
                            break



        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def CargarDatos(self):
        try:
            cursor.execute("SELECT idprg, nombre, descripcion FROM tbprg23")
            data = cursor.fetchall()

            if data:
                self.ui.tablaroles.setRowCount(len(data))
                for i, row in enumerate(data):

                    for j, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        if j == 2:
                            checkbox = QCheckBox()
                            self.ui.tablaroles.setCellWidget(i, 3, checkbox)

                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tablaroles.setItem(i, j, item)
            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"No hay programas")
                self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevoRol(self):
        try:
            self.ui.idusu24.clear()
            self.ui.tablaroles.clearContents()
            self.ui.tablaroles.setRowCount(0)
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


########################################################################################################################
############################################## Mantenimiento de Programa ###############################################
########################################################################################################################

    def VentanaBusPrgMnt(self):
        try:
            self.programa.CargarPrograma()
            self.programa.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevoPrograma(self):
        try:
            self.ui.nomprg23.clear()
            self.ui.desprg23.clear()

            self.GenerarIDPrograma()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GenerarIDPrograma(self):
        try:
            global numero
            cont = "1"

            cursor.execute("SELECT MAX(idprg + 1) FROM tbprg23")
            data = cursor.fetchall()

            for i in data:
                numero = str(i[0])

            if numero == "None":
                self.ui.idprg23.setText(cont)
            else:
                self.ui.idprg23.setText(str(numero))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def EliminarPrograma(self):
        try:
            idprograma = self.ui.idprg23.text()

            if not idprograma:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes ingresar un ID de programa para poder eliminar")
                self.mensaje.show()
            else:
                cursor.execute("DELETE FROM tbprg23 WHERE idprg='"+idprograma+"'")
                conexion.commit()

                self.NuevoPrograma()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText("El programa se ha eliminado correctamente")
                self.mensaje.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GuardarPrograma(self):
        try:
            idprograma = self.ui.idprg23.text()
            nombre = self.ui.nomprg23.text()
            descripcion = self.ui.desprg23.text()

            if not idprograma or not nombre or not descripcion:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes rellenar todos los campos")
                self.mensaje.show()
            else:
                cursor.execute("SELECT idprg FROM tbprg23 WHERE idprg='"+idprograma+"'")
                if cursor.fetchall():
                    sql = "UPDATE tbprg23 SET nombre=%s, descripcion=%s, creacion=now() WHERE idprg=%s"
                    valores = (nombre, descripcion, idprograma)
                    cursor.execute(sql, valores)

                    conexion.commit()

                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.setText(f"El programa se ha modificado correctamente")
                    self.mensaje.show()

                else:
                    sql = "INSERT INTO tbprg23 VALUES(default, %s, %s, now())"
                    valores = (nombre, descripcion)
                    cursor.execute(sql, valores)

                    conexion.commit()

                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.setText(f"El registro se ha insertado correctamente")
                    self.mensaje.show()

                self.NuevoPrograma()


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def RellenarPrograma(self):
        try:
            idprograma = self.ui.idprg23.text()

            cursor.execute("SELECT idprg, nombre, descripcion FROM tbprg23 WHERE idprg='"+idprograma+"'")
            data = cursor.fetchall()

            if data:
                for i in data:
                    self.ui.idprg23.setText(str(i[0]))
                    self.ui.nomprg23.setText(str(i[1]))
                    self.ui.desprg23.setText(str(i[2]))
            else:
                self.NuevoPrograma()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



########################################################################################################################
############################################## Mantenimiento de Producto ###############################################
########################################################################################################################

    def VentanaBusProMnt(self):
        try:
            self.modo = "producto"
            self.producto.CargarProductos()
            self.producto.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def LlenarComboCategoriaPro(self):

        try:
            cursor.execute("SELECT * FROM tbcat00")
            data = cursor.fetchall()

            if data:
                for i in data:
                    item_text = f"{i[0]} - {i[1]}"
                    self.ui.idcatpro10.addItem(str(item_text))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()




    def GuardarProducto(self):

        try:
            idpro = self.ui.idpro10.text()
            idcategoria = self.ui.idcatpro10.currentText()[0]

            suplidor = self.ui.ultsuppro10.text()
            nombre = self.ui.nompro10.text()
            puntoretorno = self.ui.punretpro10.text()
            existencia = self.ui.exipro10.text()
            precio = self.ui.prepro10.text()
            referencia = self.ui.refpro10.text()
            unidadcompra = self.ui.unicompro10.text()
            costo = self.ui.cospro10.text()
            especificacion = self.ui.espepro10.toPlainText()

            if not idpro or not idcategoria or not suplidor or not nombre or not puntoretorno or not existencia or not precio or not referencia or not unidadcompra or not costo:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes rellenar los campos en blanco")
                self.mensaje.show()
            else:
                cursor.execute("SELECT idpro FROM tbpro10 WHERE idpro='"+idpro+"'")
                if cursor.fetchall():
                    sql = "UPDATE tbpro10 SET idcategoria=%s, iduse=%s, ultsup=%s, nompro=%s, " \
                              "punret=%s, especificaciones=%s, canexis=%s, precio=%s, referencia=%s, unicomp=%s, costo=%s WHERE idpro=%s"

                    valores = (idcategoria, self.codeusu, suplidor, nombre, puntoretorno, especificacion, existencia,
                                   precio, referencia, unidadcompra, costo, idpro)
                    cursor.execute(sql, valores)
                    conexion.commit()

                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.setText("El registro se ha modificado correctamente")
                    self.mensaje.show()

                    self.NuevoProducto()
                else:


                    sql = "INSERT INTO tbpro10(idpro, idcategoria, iduse, ultsup, nompro, punret, " \
                              "canexis, precio, referencia, unicomp, costo, especificaciones) " \
                              "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                    valores = (idpro, idcategoria, self.codeusu, suplidor, nombre, puntoretorno, existencia,
                                   precio, referencia, unidadcompra, costo, especificacion)
                    cursor.execute(sql, valores)
                    conexion.commit()

                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.setText("El registro se ha agregado correctamente")
                    self.mensaje.show()

                    self.NuevoProducto()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def EliminarProducto(self):
        try:
            idpro = self.ui.idpro10.text()

            if not idpro:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Dbes ingresar un ID para elimianr el registro")
                self.mensaje.show()
            else:
                cursor.execute("DELETE FROM tbpro10 WHERE idpro='"+idpro+"'")
                conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText("Se ha eliminado el registro correctamente")
                self.mensaje.show()

                self.NuevoProducto()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevoProducto(self):
        try:
            self.ui.idpro10.clear()
            self.ui.ultsuppro10.clear()
            self.ui.nompro10.clear()
            self.ui.punretpro10.clear()
            self.ui.exipro10.clear()
            self.ui.prepro10.clear()
            self.ui.refpro10.clear()
            self.ui.espepro10.clear()
            self.ui.unicompro10.clear()
            self.ui.cospro10.clear()
            self.ui.espepro10.clear()
            self.GenerarIDProducto()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def RellenarProducto(self):
        try:
            idpro = self.ui.idpro10.text()
            cursor.execute("SELECT * FROM tbpro10 WHERE idpro='"+idpro+"'")
            data = cursor.fetchall()

            if data:
                for i in data:
                    self.ui.idpro10.setText(str(i[0]))
                    self.ui.idcatpro10.setCurrentText(str(i[1]))
                    self.ui.ultsuppro10.setText(str(i[3]))
                    self.ui.nompro10.setText(str(i[4]))
                    self.ui.punretpro10.setText(str(i[5]))
                    self.ui.exipro10.setText(str(i[7]))
                    self.ui.prepro10.setText(str(i[8]))
                    self.ui.refpro10.setText(str(i[9]))
                    self.ui.unicompro10.setText(str(i[10]))
                    self.ui.cospro10.setText(str(i[11]))
                    self.ui.espepro10.setText(str(i[6]))

            else:
                self.NuevoProducto()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def GenerarIDProducto(self):
        try:
            global numero
            cont = "1"

            cursor.execute("SELECT MAX(idpro + 1) FROM tbpro10")
            data = cursor.fetchall()

            for i in data:
                numero = str(i[0])

            if numero == "None":
                self.ui.idpro10.setText(cont)
            else:
                self.ui.idpro10.setText(str(numero))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


########################################################################################################################
############################################## Mantenimiento de Categoria ##############################################
########################################################################################################################

    def VentanaBusCatMnt(self):
        try:
            self.categoria.CargarCategoria()
            self.categoria.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GuardarCategoria(self):
        try:
            idcategoria = self.ui.idcat00.text()
            descripcion = self.ui.descat00.text()

            if not idcategoria or not descripcion:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes rellenar los campos en blanco")
                self.mensaje.show()
            else:
                cursor.execute("SELECT idcategoria FROM tbcat00 WHERE idcategoria='"+idcategoria+"'")
                if cursor.fetchall():
                    sql = "UPDATE tbcat00 SET descripcion=%s WHERE idcategoria=%s"
                    valores = (descripcion, idcategoria)
                    cursor.execute(sql, valores)
                    conexion.commit()

                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.setText("El registro se ha agregado correctamente")
                    self.mensaje.show()

                    self.NuevaCategoria()
                else:

                    sql = "INSERT INTO tbcat00(idcategoria, descripcion)" \
                              "VALUES(%s, %s)"
                    valores = (idcategoria, descripcion)
                    cursor.execute(sql, valores)
                    conexion.commit()

                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.setText("El registro se ha agregado correctamente")
                    self.mensaje.show()

                    self.NuevaCategoria()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def EliminarCategoria(self):
        try:
            idcategoria = self.ui.idcat00.text()

            if not idcategoria:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes ingresar un ID para eliminar el registro")
                self.mensaje.show()
            else:
                cursor.execute("DELETE FROM tbcat00 WHERE idcategoria='"+idcategoria+"'")
                conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText("El registro se ha eliminar correctamente")
                self.mensaje.show()

                self.NuevaCategoria()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevaCategoria(self):
        try:
            self.ui.idcat00.clear()
            self.ui.descat00.clear()

            self.GenerarIDCategoria()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def GenerarIDCategoria(self):
        try:
            global numero
            cont = "1"

            cursor.execute("SELECT MAX(idcategoria + 1) FROM tbcat00")
            data = cursor.fetchall()

            for i in data:
                numero = str(i[0])

            if numero == "None":
                self.ui.idcat00.setText(cont)
            else:
                self.ui.idcat00.setText(str(numero))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def RellenarCategoria(self):
        try:
            idcategoria = self.ui.idcat00.text()
            cursor.execute("SELECT * FROM tbcat00 WHERE idcategoria='"+idcategoria+"'")
            data = cursor.fetchall()

            if data:
                for i in data:
                    self.ui.idcat00.setText(str(i[0]))
                    self.ui.descat00.setText(str(i[1]))

            else:
                self.NuevaCategoria()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


########################################################################################################################
############################################## Mantenimiento de Impuesto ###############################################
########################################################################################################################


    def GuardarImpuesto(self):
        try:
            idimpuesto = self.ui.idimp07.text()
            descripcion = self.ui.desimp07.text()
            porcentaje = self.ui.prcimp07.text()

            if not idimpuesto or not descripcion or not porcentaje:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes rellenar los campos en blanco")
                self.mensaje.show()
            else:
                cursor.execute("SELECT idimpuesto FROM tbimp07 WHERE idimpuesto='"+idimpuesto+"'")
                if cursor.fetchall():

                    sql = "UPDATE tbimp07 SET descripcion=%s, porcentaje=%s, fecha=now() WHERE idimpuesto=%s"
                    valores = (descripcion, porcentaje, idimpuesto)
                    cursor.execute(sql, valores)
                    conexion.commit()

                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.setText("El registro se ha modificado correctamente")
                    self.mensaje.show()

                    self.NuevoImpuesto()

                else:
                    sql = "INSERT INTO tbimp07(idimpuesto, descripcion, porcentaje, fecha)" \
                          "VALUES(%s, %s, %s, now())"
                    valores = (idimpuesto, descripcion, porcentaje)
                    cursor.execute(sql, valores)
                    conexion.commit()

                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.setText("EL registro se ha agregado correctamente")
                    self.mensaje.show()

                    self.NuevoImpuesto()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def EliminarImpuesto(self):
        try:
            idimpuesto = self.ui.idimp07.text()

            if not idimpuesto:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes ingresar un ID para eliminar el registro")
                self.mensaje.show()
            else:
                cursor.execute("DELETE FROM tbimp07 WHERE idimpuesto='"+idimpuesto+"'")
                conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText("El registro se ha eliminado correctamente")
                self.mensaje.show()

                self.NuevoImpuesto()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevoImpuesto(self):
        try:
            fecha = self.GenerarFechaActual()
            self.ui.idimp07.clear()
            self.ui.desimp07.clear()
            self.ui.prcimp07.setValue(0.0000)
            self.ui.fecimp07.clear()

            self.GenerarImpuesto()
            self.ui.fecimp07.setText(str(fecha))
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GenerarImpuesto(self):
        try:
            global numero
            cont = "1"

            cursor.execute("SELECT MAX(idimpuesto + 1) FROM tbimp07")
            data = cursor.fetchall()

            for i in data:
                numero = str(i[0])

            if numero == "None":
                self.ui.idimp07.setText(cont)
            else:
                self.ui.idimp07.setText(str(numero))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def RellenarImpuesto(self):
        try:
            idimpuesto = self.ui.idimp07.text()
            cursor.execute("SELECT * FROM tbimp07 WHERE idimpuesto='" + idimpuesto + "'")
            data = cursor.fetchall()
            if data:
                for i in data:
                    self.ui.idimp07.setText(str(i[0]))
                    self.ui.desimp07.setText(str(i[1]))
                    self.ui.prcimp07.setValue(float(i[2]))
                    self.ui.fecimp07.setText(str(i[3]))

            else:
                self.NuevoImpuesto()


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


########################################################################################################################
############################################## Mantenimiento de Cliente ################################################
########################################################################################################################

    def VentanaBusCliMnt(self):
        try:
            self.modo = "cliente"
            self.cliente.CargarCliente()
            self.cliente.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GuardarCliente(self):
        try:
            idcli = self.ui.idcli03.text()
            nombre = self.ui.nomcli03.text()
            apellido = self.ui.apecli03.text()
            correo = self.ui.corcli03.text()
            telefono = self.ui.telcli03.text()
            direccion = self.ui.dircli03.text()
            ncf = self.ui.ncfcli03.text()
            rnc = self.ui.rnccli03.text()

            if not idcli or not nombre or not apellido or not correo or not telefono or not direccion:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes rellenar los campos en blanco")
                self.mensaje.show()
            else:

                cursor.execute("SELECT * FROM tbcli03 WHERE idcli='"+idcli+"'")
                if cursor.fetchall():
                    sql = "UPDATE tbcli03 SET nombre=%s, apellido=%s, correo=%s, telefono=%s, direccion=%s, " \
                          "tipncf=%s, rnc=%s WHERE idcli=%s"
                    valores = (nombre, apellido, correo, telefono, direccion, ncf, rnc, idcli)

                    cursor.execute(sql, valores)
                    conexion.commit()

                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.setText("El registro se ha modificado correctamente")
                    self.mensaje.show()

                    self.NuevoCliente()

                else:
                    sql = "INSERT INTO tbcli03(idcli, nombre, apellido, correo, telefono, direccion, tipncf, rnc)" \
                          "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
                    valores = (idcli, nombre, apellido, correo, telefono, direccion, ncf, rnc)

                    cursor.execute(sql, valores)
                    conexion.commit()

                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.setText("El registro se ha agregado correctamente")
                    self.mensaje.show()

                    self.NuevoCliente()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def EliminarCliente(self):
        try:
            idcli = self.ui.idcli03.text()

            if not idcli:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes ingresar un ID para eliminar el registro")
                self.mensaje.show()
            else:
                cursor.execute("DELETE FROM tbcli03 WHERE idcli='"+idcli+"'")
                conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText("El registro se ha eliminado correctamente")
                self.mensaje.show()

                self.NuevoCliente()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def RellenarInfoCliente(self):
        try:
            idcli = self.ui.idcli03.text()
            cursor.execute("SELECT * FROM tbcli03 WHERE idcli='"+idcli+"'")
            data = cursor.fetchall()
            if data:
                for i in data:
                    self.ui.idcli03.setText(str(i[0]))
                    self.ui.nomcli03.setText(str(i[1]))
                    self.ui.apecli03.setText(str(i[2]))
                    self.ui.corcli03.setText(str(i[3]))
                    self.ui.telcli03.setText(str(i[4]))
                    self.ui.dircli03.setText(str(i[5]))
                    self.ui.ncfcli03.setText(str(i[6]))
                    self.ui.rnccli03.setText(str(i[7]))
            else:
                self.NuevoCliente()


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GenerarIDCliente(self):
        global numero
        try:
            cont = "1"

            cursor.execute("SELECT MAX(idcli + 1) FROM tbcli03")
            data = cursor.fetchall()

            for i in data:
                numero = str(i[0])

            if numero == "None":
                self.ui.idcli03.setText(cont)
            else:
                self.ui.idcli03.setText(str(numero))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def NuevoCliente(self):
        try:
            self.ui.idcli03.clear()
            self.ui.nomcli03.clear()
            self.ui.apecli03.clear()
            self.ui.corcli03.clear()
            self.ui.telcli03.clear()
            self.ui.dircli03.clear()
            self.ui.ncfcli03.clear()
            self.ui.rnccli03.clear()
            self.GenerarIDCliente()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()




########################################################################################################################
############################################## Mantenimiento de Bancos #################################################
########################################################################################################################

    def VentanaBusBanMnt(self):
        try:
            self.banco.CargarBanco()
            self.banco.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GenerarIDBanco(self):

        global numero
        try:
            cont = "1"

            cursor.execute("SELECT MAX(idbanco + 1) FROM tbban06")
            data = cursor.fetchall()

            for i in data:
                numero = str(i[0])

            if numero == "None":
                self.ui.idban06.setText(cont)
            else:
                self.ui.idban06.setText(str(numero))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevoBanco(self):

        try:
            self.ui.idban06.clear()
            self.ui.nomban06.clear()

            self.GenerarIDBanco()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ourrido un error {ex}")
            self.mensaje.show()

    def RellenarInfoBanco(self):

        try:
            idbanco = self.ui.idban06.text()
            cursor.execute("SELECT * FROM tbban06 WHERE idbanco='"+idbanco+"'")
            data = cursor.fetchall()

            if data:
                for i in data:
                    self.ui.idban06.setText(str(i[0]))
                    self.ui.nomban06.setText(str(i[1]))

            else:
                self.NuevoBanco()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def EliminarBanco(self):
        try:
            idbanco = self.ui.idban06.text()

            if not idbanco:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes ingresar un ID para eliminar el registro")
                self.mensaje.show()
            else:
                cursor.execute("DELETE FROM tbban06 WHERE idbanco='"+idbanco+"'")
                conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText("El regisro se ha eliminado correctamente")
                self.mensaje.show()

            self.NuevoBanco()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GuardarBanco(self):

        try:
            idbanco = self.ui.idban06.text()
            nombre = self.ui.nomban06.text()

            if not idbanco or not nombre:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes rellenar los campos en blanco")
                self.mensaje.show()
            else:

                cursor.execute("SELECT * FROM tbban06 WHERE idbanco='"+idbanco+"'")
                if cursor.fetchall():

                    sql = "UPDATE tbban06 SET nombre=%s WHERE idbanco=%s"
                    valores = (nombre, idbanco)
                    cursor.execute(sql, valores)
                    conexion.commit()

                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.setText("El registro se ha modificado correctamente")
                    self.mensaje.show()

                    self.NuevoBanco()

                else:

                    sql = "INSERT INTO tbban06(idbanco, nombre) " \
                          "VALUES(%s, %s)"

                    valores = (idbanco, nombre)
                    cursor.execute(sql, valores)
                    conexion.commit()

                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.setText("El registro se ha agregado correctamente")
                    self.mensaje.show()

                    self.NuevoBanco()


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



########################################################################################################################
############################################## Mantenimiento de Usuarios ###############################################
########################################################################################################################

    def VisualUsuario(self):
        try:
            if self.ui.btnvisualusu08.isChecked():
                icono = QIcon("iconos_negros/eye.svg")
                self.ui.clavusu08.setEchoMode(QLineEdit.Normal)
            else:
                icono = QIcon("iconos_negros/eye-off.svg")
                self.ui.clavusu08.setEchoMode(QLineEdit.Password)

            self.ui.btnvisualusu08.setIcon(icono)

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def VentanaBusUsuMnt(self):
        try:
            self.usuario.CargarUsuario()
            self.usuario.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def RellenarInfoUsuario(self):

        try:
            idusuario = self.ui.idusu08.text()
            cursor.execute("SELECT * FROM tbusu08 WHERE iduse='"+idusuario+"'")
            data = cursor.fetchall()

            if data:
                for i in data:
                    imagen = i[8]
                    self.ui.idusu08.setText(str(i[0]))
                    self.ui.cedusu08.setText(str(i[1]))
                    self.ui.nomusu08.setText(str(i[3]))
                    self.ui.apeusu08.setText(str(i[4]))
                    self.ui.corusu08.setText(str(i[5]))
                    self.ui.telusu08.setText(str(i[6]))
                    self.ui.clavusu08.setText(str(i[7]))

                    pix = self.BytesPixmap(imagen)
                    self.ui.imgusu08.setPixmap(pix)

            else:
                self.NuevoUsuario()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def EliminarUsuario(self):

        try:
            iduse = self.ui.idusu08.text()

            if not iduse:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes ingresar un ID para eliminar el registro")
                self.mensaje.show()
            else:
                cursor.execute("DELETE FROM tbusu08 WHERE iduse='"+iduse+"'")
                conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText("El regitro se ha eliminado correctamente")
                self.mensaje.show()

                self.NuevoUsuario()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GuardarUsuario(self):
        try:
            iduse = self.ui.idusu08.text()
            nombre = self.ui.nomusu08.text()
            cedula = self.ui.cedusu08.text()
            apellido = self.ui.apeusu08.text()
            correo = self.ui.corusu08.text()
            telefono = self.ui.telusu08.text()
            clave = self.ui.clavusu08.text()
            sucursal = self.ui.idsucusu08.currentText()[0] + "" + \
                       self.ui.idsucusu08.currentText()[1]

            pixmap = self.ui.imgusu08.pixmap()

            if pixmap is not None:
                with open(self.archivo, 'rb') as image_file:
                    image_blob = image_file.read()

                if not iduse or not nombre or not cedula or not apellido or not correo or not telefono or not clave or not sucursal:
                    self.mensaje.setIcon(QMessageBox.Warning)
                    self.mensaje.setText("Debes rellenar todos los campos en blanco")
                    self.mensaje.show()
                else:
                    cursor.execute("SELECT * FROM tbusu08 WHERE iduse='" + iduse + "'")
                    if cursor.fetchall():

                        sql = "UPDATE tbusu08 SET nombre=%s, idsuc=%s, cedula=%s, apellido=%s, correo=%s, telefono=%s, clave=%s, imagen=%s, creacion=now() WHERE iduse=%s"
                        valores = (nombre, sucursal, cedula, apellido, correo, telefono, clave, image_blob, iduse, )
                        cursor.execute(sql, valores)
                        conexion.commit()

                        self.mensaje.setIcon(QMessageBox.Information)
                        self.mensaje.setText("El registro se ha modificado correctamente")
                        self.mensaje.show()

                        self.CargarImagen(False)
                        self.NuevoUsuario()

                    else:

                        sql = "INSERT INTO tbusu08(iduse, cedula, idsuc, nombre, apellido, correo, telefono, clave, imagen, creacion) " \
                                  "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, now())"

                        valores = (iduse, cedula, sucursal, nombre, apellido, correo, telefono, clave, image_blob)
                        cursor.execute(sql, valores)
                        conexion.commit()

                        self.mensaje.setIcon(QMessageBox.Information)
                        self.mensaje.setText("El registro se ha agregado correctamente")
                        self.mensaje.show()


                        self.NuevoUsuario()

            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"La imagen es obligatoria")
                self.mensaje.show()


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def RellenarSucursalUsu(self):
        try:
            cursor.execute("SELECT idsuc, nombre FROM tbsuc26")
            data = cursor.fetchall()

            if data:
                for i in data:
                    formato = f"{i[0]}   - {i[1]}"
                    self.ui.idsucusu08.addItem(str(formato))

            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"No existe ninguna sucursal")
                self.mensaje.show()


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevoUsuario(self):
        try:
            self.ui.nomusu08.clear()
            self.ui.apeusu08.clear()
            self.ui.cedusu08.clear()
            self.ui.corusu08.clear()
            self.ui.telusu08.clear()
            self.ui.clavusu08.clear()
            self.ui.imgusu08.clear()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


########################################################################################################################
############################################## Mantenimiento de Suplidor ###############################################
########################################################################################################################

    def VentanaBusSupMnt(self):
        try:
            self.modo = "suplidor"
            self.suplidor.CargarSuplidores()
            self.suplidor.show()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def EliminarSuplidor(self):

        try:
            idsuplidor = self.ui.idsup09.text()

            if not idsuplidor:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("Debes ingresar un ID para poder eliminar el registro")
                self.mensaje.show()
            else:
                cursor.execute("DELETE FROM tbsup09 WHERE idsup='"+idsuplidor+"'")
                conexion.commit()

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText("El registro se ha eliminado correctamente")
                self.mensaje.show()

                self.NuevoSuplidor()


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def NuevoSuplidor(self):

        try:
            self.ui.idsup09.clear()
            self.ui.nomsup09.clear()
            self.ui.dirsup09.clear()
            self.ui.telsup09.clear()
            self.ui.rncsup09.clear()
            self.ui.corsup09.clear()
            self.ui.websup09.clear()
            self.ui.nomcontact09.clear()
            self.ui.telcontact09.clear()

            self.GenerarIDSuplidor()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def GuardarSuplidor(self):

        try:

            idsup = self.ui.idsup09.text()
            nombre = self.ui.nomsup09.text()
            direccion = self.ui.dirsup09.text()
            telefono = self.ui.telsup09.text()
            rnc = self.ui.rncsup09.text()
            correo = self.ui.corsup09.text()
            web = self.ui.websup09.text()
            nomcontact = self.ui.nomcontact09.text()
            telcontact = self.ui.telcontact09.text()

            if not idsup or not nombre or not direccion or not telefono or not rnc or not correo or not web or not nomcontact or not telcontact:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"Debes rellenar todos los campos en blanco")
                self.mensaje.show()
            else:
                cursor.execute("SELECT * FROM tbsup09 WHERE idsup='"+idsup+"'")
                if cursor.fetchall():

                    sql = "UPDATE tbsup09 SET iduse=%s, nombre=%s, direccion=%s, telefono=%s, rnc=%s, " \
                          "correo=%s, web=%s, nombrecontact=%s, telefonocontact=%s WHERE idsup=%s"
                    valores = (self.codeusu, nombre, direccion, telefono, rnc, correo, web, nomcontact, telcontact, idsup)

                    cursor.execute(sql, valores)
                    conexion.commit()

                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.setText("El registro se ha modificado correctamente")
                    self.mensaje.show()

                    self.NuevoSuplidor()

                else:

                    sql = "INSERT INTO tbsup09(idsup, iduse, nombre, direccion, telefono, rnc, correo, web, nombrecontact, telefonocontact)" \
                          "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    valores = (idsup, self.codeusu, nombre, direccion, telefono, rnc, correo, web, nomcontact, telcontact)

                    cursor.execute(sql, valores)
                    conexion.commit()

                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.setText("El registro se ha agregado correctamente")
                    self.mensaje.show()

                    self.NuevoSuplidor()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def GenerarIDSuplidor(self):

        global numero
        try:
            cont = "1"

            cursor.execute("SELECT MAX(idsup + 1) FROM tbsup09")
            data = cursor.fetchall()

            for i in data:
                numero = str(i[0])

            if numero == "None":
                self.ui.idsup09.setText(cont)
            else:
                self.ui.idsup09.setText(str(numero))

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def RellenarInfoSuplidor(self):

        try:

            idsuplidor = self.ui.idsup09.text()

            cursor.execute("SELECT * FROM tbsup09 WHERE idsup='"+idsuplidor+"'")
            data = cursor.fetchall()

            if data:
                for i in data:
                    self.ui.idsup09.setText(str(i[0]))
                    self.ui.nomsup09.setText(str(i[2]))
                    self.ui.dirsup09.setText(str(i[3]))
                    self.ui.telsup09.setText(str(i[4]))
                    self.ui.rncsup09.setText(str(i[5]))
                    self.ui.corsup09.setText(str(i[6]))
                    self.ui.websup09.setText(str(i[7]))
                    self.ui.nomcontact09.setText(str(i[8]))
                    self.ui.telcontact09.setText(str(i[9]))
            else:
                self.NuevoSuplidor()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def Consultas(self):

        # Condicion para determinar la accion de la animacion
        if True:
            width = self.ui.frame_botones2.width()
            normal = 0
            if width == 0:
                extender = 300
            else:
                extender = normal

            # Creacion de la animacion
            self.animacion = QPropertyAnimation(self.ui.frame_botones2, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()
            self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_consulta)

    def Movimiento(self):

        # Condicion para determinar la accion de la animacion
        if True:
            width = self.ui.frame_botones2.width()
            normal = 0
            if width == 0:
                extender = 300
            else:
                extender = normal

            # Creacion de la animacion
            self.animacion = QPropertyAnimation(self.ui.frame_botones2, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()
            self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_movimiento)

    def Mantenimiento(self):

        # Condicion para determinar la accion de la animacion
        if True:
            width = self.ui.frame_botones2.width()
            normal = 0
            if width == 0:
                extender = 300
            else:
                extender = normal

            # Creacion de la animacion
            self.animacion = QPropertyAnimation(self.ui.frame_botones2, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()
            self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_mantenimientos)

    def Menu(self):

        # Condicion para determinar la accion de la animacion
        if True:
            width = self.ui.frame_botones.width()
            normal = 60
            if width == 60:
                extender = 225
            else:
                extender = normal

            # Creacion de la animacion
            self.animacion = QPropertyAnimation(self.ui.frame_botones, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()


    def PixmapBytes(self, pixmap):
        try:
            image = pixmap.toImage()

            # Convertir el QImage a bytes
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QIODevice.WriteOnly)

            image.save(buffer, 'PNG')  # Puedes ajustar el formato según tus necesidades

            return byte_array
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def BytesPixmap(self, byte_array):
        try:
            pixmap = QPixmap()
            pixmap.loadFromData(byte_array)

            return pixmap
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()
        # Convertir datos binarios a QPixmap



    def SeleccionarImagen(self, desicion):

        try:
            filename = QFileDialog.getOpenFileName(None, "Selecciona un archivo de imagen", "",
                                                        "Images (*.png *.xpm *.jpg *.bmp *.jpeg)")[0]

            if not filename:
                pass
            else:

                self.archivo = filename

                if desicion == "empresa":
                    pixmap = QPixmap(filename)
                    self.ui.imglog32.setPixmap(pixmap)

                elif desicion == "usuario":
                    pixmap = QPixmap(filename)
                    self.ui.imgusu08.setPixmap(pixmap)

                elif desicion == "configuracion":
                    self.GuardarImagen(filename)
                    self.CargarImagen(desicion)


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def GuardarImagen(self, archivo):
        try:
            # Abrir la imagen y convertirla en bytes
            with open(archivo, 'rb') as file:
                image = file.read()

            # Insertar la imagen en la base de datos
            cursor.execute("UPDATE tbusu08 SET imagen=%s WHERE iduse=%s", (image, self.codeusu))
            conexion.commit()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}.")
            self.mensaje.show()

    def CargarImagenEmpresa(self, nomemp):

        try:

            cursor.execute("SELECT logo FROM tbemp32 WHERE nombre=%s", (nomemp))
            self.data = cursor.fetchone()

            if self.data[0]:
                imagenrec = self.data[0]
                image = QImage.fromData(imagenrec)

                if not image.isNull():
                    pixmap = QPixmap.fromImage(image)
                    # Escalar la imagen para ajustarla al tamaño del botón
                    pixmap = pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio)

                    if pixmap is not None:
                        return pixmap
                    else:
                        pass
            else:
                pass

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def Sesion(self):

        # Condicion para determinar la accion de la animacion
        if True:
            width = self.ui.frame_botones2.width()
            normal = 0
            if width == 0:
                extender = 300
            else:
                extender = normal

            # Creacion de la animacion
            self.animacion = QPropertyAnimation(self.ui.frame_botones2, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()
            self.ui.stackedWidget.setCurrentWidget(self.ui.sesion)



    def CerrarSesion(self):

        try:
            self.mensaje = QMessageBox.question(self, "Pregunta", "Deseas cerrar sesion?", QMessageBox.Yes | QMessageBox.No)

            if self.mensaje == QMessageBox.Yes:
                self.instancia.show()
                self.close()
            else:
                pass

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def GenerarFechaActual(self):
        try:
            fecha = datetime.datetime.today().strftime("%Y-%m-%d")
            return fecha
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def Salir(self):

        try:

            self.mensaje = QMessageBox.question(self, "Pregunta", "Deseas cerrar el sistema?", QMessageBox.Yes | QMessageBox.No)

            if self.mensaje == QMessageBox.Yes:
                self.close()

            else:
                pass

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()



    def closeEvent(self, event):
        # Sobrescribir el evento de cierre
        respuesta = QMessageBox.question(self, 'Cierre de sistema',
                                         '¿Estás seguro de que quieres cerrar la ventana?',
                                         QMessageBox.No | QMessageBox.Yes, QMessageBox.No)

        # Procesar la respuesta del usuario
        if respuesta == QMessageBox.Yes:
            event.accept()  # Aceptar el evento de cierre si el usuario elige "Sí"
        else:
            event.ignore()  # Ignorar el evento de cierre si el usuario elige "No"


    def CargarImagen(self, desicion):

        try:

            cursor.execute("SELECT imagen FROM tbusu08 WHERE iduse=%s", (self.codeusu))
            self.data = cursor.fetchone()

            if self.data[0]:
                imagenrec = self.data[0]
                image = QImage.fromData(imagenrec)

                if not image.isNull():
                    pixmap = QPixmap.fromImage(image)
                    # Escalar la imagen para ajustarla al tamaño del botón
                    pixmap = pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio)
                    icono = QIcon(pixmap)

                    if desicion == "usuario":
                        return pixmap

                    elif desicion == "empresa":
                        return pixmap
                    else:
                        self.ui.salir.setIcon(icono)
            else:
                # Si no hay imagen disponible, puedes establecer un icono predeterminado
                icono = QIcon("C:/Users/elian/OneDrive/Escritorio/TRABAJOS DE PYTHON/IMAGEN BD/iconos_blancos/user.svg")

                self.ui.salir.setIcon(icono)

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

