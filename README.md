# tac3-sistema-ecommerce

Atividade prática da disciplina TAC-3 (Testes) da UNIVASF.

---

## 📋 Informações Gerais

- **Período:** 3º
- **Disciplina:** TAC-3 - Tópicos Avançados em Computação III - Testes

Este projeto implementa um sistema de e-commerce em Python, com foco em testes automatizados utilizando **Pytest**, **unittest** e **Testify**. O sistema permite compras com pagamento via cartão de crédito (à vista ou parcelado) e PIX, seguindo princípios de Clean Code e SOLID.

---

## 🏗️ Estrutura do Sistema

O sistema é composto pelas seguintes classes principais:

- **Produto:** Item à venda, com atributos como `id`, `nome`, `descrição`, `preço`, `quantidade em estoque` e `categoria`. Métodos para disponibilidade, atualização de estoque e informações detalhadas.
- **Carrinho:** Gerencia itens selecionados para compra. Permite adicionar, remover, atualizar itens, calcular valor total, aplicar descontos e limpar o carrinho.
- **SistemaPagamento:** Processa transações financeiras (cartão de crédito e PIX). Implementa autorização, verificação de fraude, reembolso e geração de comprovantes.
- **Pedido:** Representa uma compra finalizada, armazenando informações do cliente, itens, endereço, método de pagamento, status e datas. Permite atualizar status, calcular frete e gerar nota fiscal.
- **SistemaEcommerce:** Classe principal que integra todas as outras, gerenciando o fluxo completo de compra.

---

## 🧪 Questões e Testes Implementados

| Questão | Ferramenta/Teste | Descrição |
|---------|------------------|-----------|
| **1**   | Pytest           | Testes para `Produto`: criação, disponibilidade e redução de estoque |
| **2**   | unittest         | Testes para `Carrinho`: adição/remoção de itens, valor total, estoque insuficiente |
| **3**   | Testify          | Testes para `SistemaPagamento`: cálculos de cartão (à vista/parcelado), PIX, parcelas |
| **4**   | Pytest           | Integração `Carrinho` + `Produto`: valor total, estoque, remoção parcial |
| **5**   | unittest         | Testes para `Pedido`: transições de estado, pagamento, restrições |
| **6**   | Testify          | Testes para `SistemaEcommerce`: produtos, pedidos, pagamentos, cancelamento/reabastecimento |
| **7**   | Pytest + Mock    | Simulação de falhas no pagamento: autorização, timeout, estado do pedido |
| **8**   | unittest + Fixtures | Integração do fluxo de compra: PIX, cartão à vista/parcelado |
| **9**   | Testify + Parametrização | Configurações: taxas de juros, descontos PIX, parcelas |
| **10**  | Pytest, unittest, Testify | Testes de performance: múltiplos produtos, pagamentos, volume de pedidos |

---

## ▶️ Como Executar o Projeto e os Testes

### 1. Crie e ative um ambiente virtual

```sh
python -m venv .venv
# Ative o ambiente virtual:
# No Windows:
.venv\Scripts\activate
# No macOS/Linux:
source .venv/bin/activate
```

### 2. Instale as dependências

```sh
pip install -r requirements.txt
```

### 3. Execute os testes

- **Pytest:**

  ```sh
  pytest test/
  ```

- **unittest:**

  ```sh
  python -m unittest discover -s test
  ```

- **Testify:**

  ```sh
  python test/test_questao3.py
  python test/test_questao6.py
  python test/test_questao9.py
  python test/test_questao10_testify.py
  ```

---

## ▶️ Como Executar a Demonstração do Sistema

Para executar uma demonstração do sistema de e-commerce, utilize o arquivo principal localizado em `app/ecommerce_sistema.py`. Siga os passos abaixo:

```sh
python app/ecommerce_sistema.py
```

Caso o arquivo aceite argumentos ou tenha um menu interativo, siga as instruções exibidas no terminal.
Se desejar modificar ou criar um fluxo de demonstração personalizado, edite o arquivo `ecommerce_sistema.py` conforme necessário.

---

## 📁 Estrutura de Pastas

```
app/
    ecommerce_sistema.py
test/
    test_questao1.py
    test_questao2.py
    test_questao3.py
    test_questao4.py
    test_questao5.py
    test_questao6.py
    test_questao7.py
    test_questao8.py
    test_questao9.py
    test_questao10_pytest.py
    test_questao10_unittest.py
    test_questao10_testify.py
```

---

## 🛠️ Requisitos

- Python 3.8+
- pytest
- unittest (builtin)
- testify

As dependências estão listadas em `requirements.txt`.

---

> **Este é um projeto acadêmico desenvolvido para fins educacionais.**
