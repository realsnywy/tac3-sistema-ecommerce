from typing import Dict, Any, Tuple, List, Optional
from datetime import datetime


# ==============================================================================
# CLASSE PRODUTO
# ==============================================================================
class Produto:
    """
    Classe que representa um item disponível para venda em um sistema de e-commerce.

    Atributos:
        id_produto (int): Identificador único do produto.
        nome (str): Nome do produto.
        descricao (str): Descrição detalhada do produto.
        preco (float): Preço unitário do produto. Deve ser positivo.
        quantidade_em_estoque (int): Número de unidades do produto disponíveis em estoque. Deve ser não negativo.
        categoria (str): Categoria à qual o produto pertence.
    """

    def __init__(
        self,
        id_produto: int,
        nome: str,
        descricao: str,
        preco: float,
        quantidade_em_estoque: int,
        categoria: str,
    ):
        if not isinstance(id_produto, int) or id_produto <= 0:
            raise ValueError("ID do produto deve ser um inteiro positivo.")
        if not nome or not isinstance(nome, str):
            raise ValueError(
                "Nome do produto não pode ser vazio e deve ser uma string."
            )
        if not isinstance(descricao, str):
            raise ValueError("Descrição do produto deve ser uma string.")
        if not isinstance(preco, (int, float)) or preco <= 0:
            raise ValueError("Preço deve ser um número positivo.")
        if not isinstance(quantidade_em_estoque, int) or quantidade_em_estoque < 0:
            raise ValueError("Quantidade em estoque deve ser um inteiro não negativo.")
        if not categoria or not isinstance(categoria, str):
            raise ValueError(
                "Categoria do produto não pode ser vazia e deve ser uma string."
            )

        self.id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.preco = float(preco)
        self.quantidade_em_estoque = quantidade_em_estoque
        self.categoria = categoria

    def verificar_disponibilidade(self, quantidade_desejada: int) -> bool:
        """
        Verifica se a quantidade desejada do produto está disponível em estoque.
        """
        if not isinstance(quantidade_desejada, int) or quantidade_desejada <= 0:
            raise ValueError("Quantidade desejada deve ser um inteiro positivo.")
        return self.quantidade_em_estoque >= quantidade_desejada

    def reduzir_estoque(self, quantidade_vendida: int) -> None:
        """
        Reduz a quantidade em estoque do produto após uma venda.
        """
        if not isinstance(quantidade_vendida, int) or quantidade_vendida <= 0:
            raise ValueError("Quantidade vendida deve ser um inteiro positivo.")
        if quantidade_vendida > self.quantidade_em_estoque:
            raise ValueError(
                f"Não há estoque suficiente para esta venda do produto '{self.nome}'. "
                f"Solicitado: {quantidade_vendida}, Disponível: {self.quantidade_em_estoque}."
            )
        self.quantidade_em_estoque -= quantidade_vendida

    def adicionar_estoque(self, quantidade_adicionada: int) -> None:
        """
        Adiciona uma quantidade ao estoque do produto.
        """
        if not isinstance(quantidade_adicionada, int) or quantidade_adicionada <= 0:
            raise ValueError("Quantidade adicionada deve ser um inteiro positivo.")
        self.quantidade_em_estoque += quantidade_adicionada

    def obter_informacoes_detalhadas(self) -> Dict[str, Any]:
        """
        Retorna um dicionário com as informações detalhadas do produto.
        """
        return {
            "id_produto": self.id_produto,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "quantidade_em_estoque": self.quantidade_em_estoque,
            "categoria": self.categoria,
        }

    def __str__(self) -> str:
        return f"Produto(ID: {self.id_produto}, Nome: '{self.nome}', Preço: R${self.preco:.2f}, Estoque: {self.quantidade_em_estoque})"

    def __repr__(self) -> str:
        return (
            f"Produto(id_produto={self.id_produto!r}, nome={self.nome!r}, descricao={self.descricao!r}, "
            f"preco={self.preco!r}, quantidade_em_estoque={self.quantidade_em_estoque!r}, categoria={self.categoria!r})"
        )

    def __hash__(self):
        return hash(self.id_produto)

    def __eq__(self, other):
        if not isinstance(other, Produto):
            return NotImplemented
        return self.id_produto == other.id_produto


