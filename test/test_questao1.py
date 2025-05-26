import pytest
from app.ecommerce_sistema import Produto


class TestProdutoQuestao1:
    """
    Testes para a classe Produto utilizando Pytest (Questão 1).
    """

    def test_criacao_produto_sucesso(self):
        produto = Produto(
            id_produto=1,
            nome="Laptop Gamer",
            descricao="Laptop de alta performance para jogos",
            preco=7500.00,
            quantidade_em_estoque=10,
            categoria="Eletrônicos",
        )
        assert produto.id_produto == 1
        assert produto.nome == "Laptop Gamer"
        assert produto.preco == 7500.00
        assert produto.quantidade_em_estoque == 10

    def test_criacao_produto_preco_invalido(self):
        with pytest.raises(ValueError, match="Preço deve ser um número positivo."):
            Produto(
                id_produto=2,
                nome="Mouse",
                descricao="Mouse óptico",
                preco=0,
                quantidade_em_estoque=50,
                categoria="Acessórios",
            )

    def test_criacao_produto_estoque_invalido(self):
        with pytest.raises(
            ValueError, match="Quantidade em estoque deve ser um inteiro não negativo."
        ):
            Produto(
                id_produto=4,
                nome="Monitor",
                descricao="Monitor 27 polegadas",
                preco=1200.00,
                quantidade_em_estoque=-5,
                categoria="Eletrônicos",
            )

    def test_verificar_disponibilidade_estoque_suficiente(self):
        produto = Produto(
            id_produto=1,
            nome="Produto A",
            descricao="Desc A",
            preco=10.0,
            quantidade_em_estoque=5,
            categoria="Cat A",
        )
        assert produto.verificar_disponibilidade(3) is True
        assert produto.verificar_disponibilidade(5) is True

    def test_verificar_disponibilidade_estoque_insuficiente(self):
        produto = Produto(
            id_produto=2,
            nome="Produto B",
            descricao="Desc B",
            preco=20.0,
            quantidade_em_estoque=2,
            categoria="Cat B",
        )
        assert produto.verificar_disponibilidade(3) is False

    def test_verificar_disponibilidade_quantidade_invalida(self):
        produto = Produto(
            id_produto=3,
            nome="Produto C",
            descricao="Desc C",
            preco=30.0,
            quantidade_em_estoque=10,
            categoria="Cat C",
        )
        with pytest.raises(
            ValueError, match="Quantidade desejada deve ser um inteiro positivo."
        ):
            produto.verificar_disponibilidade(0)

    def test_reduzir_estoque_sucesso(self):
        produto = Produto(
            id_produto=4,
            nome="Produto D",
            descricao="Desc D",
            preco=40.0,
            quantidade_em_estoque=10,
            categoria="Cat D",
        )
        produto.reduzir_estoque(3)
        assert produto.quantidade_em_estoque == 7

    def test_reduzir_estoque_insuficiente(self):
        produto = Produto(
            id_produto=5,
            nome="Produto E",
            descricao="Desc E",
            preco=50.0,
            quantidade_em_estoque=5,
            categoria="Cat E",
        )
        with pytest.raises(
            ValueError, match="Não há estoque suficiente para esta venda"
        ):
            produto.reduzir_estoque(6)
        assert produto.quantidade_em_estoque == 5

    def test_reduzir_estoque_quantidade_invalida(self):
        produto = Produto(
            id_produto=6,
            nome="Produto F",
            descricao="Desc F",
            preco=60.0,
            quantidade_em_estoque=8,
            categoria="Cat F",
        )
        with pytest.raises(
            ValueError, match="Quantidade vendida deve ser um inteiro positivo."
        ):
            produto.reduzir_estoque(0)

    def test_adicionar_estoque_sucesso(self):
        produto = Produto(
            id_produto=7,
            nome="Produto G",
            descricao="Desc G",
            preco=70.0,
            quantidade_em_estoque=10,
            categoria="Cat G",
        )
        produto.adicionar_estoque(5)
        assert produto.quantidade_em_estoque == 15

    def test_adicionar_estoque_quantidade_invalida(self):
        produto = Produto(
            id_produto=8,
            nome="Produto H",
            descricao="Desc H",
            preco=80.0,
            quantidade_em_estoque=12,
            categoria="Cat H",
        )
        with pytest.raises(
            ValueError, match="Quantidade adicionada deve ser um inteiro positivo."
        ):
            produto.adicionar_estoque(0)
