import io
from flask import Flask, request, send_file
from weasyprint import HTML
from datetime import timedelta
import datetime
import pymysql

conexion = pymysql.connect(host="Localhost",
                           user="root",
                           password="elian2003",
                           database="sispos",
                           autocommit=True)
cursor = conexion.cursor()

class FacturaProcessorApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.username = "ElianGomez"
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/respuesta', methods=['POST'])
        def procesar_compra():
            return self.procesar_compra()

    def procesar_compra(self):
        fecha = datetime.datetime.now().strftime("%Y-%m-%d")
        condicion = 0
        ncf = "-----------"
        secncf = 0

        productos_seleccionados = []

        # Recibir productos seleccionados desde el formulario
        productos = request.form.getlist("productos[]")

        # Obtener los valores ocultos de id_cliente y id_sucursal
        id_cliente = request.form.get("id_cliente")
        id_sucursal = request.form.get("id_sucursal")

        for id_producto in productos:
            cantidad = int(request.form[f"cantidad_{id_producto}"])
            descripcion = request.form[f"descripcion_{id_producto}"]
            precio = float(request.form[f"precio_{id_producto}"])
            itebis = precio * 0.18  # Calcular ITBIS (18%)
            importe = (precio + itebis) * cantidad

            # Crear diccionario para el producto
            producto = {
                "id": id_producto,
                "nombre": descripcion,
                "cantidad": cantidad,
                "precio": precio,
                "itebis": itebis,
                "importe": importe
            }
            productos_seleccionados.append(producto)

        # Calcular totales
        total_itebis = sum(p["itebis"] * p["cantidad"] for p in productos_seleccionados)
        total_facturado = sum(p["importe"] for p in productos_seleccionados)

        # Obtener número de factura
        cursor.execute("SELECT MAX(nofac + 1) FROM tbfacmae20")
        nofacdet = cursor.fetchone()

        devuelta = 0

        # Insertar factura en la base de datos
        sql = "INSERT INTO tbfacmae20 VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        valores = (nofacdet[0], id_cliente, self.username, id_sucursal, fecha, condicion, total_facturado, total_facturado, ncf, secncf, "A")
        cursor.execute(sql, valores)


        # Insertar detalles de la factura
        for i in productos_seleccionados:
            sqldet = "INSERT INTO tbfacdet21 VALUES(%s, %s, %s, %s, %s, %s)"
            valuesdet = (nofacdet[0], i["id"], i["cantidad"], i["precio"], i["itebis"], devuelta)
            cursor.execute(sqldet, valuesdet)

        # Obtener el número de factura generado

          # Si es None, usar 1 como predeterminado

        # Generar factura en PDF
        pdf_file = self.generar_factura_pdf(productos_seleccionados, total_itebis, total_facturado, id_cliente, id_sucursal, nofacdet[0])

        # Enviar el PDF como respuesta
        return send_file(
            io.BytesIO(pdf_file),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='factura.pdf'
        )

    def generar_factura_pdf(self, productos, total_itebis, total_facturado, id_cliente, id_sucursal, nofac):
        fecha = datetime.datetime.now().strftime("%Y-%m-%d")
        valido_hasta = (datetime.datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")

        # Obtener datos de la empresa
        cursor.execute("SELECT nombre, rnc, telefono FROM tbemp32")
        data = cursor.fetchall()

        nombre, rnc, telefono = "", "", ""
        if data:
            for i in data:
                nombre = i[0]
                rnc = i[1]
                telefono = i[2]

        # Obtener el nombre del cliente
        cursor.execute(f"SELECT CONCAT(nombre, ' ', apellido) FROM tbcli03 WHERE idcli='{id_cliente}'")
        cliente = cursor.fetchone()
        cliente_nombre = cliente[0] if cliente else "Cliente Desconocido"

        # Generar factura HTML
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <style>
        h3 {{ font-family: Helvetica-Bold; text-align: center; }}
        table {{ font-family: arial, sans-serif; border-collapse: collapse; width: 100%; }}
        td {{ text-align: left; padding: 4px; }}
        th {{ text-align: left; padding: 4px; background-color: black; color: white; }}
        .encabezadoder {{ text-align: right; }}
        .encabezadoizq {{ text-align: left; }}
        .piepagina {{ text-align: right; }}
        .piepagina .sec {{ text-decoration: underline; }}
        tr:nth-child(even) {{ background-color: #dddddd; }}
        hr {{ color: #000; background-color: #000; height: 2px; }}
        </style>
        </head>
        <body>
        <h3>{nombre}<br/></h3>
        <div class="encabezadoizq">
        <p> Factura </p> <br>
        <label>RNC: {rnc}</label> <br>
        <label>Fecha: {fecha}</label> <br>
        <label>Sucursal ID: {id_sucursal}</label> <br>
        <label>Vendido A: {id_cliente} -- {cliente_nombre}</label> <br>
        <label>Teléfono: {telefono}</label>
        </div>
        <div class="encabezadoder">
            <label>Válido Hasta: {valido_hasta}</label> <br>
            <label>Factura No.: {nofac} </label> <br>
        </div>

        <table align="left" width="100%" cellspacing="0">
            <tr>
                <th>ID ART.</th>
                <th>DESCRIPCION</th>
                <th>CANTIDAD</th>
                <th>PRECIO</th>
                <th>ITEBIS</th>
                <th>IMPORTE</th>
            </tr>
        """
        for p in productos:
            html += f"""
            <tr>
                <td>{p['id']}</td>
                <td>{p['nombre']}</td>
                <td>{p['cantidad']}</td>
                <td>${p['precio']:.2f}</td>
                <td>${p['itebis']:.2f}</td>
                <td>${p['importe']:.2f}</td>
            </tr>
            """
        html += f"""
        </table>
        <div class="piepagina">
        <br> <br>
        <hr> <br>
        <label>ITBIS: </label>
        <label class="sec">${total_itebis:.2f}</label><br>
        <label>Total Facturado: </label>
        <label class="sec">${total_facturado:.2f}</label><br>
        </div>
        </body>
        </html>
        """

        # Convertir HTML a PDF
        pdf_file = HTML(string=html).write_pdf()
        return pdf_file

    def run(self):
        self.app.run(debug=True)


# Instanciar y ejecutar la aplicación
if __name__ == '__main__':
    app = FacturaProcessorApp()
    app.run()