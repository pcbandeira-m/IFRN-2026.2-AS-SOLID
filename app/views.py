import sys

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse

from django.views import View

import sqlite3

from . services import CategoriaService, ProdutoService


# Exibe a página inicial da aplicação
def home(request):
    '''Exibe a pagina inicial da aplicação'''
    # define a página HTML (template) que deverá será carregada
    template = 'home.html'
    return render(request, template)

#======================= Atividade ==============================
#======================= Atividade ==============================
#======================= Atividade ==============================

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
                            context={'acao': 'Inclusão', 'form': CategoriaForm() })
        
        elif acao in ['alterar', 'excluir']:
            registro_dict = self.service.exibir_por_id(id)

            acao = 'Alteração' if acao == 'alterar' else 'Exclusão'

            return render(request, 'categorias_editar.html', 
                            context={'acao': acao, 'form': CategoriaForm(initial=registro_dict) })
        
        else:
            categoria = self.service.exibir()
        
        return render(request,'categorias_listar.html',{'registros':categoria})

    def post(self, request, acao=None):

        acao_form = request.POST.get('acao')

        if acao_form == 'Inclusão':
            self._incluir(request)
        elif acao_form == 'Alteração':
            self._alterar(request)
        elif acao_form == 'Exclusão':
            self._excluir(request)
        return HttpResponseRedirect(reverse("categorias"))

    def _incluir(self, request):
        self.service.incluir(request.POST.get('descricao'))

    def _alterar(self, request):
        self.service.alterar(
            request.POST.get('id'),
            request.POST.get('descricao'),
        )

    def _excluir(self, request):
        self.service.excluir(request.POST.get('id'))

 


class ProdutoForm(forms.Form):
    id = forms.IntegerField(label='ID', widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    descricao = forms.CharField(label='Descrição', max_length=30, required=True)
    preco_unitario = forms.DecimalField(label='Preço Unitário', max_digits=10, decimal_places=2, required=True)
    quantidade_estoque = forms.IntegerField(label='Qtd. Estoque', required=True)
    categoria_id = forms.ChoiceField(label='Categoria', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria_id'].choices = CategoriaService().exibir()


class ProdutoView(View):

    '''
    Trabalha com as requisições HTTP
    E respostas para o usuário
    '''
    def __init__(self):
        self.produto = ProdutoService()

    def get(self, request, id=None, acao=None):

        if acao == 'incluir':
            return render(request, 'produtos_editar.html', {
                'acao': 'Inclusão',
                'form': ProdutoForm(),
            })

        if acao in ['alterar', 'excluir']:
            produto = self.produto.exibir_por_id(id)
            acao = 'Alteração' if acao == 'alterar' else 'Exclusão'
            return render(request, 'produtos_editar.html', {
                'acao': acao,
                'form': ProdutoForm(initial=produto),
            })

        produto = self.produto.exibir()
        return render(request, 'produtos_listar.html', {'registros': produto})

    def post(self, request, acao=None):

        acao_form = request.POST.get('acao')

        if acao_form == 'Exclusão':
            self._excluir(request)
        elif acao_form == 'Alteração':
            self._alterar(request)
        elif acao_form == 'Inclusão':
            self._incluir(request)
        return HttpResponseRedirect(reverse("produtos"))

    def _incluir(self, request):
        dados = {
            'descricao': request.POST.get('descricao'),
            'preco_unitario': request.POST.get('preco_unitario'),
            'quantidade_estoque': request.POST.get('quantidade_estoque'),
            'categoria_id': request.POST.get('categoria_id'),
        }
        self.produto.incluir(dados)

    def _alterar(self, request):
        dados = {
            'id': request.POST.get('id'),
            'descricao': request.POST.get('descricao'),
            'preco_unitario': request.POST.get('preco_unitario'),
            'quantidade_estoque': request.POST.get('quantidade_estoque'),
            'categoria_id': request.POST.get('categoria_id'),
        }
        self.produto.alterar(dados)

    def _excluir(self, request):
        self.produto.excluir(request.POST.get('id'))


