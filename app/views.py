import sys

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse

from django.views import View

from . services import CategoriaService, ProdutoService

# Exibe a página inicial da aplicação
def home(request):
    '''Exibe a pagina inicial da aplicação'''
    # define a página HTML (template) que deverá será carregada
    template = 'home.html'
    return render(request, template)

class CategoriaForm(forms.Form):
    id = forms.IntegerField(label='ID', widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    descricao = forms.CharField(label='Descrição', max_length=30, required=True)

class CategoriaView(View):

    '''
    Trabalha com as requisições HTTP
    E respostas para o usuário
    '''

    def __init__(self):
        self.service = CategoriaService()

        
    def get(self,request, id=None, acao=None):

        if acao == 'incluir':
            return render(request, 'categorias_editar.html',
                          {'acao': 'Inclusão', 'form': CategoriaForm()})

        if id is not None:
            registro_dict = self.service.exibir_por_id(id)
            return render(request, 'categorias_editar.html', 
                            context={'acao': 'Alteração', 'form': CategoriaForm(initial=registro_dict)})

        return render(request, 'categorias_listar.html',
                      {'registros': self.service.exibir()})

    def post(self, request, id=None, acao=None):

        descricao = request.POST.get('descricao')
        if request.POST.get('acao') == 'Exclusão':
            self.service.excluir(id)
        elif id is None:
            self.service.incluir(descricao)
        else:
            self.service.alterar(id, descricao)

        return HttpResponseRedirect(reverse("categorias"))
        

    def put(self, request, id):

        descricao = request.PUT.get('descricao')
        self.service.alterar(id, descricao)
        return HttpResponseRedirect(reverse("categorias"))
 

    def delete(self, id):

        self.service.excluir(id)
        return HttpResponseRedirect(reverse("categorias"))

class ProdutoView(View):

    '''
    Trabalha com as requisições HTTP
    E respostas para o usuário
    '''
    def __init__(self):
        self.produto = ProdutoService()

    def get(self, request, id=None):

        if id:
            produto = self.produto.exibir_por_id(id)
            return render(request,'produtos_lista.html',{'registros':produto})

        produto = self.produto.exibir()
        return render(request,'produtos_listar.html',{'registros':produto})

    def post(self, request):

        dados = {
            'id': request.POST.get('id'),
            'descricao':request.POST.get('descricao'),
            'preco_unitario':request.POST.get('preco_unitario'),
            'quantidade_estoque':request.POST.get('quantidade_estoque'),
            'categoria':request.POST.get('categoria'),
            'acao':request.POST.get('acao')
        }

        self.produto.incluir(dados)
        return HttpResponseRedirect(reverse("produtos"))


    def put(self, request, id):

        dados = {
                'id':id,
                'desicao': request.PUT.get('descricao'),
                'preco_unitario': request.PUT.get('preco_unitario'),
                'quantidade_estoque':request.PUT.get('quantidade_estoque'),
                'categoria':request.PUT.get('categoria'),
                'acao':request.PUT.get('acao')
                 }

        self.produto.alterar(dados)
        return HttpResponseRedirect(reverse("produtos"))
        

    def delete(self, id):

        self.produto.excluir(id)
        return HttpResponseRedirect(reverse("produtos"))