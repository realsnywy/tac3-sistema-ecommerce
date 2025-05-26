import pytest
from unittest.mock import patch
from app.ecommerce_sistema import SistemaEcommerce, Carrinho, Produto


@pytest.fixture
def sistema_com_usuario_e_produto():
    sistema = SistemaEcommerce()
    cliente_id = "user_mock_test"
    sistema.registrar_usuario(
        cliente_id, {"nome": "Mock User", "email": "mock@example.com"}
    )
    produto_mock = sistema.adicionar_produto_catalogo(
        "Produto Mock", "Para testes de mock", 100.00, 5, "Mocks"
    )
    return sistema, cliente_id, produto_mock


@pytest.fixture
def carrinho_com_produto(sistema_com_usuario_e_produto):  # Depende do fixture anterior
    _, _, produto_mock = sistema_com_usuario_e_produto
    carrinho = Carrinho()
    carrinho.adicionar_item(produto_mock, 1)
    return carrinho


class TestFalhasPagamentoQuestao7:
    """
    Testes para simular falhas no processamento de pagamento usando Pytest e Mock (Questão 7).
    """

    def test_simular_falha_autorizacao_cartao(
        self, sistema_com_usuario_e_produto, carrinho_com_produto
    ):
        sistema, cliente_id, _ = sistema_com_usuario_e_produto
        carrinho = carrinho_com_produto
        endereco = {"rua": "Rua Mock", "cep": "00000-111"}

        pedido = sistema.criar_pedido(cliente_id, carrinho, endereco, "cartao_credito")
        assert pedido is not None
        assert pedido.status_pedido == "pendente"
        id_pedido = pedido.id_pedido

        detalhes_cartao_falha_autorizacao = {
            "numero_cartao": "1234567890_falha_autorizacao",
            "cvv": "123",
            "validade": "12/25",
            "numero_parcelas": 1,
        }

        resultado = sistema.processar_pagamento_pedido(
            id_pedido, detalhes_cartao_falha_autorizacao
        )

        assert resultado["status"] == "rejeitado"
        assert "Falha na autorização do cartão de crédito" in resultado["mensagem"]

        pedido_apos_falha = sistema.pedidos_registrados[id_pedido]
        assert pedido_apos_falha.status_pedido == "pendente"
        assert pedido_apos_falha.id_transacao_pagamento is None
        assert pedido_apos_falha.valor_final_pago is None
        assert pedido_apos_falha.datas["pagamento"] is None

    def test_simular_timeout_gateway_pagamento(
        self, sistema_com_usuario_e_produto, carrinho_com_produto
    ):
        sistema, cliente_id, _ = sistema_com_usuario_e_produto
        carrinho = carrinho_com_produto
        endereco = {"rua": "Rua Timeout", "cep": "00000-222"}

        pedido = sistema.criar_pedido(cliente_id, carrinho, endereco, "cartao_credito")
        assert pedido is not None
        assert pedido.status_pedido == "pendente"
        id_pedido = pedido.id_pedido

        detalhes_cartao_timeout = {
            "numero_cartao": "9876543210_timeout",
            "cvv": "321",
            "validade": "10/26",
            "numero_parcelas": 1,
        }

        resultado = sistema.processar_pagamento_pedido(
            id_pedido, detalhes_cartao_timeout
        )

        assert resultado["status"] == "erro"
        assert (
            "Timeout na comunicação com o gateway de pagamento" in resultado["mensagem"]
        )

        pedido_apos_timeout = sistema.pedidos_registrados[id_pedido]
        assert pedido_apos_timeout.status_pedido == "pendente"
        assert pedido_apos_timeout.id_transacao_pagamento is None
        assert pedido_apos_timeout.valor_final_pago is None
        assert pedido_apos_timeout.datas["pagamento"] is None

    def test_pedido_mantem_estado_correto_apos_falha_generica_no_pagamento_usando_patch(
        self, sistema_com_usuario_e_produto, carrinho_com_produto
    ):
        sistema, cliente_id, produto_no_carrinho = sistema_com_usuario_e_produto
        carrinho = carrinho_com_produto
        endereco = {"rua": "Rua Patch", "cep": "00000-333"}

        estoque_original = produto_no_carrinho.quantidade_em_estoque

        pedido = sistema.criar_pedido(cliente_id, carrinho, endereco, "pix")
        assert pedido is not None
        id_pedido = pedido.id_pedido

        with patch.object(
            sistema.sistema_pagamento,
            "processar_pagamento",
            return_value={
                "status": "rejeitado",
                "mensagem": "Falha genérica simulada",
                "id_transacao": None,
            },
        ) as mock_processar_pagamento:

            detalhes_pagamento_qualquer = {"chave_pix": "falha@pix.com"}
            resultado = sistema.processar_pagamento_pedido(
                id_pedido, detalhes_pagamento_qualquer
            )

            mock_processar_pagamento.assert_called_once()
            assert resultado["status"] == "rejeitado"
            assert resultado["mensagem"] == "Falha genérica simulada"

            pedido_apos_falha = sistema.pedidos_registrados[id_pedido]
            assert pedido_apos_falha.status_pedido == "pendente"
            assert pedido_apos_falha.id_transacao_pagamento is None
            assert pedido_apos_falha.valor_final_pago is None
            assert pedido_apos_falha.datas["pagamento"] is None

            produto_catalogo = sistema.recuperar_produto_por_id(
                produto_no_carrinho.id_produto
            )
            assert produto_catalogo.quantidade_em_estoque == estoque_original

    def test_simular_falha_fraude_no_pagamento(
        self, sistema_com_usuario_e_produto, carrinho_com_produto
    ):
        sistema, cliente_id, _ = sistema_com_usuario_e_produto
        carrinho = carrinho_com_produto
        endereco = {"rua": "Rua da Fraude", "cep": "00000-444"}

        pedido = sistema.criar_pedido(cliente_id, carrinho, endereco, "cartao_credito")
        assert pedido is not None
        id_pedido = pedido.id_pedido

        detalhes_cartao_fraude = {
            "numero_cartao": "111_cartao_suspeito_222",
            "cvv": "789",
            "validade": "01/27",
            "numero_parcelas": 1,
        }
        resultado = sistema.processar_pagamento_pedido(
            id_pedido, detalhes_cartao_fraude
        )

        assert resultado["status"] == "rejeitado"
        assert "Pagamento rejeitado por suspeita de fraude" in resultado["mensagem"]

        pedido_apos_falha = sistema.pedidos_registrados[id_pedido]
        assert pedido_apos_falha.status_pedido == "pendente"
        assert pedido_apos_falha.id_transacao_pagamento is None
