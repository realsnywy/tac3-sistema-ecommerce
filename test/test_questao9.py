import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from testify import (
    TestCase,
    assert_equal,
    assert_almost_equal,
    run,
    setup,
    suite,
    assert_is_not,
)
from app.ecommerce_sistema import SistemaEcommerce, Carrinho, Produto


@suite("SistemaConfiguracaoTestifySuiteQuestao9")
class TestSistemaConfiguracaoComTestifyQuestao9(TestCase):
    """
    Testes para o comportamento do sistema com diferentes configurações,
    utilizando Testify e parametrização manual (Questão 9).
    """

    @setup
    def inicializar_sistema(self):
        self.sistema = SistemaEcommerce()
        self.cliente_id = "user_config_test"
        self.sistema.registrar_usuario(
            self.cliente_id, {"nome": "Config Tester", "email": "config@example.com"}
        )
        self.produto_base_template = Produto(
            id_produto=901,
            nome="Produto Configurável",
            descricao="Teste de configs",
            preco=1000.00,
            quantidade_em_estoque=50,
            categoria="Config",
        )
        self.endereco_padrao = {
            "rua": "Rua da Configuração",
            "numero": "99",
            "cep": "88888-000",
        }

    def _get_produto_base_fresco(self):
        # Cria uma nova instância do produto para cada teste/iteração para evitar efeitos colaterais no estoque
        return self.sistema.adicionar_produto_catalogo(
            nome=self.produto_base_template.nome,
            descricao=self.produto_base_template.descricao,
            preco=self.produto_base_template.preco,
            quantidade_em_estoque=self.produto_base_template.quantidade_em_estoque,  # Estoque inicial
            categoria=self.produto_base_template.categoria,
        )

    def test_diferentes_taxas_juros_parcelamento(self):
        valor_original = self.produto_base_template.preco
        numero_parcelas_fixo = 3
        parametros_juros = [
            (0.00, 1000.00, round(1000.00 / 3, 2)),
            (0.05, 1050.00, round(1050.00 / 3, 2)),
            (0.10, 1100.00, round(1100.00 / 3, 2)),
            (0.25, 1250.00, round(1250.00 / 3, 2)),
        ]

        for i, (taxa_juros, total_esperado, parcela_esperada) in enumerate(
            parametros_juros
        ):
            self.sistema.configurar_sistema_pagamento(
                taxa_juros_parcelamento=taxa_juros
            )
            produto_teste_iter = (
                self._get_produto_base_fresco()
            )  # Produto novo para este ciclo

            total_calculado, parcela_calculada = (
                self.sistema.sistema_pagamento.calcular_valor_final_cartao_credito_parcelado(
                    valor_original, numero_parcelas_fixo
                )
            )
            mensagem_erro = f"Erro para taxa de juros {taxa_juros*100}% (iteração {i})"
            assert_almost_equal(total_calculado, total_esperado, 2)
            assert_almost_equal(parcela_calculada, parcela_esperada, 2)

            carrinho = Carrinho()
            carrinho.adicionar_item(produto_teste_iter, 1)
            pedido = self.sistema.criar_pedido(
                self.cliente_id, carrinho, self.endereco_padrao, "cartao_credito"
            )
            assert_is_not(pedido, None, f"{mensagem_erro} - Criação de pedido falhou")
            id_pedido = pedido.id_pedido

            detalhes_pagamento = {
                "numero_cartao": f"1234_juros_{taxa_juros}",
                "numero_parcelas": numero_parcelas_fixo,
            }
            resultado_processamento = self.sistema.processar_pagamento_pedido(
                id_pedido, detalhes_pagamento
            )

            assert_equal(
                resultado_processamento["status"],
                "aprovado",
                f"{mensagem_erro} - Processamento falhou: {resultado_processamento.get('mensagem')}",
            )
            pedido_processado = self.sistema.pedidos_registrados[id_pedido]
            assert_almost_equal(pedido_processado.valor_final_pago, total_esperado, 2)

            # Não é necessário limpar explicitamente o pedido se o sistema for recriado ou se os IDs de pedido forem sempre únicos

    def test_diferentes_percentuais_desconto_pix(self):
        valor_original = self.produto_base_template.preco
        parametros_pix = [
            (0.00, 1000.00),
            (0.05, 950.00),
            (0.10, 900.00),
            (0.15, 850.00),
        ]

        for i, (desconto_pix, final_esperado) in enumerate(parametros_pix):
            self.sistema.configurar_sistema_pagamento(desconto_pix=desconto_pix)
            produto_teste_iter = self._get_produto_base_fresco()

            valor_calculado = self.sistema.sistema_pagamento.calcular_valor_final_pix(
                valor_original
            )
            mensagem_erro = f"Erro para desconto PIX {desconto_pix*100}% (iteração {i})"
            assert_almost_equal(valor_calculado, final_esperado, 2)

            carrinho = Carrinho()
            carrinho.adicionar_item(produto_teste_iter, 1)
            pedido = self.sistema.criar_pedido(
                self.cliente_id, carrinho, self.endereco_padrao, "pix"
            )
            assert_is_not(
                pedido, None, f"{mensagem_erro} - Criação de pedido PIX falhou"
            )
            id_pedido = pedido.id_pedido

            detalhes_pagamento = {"chave_pix": f"pix_desconto_{desconto_pix}@teste.com"}
            resultado_processamento = self.sistema.processar_pagamento_pedido(
                id_pedido, detalhes_pagamento
            )

            assert_equal(
                resultado_processamento["status"],
                "aprovado",
                f"{mensagem_erro} - Processamento PIX falhou: {resultado_processamento.get('mensagem')}",
            )
            pedido_processado = self.sistema.pedidos_registrados[id_pedido]
            assert_almost_equal(pedido_processado.valor_final_pago, final_esperado, 2)

    def test_diferentes_quantidades_de_parcelas_com_juros_fixos(self):
        valor_original = self.produto_base_template.preco
        taxa_juros_fixa = 0.08
        self.sistema.configurar_sistema_pagamento(
            taxa_juros_parcelamento=taxa_juros_fixa
        )

        total_com_juros_esperado = 1080.00

        parametros_parcelas = [
            (1, valor_original, valor_original),
            (2, total_com_juros_esperado, round(total_com_juros_esperado / 2, 2)),
            (4, total_com_juros_esperado, round(total_com_juros_esperado / 4, 2)),
            (6, total_com_juros_esperado, round(total_com_juros_esperado / 6, 2)),
        ]

        for i, (num_parcelas, total_esperado_iter, parcela_esperada_iter) in enumerate(
            parametros_parcelas
        ):
            produto_teste_iter = self._get_produto_base_fresco()
            total_calculado_iter, parcela_calculada_iter = (
                self.sistema.sistema_pagamento.calcular_valor_final_cartao_credito_parcelado(
                    valor_original, num_parcelas
                )
            )

            mensagem_erro = f"Erro para {num_parcelas} parcelas com juros de {taxa_juros_fixa*100}% (iteração {i})"
            assert_almost_equal(total_calculado_iter, total_esperado_iter, 2)
            assert_almost_equal(parcela_calculada_iter, parcela_esperada_iter, 2)

            carrinho = Carrinho()
            carrinho.adicionar_item(produto_teste_iter, 1)
            pedido = self.sistema.criar_pedido(
                self.cliente_id, carrinho, self.endereco_padrao, "cartao_credito"
            )
            assert_is_not(pedido, None, f"{mensagem_erro} - Criação de pedido falhou")
            id_pedido = pedido.id_pedido

            detalhes_pagamento = {
                "numero_cartao": f"1234_parcelas_{num_parcelas}",
                "numero_parcelas": num_parcelas,
            }
            resultado_processamento = self.sistema.processar_pagamento_pedido(
                id_pedido, detalhes_pagamento
            )

            assert_equal(
                resultado_processamento["status"],
                "aprovado",
                f"{mensagem_erro} - Processamento falhou: {resultado_processamento.get('mensagem')}",
            )
            pedido_processado = self.sistema.pedidos_registrados[id_pedido]
            assert_almost_equal(
                pedido_processado.valor_final_pago, total_esperado_iter, 2
            )


if __name__ == "__main__":
    run()