# ==============================================================================
# CLASSE CARRINHO
# ==============================================================================
class Carrinho:
    """
    Classe que gerencia os itens selecionados pelo usuário para compra.
    """

    def __init__(self):
        self.itens: Dict[Produto, int] = {}  # Produto como chave, quantidade como valor

    def adicionar_item(self, produto: Produto, quantidade: int = 1) -> None:
        if not isinstance(produto, Produto):
            raise TypeError(
                "Item a ser adicionado deve ser uma instância da classe Produto."
            )
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("Quantidade deve ser um inteiro positivo.")

        quantidade_total_desejada_no_carrinho = self.itens.get(produto, 0) + quantidade

        if produto.quantidade_em_estoque < quantidade_total_desejada_no_carrinho:
            raise ValueError(
                f"Não é possível adicionar {quantidade} unidades do produto '{produto.nome}'. "
                f"Quantidade total desejada no carrinho ({quantidade_total_desejada_no_carrinho}) excederia o estoque "
                f"disponível ({produto.quantidade_em_estoque})."
            )

        self.itens[produto] = self.itens.get(produto, 0) + quantidade

    def remover_item(self, produto: Produto, quantidade: int = 1) -> None:
        if not isinstance(produto, Produto):
            raise TypeError(
                "Item a ser removido deve ser uma instância da classe Produto."
            )
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("Quantidade a ser removida deve ser um inteiro positivo.")
        if produto not in self.itens:
            raise ValueError(f"Produto '{produto.nome}' não encontrado no carrinho.")

        if self.itens[produto] <= quantidade:
            del self.itens[produto]
        else:
            self.itens[produto] -= quantidade

    def atualizar_quantidade_item(self, produto: Produto, nova_quantidade: int) -> None:
        if not isinstance(produto, Produto):
            raise TypeError(
                "Item a ser atualizado deve ser uma instância da classe Produto."
            )
        if not isinstance(nova_quantidade, int) or nova_quantidade < 0:
            raise ValueError("Nova quantidade deve ser um inteiro não negativo.")

        if nova_quantidade == 0:
            if produto in self.itens:
                del self.itens[produto]
            return

        if produto.quantidade_em_estoque < nova_quantidade:
            raise ValueError(
                f"Produto '{produto.nome}' não tem estoque suficiente para a nova quantidade ({nova_quantidade}). "
                f"Disponível: {produto.quantidade_em_estoque}."
            )

        if nova_quantidade > 0:
            self.itens[produto] = nova_quantidade
        elif produto in self.itens:  # nova_quantidade é 0 e produto existe
            del self.itens[produto]

    def calcular_valor_total(self) -> float:
        total = 0.0
        for produto_item, quantidade_item in self.itens.items():
            total += produto_item.preco * quantidade_item
        return round(total, 2)

    def aplicar_desconto(self, percentual_desconto: float) -> float:
        if not (0 <= percentual_desconto <= 100):
            raise ValueError("Percentual de desconto deve estar entre 0 e 100.")

        valor_total = self.calcular_valor_total()
        desconto = valor_total * (percentual_desconto / 100)
        return round(desconto, 2)

    def limpar_carrinho(self) -> None:
        self.itens.clear()

    def get_itens(self) -> List[Tuple[Produto, int]]:
        return list(self.itens.items())

    def __str__(self) -> str:
        if not self.itens:
            return "Carrinho vazio."

        detalhes_itens = []
        for produto_item, quantidade_item in self.itens.items():
            detalhes_itens.append(
                f"  - {produto_item.nome} (ID: {produto_item.id_produto}): {quantidade_item} unid. @ R${produto_item.preco:.2f} cada = R${produto_item.preco * quantidade_item:.2f}"
            )

        return (
            "Itens no Carrinho:\n"
            + "\n".join(detalhes_itens)
            + f"\nValor Total: R${self.calcular_valor_total():.2f}"
        )


