import unittest
import time
from app.ecommerce_sistema import SistemaEcommerce, Carrinho, Produto

NUM_PRODUTOS_CARRINHO_PERF_UT = 500
NUM_PAGAMENTOS_PERF_UT = 50
NUM_PEDIDOS_VOLUME_PERF_UT = 100


class TestPerformanceUnittestQuestao10(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sistema_template_ut = SistemaEcommerce()
        cls.sistema_template_ut.registrar_usuario(
            "perf_user_ut", {"nome": "Unittest Perf User"}
        )
        cls.produtos_template_ut = []
        for i in range(max(NUM_PRODUTOS_CARRINHO_PERF_UT // 20, 20)):
            produto = cls.sistema_template_ut.adicionar_produto_catalogo(
                nome=f"PerfUT Produto {i}",
                descricao="Produto para teste de performance Unittest",
                preco=float(10 + i),
                quantidade_em_estoque=NUM_PRODUTOS_CARRINHO_PERF_UT
                + NUM_PEDIDOS_VOLUME_PERF_UT
                + 100,  # Estoque alto
                categoria="PerformanceUT",
            )
            cls.produtos_template_ut.append(produto)

    def setUp(self):
        # Recria o sistema e os produtos para cada teste para isolamento
        self.sistema = SistemaEcommerce()
        self.sistema.registrar_usuario("perf_user_ut", {"nome": "Unittest Perf User"})
        self.produtos_catalogo_ut = []
        for p_template in self.produtos_template_ut:
            produto = self.sistema.adicionar_produto_catalogo(
                nome=p_template.nome,
                descricao=p_template.descricao,
                preco=p_template.preco,
                quantidade_em_estoque=p_template.quantidade_em_estoque,  # Usa o estoque inicial alto
                categoria=p_template.categoria,
            )
            self.produtos_catalogo_ut.append(produto)

    def test_tempo_adicao_produtos_carrinho_unittest(self):
        if not self.produtos_catalogo_ut:
            self.skipTest(
                "Sem produtos no catálogo para teste de performance do carrinho UT."
            )

        carrinho = Carrinho()
        start_time = time.perf_counter()
        for i in range(NUM_PRODUTOS_CARRINHO_PERF_UT):
            produto = self.produtos_catalogo_ut[i % len(self.produtos_catalogo_ut)]
            try:
                carrinho.adicionar_item(produto, 1)
            except ValueError:
                produto.adicionar_estoque(NUM_PRODUTOS_CARRINHO_PERF_UT)
                carrinho.adicionar_item(produto, 1)
        end_time = time.perf_counter()
        tempo_gasto = end_time - start_time
        print(
            f"\n[Unittest] Adicionar {NUM_PRODUTOS_CARRINHO_PERF_UT} itens ao carrinho levou: {tempo_gasto:.6f}s"
        )
        self.assertTrue(
            len(carrinho.get_itens()) > 0 or NUM_PRODUTOS_CARRINHO_PERF_UT == 0
        )

    def test_tempo_processamento_pagamentos_unittest(self):
        if not self.produtos_catalogo_ut:
            self.skipTest(
                "Sem produtos para criar pedidos para teste de performance de pagamento UT."
            )

        pedidos_ids = []
        for i in range(NUM_PAGAMENTOS_PERF_UT):
            carrinho_temp = Carrinho()
            produto = self.produtos_catalogo_ut[i % len(self.produtos_catalogo_ut)]
            if produto.quantidade_em_estoque < 1:
                produto.adicionar_estoque(NUM_PAGAMENTOS_PERF_UT + 10)
            carrinho_temp.adicionar_item(produto, 1)
            pedido = self.sistema.criar_pedido(
                "perf_user_ut", carrinho_temp, {"rua": "Rua Perf UT"}, "pix"
            )
            if pedido:
                pedidos_ids.append(pedido.id_pedido)

        if not pedidos_ids:
            self.skipTest(
                "Não foi possível criar pedidos para o teste de performance de pagamento UT."
            )

        start_time = time.perf_counter()
        pagamentos_bem_sucedidos = 0
        for i, pedido_id in enumerate(pedidos_ids):
            resultado = self.sistema.processar_pagamento_pedido(
                pedido_id, {"chave_pix": f"pix_perf_ut_{i}"}
            )
            if resultado.get("status") == "aprovado":
                pagamentos_bem_sucedidos += 1
        end_time = time.perf_counter()
        tempo_gasto = end_time - start_time
        print(
            f"\n[Unittest] Processar {len(pedidos_ids)} pagamentos ({pagamentos_bem_sucedidos} aprovados) sequenciais levou: {tempo_gasto:.6f}s"
        )
        self.assertTrue(pagamentos_bem_sucedidos > 0 or not pedidos_ids)

    def test_tempo_criacao_volume_pedidos_unittest(self):
        if not self.produtos_catalogo_ut:
            self.skipTest(
                "Sem produtos para teste de performance de criação de pedidos UT."
            )

        start_time = time.perf_counter()
        pedidos_criados_efetivamente = 0
        for i in range(NUM_PEDIDOS_VOLUME_PERF_UT):
            carrinho_temp = Carrinho()
            produto = self.produtos_catalogo_ut[i % len(self.produtos_catalogo_ut)]
            if produto.quantidade_em_estoque < 1:
                produto.adicionar_estoque(NUM_PEDIDOS_VOLUME_PERF_UT + 10)
            carrinho_temp.adicionar_item(produto, 1)
            if self.sistema.criar_pedido(
                "perf_user_ut",
                carrinho_temp,
                {"rua": "Rua Volume UT"},
                "cartao_credito",
            ):
                pedidos_criados_efetivamente += 1
        end_time = time.perf_counter()
        tempo_gasto = end_time - start_time
        print(
            f"\n[Unittest] Criar {pedidos_criados_efetivamente} pedidos sequenciais levou: {tempo_gasto:.6f}s"
        )
        self.assertTrue(
            pedidos_criados_efetivamente > 0 or NUM_PEDIDOS_VOLUME_PERF_UT == 0
        )


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
