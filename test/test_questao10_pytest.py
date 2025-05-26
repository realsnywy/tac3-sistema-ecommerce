import pytest
import time
from app.ecommerce_sistema import SistemaEcommerce, Carrinho, Produto

NUM_PRODUTOS_CARRINHO_PERF = 500
NUM_PAGAMENTOS_PERF = 50
NUM_PEDIDOS_VOLUME_PERF = 100


@pytest.fixture(scope="module")
def sistema_para_performance_pytest():
    sistema = SistemaEcommerce()
    sistema.registrar_usuario("perf_user_pytest", {"nome": "Pytest Perf User"})
    for i in range(max(NUM_PRODUTOS_CARRINHO_PERF // 20, 20)):
        sistema.adicionar_produto_catalogo(
            nome=f"PerfPy Produto {i}",
            descricao="Produto para teste de performance Pytest",
            preco=float(10 + i),
            quantidade_em_estoque=NUM_PRODUTOS_CARRINHO_PERF
            + NUM_PEDIDOS_VOLUME_PERF
            + 100,
            categoria="Performance",
        )
    return sistema


@pytest.fixture
def produtos_catalogo_pytest(sistema_para_performance_pytest):
    return list(sistema_para_performance_pytest.produtos_catalogo.values())


class TestPerformancePytestQuestao10:

    def test_tempo_adicao_produtos_carrinho_pytest(self, produtos_catalogo_pytest):
        if not produtos_catalogo_pytest:
            pytest.skip(
                "Sem produtos no catálogo para teste de performance do carrinho."
            )

        carrinho = Carrinho()
        start_time = time.perf_counter()
        for i in range(NUM_PRODUTOS_CARRINHO_PERF):
            produto = produtos_catalogo_pytest[i % len(produtos_catalogo_pytest)]
            try:
                carrinho.adicionar_item(produto, 1)
            except ValueError:
                produto.adicionar_estoque(
                    NUM_PRODUTOS_CARRINHO_PERF
                )  # Adiciona mais estoque se acabar
                carrinho.adicionar_item(produto, 1)
        end_time = time.perf_counter()
        tempo_gasto = end_time - start_time
        print(
            f"\n[Pytest] Adicionar {NUM_PRODUTOS_CARRINHO_PERF} itens ao carrinho levou: {tempo_gasto:.6f}s"
        )
        assert len(carrinho.get_itens()) > 0 or NUM_PRODUTOS_CARRINHO_PERF == 0

    def test_tempo_processamento_pagamentos_pytest(
        self, sistema_para_performance_pytest, produtos_catalogo_pytest
    ):
        if not produtos_catalogo_pytest:
            pytest.skip(
                "Sem produtos para criar pedidos para teste de performance de pagamento."
            )

        pedidos_ids = []
        for i in range(NUM_PAGAMENTOS_PERF):
            carrinho_temp = Carrinho()
            produto = produtos_catalogo_pytest[i % len(produtos_catalogo_pytest)]
            if produto.quantidade_em_estoque < 1:
                produto.adicionar_estoque(NUM_PAGAMENTOS_PERF + 10)  # Garante estoque
            carrinho_temp.adicionar_item(produto, 1)
            pedido = sistema_para_performance_pytest.criar_pedido(
                "perf_user_pytest", carrinho_temp, {"rua": "Rua Perf"}, "pix"
            )
            if pedido:
                pedidos_ids.append(pedido.id_pedido)

        if not pedidos_ids:
            pytest.skip(
                "Não foi possível criar pedidos para o teste de performance de pagamento."
            )

        start_time = time.perf_counter()
        pagamentos_bem_sucedidos = 0
        for i, pedido_id in enumerate(pedidos_ids):
            resultado = sistema_para_performance_pytest.processar_pagamento_pedido(
                pedido_id, {"chave_pix": f"pix_perf_{i}"}
            )
            if resultado.get("status") == "aprovado":
                pagamentos_bem_sucedidos += 1
        end_time = time.perf_counter()
        tempo_gasto = end_time - start_time
        print(
            f"\n[Pytest] Processar {len(pedidos_ids)} pagamentos ({pagamentos_bem_sucedidos} aprovados) sequenciais levou: {tempo_gasto:.6f}s"
        )
        assert pagamentos_bem_sucedidos > 0 or not pedidos_ids

    def test_tempo_criacao_volume_pedidos_pytest(
        self, sistema_para_performance_pytest, produtos_catalogo_pytest
    ):
        if not produtos_catalogo_pytest:
            pytest.skip("Sem produtos para teste de performance de criação de pedidos.")

        start_time = time.perf_counter()
        pedidos_criados_efetivamente = 0
        for i in range(NUM_PEDIDOS_VOLUME_PERF):
            carrinho_temp = Carrinho()
            produto = produtos_catalogo_pytest[i % len(produtos_catalogo_pytest)]
            if produto.quantidade_em_estoque < 1:
                produto.adicionar_estoque(
                    NUM_PEDIDOS_VOLUME_PERF + 10
                )  # Garante estoque
            carrinho_temp.adicionar_item(produto, 1)
            if sistema_para_performance_pytest.criar_pedido(
                "perf_user_pytest",
                carrinho_temp,
                {"rua": "Rua Volume"},
                "cartao_credito",
            ):
                pedidos_criados_efetivamente += 1
        end_time = time.perf_counter()
        tempo_gasto = end_time - start_time
        print(
            f"\n[Pytest] Criar {pedidos_criados_efetivamente} pedidos sequenciais levou: {tempo_gasto:.6f}s"
        )
        assert pedidos_criados_efetivamente > 0 or NUM_PEDIDOS_VOLUME_PERF == 0