# ==============================================================================
# CLASSE SISTEMA PAGAMENTO
# ==============================================================================
class SistemaPagamento:
    TAXA_JUROS_PARCELAMENTO_DEFAULT = (
        0.05  # 5% de juros sobre o valor se parcelado (taxa única)
    )
    DESCONTO_PIX_DEFAULT = 0.10  # 10% de desconto para PIX padrão

    def __init__(
        self,
        taxa_juros_parcelamento: float = TAXA_JUROS_PARCELAMENTO_DEFAULT,
        desconto_pix: float = DESCONTO_PIX_DEFAULT,
    ):
        if not (0 <= taxa_juros_parcelamento <= 1):
            raise ValueError("Taxa de juros para parcelamento deve estar entre 0 e 1.")
        if not (0 <= desconto_pix <= 1):
            raise ValueError("Desconto PIX deve estar entre 0 e 1.")

        self.taxa_juros_parcelamento = taxa_juros_parcelamento
        self.desconto_pix = desconto_pix

    def calcular_valor_final_cartao_credito_a_vista(
        self, valor_original: float
    ) -> float:
        if valor_original < 0:
            raise ValueError("Valor original não pode ser negativo.")
        return round(valor_original, 2)

    def calcular_valor_final_cartao_credito_parcelado(
        self, valor_original: float, numero_parcelas: int
    ) -> Tuple[float, float]:
        if valor_original < 0:
            raise ValueError("Valor original não pode ser negativo.")
        if not isinstance(numero_parcelas, int) or numero_parcelas < 1:
            raise ValueError("Número de parcelas deve ser um inteiro positivo.")

        valor_total_com_juros = valor_original
        if numero_parcelas > 1 and self.taxa_juros_parcelamento > 0:
            valor_total_com_juros = valor_original * (1 + self.taxa_juros_parcelamento)

        valor_da_parcela = valor_total_com_juros / numero_parcelas

        return round(valor_total_com_juros, 2), round(valor_da_parcela, 2)

    def calcular_valor_final_pix(self, valor_original: float) -> float:
        if valor_original < 0:
            raise ValueError("Valor original não pode ser negativo.")

        valor_com_desconto = valor_original * (1 - self.desconto_pix)
        return round(valor_com_desconto, 2)

    def processar_pagamento(
        self,
        valor_a_pagar: float,
        metodo_pagamento: str,
        detalhes_pagamento: Dict[str, Any],
    ) -> Dict[str, Any]:
        if valor_a_pagar <= 0:
            return {
                "status": "rejeitado",
                "mensagem": "Valor do pagamento deve ser positivo.",
                "id_transacao": None,
            }

        if self._simular_verificacao_fraude(detalhes_pagamento, valor_a_pagar):
            return {
                "status": "rejeitado",
                "mensagem": "Pagamento rejeitado por suspeita de fraude.",
                "id_transacao": None,
            }

        if metodo_pagamento == "cartao_credito":
            numero_cartao = detalhes_pagamento.get("numero_cartao", "")
            numero_parcelas = detalhes_pagamento.get("numero_parcelas", 1)

            if not numero_cartao:
                return {
                    "status": "rejeitado",
                    "mensagem": "Número do cartão não fornecido.",
                    "id_transacao": None,
                }
            if "timeout" in numero_cartao:
                return {
                    "status": "erro",
                    "mensagem": "Timeout na comunicação com o gateway de pagamento.",
                    "id_transacao": None,
                }
            if "falha_autorizacao" in numero_cartao:
                return {
                    "status": "rejeitado",
                    "mensagem": "Falha na autorização do cartão de crédito.",
                    "id_transacao": None,
                }

            valor_da_parcela = (
                round(valor_a_pagar / numero_parcelas, 2)
                if numero_parcelas > 0
                else valor_a_pagar
            )
            mensagem_aprovado = (
                f"Pagamento de R${valor_a_pagar:.2f} com cartão de crédito aprovado"
            )
            if numero_parcelas > 1:
                mensagem_aprovado += (
                    f" em {numero_parcelas}x de R${valor_da_parcela:.2f}."
                )
            else:
                mensagem_aprovado += " à vista."
            return {
                "status": "aprovado",
                "mensagem": mensagem_aprovado,
                "id_transacao": f"CC_SIM_{abs(hash(numero_cartao + str(valor_a_pagar)))}",
            }

        elif metodo_pagamento == "pix":
            chave_pix = detalhes_pagamento.get("chave_pix", "")
            if not chave_pix:
                return {
                    "status": "rejeitado",
                    "mensagem": "Chave PIX não fornecida.",
                    "id_transacao": None,
                }
            return {
                "status": "aprovado",
                "mensagem": f"Pagamento PIX de R${valor_a_pagar:.2f} aprovado.",
                "id_transacao": f"PIX_SIM_{abs(hash(chave_pix + str(valor_a_pagar)))}",
            }

        else:
            return {
                "status": "erro",
                "mensagem": "Método de pagamento desconhecido.",
                "id_transacao": None,
            }

    def _simular_verificacao_fraude(
        self, detalhes_pagamento: Dict[str, Any], valor_compra: float
    ) -> bool:
        if valor_compra > 20000:
            return True
        if "cartao_suspeito" in detalhes_pagamento.get("numero_cartao", ""):
            return True
        return False

    def processar_reembolso(
        self, id_transacao_original: str, valor_reembolso: float
    ) -> Dict[str, Any]:
        if not id_transacao_original:
            return {
                "status": "falha",
                "mensagem": "ID da transação original não fornecido.",
            }
        if valor_reembolso <= 0:
            return {
                "status": "falha",
                "mensagem": "Valor do reembolso deve ser positivo.",
            }

        return {
            "status": "sucesso",
            "mensagem": f"Reembolso de R${valor_reembolso:.2f} para transação {id_transacao_original} processado.",
            "id_reembolso": f"REEMB_{abs(hash(id_transacao_original))}",
        }

    def gerar_comprovante(self, id_transacao: str, dados_compra: Dict[str, Any]) -> str:
        if not id_transacao:
            return "Erro: ID da transação não fornecido para gerar comprovante."

        valor_pago = dados_compra.get("valor_pago", 0.0)
        metodo = dados_compra.get("metodo_pagamento", "N/A")
        data_pagamento = dados_compra.get(
            "data_pagamento", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        return (
            f"--- Comprovante de Pagamento ---\n"
            f"ID da Transação: {id_transacao}\n"
            f"Valor Pago: R${valor_pago:.2f}\n"
            f"Método de Pagamento: {metodo}\n"
            f"Data: {data_pagamento}\n"
            f"---------------------------------"
        )


# ==============================================================================
# CLASSE PEDIDO
# ==============================================================================
class Pedido:
    """
    Classe que representa uma compra finalizada.
    """

    ESTADOS_VALIDOS = ["pendente", "pago", "enviado", "entregue", "cancelado"]
    TRANSICOES_PERMITIDAS = {
        "pendente": ["pago", "cancelado"],
        "pago": ["enviado", "cancelado"],
        "enviado": ["entregue", "cancelado"],
        "entregue": ["cancelado"],
        "cancelado": [],
    }

    def __init__(
        self,
        id_pedido: int,
        cliente_id: str,
        carrinho: Carrinho,
        endereco_entrega: Dict,
        metodo_pagamento_escolhido: str,
    ):
        if not id_pedido or not isinstance(id_pedido, int) or id_pedido <= 0:
            raise ValueError("ID do pedido inválido.")
        if not cliente_id:
            raise ValueError("ID do cliente não pode ser vazio.")
        if not isinstance(carrinho, Carrinho) or not carrinho.get_itens():
            raise ValueError("Carrinho inválido ou vazio para criar um pedido.")
        if not endereco_entrega or not isinstance(endereco_entrega, dict):
            raise ValueError("Endereço de entrega inválido.")
        if not metodo_pagamento_escolhido:
            raise ValueError("Método de pagamento deve ser escolhido.")

        self.id_pedido = id_pedido
        self.cliente_id = cliente_id
        self.itens_comprados: List[Tuple[Produto, int]] = list(carrinho.get_itens())
        self.valor_total_pedido = carrinho.calcular_valor_total()
        self.endereco_entrega = endereco_entrega
        self.metodo_pagamento_escolhido = metodo_pagamento_escolhido
        self.status_pedido: str = "pendente"
        self.datas: Dict[str, Optional[datetime]] = {
            "criacao": datetime.now(),
            "pagamento": None,
            "envio": None,
            "entrega": None,
            "cancelamento": None,
        }
        self.id_transacao_pagamento: Optional[str] = None
        self.valor_final_pago: Optional[float] = None

    def _atualizar_data(self, evento: str):
        if evento in self.datas:
            self.datas[evento] = datetime.now()
        else:
            raise ValueError(
                f"Evento '{evento}' desconhecido para atualização de data."
            )

    def atualizar_status(self, novo_status: str) -> bool:
        if novo_status not in self.ESTADOS_VALIDOS:
            return False

        transicoes_possiveis = self.TRANSICOES_PERMITIDAS.get(self.status_pedido, [])
        if (
            novo_status not in transicoes_possiveis
            and self.status_pedido != novo_status
        ):
            if self.status_pedido == "entregue" and novo_status == "cancelado":
                pass
            elif self.status_pedido == "cancelado" and novo_status == "cancelado":
                pass
            else:
                return False

        self.status_pedido = novo_status
        if novo_status == "pago":
            self._atualizar_data("pagamento")
        elif novo_status == "enviado":
            self._atualizar_data("envio")
        elif novo_status == "entregue":
            self._atualizar_data("entrega")
        elif novo_status == "cancelado":
            self._atualizar_data("cancelamento")
        return True

    def calcular_frete(self) -> float:
        if self.valor_total_pedido > 200:
            return 0.0
        return 25.0

    def gerar_nota_fiscal(self) -> str:
        if self.status_pedido not in ["pago", "enviado", "entregue"]:
            return "Nota fiscal não pode ser gerada: pedido não foi pago ou está pendente/cancelado."

        nota = f"--- Nota Fiscal ---\n"
        nota += f"Pedido ID: {self.id_pedido}\nCliente ID: {self.cliente_id}\n"
        data_criacao_str = (
            self.datas["criacao"].strftime("%Y-%m-%d %H:%M:%S")
            if self.datas["criacao"]
            else "N/A"
        )
        nota += f"Data da Compra: {data_criacao_str}\n"
        if self.datas["pagamento"]:
            data_pagamento_str = (
                self.datas["pagamento"].strftime("%Y-%m-%d %H:%M:%S")
                if self.datas["pagamento"]
                else "N/A"
            )
            nota += f"Data do Pagamento: {data_pagamento_str}\n"
        nota += "Itens:\n"
        for produto_item, qtd in self.itens_comprados:
            nota += f"  - {produto_item.nome}: {qtd} x R${produto_item.preco:.2f} = R${produto_item.preco * qtd:.2f}\n"
        subtotal = sum(p.preco * q for p, q in self.itens_comprados)
        nota += f"Subtotal: R${subtotal:.2f}\n"
        frete = self.calcular_frete()
        nota += f"Frete: R${frete:.2f}\n"
        total_nf = (
            self.valor_final_pago
            if self.valor_final_pago is not None
            else subtotal + frete
        )
        nota += f"Valor Final Pago: R${total_nf:.2f}\n"
        nota += f"Método de Pagamento: {self.metodo_pagamento_escolhido}\n"
        nota += f"Endereço de Entrega: {self.endereco_entrega.get('rua', '')}, {self.endereco_entrega.get('cep', '')}\n"
        nota += "--------------------"
        return nota

    def registrar_pagamento(self, id_transacao: str, valor_pago_efetivo: float):
        self.id_transacao_pagamento = id_transacao
        self.valor_final_pago = valor_pago_efetivo
        self.atualizar_status("pago")

    def __str__(self):
        return (
            f"Pedido(ID: {self.id_pedido}, Cliente: {self.cliente_id}, "
            f"Status: {self.status_pedido}, Valor Original: R${self.valor_total_pedido:.2f}, "
            f"Pago: R${self.valor_final_pago if self.valor_final_pago is not None else 'N/A'})"
        )


# ==============================================================================
# CLASSE SISTEMA ECOMMERCE
# ==============================================================================
class SistemaEcommerce:
    def __init__(self):
        self.produtos_catalogo: Dict[int, Produto] = {}
        self.pedidos_registrados: Dict[int, Pedido] = {}
        self.usuarios: Dict[str, Dict] = {}
        self.sistema_pagamento = SistemaPagamento()
        self._proximo_id_produto = 1
        self._proximo_id_pedido = 1

    def configurar_sistema_pagamento(
        self,
        taxa_juros_parcelamento: Optional[float] = None,
        desconto_pix: Optional[float] = None,
    ):
        current_juros = (
            self.sistema_pagamento.taxa_juros_parcelamento
            if taxa_juros_parcelamento is None
            else taxa_juros_parcelamento
        )
        current_pix = (
            self.sistema_pagamento.desconto_pix
            if desconto_pix is None
            else desconto_pix
        )
        self.sistema_pagamento = SistemaPagamento(
            taxa_juros_parcelamento=current_juros, desconto_pix=current_pix
        )

    def adicionar_produto_catalogo(
        self,
        nome: str,
        descricao: str,
        preco: float,
        quantidade_em_estoque: int,
        categoria: str,
    ) -> Produto:
        novo_id = self._proximo_id_produto
        produto = Produto(
            id_produto=novo_id,
            nome=nome,
            descricao=descricao,
            preco=preco,
            quantidade_em_estoque=quantidade_em_estoque,
            categoria=categoria,
        )
        self.produtos_catalogo[novo_id] = produto
        self._proximo_id_produto += 1
        return produto

    def recuperar_produto_por_id(self, id_produto: int) -> Optional[Produto]:
        return self.produtos_catalogo.get(id_produto)

    def buscar_produtos(
        self, termo_busca: str, categoria: Optional[str] = None
    ) -> List[Produto]:
        resultados = []
        termo_busca_lower = termo_busca.lower()
        for produto_item in self.produtos_catalogo.values():
            if (
                termo_busca_lower in produto_item.nome.lower()
                or termo_busca_lower in produto_item.descricao.lower()
            ):
                if categoria and produto_item.categoria.lower() != categoria.lower():
                    continue
                resultados.append(produto_item)
        return resultados

    def registrar_usuario(self, user_id: str, dados_usuario: Dict):
        if user_id in self.usuarios:
            raise ValueError(f"Usuário com ID '{user_id}' já existe.")
        self.usuarios[user_id] = dados_usuario

    def criar_pedido(
        self,
        cliente_id: str,
        carrinho: Carrinho,
        endereco_entrega: Dict,
        metodo_pagamento_escolhido: str,
    ) -> Optional[Pedido]:
        if cliente_id not in self.usuarios:
            return None
        if not carrinho.get_itens():
            return None

        novo_id_pedido = self._proximo_id_pedido
        try:
            pedido = Pedido(
                id_pedido=novo_id_pedido,
                cliente_id=cliente_id,
                carrinho=carrinho,
                endereco_entrega=endereco_entrega,
                metodo_pagamento_escolhido=metodo_pagamento_escolhido,
            )
            self.pedidos_registrados[novo_id_pedido] = pedido
            self._proximo_id_pedido += 1
            return pedido
        except ValueError:
            return None

    def processar_pagamento_pedido(
        self, id_pedido: int, detalhes_pagamento_cliente: Dict
    ) -> Dict[str, Any]:
        pedido = self.pedidos_registrados.get(id_pedido)
        if not pedido:
            return {
                "status": "erro",
                "mensagem": f"Pedido ID {id_pedido} não encontrado.",
            }
        if pedido.status_pedido != "pendente":
            return {
                "status": "erro",
                "mensagem": f"Pedido ID {id_pedido} não está pendente de pagamento (status: {pedido.status_pedido}).",
            }

        valor_a_pagar = pedido.valor_total_pedido

        if pedido.metodo_pagamento_escolhido == "pix":
            valor_a_pagar = self.sistema_pagamento.calcular_valor_final_pix(
                pedido.valor_total_pedido
            )
        elif pedido.metodo_pagamento_escolhido == "cartao_credito":
            num_parcelas = detalhes_pagamento_cliente.get("numero_parcelas", 1)
            valor_total_com_juros, _ = (
                self.sistema_pagamento.calcular_valor_final_cartao_credito_parcelado(
                    pedido.valor_total_pedido, num_parcelas
                )
            )
            valor_a_pagar = valor_total_com_juros
            if "numero_parcelas" not in detalhes_pagamento_cliente:
                detalhes_pagamento_cliente["numero_parcelas"] = num_parcelas

        detalhes_pagamento_cliente_com_valor = {
            **detalhes_pagamento_cliente,
            "valor_compra_calculado": valor_a_pagar,
        }

        resultado_pagamento = self.sistema_pagamento.processar_pagamento(
            valor_a_pagar,
            pedido.metodo_pagamento_escolhido,
            detalhes_pagamento_cliente_com_valor,
        )

        if resultado_pagamento["status"] == "aprovado":
            pedido.registrar_pagamento(
                resultado_pagamento["id_transacao"], valor_a_pagar
            )
            try:
                for produto_no_pedido, quantidade_comprada in pedido.itens_comprados:
                    produto_catalogo = self.produtos_catalogo.get(
                        produto_no_pedido.id_produto
                    )
                    if produto_catalogo:
                        produto_catalogo.reduzir_estoque(quantidade_comprada)
                    else:
                        raise Exception(
                            f"Produto ID {produto_no_pedido.id_produto} do pedido não encontrado no catálogo para reduzir estoque."
                        )
            except ValueError as e:
                resultado_pagamento["status"] = "aprovado_com_erro_estoque"
                resultado_pagamento["mensagem"] = (
                    f"{resultado_pagamento['mensagem']} Erro ao reduzir estoque: {e}"
                )
        elif resultado_pagamento["status"] in ["rejeitado", "erro"]:
            pass

        return resultado_pagamento

    def cancelar_pedido(
        self, id_pedido: int, motivo: str = "Cancelado pelo sistema"
    ) -> bool:
        pedido = self.pedidos_registrados.get(id_pedido)
        if not pedido:
            return False

        status_anterior = pedido.status_pedido
        if pedido.atualizar_status("cancelado"):
            if status_anterior in ["pago", "enviado"]:
                for produto_no_pedido, quantidade_comprada in pedido.itens_comprados:
                    produto_catalogo = self.produtos_catalogo.get(
                        produto_no_pedido.id_produto
                    )
                    if produto_catalogo:
                        produto_catalogo.adicionar_estoque(quantidade_comprada)
            return True
        return False

    def gerar_relatorio_vendas(self, status_filtro: Optional[str] = None) -> Dict:
        total_vendas = 0.0
        num_pedidos = 0
        pedidos_filtrados = []

        for pedido_obj in self.pedidos_registrados.values():
            if status_filtro and pedido_obj.status_pedido != status_filtro:
                continue

            if pedido_obj.status_pedido in ["pago", "enviado", "entregue"]:
                if pedido_obj.valor_final_pago is not None:
                    total_vendas += pedido_obj.valor_final_pago
                num_pedidos += 1
            pedidos_filtrados.append(str(pedido_obj))

        return {
            "total_vendas_apuradas": round(total_vendas, 2),
            "numero_de_pedidos_contabilizados": num_pedidos,
            "filtro_status_aplicado": (
                status_filtro
                if status_filtro
                else "Nenhum (considerados pagos/enviados/entregues)"
            ),
            "lista_pedidos_no_relatorio": pedidos_filtrados,
        }
