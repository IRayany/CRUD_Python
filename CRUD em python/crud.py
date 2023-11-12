import psycopg2
from datetime import datetime, timedelta

class AppBD:
    def __init__(self):
        print('Método Construtor')

    def abrirConexao(self):
        try:
            self.connection = psycopg2.connect(user="postgres", password="estudante123",
            host="localhost",port="5432",
            database= "postgres")
        except (Exception, psycopg2.Error) as error:
            if(self.connection):
                print("Falha ao se conectar ao Banco de Dados", error)

    
                
    def calcularProximaConsulta(self, data_consulta):
        try:
            data_consulta = datetime.strptime(data_consulta, '%Y%m%d')
            dias_para_proxima_consulta = 7
            data_proxima_consulta = data_consulta + timedelta(days=dias_para_proxima_consulta)
            return data_proxima_consulta.strftime('%Y-%m-%d')
        except Exception as e:
            print('Não foi possível calcular a próxima consulta. Erro:', e)
            return None

    def inserirDados(self, raca, nome, peso, data_consulta, valor_medicamentos, valor_total):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()

            data_proxima_consulta_str = self.calcularProximaConsulta(data_consulta)
            

            postgres_insert_query = """INSERT INTO public."pets"
                                       ("raca", "nome", "peso", "data_consulta", "proxima_consulta", "valor_medicamentos", "valor_total") VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            record_to_insert = (raca, nome, peso, data_consulta, data_proxima_consulta_str, valor_medicamentos, valor_total)
            cursor.execute(postgres_insert_query, record_to_insert)

            self.connection.commit()
            count = cursor.rowcount
            print(count, "Registro inserido com sucesso na tabela PETS")
        except (Exception, psycopg2.Error) as error:
            if self.connection:
                print("Falha ao inserir registro na tabela PETS", error)
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada")

    def atualizarDados(self, raca, nome, peso, data_consulta, proxima_consulta, valor_medicamentos, valor_total):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            sql_update_query = """Update public."pets" set "nome" = %s, "peso" = %s, "data_consulta" = %s, "proxima_consulta" = %s, "valor_medicamentos" = %s, "valor_total" =%s where "raca" = %s AND "nome" = %s AND "peso" = %s"""
            cursor.execute(sql_update_query, (nome, peso, data_consulta, proxima_consulta, valor_medicamentos, valor_total, raca, nome, peso))


            self.connection.commit()
            count = cursor.rowcount
            print(count, "Registro atualizado com sucesso!")
            print("Registro Depois da Atualização ")
            sql_select_query = """select * from public."pets"
            where "raca" = %s"""
            cursor.execute(sql_select_query, (raca,))
            record = cursor.fetchone()
            print(record)
        except (Exception, psycopg2.Error) as error:
            print("Erro na Atualização", error)
        finally:
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada")

    def excluirDados(self, raca, nome, peso):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            sql_delete_query = """Delete from public."pets"
            where "raca" = %s AND "nome" = %s AND "peso" = %s"""
            cursor.execute(sql_delete_query, (raca, nome, peso))
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Registro excluído com sucesso!")
        except (Exception, psycopg2.Error) as error:
            print("Erro na Exclusão", error)
        finally:
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada")
