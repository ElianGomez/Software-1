import numpy as np
from keras.models import load_model
import pymysql
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

conexion = pymysql.connect(host="Localhost",
                           user="root",
                           password="elian2003",
                           database="sispos")
cursor = conexion.cursor()

class Recomendacion:
    def __init__(self):
        super(Recomendacion, self).__init__()
        self.model = load_model("Model_Recommender.h5")

    def Recomendar(self, cliente_id):


        # Conexión a la base de datos para obtener el mapeo de clientes y productos

        # Consulta SQL para obtener los datos necesarios
        query = """
                SELECT c.idcli, p.nompro
                FROM tbcli03 c
                JOIN tbfacmae20 f ON c.idcli = f.idcli
                JOIN tbfacdet21 d ON f.nofac = d.nofac
                JOIN tbpro10 p ON d.idpro = p.idpro;
                """

        # Cargar datos en DataFrame
        df = pd.read_sql(query, conexion)
        conexion.close()

        # Crear los mapeos de usuarios y productos
        self.user_mapping = {idcli: i for i, idcli in enumerate(df['idcli'].unique())}
        self.product_mapping = {nompro: i for i, nompro in enumerate(df['nompro'].unique())}
        # Obtener el índice correspondiente al cliente
        if cliente_id not in self.user_mapping:
            print(f"Cliente {cliente_id} no encontrado.")
            return

        client_index = self.user_mapping[cliente_id]

        # Lista de todos los productos
        product_for_prediction = list(self.product_mapping.values())

        # Realizar la predicción
        predictions = self.model.predict([np.array([client_index] * len(product_for_prediction)), np.array(product_for_prediction)])

        # Obtener los 5 productos recomendados
        recommended_product_ids = np.argsort(predictions[:, 0])[-5:]
        recommended_product = [list(self.product_mapping.keys())[i] for i in recommended_product_ids]

        return recommended_product


# Ejemplo de uso
"""cliente_id = 1  # Reemplazar con el ID del cliente deseado
Predi = Recomendacion()
productos_recomendados = Predi.Recomendar(cliente_id)

if productos_recomendados:
    print(f"Productos recomendados para el cliente {cliente_id}: {productos_recomendados}")
"""