# -*- coding: utf-8 -*-
from li_common.comunicacao import requisicao

from pagador.reloaded import servicos


class EntregaPagamento(servicos.EntregaPagamento):
    def __init__(self, loja_id, plano_indice=1, dados=None):
        super(EntregaPagamento, self).__init__(loja_id, plano_indice, dados=dados)
        self.tem_malote = True

    def processa_dados_pagamento(self):
        dados = self.malote.to_dict()
        self.resultado = {"dados": dados}


class SituacoesDePagamento(servicos.SituacoesDePagamento):
    DE_PARA = {
        'Em Andamento': servicos.SituacaoPedido.SITUACAO_AGUARDANDO_PAGTO,
        'Aprovada': servicos.SituacaoPedido.SITUACAO_PEDIDO_PAGO,
        'Disputa': servicos.SituacaoPedido.SITUACAO_PAGTO_EM_DISPUTA,
        'Devolvida': servicos.SituacaoPedido.SITUACAO_PAGTO_DEVOLVIDO,
        'Cancelada': servicos.SituacaoPedido.SITUACAO_PEDIDO_CANCELADO,
        'Chargebcak': servicos.SituacaoPedido.SITUACAO_PAGTO_CHARGEBACK,
        '0': servicos.SituacaoPedido.SITUACAO_AGUARDANDO_PAGTO,
        '1': servicos.SituacaoPedido.SITUACAO_PEDIDO_PAGO,
        '2': servicos.SituacaoPedido.SITUACAO_PEDIDO_CANCELADO,
    }


class RegistraResultado(servicos.RegistraResultado):
    def __init__(self, loja_id, dados=None):
        super(RegistraResultado, self).__init__(loja_id, dados)
        self.redirect_para = dados.get('next_url', None)

    def monta_dados_pagamento(self):
        self.pedido_numero = self.dados["referencia"]
        self.dados_pagamento['identificador_id'] = self.dados['id_transacao']
        self.dados_pagamento['transacao_id'] = self.dados['id_transacao']
        self.situacao_pedido = SituacoesDePagamento.do_tipo(self.dados['cod_status'])
        self.resultado = {'resultado': 'OK'}


class RegistraNotificacao(servicos.RegistraResultado):
    def __init__(self, loja_id, dados=None):
        super(RegistraNotificacao, self).__init__(loja_id, dados)

    def monta_dados_pagamento(self):
        self.pedido_numero = self.dados["pedido"]
        self.dados_pagamento['identificador_id'] = self.dados['transacao_id']
        self.dados_pagamento['transacao_id'] = self.dados['id_transacao']
        self.situacao_pedido = SituacoesDePagamento.do_tipo(self.dados['status'])
        self.resultado = {'resultado': 'OK'}
