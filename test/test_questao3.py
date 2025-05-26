from testify import (
    TestCase,
    assert_equal,
    assert_raises,
    run,
    setup,
    suite,
    assert_almost_equal,
)
from app.ecommerce_sistema import SistemaPagamento


@suite("SistemaPagamentoTestifySuiteQuestao3")
class TestSistemaPagamentoComTestifyQuestao3(TestCase):
    """
    Testes para a classe SistemaPagamento utilizando a biblioteca Testify (Questão 3).
    """

    @setup
    def inicializar_sistema_pagamento(self):
        self.sistema_pagamento_padrao = SistemaPagamento()
        self.sistema_pagamento_juros_altos = SistemaPagamento(
            taxa_juros_parcelamento=0.10
        )
        self.sistema_pagamento_desconto_maior_pix = SistemaPagamento(desconto_pix=0.15)
        self.sistema_pagamento_sem_juros_sem_desconto = SistemaPagamento(
            taxa_juros_parcelamento=0.0, desconto_pix=0.0
        )

    def test_calculo_cartao_credito_a_vista(self):
        valor_original = 100.00
        valor_final = (
            self.sistema_pagamento_padrao.calcular_valor_final_cartao_credito_a_vista(
                valor_original
            )
        )
        assert_equal(valor_final, 100.00)

        valor_final_sem_juros = self.sistema_pagamento_sem_juros_sem_desconto.calcular_valor_final_cartao_credito_a_vista(
            valor_original
        )
        assert_equal(valor_final_sem_juros, 100.00)

        assert_raises(
            ValueError,
            self.sistema_pagamento_padrao.calcular_valor_final_cartao_credito_a_vista,
            -50.00,
        )

    def test_calculo_cartao_credito_parcelado_e_valor_parcelas(self):
        valor_original = 1000.00

        total_1x, parcela_1x = (
            self.sistema_pagamento_padrao.calcular_valor_final_cartao_credito_parcelado(
                valor_original, 1
            )
        )
        assert_almost_equal(total_1x, 1000.00, msg="Total 1x padrão")
        assert_almost_equal(parcela_1x, 1000.00, msg="Parcela 1x padrão")

        total_3x, parcela_3x = (
            self.sistema_pagamento_padrao.calcular_valor_final_cartao_credito_parcelado(
                valor_original, 3
            )
        )
        assert_almost_equal(total_3x, 1050.00, msg="Total 3x padrão")
        assert_almost_equal(parcela_3x, 350.00, msg="Parcela 3x padrão")

        total_5x_altos, parcela_5x_altos = (
            self.sistema_pagamento_juros_altos.calcular_valor_final_cartao_credito_parcelado(
                valor_original, 5
            )
        )
        assert_almost_equal(total_5x_altos, 1100.00, msg="Total 5x juros altos")
        assert_almost_equal(parcela_5x_altos, 220.00, msg="Parcela 5x juros altos")

        total_6x_semj, parcela_6x_semj = (
            self.sistema_pagamento_sem_juros_sem_desconto.calcular_valor_final_cartao_credito_parcelado(
                valor_original, 6
            )
        )
        assert_almost_equal(total_6x_semj, 1000.00, msg="Total 6x sem juros")
        assert_almost_equal(
            parcela_6x_semj, round(1000.00 / 6, 2), msg="Parcela 6x sem juros"
        )

        assert_raises(
            ValueError,
            self.sistema_pagamento_padrao.calcular_valor_final_cartao_credito_parcelado,
            valor_original,
            0,
        )

    def test_calculo_pix_com_desconto(self):
        valor_original = 200.00

        valor_pix_padrao = self.sistema_pagamento_padrao.calcular_valor_final_pix(
            valor_original
        )
        assert_almost_equal(valor_pix_padrao, 180.00, msg="PIX padrão")

        valor_pix_maior_desc = (
            self.sistema_pagamento_desconto_maior_pix.calcular_valor_final_pix(
                valor_original
            )
        )
        assert_almost_equal(valor_pix_maior_desc, 170.00, msg="PIX desconto maior")

        valor_pix_sem_desc = (
            self.sistema_pagamento_sem_juros_sem_desconto.calcular_valor_final_pix(
                valor_original
            )
        )
        assert_almost_equal(valor_pix_sem_desc, 200.00, msg="PIX sem desconto")

        assert_raises(
            ValueError, self.sistema_pagamento_padrao.calcular_valor_final_pix, -100.00
        )


if __name__ == "__main__":
    run()
