import numpy as np
import pymysql
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.layers import Embedding, Flatten, Dot, Input
from keras.models import Model

# Conexión a la base de datos
conexion = pymysql.connect(host="Localhost",
                           user="root",
                           password="elian2003",
                           database="prbiapos")
cursor = conexion.cursor()

# Consulta SQL
query = """
SELECT c.idcli, p.nompro, f.nofac, d.cantipro, d.prepro
FROM tbcli03 c
JOIN tbfacmae20 f ON c.idcli = f.idcli
JOIN tbfacdet21 d ON f.nofac = d.nofac
JOIN tbpro10 p ON d.idpro = p.idpro;
"""

# Cargar datos en DataFrame
df = pd.read_sql(query, conexion)
conexion.close()

# Crear matriz cliente-producto
client_product_matrix = df.pivot_table(index="idcli", columns="nompro", values="cantipro", aggfunc="sum", fill_value=0)

# Convertir la matriz a formato largo
interaction = client_product_matrix.stack().reset_index()
interaction.columns = ['idcli', 'nompro', 'cantipro']

# Dividir en datos de entrenamiento y prueba
train_data, test_data = train_test_split(interaction, test_size=0.2, random_state=42)

# Obtener el número de usuarios y productos únicos
n_users = interaction['idcli'].nunique()
n_products = interaction['nompro'].nunique()

# Mapear usuarios y productos a índices
user_mapping = {idcli: i for i, idcli in enumerate(interaction['idcli'].unique())}
product_mapping = {nompro: i for i, nompro in enumerate(interaction['nompro'].unique())}

interaction["user_id"] = interaction["idcli"].map(user_mapping)
interaction["product_id"] = interaction["nompro"].map(product_mapping)

# Verificar que no haya NaN y que los índices estén en rango
assert interaction["user_id"].notnull().all(), "Hay valores NaN en user_id"
assert interaction["product_id"].notnull().all(), "Hay valores NaN en product_id"
assert interaction["user_id"].between(0, n_users - 1).all(), "user_id fuera de rango"
assert interaction["product_id"].between(0, n_products - 1).all(), "product_id fuera de rango"

# Construir el modelo
user_input = Input(shape=(1,))
producto_input = Input(shape=(1,))
user_embedding = Embedding(n_users, 50)(user_input)
product_embedding = Embedding(n_products, 50)(producto_input)

user_vec = Flatten()(user_embedding)
product_vec = Flatten()(product_embedding)
dot_product = Dot(axes=1)([user_vec, product_vec])

model = Model([user_input, producto_input], dot_product)
model.compile(optimizer="adam", loss="mean_squared_error")

# Entrenar el modelo
model.fit([interaction["user_id"], interaction["product_id"]], interaction["cantipro"], epochs=10, batch_size=32, validation_split=0.2)

model.save("Model_Recommender.h5")
print("Modelo Entrenado y Guardado")
# Predecir productos para un cliente específico
client_id = 73670
client_index = user_mapping[client_id]  # Mapea el ID del cliente al índice correspondiente
product_for_prediction = list(product_mapping.values())

# Predecir
predictions = model.predict([np.array([client_index] * len(product_for_prediction)), np.array(product_for_prediction)])

# Obtener los 5 productos recomendados
recommended_product_ids = np.argsort(predictions[:, 0])[-5:]
recommended_product = [list(product_mapping.keys())[i] for i in recommended_product_ids]
print("Productos recomendados: ", recommended_product)
