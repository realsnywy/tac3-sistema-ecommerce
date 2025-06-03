from testify import (
    TestCase,
    assert_equal,
    assert_is_not,
    assert_in,
    assert_gte,
    run,
    setup,
    suite,
)
from app.ecommerce_sistema import SistemaEcommerce, Carrinho, Produto


@suite("SistemaEcommerceTestifySuiteQuestao6")
class TestSistemaEcommerceComTestifyQuestao6(TestCase):
    """
    Testes para a classe SistemaEcommerce utilizando a biblioteca Testify (Questão 6).
    """

    @setup
    def inicializar_sistema_ecommerce(self):
        self.sistema = SistemaEcommerce()
        self.cliente_id_teste = "user_AgostinhoCarrara"
        self.sistema.registrar_usuario(
            self.cliente_id_teste,
            {"nome": "Agostinho Carrara", "email": "agostinho@example.com"},
        )
        self.endereco_teste = {
            "rua": "Rua das Palmeiras",
            "numero": "10",
            "cep": "22222-000",
            "cidade": "Rio de Janeiro",
        }
        self.produto_tv = self.sistema.adicionar_produto_catalogo(
            'TV 4K 50"', "Smart TV com HDR", 2500.00, 10, "Eletrônicos"
        )
        self.produto_fone = self.sistema.adicionar_produto_catalogo(
            "Fone Bluetooth", "Cancelamento de ruído", 300.00, 25, "Áudio"
        )
        self.produto_livro = self.sistema.adicionar_produto_catalogo(
            "A Arte da Guerra", "Sun Tzu", 50.00, 0, "Livros"
        )

    def test_adicao_e_recuperacao_de_produtos(self):
        assert_equal(len(self.sistema.produtos_catalogo), 3)
        produto_recuperado_tv = self.sistema.recuperar_produto_por_id(
            self.produto_tv.id_produto
        )
        assert_is_not(produto_recuperado_tv, None, "TV deveria ser recuperada")
        assert_equal(produto_recuperado_tv.nome, 'TV 4K 50"')
        produto_inexistente = self.sistema.recuperar_produto_por_id(999)
        assert_is_not(produto_inexistente, None, "Produto ID 999 não deveria existir")
        novo_produto = self.sistema.adicionar_produto_catalogo(
            "Cadeira Gamer", "Confortável", 1200.00, 5, "Móveis"
        )
        assert_equal(len(self.sistema.produtos_catalogo), 4)
        produto_recuperado_cadeira = self.sistema.recuperar_produto_por_id(
            novo_produto.id_produto
        )
        assert_equal(produto_recuperado_cadeira.nome, "Cadeira Gamer")

    def test_criacao_de_pedidos_sucesso(self):
        carrinho_compra = Carrinho()
        carrinho_compra.adicionar_item(self.produto_tv, 1)
        pedido = self.sistema.criar_pedido(
            self.cliente_id_teste, carrinho_compra, self.endereco_teste, "pix"
        )
        assert_is_not(pedido, None, "Pedido deveria ser criado")
        assert_equal(pedido.cliente_id, self.cliente_id_teste)
        assert_equal(len(pedido.itens_comprados), 1)
        assert_equal(
            pedido.itens_comprados[0][0].id_produto, self.produto_tv.id_produto
        )
        assert_equal(pedido.status_pedido, "pendente")
        assert_in(pedido.id_pedido, self.sistema.pedidos_registrados)

    def test_criacao_de_pedidos_falha_carrinho_vazio_ou_usuario_invalido(self):
        carrinho_vazio = Carrinho()
        pedido_carrinho_vazio = self.sistema.criar_pedido(
            self.cliente_id_teste, carrinho_vazio, self.endereco_teste, "pix"
        )
        assert_is_not(
            pedido_carrinho_vazio,
            None,
            "Pedido com carrinho vazio não deveria ser criado",
        )
        pedido_usuario_invalido = self.sistema.criar_pedido(
            "usuario_fantasma", carrinho_vazio, self.endereco_teste, "pix"
        )
        assert_is_not(
            pedido_usuario_invalido,
            None,
            "Pedido com usuário inválido não deveria ser criado",
        )

    def test_processamento_de_pagamento_sucesso_e_reducao_estoque(self):
        carrinho_pagamento = Carrinho()
        carrinho_pagamento.adicionar_item(self.produto_fone, 2)
        pedido = self.sistema.criar_pedido(
            self.cliente_id_teste, carrinho_pagamento, self.endereco_teste, "pix"
        )
        assert_is_not(pedido, None)
        id_pedido = pedido.id_pedido
        estoque_fone_antes = self.produto_fone.quantidade_em_estoque
        detalhes_pagamento_pix = {"chave_pix": "teste@pix.com"}
        resultado_pagamento = self.sistema.processar_pagamento_pedido(
            id_pedido, detalhes_pagamento_pix
        )
        assert_equal(
            resultado_pagamento["status"],
            "aprovado",
            f"Mensagem: {resultado_pagamento.get('mensagem')}",
        )
        pedido_processado = self.sistema.pedidos_registrados[id_pedido]
        assert_equal(pedido_processado.status_pedido, "pago")
        estoque_fone_depois = self.produto_fone.quantidade_em_estoque
        assert_equal(
            estoque_fone_depois,
            estoque_fone_antes - 2,
            "Estoque do fone deveria ter sido reduzido em 2",
        )

    def test_processamento_de_pagamento_falha_autorizacao(self):
        carrinho_falha = Carrinho()
        carrinho_falha.adicionar_item(self.produto_tv, 1)
        pedido = self.sistema.criar_pedido(
            self.cliente_id_teste, carrinho_falha, self.endereco_teste, "cartao_credito"
        )
        assert_is_not(pedido, None)
        id_pedido = pedido.id_pedido
        estoque_tv_antes = self.produto_tv.quantidade_em_estoque
        detalhes_cartao_falha = {
            "numero_cartao": "1234_falha_autorizacao",
            "cvv": "123",
            "validade": "12/28",
        }
        resultado_pagamento = self.sistema.processar_pagamento_pedido(
            id_pedido, detalhes_cartao_falha
        )
        assert_equal(resultado_pagamento["status"], "rejeitado")
        assert_in("Falha na autorização", resultado_pagamento["mensagem"])
        pedido_apos_falha = self.sistema.pedidos_registrados[id_pedido]
        assert_equal(pedido_apos_falha.status_pedido, "pendente")
        assert_equal(
            self.produto_tv.quantidade_em_estoque,
            estoque_tv_antes,
            "Estoque da TV não deveria mudar.",
        )

    def test_processamento_de_pagamento_falha_estoque_insuficiente_apos_criacao(self):
        prod_pouco_estoque = self.sistema.adicionar_produto_catalogo(
            "Item Raro", "Só 1 unidade", 1000.00, 1, "Colecionáveis"
        )
        carrinho_item_raro = Carrinho()
        carrinho_item_raro.adicionar_item(prod_pouco_estoque, 1)
        pedido_raro = self.sistema.criar_pedido(
            self.cliente_id_teste, carrinho_item_raro, self.endereco_teste, "pix"
        )
        assert_is_not(pedido_raro, None)
        id_pedido_raro = pedido_raro.id_pedido
        prod_pouco_estoque.reduzir_estoque(1)
        detalhes_pagamento_pix = {"chave_pix": "raro@pix.com"}
        resultado_pagamento = self.sistema.processar_pagamento_pedido(
            id_pedido_raro, detalhes_pagamento_pix
        )
        assert_equal(resultado_pagamento["status"], "aprovado_com_erro_estoque")
        assert_in("Erro ao reduzir estoque", resultado_pagamento["mensagem"])
        pedido_processado = self.sistema.pedidos_registrados[id_pedido_raro]
        assert_equal(pedido_processado.status_pedido, "pago")

    def test_cancelamento_de_pedido_pendente_sem_reabastecimento(self):
        carrinho_cancelar = Carrinho()
        carrinho_cancelar.adicionar_item(self.produto_fone, 3)
        pedido = self.sistema.criar_pedido(
            self.cliente_id_teste,
            carrinho_cancelar,
            self.endereco_teste,
            "cartao_credito",
        )
        assert_is_not(pedido, None)
        id_pedido = pedido.id_pedido
        estoque_fone_antes_cancel = self.produto_fone.quantidade_em_estoque
        sucesso_cancelamento = self.sistema.cancelar_pedido(id_pedido)
        assert_gte(sucesso_cancelamento, True, "Cancelamento deveria ser bem-sucedido")
        pedido_cancelado = self.sistema.pedidos_registrados[id_pedido]
        assert_equal(pedido_cancelado.status_pedido, "cancelado")
        assert_equal(
            self.produto_fone.quantidade_em_estoque,
            estoque_fone_antes_cancel,
            "Estoque não deveria mudar.",
        )

    def test_cancelamento_de_pedido_pago_com_reabastecimento_de_estoque(self):
        carrinho_reabastecer = Carrinho()
        qtd_comprada = 2
        carrinho_reabastecer.adicionar_item(self.produto_tv, qtd_comprada)
        pedido = self.sistema.criar_pedido(
            self.cliente_id_teste, carrinho_reabastecer, self.endereco_teste, "pix"
        )
        assert_is_not(pedido, None)
        id_pedido = pedido.id_pedido
        estoque_tv_inicial = self.produto_tv.quantidade_em_estoque
        resultado_pagamento = self.sistema.processar_pagamento_pedido(
            id_pedido, {"chave_pix": "reab@pix.com"}
        )
        assert_equal(resultado_pagamento["status"], "aprovado")
        assert_equal(
            self.produto_tv.quantidade_em_estoque, estoque_tv_inicial - qtd_comprada
        )
        estoque_tv_antes_cancel_pago = self.produto_tv.quantidade_em_estoque
        sucesso_cancelamento = self.sistema.cancelar_pedido(id_pedido)
        assert_gte(
            sucesso_cancelamento,
            True,
            "Cancelamento de pedido pago deveria ser bem-sucedido",
        )
        pedido_cancelado = self.sistema.pedidos_registrados[id_pedido]
        assert_equal(pedido_cancelado.status_pedido, "cancelado")
        estoque_tv_depois_cancel_pago = self.produto_tv.quantidade_em_estoque
        assert_equal(
            estoque_tv_depois_cancel_pago,
            estoque_tv_antes_cancel_pago + qtd_comprada,
            "Estoque da TV deveria ter sido reabastecido.",
        )
        assert_equal(
            estoque_tv_depois_cancel_pago,
            estoque_tv_inicial,
            "Estoque da TV deveria ter voltado ao valor inicial.",
        )


if __name__ == "__main__":
    run()
