import unittest
from app.ecommerce_sistema import Produto, Carrinho, Pedido
from datetime import datetime, timedelta


class TestPedidoQuestao5(unittest.TestCase):
    """
    Testes para a classe Pedido utilizando unittest (Questão 5).
    """

    def setUp(self):
        self.produto1 = Produto(
            id_produto=301,
            nome="Smartphone XPTO",
            descricao="Última geração",
            preco=3000.00,
            quantidade_em_estoque=10,
            categoria="Celulares",
        )
        self.produto2 = Produto(
            id_produto=302,
            nome="Capa Protetora",
            descricao="Anti-impacto",
            preco=80.00,
            quantidade_em_estoque=50,
            categoria="Acessórios",
        )

        self.carrinho_valido = Carrinho()
        self.carrinho_valido.adicionar_item(self.produto1, 1)
        self.carrinho_valido.adicionar_item(self.produto2, 2)

        self.endereco_entrega = {
            "rua": "Rua Teste",
            "numero": "123",
            "cep": "12345-000",
            "cidade": "Testelândia",
        }
        self.cliente_id = "cliente_teste_123"

        self.pedido = Pedido(
            id_pedido=1,
            cliente_id=self.cliente_id,
            carrinho=self.carrinho_valido,
            endereco_entrega=self.endereco_entrega,
            metodo_pagamento_escolhido="cartao_credito",
        )

    def test_criacao_pedido_estado_inicial_pendente(self):
        self.assertEqual(self.pedido.status_pedido, "pendente")
        self.assertIsNotNone(self.pedido.datas["criacao"])
        self.assertIsNone(self.pedido.datas["pagamento"])

    def test_transicao_pendente_para_pago(self):
        id_transacao_simulada = "TRANSACAO_PAGA_123"
        valor_pago_simulado = self.pedido.valor_total_pedido

        self.pedido.registrar_pagamento(id_transacao_simulada, valor_pago_simulado)

        self.assertEqual(self.pedido.status_pedido, "pago")
        self.assertEqual(self.pedido.id_transacao_pagamento, id_transacao_simulada)
        self.assertEqual(self.pedido.valor_final_pago, valor_pago_simulado)
        self.assertIsNotNone(self.pedido.datas["pagamento"])

    def test_transicao_pago_para_enviado(self):
        self.pedido.registrar_pagamento(
            "TRANS_PAGA_456", self.pedido.valor_total_pedido
        )
        self.assertTrue(self.pedido.atualizar_status("enviado"))
        self.assertEqual(self.pedido.status_pedido, "enviado")
        self.assertIsNotNone(self.pedido.datas["envio"])

    def test_transicao_enviado_para_entregue(self):
        self.pedido.registrar_pagamento(
            "TRANS_PAGA_789", self.pedido.valor_total_pedido
        )
        self.pedido.atualizar_status("enviado")
        self.assertTrue(self.pedido.atualizar_status("entregue"))
        self.assertEqual(self.pedido.status_pedido, "entregue")
        self.assertIsNotNone(self.pedido.datas["entrega"])

    def test_transicao_para_cancelado_de_pendente(self):
        self.assertTrue(self.pedido.atualizar_status("cancelado"))
        self.assertEqual(self.pedido.status_pedido, "cancelado")
        self.assertIsNotNone(self.pedido.datas["cancelamento"])

    def test_transicao_para_cancelado_de_pago(self):
        self.pedido.registrar_pagamento(
            "TRANS_PAGA_ABC", self.pedido.valor_total_pedido
        )
        self.assertTrue(self.pedido.atualizar_status("cancelado"))
        self.assertEqual(self.pedido.status_pedido, "cancelado")
        self.assertIsNotNone(self.pedido.datas["cancelamento"])
        self.assertIsNotNone(self.pedido.datas["pagamento"])

    def test_transicao_para_cancelado_de_enviado(self):
        self.pedido.registrar_pagamento(
            "TRANS_PAGA_DEF", self.pedido.valor_total_pedido
        )
        self.pedido.atualizar_status("enviado")
        self.assertTrue(self.pedido.atualizar_status("cancelado"))
        self.assertEqual(self.pedido.status_pedido, "cancelado")
        self.assertIsNotNone(self.pedido.datas["cancelamento"])

    def test_transicao_para_cancelado_de_entregue(self):
        self.pedido.registrar_pagamento(
            "TRANS_PAGA_GHI", self.pedido.valor_total_pedido
        )
        self.pedido.atualizar_status("enviado")
        self.pedido.atualizar_status("entregue")
        self.assertTrue(self.pedido.atualizar_status("cancelado"))
        self.assertEqual(self.pedido.status_pedido, "cancelado")
        self.assertIsNotNone(self.pedido.datas["cancelamento"])

    def test_restricao_transicao_pendente_para_entregue(self):
        self.assertFalse(self.pedido.atualizar_status("entregue"))
        self.assertEqual(self.pedido.status_pedido, "pendente")

    def test_restricao_transicao_pago_para_pendente(self):
        self.pedido.registrar_pagamento(
            "TRANS_PAGA_JKL", self.pedido.valor_total_pedido
        )
        self.assertFalse(self.pedido.atualizar_status("pendente"))
        self.assertEqual(self.pedido.status_pedido, "pago")

    def test_restricao_transicao_enviado_para_pago(self):
        self.pedido.registrar_pagamento(
            "TRANS_PAGA_MNO", self.pedido.valor_total_pedido
        )
        self.pedido.atualizar_status("enviado")
        self.assertFalse(self.pedido.atualizar_status("pago"))
        self.assertEqual(self.pedido.status_pedido, "enviado")

    def test_restricao_transicao_entregue_para_enviado(self):
        self.pedido.registrar_pagamento(
            "TRANS_PAGA_PQR", self.pedido.valor_total_pedido
        )
        self.pedido.atualizar_status("enviado")
        self.pedido.atualizar_status("entregue")
        self.assertFalse(self.pedido.atualizar_status("enviado"))
        self.assertEqual(self.pedido.status_pedido, "entregue")

    def test_restricao_transicao_de_cancelado(self):
        self.pedido.atualizar_status("cancelado")
        self.assertFalse(self.pedido.atualizar_status("pendente"))
        self.assertFalse(self.pedido.atualizar_status("pago"))
        self.assertFalse(self.pedido.atualizar_status("enviado"))
        self.assertFalse(self.pedido.atualizar_status("entregue"))
        self.assertEqual(self.pedido.status_pedido, "cancelado")

        self.assertTrue(self.pedido.atualizar_status("cancelado"))
        self.assertEqual(self.pedido.status_pedido, "cancelado")

    def test_processamento_pagamento_afeta_status_e_datas(self):
        valor_pago_efetivo = 3100.00
        id_transacao = "PAG_XYZ789"

        self.assertEqual(self.pedido.status_pedido, "pendente")
        self.assertIsNone(self.pedido.id_transacao_pagamento)
        self.assertIsNone(self.pedido.valor_final_pago)
        self.assertIsNone(self.pedido.datas["pagamento"])

        self.pedido.registrar_pagamento(id_transacao, valor_pago_efetivo)

        self.assertEqual(self.pedido.status_pedido, "pago")
        self.assertEqual(self.pedido.id_transacao_pagamento, id_transacao)
        self.assertEqual(self.pedido.valor_final_pago, valor_pago_efetivo)
        self.assertIsNotNone(self.pedido.datas["pagamento"])
        self.assertTrue(
            datetime.now() - self.pedido.datas["pagamento"] < timedelta(seconds=5)
        )

    def test_gerar_nota_fiscal_apos_pago(self):
        self.pedido.registrar_pagamento("NF_TRANS_001", self.pedido.valor_total_pedido)
        nota = self.pedido.gerar_nota_fiscal()
        self.assertIn("--- Nota Fiscal ---", nota)
        self.assertIn(f"Pedido ID: {self.pedido.id_pedido}", nota)
        self.assertIn(f"Valor Final Pago: R${self.pedido.valor_final_pago:.2f}", nota)

    def test_gerar_nota_fiscal_pedido_pendente(self):
        nota = self.pedido.gerar_nota_fiscal()
        self.assertIn("pedido não foi pago", nota)

    def test_calcular_frete_pedido(self):
        self.assertEqual(self.pedido.calcular_frete(), 0.0)

        carrinho_pequeno = Carrinho()
        produto_barato = Produto(
            id_produto=303,
            nome="Chaveiro",
            descricao="Chaveiro legal",
            preco=20.00,
            quantidade_em_estoque=5,
            categoria="Lembranças",
        )
        carrinho_pequeno.adicionar_item(produto_barato, 1)
        pedido_pequeno = Pedido(
            id_pedido=2,
            cliente_id="cli_peq",
            carrinho=carrinho_pequeno,
            endereco_entrega=self.endereco_entrega,
            metodo_pagamento_escolhido="pix",
        )
        self.assertEqual(pedido_pequeno.calcular_frete(), 25.0)


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
