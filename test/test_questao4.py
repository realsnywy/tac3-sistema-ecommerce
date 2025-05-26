import pytest
from app.ecommerce_sistema import Produto, Carrinho


class TestIntegracaoCarrinhoProdutoQuestao4:
    """
    Testes de integração entre Carrinho e Produto usando Pytest (Questão 4).
    """

    @pytest.fixture
    def produto_a(self):
        return Produto(
            id_produto=201,
            nome="Teclado Gamer",
            descricao="Mecânico, RGB",
            preco=350.00,
            quantidade_em_estoque=10,
            categoria="Periféricos",
        )

    @pytest.fixture
    def produto_b(self):
        return Produto(
            id_produto=202,
            nome="Headset Pro",
            descricao="7.1 Surround",
            preco=450.00,
            quantidade_em_estoque=5,
            categoria="Áudio",
        )

    @pytest.fixture
    def produto_sem_estoque(self):
        return Produto(
            id_produto=203,
            nome="Mousepad XXL",
            descricao="Grande porte",
            preco=120.00,
            quantidade_em_estoque=0,
            categoria="Acessórios",
        )

    @pytest.fixture
    def carrinho_novo(self):
        return Carrinho()

    def test_carrinho_atualiza_valor_total_ao_adicionar_produtos(
        self, carrinho_novo, produto_a, produto_b
    ):
        carrinho_novo.adicionar_item(produto_a, 1)
        assert carrinho_novo.calcular_valor_total() == 350.00

        carrinho_novo.adicionar_item(produto_b, 2)
        assert carrinho_novo.calcular_valor_total() == 1250.00

        carrinho_novo.adicionar_item(produto_a, 2)
        assert carrinho_novo.calcular_valor_total() == 1950.00
        assert carrinho_novo.itens[produto_a] == 3

    def test_carrinho_impede_adicao_de_produtos_sem_estoque(
        self, carrinho_novo, produto_a, produto_sem_estoque
    ):
        with pytest.raises(ValueError) as excinfo_sem_estoque:
            carrinho_novo.adicionar_item(produto_sem_estoque, 1)
        assert "excederia o estoque" in str(excinfo_sem_estoque.value)
        assert len(carrinho_novo.itens) == 0

        carrinho_novo.adicionar_item(produto_a, 5)
        assert carrinho_novo.itens[produto_a] == 5

        with pytest.raises(ValueError) as excinfo_excedente:
            carrinho_novo.adicionar_item(produto_a, 6)
        assert "excederia o estoque" in str(excinfo_excedente.value)
        assert carrinho_novo.itens[produto_a] == 5

    def test_carrinho_permite_remover_produtos_parcialmente(
        self, carrinho_novo, produto_a, produto_b
    ):
        carrinho_novo.adicionar_item(produto_a, 5)
        carrinho_novo.adicionar_item(produto_b, 3)
        valor_inicial = (5 * produto_a.preco) + (3 * produto_b.preco)
        assert carrinho_novo.calcular_valor_total() == valor_inicial

        carrinho_novo.remover_item(produto_a, 2)
        assert produto_a in carrinho_novo.itens
        assert carrinho_novo.itens[produto_a] == 3
        valor_apos_remocao_parcial_a = (3 * produto_a.preco) + (3 * produto_b.preco)
        assert carrinho_novo.calcular_valor_total() == valor_apos_remocao_parcial_a

        carrinho_novo.remover_item(produto_b, 1)
        assert produto_b in carrinho_novo.itens
        assert carrinho_novo.itens[produto_b] == 2
        valor_apos_remocao_parcial_b = (3 * produto_a.preco) + (2 * produto_b.preco)
        assert carrinho_novo.calcular_valor_total() == valor_apos_remocao_parcial_b

    def test_carrinho_remove_totalmente_se_quantidade_remover_maior_ou_igual(
        self, carrinho_novo, produto_a
    ):
        carrinho_novo.adicionar_item(produto_a, 3)

        carrinho_novo.remover_item(produto_a, 5)
        assert produto_a not in carrinho_novo.itens
        assert carrinho_novo.calcular_valor_total() == 0.0

        carrinho_novo.adicionar_item(produto_a, 2)
        carrinho_novo.remover_item(produto_a, 2)
        assert produto_a not in carrinho_novo.itens
        assert carrinho_novo.calcular_valor_total() == 0.0

    def test_tentar_remover_produto_nao_existente_no_carrinho(
        self, carrinho_novo, produto_a
    ):
        with pytest.raises(
            ValueError, match=f"Produto '{produto_a.nome}' não encontrado no carrinho."
        ):
            carrinho_novo.remover_item(produto_a, 1)
