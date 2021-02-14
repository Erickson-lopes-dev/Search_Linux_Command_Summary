import os
import sqlite3

from web_scraping import scraping_summary


class DataBase:
    def __init__(self):
        # nome da base de dados
        self.name_file = 'database.db'
        # verifica se não existe o arquivo
        if not os.path.exists(self.name_file):
            try:
                # tenta criar o arquivo e se conectar a ele
                self.conn = sqlite3.connect(self.name_file)
                # cria um cursor
                cursor = self.conn.cursor()
                # executa um script para criar uma tabela com duas colunas
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS summary (
                    id integer primary key,
                    command text,
                    overview text,
                    link text
                )
                """)
                print('[!] Tabela summary foi Criada com sucesso!')
                # adiciona os itens do sumario dentro da
                self.add_items_summary()
                # Fecha a conexão
                self.conn.close()
            except Exception as err:
                print(err)
                # Caso ocorra algum erro, exclui a base
                os.remove(self.name_file)

    # Adicionar todos os itens do sumário dentro da bd
    def add_items_summary(self):
        # instancia um cursos
        cursor = self.conn.cursor()
        # Sql para adicionar itens dentro da base de dados
        sql = 'INSERT INTO summary (command, overview, link) VALUES (?, ?, ?)'
        # Carrega os itens recebidos da função de scraping
        val = scraping_summary()
        # Realiza a query de inserção de todos os itens da lista
        cursor.executemany(sql, val)

        # Comita dentro da base de dados, salvando as alterações
        self.conn.commit()
        # Exibe o total de linhas afetadas
        print(f"[!] Adicionando um total de '{cursor.rowcount}' linha(s)")

    # Retorna os dados do do sumario de dentro da base de dados
    def select_all_summary(self):
        # Faz a conexão com o banco
        conn = sqlite3.connect(self.name_file)
        # Instancia um cursor
        cursor = conn.cursor()
        # Seleciona todos os itens do summary
        cursor.execute('SELECT * FROM summary')
        # Armazena o resultado da query
        result = cursor.fetchall()

        for item in result:
            print(item)


# create_table()
if __name__ == '__main__':
    db = DataBase()

    # db.select_all()
