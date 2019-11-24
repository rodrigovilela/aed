import psycopg2
import urllib.parse as urlparse
import os

import time

class db():
    
    @staticmethod
    def _connect():
        return psycopg2.connect(
            dbname="dfirdveeu96qjl",
            user="rddckunaytjjjw",
            password="e58481f98da1f39fc82cf7d9be7c90186e1f32ad19d6b30d8603e41699b919c8",
            host="ec2-174-129-18-42.compute-1.amazonaws.com",
            port="5432"
        )

    @staticmethod
    def _close(cursor, connection):
        if (connection):
            cursor.close()
            connection.close()

    @staticmethod
    def query_select():
        try:
            connection = db._connect()
            cursor = connection.cursor()
            
            sql_query = """ SELECT * FROM hello_noticia """
            cursor.execute(sql_query)
            record = cursor.fetchone()

            print(record)

            db._close(cursor, connection)

        except (Exception, psycopg2.Error) as error:
            print("Error while execute query db", error)

    @staticmethod
    def query_insert(data, dataset_name):
        try:            
            connection = db._connect()
            cursor = connection.cursor()

            for titulo, texto in data:
                sql_query = """ INSERT INTO hello_noticia(TITULO, TEXTO, VEICULO) VALUES (%s, %s, %s)"""
                record_data = (titulo, texto, dataset_name)

                cursor.execute(sql_query, record_data)
                connection.commit()
                time.sleep(1)

            count = cursor.rowcount
            print(count, "Record inserted")

            db._close(cursor, connection)

        except (Exception, psycopg2.Error) as error:
            print("Error while execute query db", error)