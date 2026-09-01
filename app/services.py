from django import forms


class CategoriaService(forms.Form):

    '''
    Trabalha com as regras de negócio persistência 
    no bancos de dados usando comandos SQL.
    '''

    id = forms.IntegerField(label='ID', widget=forms.TextInput(attrs{'readonly':'readonly'}), required = False)
    descricao = forms.CharField(label= 'Descrição', max_length=30, required=True)

    exibir():
        pass 
    
    incluir():
        pass
    
    excluir():
        pass

    alterar():
        pass
    
    salvar():
        pass


class ProdutoService(forms.Form):

    '''
    Trabalha com as regras de negócio persistência 
    no bancos de dados usando comandos SQL.
    '''

    id = forms.IntegerField(label='ID', widget=forms.TextInput(attrs{'readonly':'readonly'}, required=False))
    descricao = forms.CharField(label='Descrição', max_length=30, required=True)
    preco_unitario = forms.DecimalField(label='Preço Unitário', max_digits=10, decimal_places=2, required=True)
    quantidade_estoque = forms.IntegerField(label='Qtd. Estoque', required=True)
    categoria_id = forms.CharField(label='Categoria', required=True)


    exibir():
        pass 
    
    incluir():
        pass
    
    excluir():
        pass

    alterar():
        pass
    
    salvar():
        pass

class ConexaoService:

    '''
    Faz a conexão com o Banco de dados
    '''

    conexao():
        pass

