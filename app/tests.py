from django.test import TestCase, Client
from django.urls import reverse


class ProdutoViewTest(TestCase):
    def test_cadastrar_produto(self):
        from app.services import CategoriaService

        categoria = CategoriaService()
        categoria.incluir('Eletrônicos')

        response = Client().post(
            '/produtos/salvar/',
            {
                'acao': 'Inclusão',
                'descricao': 'Mouse',
                'preco_unitario': '25.90',
                'quantidade_estoque': '12',
                'categoria_id': '1',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('produtos'))
