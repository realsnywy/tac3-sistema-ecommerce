import unittest
from app.ecommerce_sistema import Produto, Carrinho


class TestCarrinhoQuestao2(unittest.TestCase):
    """
    Testes para a classe Carrinho utilizando unittest (Questão 2).
    """

    def setUp(self):
        self.produto1 = Produto(
            id_produto=101,
            nome="Laptop",
            descricao="Core i7, 16GB RAM",
            preco=5000.00,
            quantidade_em_estoque=10,
            categoria="Eletrônicos",
        )
        self.produto2 = Produto(
            id_produto=102,
            nome="Mouse Gamer",
            descricao="Mouse com RGB",
            preco=150.00,
            quantidade_em_estoque=20,
            categoria="Acessórios",
        )
        self.produto_sem_estoque = Produto(
            id_produto=103,
            nome="Monitor Ultrawide",
            descricao="34 polegadas",
            preco=2500.00,
            quantidade_em_estoque=0,
            categoria="Monitores",
        )
        self.carrinho = Carrinho()

    def test_adicao_de_itens_no_carrinho(self):
        self.carrinho.adicionar_item(self.produto1, 2)
        self.assertIn(self.produto1, self.carrinho.itens)
        self.assertEqual(self.carrinho.itens[self.produto1], 2)

        self.carrinho.adicionar_item(self.produto2, 1)
        self.assertIn(self.produto2, self.carrinho.itens)
        self.assertEqual(self.carrinho.itens[self.produto2], 1)

    def test_remocao_de_itens_do_carrinho(self):
        self.carrinho.adicionar_item(self.produto1, 3)
        self.carrinho.remover_item(self.produto1, 1)
        self.assertEqual(self.carrinho.itens[self.produto1], 2)

        self.carrinho.remover_item(self.produto1, 2)
        self.assertNotIn(self.produto1, self.carrinho.itens)

    def test_calculo_do_valor_total_do_carrinho(self):
        self.carrinho.adicionar_item(self.produto1, 1)
        self.carrinho.adicionar_item(self.produto2, 2)
        self.assertEqual(self.carrinho.calcular_valor_total(), 5300.00)

    def test_comportamento_ao_tentar_adicionar_produto_sem_estoque_suficiente(self):
        with self.assertRaisesRegex(ValueError, "excederia o estoque"):
            self.carrinho.adicionar_item(self.produto1, 11)

        with self.assertRaisesRegex(ValueError, "excederia o estoque"):
            self.carrinho.adicionar_item(self.produto_sem_estoque, 1)

        self.carrinho.adicionar_item(self.produto2, 18)
        with self.assertRaisesRegex(ValueError, "excederia o estoque"):
            self.carrinho.adicionar_item(self.produto2, 3)

    def test_adicionar_item_duas_vezes_soma_quantidade(self):
        produto_estoque_suf_soma = Produto(
            id_produto=104,
            nome="SSD",
            descricao="1TB NVMe",
            preco=800.00,
            quantidade_em_estoque=5,
            categoria="Armazenamento",
        )
        self.carrinho.adicionar_item(produto_estoque_suf_soma, 2)
        self.assertEqual(self.carrinho.itens[produto_estoque_suf_soma], 2)

        self.carrinho.adicionar_item(produto_estoque_suf_soma, 3)
        self.assertEqual(self.carrinho.itens[produto_estoque_suf_soma], 5)

    def test_limpar_carrinho(self):
        self.carrinho.adicionar_item(self.produto1, 1)
        self.carrinho.limpar_carrinho()
        self.assertEqual(len(self.carrinho.itens), 0)
        self.assertEqual(self.carrinho.calcular_valor_total(), 0.0)


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
