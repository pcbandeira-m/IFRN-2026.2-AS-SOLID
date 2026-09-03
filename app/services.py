import sqlite3

class ConexaoService:

    '''
    Faz a conexão com o Banco de dados
    '''

    def conexao(self):
        # obtem a conexao com o banco de dados
        conexao = sqlite3.connect('db_solid.sqlite3')
        # comando para não permitir DELETE CASCADE (exclusão em cascata)
        conexao.execute("PRAGMA foreign_keys = ON;")

        return conexao
    

class CategoriaService:

    '''
    Trabalha com as regras de negócio persistência 
    no bancos de dados usando comandos SQL.
    '''

    def __init__(self):
        self.conexao = ConexaoService().conexao()
    
    def exibir(self):
        sql = '''
                SELECT  id, 
                        descricao
                FROM Categoria 
                ORDER BY descricao
              '''
            
        # cria um cursor(), executa o SELECT informado e traz os todos os registros
        return self.conexao.cursor().execute(sql).fetchall()

    def exibir_por_id(self, id):
        sql = '''
                SELECT  id, 
                        descricao 
                FROM Categoria 
            WHERE id = ?
            '''

        # cria um cursor(), executa o SELECT para retornar o registro pelo ID
        registro = self.conexao.cursor().execute(sql, (id,)).fetchone()
        registro_dict = {'id': registro[0], 'descricao': registro[1]}
        return registro_dict

    def incluir(self, descricao):
        sql = f"INSERT INTO Categoria(descricao) VALUES('{descricao}')"

        # cria um cursor() e executa o SQL informado
        self.conexao.cursor().execute(sql)
        self.conexao.commit()
    
    def excluir(self, id):
        sql = f"DELETE FROM Categoria WHERE id = {id}"

        # cria um cursor() e executa o SQL informado
        self.conexao.cursor().execute(sql)
        self.conexao.commit()

    def alterar(self, id, descricao):
        sql = f'''
                UPDATE Categoria 
                SET descricao = '{descricao}' 
                WHERE id = {id}
                '''

        # cria um cursor() e executa o SQL informado
        self.conexao.cursor().execute(sql)
        self.conexao.commit()


class ProdutoService:

    '''
    Trabalha com as regras de negócio persistência 
    no bancos de dados usando comandos SQL.
    '''

    def __init__(self):
        self.conexao = ConexaoService().conexao()

    def exibir(self):
        # define o comando SQL que será executado
        sql = '''
            SELECT  pro.id,
                    pro.descricao, 
                    pro.preco_unitario,
                    pro.quantidade_estoque,
                    pro.categoria_id,
                    cat.descricao as 'categoria'
                    
            FROM Produto pro
            INNER JOIN Categoria cat ON cat.id = pro.categoria_id

            ORDER BY pro.descricao
        '''
        
        # cria um cursor(), executa o SELECT informado e traz os todos os registros
        return self.conexao.cursor().execute(sql).fetchall()

    def exibir_por_id(self, id):
        sql = f'''
                SELECT  pro.id,
                        pro.descricao, 
                        pro.preco_unitario,
                        pro.quantidade_estoque,
                        pro.categoria_id,
                        cat.descricao as 'categoria'
                        
                FROM Produto pro
                INNER JOIN Categoria cat ON cat.id = pro.categoria_id

                WHERE pro.id={id}    
            '''

        # cria um cursor(), executa o SELECT para retornar o registro pelo ID
        registro = self.conexao.cursor().execute(sql).fetchone()
        registro_dict = {
            'id': registro[0], 
            'descricao': registro[1],
            'preco_unitario': registro[2],
            'quantidade_estoque': registro[3],
            'categoria_id': registro[4],
            'categoria': registro[5],
        }
        
        return registro_dict
    
    def incluir(self, dados):
        sql = f'''
                    INSERT INTO Produto (
                        descricao, 
                        preco_unitario, 
                        quantidade_estoque, 
                        categoria_id
                    )
                    VALUES(
                        '{dados['descricao']}', 
                        {dados['preco_unitario']}, 
                        {dados['quantidade_estoque']}, 
                        {dados['categoria_id']}
                    );
                '''

        # cria um cursor() e executa o SQL informado
        self.conexao.cursor().execute(sql)
        self.conexao.commit()
    
    def excluir(self, id):
        sql = f"DELETE FROM Produto WHERE id = {'id'}"

        # cria um cursor() e executa o SQL informado
        self.conexao.cursor().execute(sql)
        self.conexao.commit()

    def alterar(self, dados):
        sql = f'''
                    UPDATE Produto 
                    SET descricao = '{dados['descricao']}', 
                        preco_unitario = {dados['preco_unitario']}, 
                        quantidade_estoque = {dados['quantidade_estoque']}, 
                        categoria_id = {dados['categoria_id']} 
                    WHERE id = {dados['id']}
                '''

        # cria um cursor() e executa o SQL informado
        self.conexao.cursor().execute(sql)
        self.conexao.commit()