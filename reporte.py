from PyQt5.QtCore import QTextCodec, QFileInfo, Qt, QByteArray, QTranslator, QLocale, QLibraryInfo
from PyQt5.QtGui import QTextDocument, QIcon
from PyQt5.QtWidgets import (QToolBar, QTreeWidget, QTreeWidgetItem, QTableWidgetItem, QDialog, QPushButton,
                             QFileDialog,
                             QMessageBox, QApplication)
from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrinter, QPrintDialog
import pymysql
from PyQt5.QtCore import Qt, QBuffer
from PyQt5.QtCore import QByteArray, QBuffer, QIODevice
from PyQt5.QtWidgets import QFileDialog, QMenu, QAction, QTableWidgetItem, QShortcut, QCheckBox, QDesktopWidget
from PyQt5.QtWidgets import QMessageBox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.mime.application import MIMEApplication
import os

from uirepfac import *


conexion = pymysql.connect(host="Localhost",
                           user="root",
                           password="elian2003",
                           database="sispos")
cursor = conexion.cursor()


class ImprimirFac(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.imp = Ui_MainWindow()
        self.imp.setupUi(self)

        self.documento = QTextDocument()
        self.mensaje = QMessageBox()


    """def Imprimir(self):
        if not self.documento.isEmpty():
            impresion = QPrinter(QPrinter.HighResolution)

            dlg = QPrintDialog(impresion, self)
            dlg.setWindowTitle("Imprimir documento")

            if dlg.exec_() == QPrintDialog.Accepted:
                self.documento.print_(impresion)

            del dlg
        else:
            QMessageBox.critical(self, "Imprimir", "No hay datos para imprimir.   ",
                                 QMessageBox.Ok)"""

    def Enviar(self, archivo):
        try:

            cursor.execute("SELECT correo, clave FROM tbemp32")
            info = cursor.fetchone()
            sender_email = info[0]
            sender_password = info[1]

            cursor.execute("SELECT correo FROM tbsup09 WHERE idsup='" + self.idsup + "'")
            correo = cursor.fetchone()

            if correo:
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = correo[0]
                msg['Subject'] = "Orden De Compra"

                mensaje = "De parte de nuestra empresa, le comunicamos por esta vía que necesitamos reponer algunos " \
                          "productos. La lista de los productos se encuentra en el siguiente documento adjunto."
                msg.attach(MIMEText(mensaje, 'plain'))

                # Adjuntar el archivo PDF al correo
                with open(archivo, 'rb') as adjunto:
                    adjunto_mime = MIMEApplication(adjunto.read(), _subtype="pdf")
                    adjunto_mime.add_header('Content-Disposition', f'attachment; filename={os.path.basename(archivo)}')
                    msg.attach(adjunto_mime)

                server = smtplib.SMTP("smtp.office365.com", 587)
                server.starttls()
                server.login(sender_email, sender_password)

                server.sendmail(sender_email, correo[0], msg.as_string())

                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText("El correo se ha enviado correctamente al suplidor.")
                self.mensaje.show()


        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()


    def ExportarPDF(self, numord):
        if not self.documento.isEmpty():
            nombreArchivo, _ = QFileDialog.getSaveFileName(self, "Exportar a PDF", f"Orden de compra-{numord}",
                                                           "Archivos PDF (*.pdf);;All Files (*)",
                                                           options=QFileDialog.Options())

            if nombreArchivo:
                impresion = QPrinter(QPrinter.HighResolution)
                impresion.setOutputFormat(QPrinter.PdfFormat)
                impresion.setOutputFileName(nombreArchivo)
                self.documento.print_(impresion)

                QMessageBox.information(self, "Exportar a PDF", "Datos exportados con éxito.   ",
                                        QMessageBox.Ok)
                self.Enviar(nombreArchivo)

        else:
            QMessageBox.critical(self, "Exportar a PDF", "No hay datos para exportar.   ",
                                 QMessageBox.Ok)

    def GenerarPDF(self, tupla, nomsup, telsup, numord, fecha, monto, impuesto, idsup, idsuc):
        try:

            self.idsup = idsup

            sucursal = idsuc[0] + "" + \
                       idsuc[1] + "" + \
                       idsuc[2]

            cursor.execute("SELECT nombre, rnc FROM tbemp32")
            data = cursor.fetchone()

            cursor.execute("SELECT direccion, telefono FROM tbsuc26 WHERE idsuc='"+sucursal+"'")
            suc = cursor.fetchone()
            dirsuc = suc[0]
            telsuc = suc[1]

            if tupla:
                self.imp.tabla.clear()

                datos = ""
                item_widget = []
                for dato in tupla:
                    cursor.execute("SELECT nompro FROM tbpro10 WHERE idpro='"+str(dato[1])+"'")
                    nompro = cursor.fetchone()
                    datos += f"<tr><td>{dato[1]}</td><td>{nompro[0]}</td><td>{dato[2]}</td><td>{dato[3]}</td><td>{dato[4]}</td><td>{dato[5]}</td></tr>"

                reporteHtml = """
                        <!DOCTYPE html>
                        <html>
                        <head>
                        <meta charset="UTF-8">
                        <style>
                        h3 {
                            font-family: Helvetica-Bold;
                            text-align: center;
                           }

                        table {
                               font-family: arial, sans-serif;
                               border-collapse: collapse;
                               width: 100%;
                              }

                        td {
                            text-align: left;
                            padding-top: 4px;
                            padding-right: 6px;
                            padding-bottom: 2px;
                            padding-left: 6px;
                           }

                        th {
                            text-align: left;
                            padding: 4px;
                            background-color: black;
                            color: white;
                           }


                        .encabezadoder{
                            text-align: right;
                        }

                        .encabezadoizq{
                            text-align: left;
                        }

                        .piepagina{
                            text-align: right;
                        }

                        .piepagina .sec{
                            text-decoration: underline;

                        }

                        tr:nth-child(even) {
                                            background-color: #dddddd;
                                           }
                                           
                        hr {
                            color: #000; /* Color de la línea */
                            background-color: #000; /* Color de fondo de la línea */
                            height: 25px; /* Grosor de la línea */
                        }
                        
                        </style>
                        </head>
                        <body>

                        <h3>Orden De Compra [numord]<br/></h3>
                        <div class="encabezadoizq">
                        <label> Comprado Por: [EMPRESA] </label> <br>
                        <label>RNC: [rnc]</label> <br>
                        <label>Fecha: [fecha]</label> <br>
                        <label>Comprado A: [nomsup]</label> <br>
                        <label>Telefono Empresa: [telsup]</label> 
                    </div>

                    <div class="encabezadoder">
                        <label>Orden De Compra No.: [numord]</label> <br>
                        <label> Sucursal A Entregar: [idsuc] </label> <br>
                        <label> Direccion A Entregar: [dirsuc] </label> <br>
                        <label> Telefono De La Sucursal A Entregar: [telsuc] </label> <br>


                    </div>
                        <table align="left" width="100%" cellspacing="0">
                          <tr>
                            <th>ID PRODUCTO</th>
                            <th>NOMBRE PRODUCTO</th>
                            <th>CANTIDAD</th>
                            <th>PRECIO</th>
                            <th>ITEBIS</th>
                            <th>IMPORTE</th>
                          </tr>
                          [DATOS]
                        </table>
                        <div class="piepagina">
                        <br> <br> <br> <br> <br> <br> <br>
                        
                        <hr> <br>
                        <label>ITBIS: </label>
                        <label class="sec">[itebis]</label><br>
                        <label>Total Facturado: </label>
                        <label class="sec">[total]</label><br>


                    </div>
                        </body>
                        </html>
                        """.replace("[DATOS]", datos).replace("[nomsup]", nomsup).\
                    replace("[telsup]", telsup).replace("[EMPRESA]", data[0]).replace("[rnc]", data[1]).\
                    replace("[fecha]", fecha).replace("[numord]", numord).replace("[total]", str(monto))\
                    .replace("[itebis]", str(impuesto)).replace("[idsuc]", idsuc).replace("[dirsuc]", dirsuc)\
                    .replace("[telsuc]", telsuc)

                datos = QByteArray()
                datos.append(str(reporteHtml))
                codec = QTextCodec.codecForHtml(datos)
                unistr = codec.toUnicode(datos)

                if Qt.mightBeRichText(unistr):
                    self.documento.setHtml(unistr)
                else:
                    self.documento.setPlainText(unistr)


                self.imp.tabla.addTopLevelItems(item_widget)
                self.ExportarPDF(numord)

            else:
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText(f"No hay datos para enviar la orden de compra")
                self.mensaje.show()

        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def VistaPrevia(self):
        if not self.documento.isEmpty():
            impresion = QPrinter(QPrinter.HighResolution)

            vista = QPrintPreviewDialog(impresion, self)
            vista.setWindowTitle("Vista previa")
            vista.setWindowFlags(Qt.Window)
            vista.resize(800, 600)

            exportarPDF = vista.findChildren(QToolBar)
            exportarPDF[0].addAction(QIcon("exportarPDF.png"), "Exportar a PDF", self.ExportarPDF)

            vista.paintRequested.connect(self.VistaPreviaImpresion)
            vista.exec_()
        else:
            QMessageBox.critical(self, "Vista previa", "No hay datos para visualizar.   ",
                                 QMessageBox.Ok)

    def VistaPreviaImpresion(self, impresion):
        self.documento.print_(impresion)


    def ImprimirFac(self, sinimp, monto, ncf, nofac, fecha, nomcli, apecli, telcli, datotb):
        try:
            cursor.execute("SELECT nombre, rnc FROM tbemp32")
            data = cursor.fetchone()

            if datotb and data:
                self.imp.tabla.clear()

                datos = ""
                item_widget = []
                for dato in datotb:
                    cursor.execute("SELECT nompro FROM tbpro10 WHERE idpro='"+str(dato[1])+"'")
                    nompro = cursor.fetchone()
                    datos += f"<tr><td>{dato[1]}</td><td>{nompro[0]}</td><td>{dato[2]}</td><td>{dato[3]}</td><td>{dato[4]}</td><td>{dato[5]}</td></tr>"

                reporteHtml = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <style>
        h3 {
            font-family: Helvetica-Bold;
            text-align: center;
           }

        table {
               font-family: arial, sans-serif;
               border-collapse: collapse;
               width: 100%;
              }

        td {
            text-align: left;
            padding-top: 4px;
            padding-right: 6px;
            padding-bottom: 2px;
            padding-left: 6px;
           }

        th {
            text-align: left;
            padding: 4px;
            background-color: black;
            color: white;
           }


        .encabezadoder{
            text-align: right;
        }

        .encabezadoizq{
            text-align: left;
        }

        .piepagina{
            text-align: right;
        }

        .piepagina .sec{
            text-decoration: underline;

        }

        tr:nth-child(even) {
                            background-color: #dddddd;
                           }
                           
        hr {
            color: #000; /* Color de la línea */
            background-color: #000; /* Color de fondo de la línea */
            height: 25px; /* Grosor de la línea */
        }
        
        </style>
        </head>
        <body>

        <h3>[EMPRESA]<br/></h3>
        <div class="encabezadoizq">
        <p> Factura </p> <br>
        <label>RNC: [rnc]</label> <br>
        <label>Fecha: [fecha]</label> <br>
        <label>Vendido A: [nomcli]</label> <br>
        <label>Telefono: [telcli]</label> 
    </div>

    <div class="encabezadoder">
        <label>NCF: [ncf]</label> <br>
        <label>Valido Hasta: [venci]</label> <br>
        <label>Factura No.: [nofac]</label> <br>


    </div>
        <table align="left" width="100%" cellspacing="0">
          <tr>
            <th>ID PRODUCTO</th>
            <th>NOMBRE PRODUCTO</th>
            <th>CANTIDAD</th>
            <th>PRECIO</th>
            <th>ITEBIS</th>
            <th>IMPORTE</th>
          </tr>
          [DATOS]
        </table>
        <div class="piepagina">
        <br> <br> <br> <br> <br> <br> <br>
        
        <hr> <br>
        <label>ITBIS: </label>
        <label class="sec">[itebis]</label><br>
        <label>Total Facturado: </label>
        <label class="sec">[total]</label><br>


    </div>
        </body>
        </html>
        """.replace("[DATOS]", datos).replace("[nomcli]", nomcli).replace("[apecli]", apecli)\
                    .replace("[telcli]", telcli).replace("[EMPRESA]", data[0]).replace("[rnc]", data[1]).\
                    replace("[fecha]", fecha).replace("[nofac]", nofac).replace("[ncf]", ncf).replace("[total]", monto)\
                    .replace("[itebis]", str(sinimp))

                datos = QByteArray()
                datos.append(str(reporteHtml))
                codec = QTextCodec.codecForHtml(datos)
                unistr = codec.toUnicode(datos)

                if Qt.mightBeRichText(unistr):
                    self.documento.setHtml(unistr)
                else:
                    self.documento.setPlainText(unistr)

                self.imp.tabla.addTopLevelItems(item_widget)

                self.VistaPrevia()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def ImprimirOrd(self, sinimp, monto, numord, fecha, nomsup, telsup, idsuc, datotb):
        try:
            cursor.execute("SELECT nombre, rnc FROM tbemp32")
            data = cursor.fetchone()

            sucursal = idsuc[0] + "" + \
                       idsuc[1] + "" + \
                       idsuc[2]

            cursor.execute("SELECT direccion, telefono FROM tbsuc26 WHERE idsuc='" + sucursal + "'")
            suc = cursor.fetchone()
            dirsuc = suc[0]
            telsuc = suc[1]

            if datotb and data:
                self.imp.tabla.clear()

                datos = ""
                item_widget = []
                for dato in datotb:
                    cursor.execute("SELECT nompro FROM tbpro10 WHERE idpro='" + str(dato[1]) + "'")
                    nompro = cursor.fetchone()
                    datos += f"<tr><td>{dato[1]}</td><td>{nompro[0]}</td><td>{dato[2]}</td><td>{dato[3]}</td><td>{dato[4]}</td><td>{dato[5]}</td></tr>"

                reporteHtml = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <style>
        h3 {
            font-family: Helvetica-Bold;
            text-align: center;
           }

        table {
               font-family: arial, sans-serif;
               border-collapse: collapse;
               width: 100%;
              }

        td {
            text-align: left;
            padding-top: 4px;
            padding-right: 6px;
            padding-bottom: 2px;
            padding-left: 6px;
           }

        th {
            text-align: left;
            padding: 4px;
            background-color: black;
            color: white;
           }


        .encabezadoder{
            text-align: right;
        }

        .encabezadoizq{
            text-align: left;
        }

        .piepagina{
            text-align: right;
        }

        .piepagina .sec{
            text-decoration: underline;

        }

        tr:nth-child(even) {
                            background-color: #dddddd;
                           }
                           
        hr {
            color: #000; /* Color de la línea */
            background-color: #000; /* Color de fondo de la línea */
            height: 25px; /* Grosor de la línea */
        }
        
        </style>
        </head>
        <body>

        <h3>Orden De Compra<br/></h3>
        <div class="encabezadoizq">
        <label> Comprado Por: [EMPRESA] </label> <br>
        <label>RNC: [rnc]</label> <br>
        <label>Fecha: [fecha]</label> <br>
        <label>Comprado A: [nomsup]</label> <br>
        <label>Telefono De Empresa: [telsup]</label> 
    </div>

    <div class="encabezadoder">
        <label>Orden De Compra No.: [noord]</label> <br>
        <label> Sucursal A Entregar: [idsuc] </label> <br>
        <label> Direccion A Entregar: [dirsuc] </label> <br>
        <label> Telefono De La Sucursal: [telsuc] </label> <br>


    </div>
        <table align="left" width="100%" cellspacing="0">
          <tr>
            <th>ID PRODUCTO</th>
            <th>NOMBRE PRODUCTO</th>
            <th>CANTIDAD</th>
            <th>PRECIO</th>
            <th>ITEBIS</th>
            <th>IMPORTE</th>
          </tr>
          [DATOS]
        </table>
        <div class="piepagina">
        <br> <br> <br> <br> <br> <br> <br>
    
        <hr> <br>
        <label>ITBIS: </label>
        <label class="sec">[itebis]</label><br>
        <label>Total Facturado: </label>
        <label class="sec">[total]</label><br>


    </div>
        </body>
        </html>
        """.replace("[DATOS]", datos).replace("[nomsup]", nomsup).replace("[telsup]", telsup).replace("[EMPRESA]", data[0]).replace("[rnc]", data[1]). \
                    replace("[fecha]", fecha).replace("[noord]", numord).replace("[total]", monto) \
                    .replace("[itebis]", str(sinimp)).replace("[idsuc]", idsuc).replace("[dirsuc]", dirsuc)\
                    .replace("[telsuc]", telsuc)

                datos = QByteArray()
                datos.append(str(reporteHtml))
                codec = QTextCodec.codecForHtml(datos)
                unistr = codec.toUnicode(datos)

                if Qt.mightBeRichText(unistr):
                    self.documento.setHtml(unistr)
                else:
                    self.documento.setPlainText(unistr)

                self.imp.tabla.addTopLevelItems(item_widget)

                self.VistaPrevia()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def ImprimirPag(self, idcli, nomcli, telcli, numrec, formpag, numdocu, banco, fecha, totalpag, tupla):
        try:
            cursor.execute("SELECT nombre, rnc FROM tbemp32")
            data = cursor.fetchone()

            cursor.execute("SELECT rnc FROM tbcli03 WHERE idcli='"+idcli+"'")
            rnc = cursor.fetchone()


            if tupla and data:
                self.imp.tabla.clear()

                datos = ""
                item_widget = []
                for dato in tupla:
                    datos += f"<tr><td>{dato[0]}</td><td>{dato[1]}</td><td>{dato[4]}</td><td>{dato[2]}</td><td>{dato[5]}</td></tr>"

                reporteHtml = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <style>
        h3 {
            font-family: Helvetica-Bold;
            text-align: center;
           }

        table {
               font-family: arial, sans-serif;
               border-collapse: collapse;
               width: 100%;
              }

        td {
            text-align: left;
            padding-top: 4px;
            padding-right: 6px;
            padding-bottom: 2px;
            padding-left: 6px;
           }

        th {
            text-align: left;
            padding: 4px;
            background-color: black;
            color: white;
           }


        .encabezadoder{
            text-align: right;
        }

        .encabezadoizq{
            text-align: left;
        }

        .piepagina{
            text-align: left;
        }

      

        tr:nth-child(even) {
                            background-color: #dddddd;
                }
                           
        hr {
            color: #000; /* Color de la línea */
            background-color: #000; /* Color de fondo de la línea */
            height: 25px; /* Grosor de la línea */
        }
        
        .firma {
            width: 50%; /* Ajusta el ancho de la línea */
        }
        
        .labelfirma{
            font-family: Helvetica-Bold;
        }
        
        </style>
        </head>
        <body>

        <h3>[EMPRESA]<br/></h3>
        <div class="encabezadoizq">
        <p> Cuenta Por Cobrar </p> <br>
        <label> Numero de Recibo: [norec] <br>
        <label>RNC: [rnc]</label> <br>
        <label>Fecha: [fecha]</label> <br>
        
    </div>

    <div class="encabezadoder">
        <label>Pagado Por: [nomcli]</label> <br>
        <label>Telefono Cliente: [telcli]</label> <br>
        <label>RNC Cliente: [rnccli]</label> <br>


    </div>
        <table align="left" width="100%" cellspacing="0">
          <tr>
            <th>FACTURA</th>
            <th>FECHA FACTURA</th>
            <th>VENCIMIENTO</th>
            <th>MONTO FACT.</th>
            <th>MONTO PAGO</th>
          </tr>
          [DATOS]
        </table>
        
        <div class="piepagina">
        <br> <br> <br> <br> <br> <br> <br>
        
        <hr> <br>
        <label>Forma De Pago: [forpag]</label> <br>
        <label>Num Documento: [numdocu]</label> <br>
        <label>Banco: [ban] </label> <br>
        
        <label>Total Pagado: [total]</label> <br>
        <label>Fecha De Pago: [fecha]</label> <br>
        
        <br> <br> <br>
        <hr class="firma" > 
        <label class="labelfirma">Firma</label> <br>


    </div>
        </body>
        </html>
        """.replace("[DATOS]", datos).replace("[nomcli]", nomcli).replace("[telcli]", telcli)\
                    .replace("[EMPRESA]", data[0]).replace("[rnc]", data[1]). \
                    replace("[fecha]", fecha).replace("[norec]", numrec).replace("[numdocu]", numdocu)\
                    .replace("[total]", str(totalpag)).replace("[ban]", banco).replace("[forpag]", formpag)\
                    .replace("[rnccli]", str(rnc[0]))

                datos = QByteArray()
                datos.append(str(reporteHtml))
                codec = QTextCodec.codecForHtml(datos)
                unistr = codec.toUnicode(datos)

                if Qt.mightBeRichText(unistr):
                    self.documento.setHtml(unistr)
                else:
                    self.documento.setPlainText(unistr)

                self.imp.tabla.addTopLevelItems(item_widget)

                self.VistaPrevia()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def ImprimirDevCli(self, balance, idcli, nofac, numrecibo, fecha, nomcli, apecli, telcli, monto, tupla):
        try:
            nombrecompleto = nomcli + " " + apecli
            cursor.execute("SELECT nombre, rnc FROM tbemp32")
            data = cursor.fetchone()

            cursor.execute("SELECT rnc FROM tbcli03 WHERE idcli='" + idcli + "'")
            rnc = cursor.fetchone()

            if tupla and data:
                self.imp.tabla.clear()

                datos = ""
                item_widget = []
                for dato in tupla:
                    datos += f"<tr><td>{dato[1]}</td><td>{dato[2]}</td><td>{dato[3]}</td><td>{dato[4]}</td><td>{dato[5]}</td></tr>"

                reporteHtml = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <style>
        h3 {
            font-family: Helvetica-Bold;
            text-align: center;
           }

        table {
               font-family: arial, sans-serif;
               border-collapse: collapse;
               width: 100%;
              }

        td {
            text-align: left;
            padding-top: 4px;
            padding-right: 6px;
            padding-bottom: 2px;
            padding-left: 6px;
           }

        th {
            text-align: left;
            padding: 4px;
            background-color: black;
            color: white;
           }


        .encabezadoder{
            text-align: right;
        }

        .encabezadoizq{
            text-align: left;
        }

        .piepagina{
            text-align: left;
        }



        tr:nth-child(even) {
                            background-color: #dddddd;
                }

        hr {
            color: #000; /* Color de la línea */
            background-color: #000; /* Color de fondo de la línea */
            height: 25px; /* Grosor de la línea */
        }

    


        </style>
        </head>
        <body>

        <h3>[EMPRESA]<br/></h3>
        <div class="encabezadoizq">
        <p> Nota de Credito </p> <br>
        <label> Numero de Devolucion: [numdev] <br>
        <label> Numero de Factura: [nofac] <br>
        <label>RNC: [rnc]</label> <br>
        <label>Fecha: [fecha]</label> <br>

    </div>

    <div class="encabezadoder">
        <label>Nombre Cliente: [nomcli]</label> <br>
        <label>Telefono Cliente: [telcli]</label> <br>
        <label>RNC Cliente: [rnccli]</label> <br>


    </div>
        <table align="left" width="100%" cellspacing="0">
          <tr>
            <th>CODIGO DE PRODUCTO</th>
            <th>NOMBRE PRODUCTO FACTURA</th>
            <th>CANTIDAD DEVUELTA</th>
            <th>PRECIO</th>
            <th>IMPORTE</th>
          </tr>
          [DATOS]
        </table>

        <div class="piepagina">
        <br> <br> <br> <br> <br> <br> <br>
        
        <hr> <br>
        <label>Balance De La Factura: [balfac]</label> <br>
        <label>Monto De Devolucion: [mondev]</label> <br>
        <label>Fecha De Devolucion: [fecha]</label> <br>



    </div>
        </body>
        </html>
        """.replace("[DATOS]", datos).replace("[nomcli]", nombrecompleto).replace("[telcli]", telcli) \
                    .replace("[EMPRESA]", data[0]).replace("[rnc]", data[1]). \
                    replace("[fecha]", fecha).replace("[nofac]", nofac).replace("[rnccli]", str(rnc[0]))\
                    .replace("[numdev]", numrecibo).replace("[balfac]", str(balance)).replace("[mondev]", monto)

                datos = QByteArray()
                datos.append(str(reporteHtml))
                codec = QTextCodec.codecForHtml(datos)
                unistr = codec.toUnicode(datos)

                if Qt.mightBeRichText(unistr):
                    self.documento.setHtml(unistr)
                else:
                    self.documento.setPlainText(unistr)

                self.imp.tabla.addTopLevelItems(item_widget)

                self.VistaPrevia()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def ImprimirDevSup(self, idsup, numrec, numrecibo, fecha, nomsup, telsup, monto, balance, tupla):
        try:
            cursor.execute("SELECT nombre, rnc FROM tbemp32")
            data = cursor.fetchone()

            cursor.execute("SELECT rnc FROM tbsup09 WHERE idsup='" + idsup + "'")
            rnc = cursor.fetchone()

            if tupla and data:
                self.imp.tabla.clear()

                datos = ""
                item_widget = []
                for dato in tupla:
                    datos += f"<tr><td>{dato[1]}</td><td>{dato[2]}</td><td>{dato[3]}</td><td>{dato[4]}</td><td>{dato[5]}</td></tr>"

                reporteHtml = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <style>
        h3 {
            font-family: Helvetica-Bold;
            text-align: center;
           }

        table {
               font-family: arial, sans-serif;
               border-collapse: collapse;
               width: 100%;
              }

        td {
            text-align: left;
            padding-top: 4px;
            padding-right: 6px;
            padding-bottom: 2px;
            padding-left: 6px;
           }

        th {
            text-align: left;
            padding: 4px;
            background-color: black;
            color: white;
           }


        .encabezadoder{
            text-align: right;
        }

        .encabezadoizq{
            text-align: left;
        }

        .piepagina{
            text-align: left;
        }



        tr:nth-child(even) {
                            background-color: #dddddd;
                }

        hr {
            color: #000; /* Color de la línea */
            background-color: #000; /* Color de fondo de la línea */
            height: 25px; /* Grosor de la línea */
        }




        </style>
        </head>
        <body>

        <h3>[EMPRESA]<br/></h3>
        <div class="encabezadoizq">
        <p> Nota de Debito </p> <br>
        <label> Numero de Recepcion: [numrecep] <br>
        <label> Numero de Recibo: [numrecibo] <br>
        <label>RNC: [rnc]</label> <br>
        <label>Fecha: [fecha]</label> <br>

    </div>

    <div class="encabezadoder">
        <label>Nombre Suplidor: [nomsup]</label> <br>
        <label>Telefono Suplidor: [telsup]</label> <br>
        <label>RNC Suplidor: [rncsup]</label> <br>


    </div>
        <table align="left" width="100%" cellspacing="0">
          <tr>
            <th>CODIGO DE PRODUCTO</th>
            <th>NOMBRE PRODUCTO FACTURA</th>
            <th>CANTIDAD DEVUELTA</th>
            <th>PRECIO</th>
            <th>IMPORTE</th>
          </tr>
          [DATOS]
        </table>

        <div class="piepagina">
        <br> <br> <br> <br> <br> <br> <br>

        <hr> <br>
        <label>Balance De La Factura: [balfac]</label> <br>
        <label>Monto De Devolucion: [mondev]</label> <br>
        <label>Fecha De Devolucion: [fecha]</label> <br>



    </div>
        </body>
        </html>
        """.replace("[DATOS]", datos).replace("[nomsup]", nomsup).replace("[telsup]", telsup) \
                    .replace("[EMPRESA]", data[0]).replace("[rnc]", data[1]). \
                    replace("[fecha]", fecha).replace("[numrecep]", numrec).replace("[rncsup]", str(rnc[0])) \
                    .replace("[numrecibo]", numrecibo).replace("[balfac]", str(balance)).replace("[mondev]", monto)

                datos = QByteArray()
                datos.append(str(reporteHtml))
                codec = QTextCodec.codecForHtml(datos)
                unistr = codec.toUnicode(datos)

                if Qt.mightBeRichText(unistr):
                    self.documento.setHtml(unistr)
                else:
                    self.documento.setPlainText(unistr)

                self.imp.tabla.addTopLevelItems(item_widget)

                self.VistaPrevia()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def ImprimirCob(self, idsup, nomsup, telsup, numrec, formpag, numdocu, banco, fecha, total, tupla):
        try:
            cursor.execute("SELECT nombre, rnc FROM tbemp32")
            data = cursor.fetchone()

            cursor.execute("SELECT rnc FROM tbsup09 WHERE idsup='" + idsup + "'")
            rnc = cursor.fetchone()

            if tupla and data:
                self.imp.tabla.clear()

                datos = ""
                item_widget = []
                for dato in tupla:
                    datos += f"<tr><td>{dato[0]}</td><td>{dato[1]}</td><td>{dato[4]}</td><td>{dato[2]}</td><td>{dato[5]}</td></tr>"

                reporteHtml = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <style>
        h3 {
            font-family: Helvetica-Bold;
            text-align: center;
           }

        table {
               font-family: arial, sans-serif;
               border-collapse: collapse;
               width: 100%;
              }

        td {
            text-align: left;
            padding-top: 4px;
            padding-right: 6px;
            padding-bottom: 2px;
            padding-left: 6px;
           }

        th {
            text-align: left;
            padding: 4px;
            background-color: black;
            color: white;
           }


        .encabezadoder{
            text-align: right;
        }

        .encabezadoizq{
            text-align: left;
        }

        .piepagina{
            text-align: left;
        }



        tr:nth-child(even) {
                            background-color: #dddddd;
                }

        hr {
            color: #000; /* Color de la línea */
            background-color: #000; /* Color de fondo de la línea */
            height: 25px; /* Grosor de la línea */
        }

        .firma {
            width: 50%; /* Ajusta el ancho de la línea */
        }

        .labelfirma{
            font-family: Helvetica-Bold;
        }

        </style>
        </head>
        <body>

        <h3>[EMPRESA]<br/></h3>
        <div class="encabezadoizq">
        <p> Cuenta Por Pagar </p> <br>
        <label> Numero de Recibo: [norec] <br>
        <label>RNC: [rnc]</label> <br>
        <label>Fecha: [fecha]</label> <br>

    </div>

    <div class="encabezadoder">
        <label>Nombre Suplidor: [nomsup]</label> <br>
        <label>Telefono Suplidor: [telsup]</label> <br>
        <label>RNC Suplidor: [rncsup]</label> <br>


    </div>
        <table align="left" width="100%" cellspacing="0">
          <tr>
            <th>FACTURA</th>
            <th>FECHA FACTURA</th>
            <th>VENCIMIENTO</th>
            <th>MONTO FACT.</th>
            <th>MONTO PAGO</th>
          </tr>
          [DATOS]
        </table>

        <div class="piepagina">
        <br> <br> <br> <br> <br> <br> <br>

        <hr> <br>
        <label>Forma De Pago: [forpag]</label> <br>
        <label>Num Documento: [numdocu]</label> <br>
        <label>Banco: [ban] </label> <br>

        <label>Total Pagado: [total]</label> <br>
        <label>Fecha De Pago: [fecha]</label> <br>

        <br> <br> <br>
        <hr class="firma" > 
        <label class="labelfirma">Firma</label> <br>


    </div>
        </body>
        </html>
        """.replace("[DATOS]", datos).replace("[nomsup]", nomsup).replace("[telsup]", telsup) \
                    .replace("[EMPRESA]", data[0]).replace("[rnc]", data[1]). \
                    replace("[fecha]", fecha).replace("[norec]", numrec).replace("[numdocu]", numdocu) \
                    .replace("[total]", str(total)).replace("[ban]", banco).replace("[forpag]", formpag) \
                    .replace("[rncsup]", str(rnc[0]))

                datos = QByteArray()
                datos.append(str(reporteHtml))
                codec = QTextCodec.codecForHtml(datos)
                unistr = codec.toUnicode(datos)

                if Qt.mightBeRichText(unistr):
                    self.documento.setHtml(unistr)
                else:
                    self.documento.setPlainText(unistr)

                self.imp.tabla.addTopLevelItems(item_widget)

                self.VistaPrevia()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

    def ImprimirRec(self, numord, fecha, nomsup, telsup, monto, idsuc, sumimp, tupla):
        try:
            cursor.execute("SELECT nombre, rnc FROM tbemp32")
            data = cursor.fetchone()

            cursor.execute("SELECT direccion, telefono FROM tbsuc26 WHERE idsuc='" + idsuc + "'")
            suc = cursor.fetchone()
            dirsuc = suc[0]
            telsuc = suc[1]

            if tupla and data:
                self.imp.tabla.clear()

                datos = ""
                item_widget = []
                for dato in tupla:
                    datos += f"<tr><td>{dato[0]}</td><td>{dato[1]}</td><td>{dato[2]}</td><td>{dato[3]}</td><td>{dato[4]}</td><td>{dato[5]}</td></tr>"

                reporteHtml = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <style>
        h3 {
            font-family: Helvetica-Bold;
            text-align: center;
           }

        table {
               font-family: arial, sans-serif;
               border-collapse: collapse;
               width: 100%;
              }

        td {
            text-align: left;
            padding-top: 4px;
            padding-right: 6px;
            padding-bottom: 2px;
            padding-left: 6px;
           }

        th {
            text-align: left;
            padding: 4px;
            background-color: black;
            color: white;
           }


        .encabezadoder{
            text-align: right;
        }

        .encabezadoizq{
            text-align: left;
        }

        .piepagina{
            text-align: right;
        }

        .piepagina .sec{
            text-decoration: underline;

        }

        tr:nth-child(even) {
                            background-color: #dddddd;
                           }

        hr {
            color: #000; /* Color de la línea */
            background-color: #000; /* Color de fondo de la línea */
            height: 25px; /* Grosor de la línea */
        }

        </style>
        </head>
        <body>

        <h3>Recepcion<br/></h3>
        <div class="encabezadoizq">
        <label> Comprado Por: [EMPRESA] </label> <br>
        <label>RNC: [rnc]</label> <br>
        <label>Fecha: [fecha]</label> <br>
        <label>Comprado A: [nomsup]</label> <br>
        <label>Telefono De Empresa: [telsup]</label> 
    </div>

    <div class="encabezadoder">
        <label>Orden De Compra No.: [noord]</label> <br>
        <label> Entregado A: [idsuc] </label> <br>
        <label> Direccion De Sucursal: [dirsuc] </label> <br>
        <label> Telefono De La Sucursal: [telsuc] </label> <br>


    </div>
        <table align="left" width="100%" cellspacing="0">
          <tr>
            <th>ID PRODUCTO</th>
            <th>NOMBRE PRODUCTO</th>
            <th>CANTIDAD</th>
            <th>PRECIO</th>
            <th>ITEBIS</th>
            <th>IMPORTE</th>
          </tr>
          [DATOS]
        </table>
        <div class="piepagina">
        <br> <br> <br> <br> <br> <br> <br>

        <hr> <br>
        <label>ITBIS: </label>
        <label class="sec">[itebis]</label><br>
        <label>Total Facturado: </label>
        <label class="sec">[total]</label><br>


    </div>
        </body>
        </html>
        """.replace("[DATOS]", datos).replace("[nomsup]", nomsup).replace("[telsup]", telsup).replace("[EMPRESA]", data[0])\
                    .replace("[rnc]", data[1]).replace("[fecha]", fecha).replace("[noord]", numord)\
                    .replace("[total]", monto).replace("[itebis]", str(sumimp)).replace("[idsuc]", idsuc)\
                    .replace("[dirsuc]", dirsuc).replace("[telsuc]", telsuc)

                datos = QByteArray()
                datos.append(str(reporteHtml))
                codec = QTextCodec.codecForHtml(datos)
                unistr = codec.toUnicode(datos)

                if Qt.mightBeRichText(unistr):
                    self.documento.setHtml(unistr)
                else:
                    self.documento.setPlainText(unistr)

                self.imp.tabla.addTopLevelItems(item_widget)

                self.VistaPrevia()
        except Exception as ex:
            self.mensaje.setIcon(QMessageBox.Critical)
            self.mensaje.setText(f"Ha ocurrido un error {ex}")
            self.mensaje.show()

