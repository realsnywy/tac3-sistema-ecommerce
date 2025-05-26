import unittest
from app.ecommerce_sistema import SistemaEcommerce, Carrinho, Produto


class TestFluxoCompletoCompraQuestao8(unittest.TestCase):
    """
    Testes para o fluxo completo de compra utilizando unittest e setUp para fixtures (Questão 8).
    """

    @classmethod
    def setUpClass(cls):
        cls.sistema_geral_template = SistemaEcommerce()  # Usado como template
        cls.produto_fluxo_1_template = (
            cls.sistema_geral_template.adicionar_produto_catalogo(
                nome="Console PS6",
                descricao="Video Game de Última Geração",
                preco=4999.90,
                quantidade_em_estoque=15,
                categoria="Games",
            )
        )
        cls.produto_fluxo_2_template = (
            cls.sistema_geral_template.adicionar_produto_catalogo(
                nome="Cadeira Ergonômica SuperConfort",
                descricao="Para longas horas de uso",
                preco=1250.00,
                quantidade_em_estoque=20,
                categoria="Móveis Escritório",
            )
        )
        cls.produto_fluxo_3_template = (
            cls.sistema_geral_template.adicionar_produto_catalogo(
                nome='Monitor Gamer Curvo 32"',
                descricao="144Hz, 1ms",
                preco=2200.00,
                quantidade_em_estoque=8,
                categoria="Monitores",
            )
        )
        cls.cliente_id_fluxo = "cliente_fluxo_completo_001"
        cls.endereco_fluxo = {
            "rua": "Av. Principal do Fluxo",
            "numero": "1000",
            "cep": "77777-000",
            "cidade": "Fluxolândia",
        }

    def setUp(self):
        self.sistema = SistemaEcommerce()

        self.p1 = self.sistema.adicionar_produto_catalogo(
            nome=self.produto_fluxo_1_template.nome,
            descricao=self.produto_fluxo_1_template.descricao,
            preco=self.produto_fluxo_1_template.preco,
            quantidade_em_estoque=self.produto_fluxo_1_template.quantidade_em_estoque,
            categoria=self.produto_fluxo_1_template.categoria,
        )
        self.p2 = self.sistema.adicionar_produto_catalogo(
            nome=self.produto_fluxo_2_template.nome,
            descricao=self.produto_fluxo_2_template.descricao,
            preco=self.produto_fluxo_2_template.preco,
            quantidade_em_estoque=self.produto_fluxo_2_template.quantidade_em_estoque,
            categoria=self.produto_fluxo_2_template.categoria,
        )
        self.p3 = self.sistema.adicionar_produto_catalogo(
            nome=self.produto_fluxo_3_template.nome,
            descricao=self.produto_fluxo_3_template.descricao,
            preco=self.produto_fluxo_3_template.preco,
            quantidade_em_estoque=self.produto_fluxo_3_template.quantidade_em_estoque,
            categoria=self.produto_fluxo_3_template.categoria,
        )

        self.sistema.registrar_usuario(
            self.cliente_id_fluxo,
            {"nome": "Cliente Testador de Fluxo", "email": "fluxo@teste.com"},
        )

        self.estoque_inicial_p1 = self.p1.quantidade_em_estoque
        self.estoque_inicial_p2 = self.p2.quantidade_em_estoque
        self.estoque_inicial_p3 = self.p3.quantidade_em_estoque

    def test_fluxo_completo_pagamento_pix(self):
        carrinho_pix = Carrinho()
        carrinho_pix.adicionar_item(self.p1, 1)

        pedido = self.sistema.criar_pedido(
            self.cliente_id_fluxo, carrinho_pix, self.endereco_fluxo, "pix"
        )
        self.assertIsNotNone(pedido, "Pedido PIX não foi criado.")
        self.assertEqual(pedido.status_pedido, "pendente")
        id_pedido_pix = pedido.id_pedido

        detalhes_pagamento_pix = {"chave_pix": "pagador_pix@teste.com"}
        resultado_pagamento = self.sistema.processar_pagamento_pedido(
            id_pedido_pix, detalhes_pagamento_pix
        )

        self.assertEqual(
            resultado_pagamento["status"],
            "aprovado",
            f"Pagamento PIX falhou: {resultado_pagamento.get('mensagem')}",
        )
        pedido_pago = self.sistema.pedidos_registrados[id_pedido_pix]
        self.assertEqual(pedido_pago.status_pedido, "pago")
        self.assertIsNotNone(pedido_pago.id_transacao_pagamento)

        valor_esperado_com_desconto = round(
            self.p1.preco * (1 - self.sistema.sistema_pagamento.DESCONTO_PIX_DEFAULT), 2
        )
        self.assertAlmostEqual(
            pedido_pago.valor_final_pago, valor_esperado_com_desconto, places=2
        )

        produto_p1_apos_venda = self.sistema.recuperar_produto_por_id(
            self.p1.id_produto
        )
        self.assertEqual(
            produto_p1_apos_venda.quantidade_em_estoque, self.estoque_inicial_p1 - 1
        )

    def test_fluxo_completo_pagamento_cartao_a_vista(self):
        carrinho_cc_avista = Carrinho()
        carrinho_cc_avista.adicionar_item(self.p2, 2)

        pedido = self.sistema.criar_pedido(
            self.cliente_id_fluxo,
            carrinho_cc_avista,
            self.endereco_fluxo,
            "cartao_credito",
        )
        self.assertIsNotNone(pedido, "Pedido Cartão à Vista não foi criado.")
        id_pedido_cc_avista = pedido.id_pedido

        detalhes_pagamento_cc_avista = {
            "numero_cartao": "1111222233334444",
            "cvv": "123",
            "validade": "12/2027",
            "numero_parcelas": 1,
        }
        resultado_pagamento = self.sistema.processar_pagamento_pedido(
            id_pedido_cc_avista, detalhes_pagamento_cc_avista
        )

        self.assertEqual(
            resultado_pagamento["status"],
            "aprovado",
            f"Pagamento Cartão à Vista falhou: {resultado_pagamento.get('mensagem')}",
        )
        pedido_pago = self.sistema.pedidos_registrados[id_pedido_cc_avista]
        self.assertEqual(pedido_pago.status_pedido, "pago")

        valor_esperado_cc_avista = round(self.p2.preco * 2, 2)
        self.assertAlmostEqual(
            pedido_pago.valor_final_pago, valor_esperado_cc_avista, places=2
        )

        produto_p2_apos_venda = self.sistema.recuperar_produto_por_id(
            self.p2.id_produto
        )
        self.assertEqual(
            produto_p2_apos_venda.quantidade_em_estoque, self.estoque_inicial_p2 - 2
        )

    def test_fluxo_completo_pagamento_cartao_parcelado(self):
        carrinho_cc_parcelado = Carrinho()
        carrinho_cc_parcelado.adicionar_item(self.p3, 1)

        pedido = self.sistema.criar_pedido(
            self.cliente_id_fluxo,
            carrinho_cc_parcelado,
            self.endereco_fluxo,
            "cartao_credito",
        )
        self.assertIsNotNone(pedido, "Pedido Cartão Parcelado não foi criado.")
        id_pedido_cc_parcelado = pedido.id_pedido

        numero_de_parcelas = 3
        detalhes_pagamento_cc_parcelado = {
            "numero_cartao": "5555666677778888",
            "cvv": "456",
            "validade": "10/2028",
            "numero_parcelas": numero_de_parcelas,
        }
        resultado_pagamento = self.sistema.processar_pagamento_pedido(
            id_pedido_cc_parcelado, detalhes_pagamento_cc_parcelado
        )

        self.assertEqual(
            resultado_pagamento["status"],
            "aprovado",
            f"Pagamento Cartão Parcelado falhou: {resultado_pagamento.get('mensagem')}",
        )
        pedido_pago = self.sistema.pedidos_registrados[id_pedido_cc_parcelado]
        self.assertEqual(pedido_pago.status_pedido, "pago")

        taxa_juros = self.sistema.sistema_pagamento.TAXA_JUROS_PARCELAMENTO_DEFAULT
        valor_esperado_com_juros = round(self.p3.preco * (1 + taxa_juros), 2)
        self.assertAlmostEqual(
            pedido_pago.valor_final_pago, valor_esperado_com_juros, places=2
        )

        self.assertIn(
            f"em {numero_de_parcelas}x de R${round(valor_esperado_com_juros/numero_de_parcelas, 2):.2f}",
            resultado_pagamento["mensagem"],
        )

        produto_p3_apos_venda = self.sistema.recuperar_produto_por_id(
            self.p3.id_produto
        )
        self.assertEqual(
            produto_p3_apos_venda.quantidade_em_estoque, self.estoque_inicial_p3 - 1
        )


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
