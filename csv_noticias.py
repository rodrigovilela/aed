import pandas as pd
import dados

data = pd.read_csv("C:/Users/Rodrigo/PycharmProjects/aed/noticias_semelhantes.csv", sep=";", header=0)
data['nfDtaNot'] = pd.to_datetime(data.DtaNot)
data['nfDtaNot'] = data['nfDtaNot'].dt.strftime('%Y-%m-%d')

doc_db = [(row['Titulo'], row['ComNot'], row['nfDtaNot']) for idx, row in data.iterrows()]
dados.db.query_insert(doc_db, "similares")