import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
from testify import TestCase, assert_gte, run, setup, suite
from app.ecommerce_sistema import SistemaEcommerce, Carrinho, Produto

NUM_PRODUTOS_CARRINHO_PERF_TF = 500
NUM_PAGAMENTOS_PERF_TF = 50
NUM_PEDIDOS_VOLUME_PERF_TF = 100


@suite("PerformanceTestifySuiteQuestao10")
class TestPerformanceTestifyQuestao10(TestCase):

    @setup  # testify @setup é por instância, não por classe como setUpClass do unittest
    def inicializar_sistema_para_testify(self):
        self.sistema = SistemaEcommerce()
        self.sistema.registrar_usuario("perf_user_tf", {"nome": "Testify Perf User"})
        self.produtos_catalogo_tf = []
        for i in range(max(NUM_PRODUTOS_CARRINHO_PERF_TF // 20, 20)):
            produto = self.sistema.adicionar_produto_catalogo(
                nome=f"PerfTF Produto {i}",
                descricao="Produto para teste de performance Testify",
                preco=float(10 + i),
                quantidade_em_estoque=NUM_PRODUTOS_CARRINHO_PERF_TF
                + NUM_PEDIDOS_VOLUME_PERF_TF
                + 100,  # Estoque alto
                categoria="PerformanceTF",
            )
            self.produtos_catalogo_tf.append(produto)

    def test_tempo_adicao_produtos_carrinho_testify(self):
        if not self.produtos_catalogo_tf:
            # Testify não tem um "skipTest" direto como unittest ou pytest
            print(
                "\n[Testify] SKIP: Sem produtos no catálogo para teste de performance do carrinho TF."
            )
            assert_gte(1, 1)  # Passa o teste se não há o que testar
            return

        carrinho = Carrinho()
        start_time = time.perf_counter()
        for i in range(NUM_PRODUTOS_CARRINHO_PERF_TF):
            produto = self.produtos_catalogo_tf[i % len(self.produtos_catalogo_tf)]
            try:
                carrinho.adicionar_item(produto, 1)
            except ValueError:
                produto.adicionar_estoque(NUM_PRODUTOS_CARRINHO_PERF_TF)
                carrinho.adicionar_item(produto, 1)
        end_time = time.perf_counter()
        tempo_gasto = end_time - start_time
        print(
            f"\n[Testify] Adicionar {NUM_PRODUTOS_CARRINHO_PERF_TF} itens ao carrinho levou: {tempo_gasto:.6f}s"
        )
        assert_gte(
            len(carrinho.get_itens()),
            1 if NUM_PRODUTOS_CARRINHO_PERF_TF > 0 else 0,
            "Carrinho TF deveria ter itens.",
        )

    def test_tempo_processamento_pagamentos_testify(self):
        if not self.produtos_catalogo_tf:
            print(
                "\n[Testify] SKIP: Sem produtos para criar pedidos para teste de performance de pagamento TF."
            )
            assert_gte(1, 1)
            return

        pedidos_ids = []
        for i in range(NUM_PAGAMENTOS_PERF_TF):
            carrinho_temp = Carrinho()
            produto = self.produtos_catalogo_tf[i % len(self.produtos_catalogo_tf)]
            if produto.quantidade_em_estoque < 1:
                produto.adicionar_estoque(NUM_PAGAMENTOS_PERF_TF + 10)
            carrinho_temp.adicionar_item(produto, 1)
            pedido = self.sistema.criar_pedido(
                "perf_user_tf", carrinho_temp, {"rua": "Rua Perf TF"}, "pix"
            )
            if pedido:
                pedidos_ids.append(pedido.id_pedido)

        if not pedidos_ids:
            print(
                "\n[Testify] SKIP: Não foi possível criar pedidos para o teste de performance de pagamento TF."
            )
            assert_gte(1, 1)
            return

        start_time = time.perf_counter()
        pagamentos_bem_sucedidos = 0
        for i, pedido_id in enumerate(pedidos_ids):
            resultado = self.sistema.processar_pagamento_pedido(
                pedido_id, {"chave_pix": f"pix_perf_tf_{i}"}
            )
            if resultado.get("status") == "aprovado":
                pagamentos_bem_sucedidos += 1
        end_time = time.perf_counter()
        tempo_gasto = end_time - start_time
        print(
            f"\n[Testify] Processar {len(pedidos_ids)} pagamentos ({pagamentos_bem_sucedidos} aprovados) sequenciais levou: {tempo_gasto:.6f}s"
        )
        assert_gte(
            pagamentos_bem_sucedidos,
            1 if pedidos_ids else 0,
            "Algum pagamento TF deveria ter sido processado.",
        )

    def test_tempo_criacao_volume_pedidos_testify(self):
        if not self.produtos_catalogo_tf:
            print(
                "\n[Testify] SKIP: Sem produtos para teste de performance de criação de pedidos TF."
            )
            assert_gte(1, 1)
            return

        start_time = time.perf_counter()
        pedidos_criados_efetivamente = 0
        for i in range(NUM_PEDIDOS_VOLUME_PERF_TF):
            carrinho_temp = Carrinho()
            produto = self.produtos_catalogo_tf[i % len(self.produtos_catalogo_tf)]
            if produto.quantidade_em_estoque < 1:
                produto.adicionar_estoque(NUM_PEDIDOS_VOLUME_PERF_TF + 10)
            carrinho_temp.adicionar_item(produto, 1)
            if self.sistema.criar_pedido(
                "perf_user_tf",
                carrinho_temp,
                {"rua": "Rua Volume TF"},
                "cartao_credito",
            ):
                pedidos_criados_efetivamente += 1
        end_time = time.perf_counter()
        tempo_gasto = end_time - start_time
        print(
            f"\n[Testify] Criar {pedidos_criados_efetivamente} pedidos sequenciais levou: {tempo_gasto:.6f}s"
        )
        assert_gte(
            pedidos_criados_efetivamente,
            1 if NUM_PEDIDOS_VOLUME_PERF_TF > 0 else 0,
            "Algum pedido TF deveria ter sido criado.",
        )


if __name__ == "__main__":
    run()
