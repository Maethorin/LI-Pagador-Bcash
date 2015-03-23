# -*- coding: utf-8 -*-

from pagador import servicos


class EntregaPagamento(servicos.EntregaPagamento):
    def __init__(self, loja_id, plano_indice=1, dados=None):
        super(EntregaPagamento, self).__init__(loja_id, plano_indice, dados=dados)
        self.tem_malote = True

    def processa_dados_pagamento(self):
        if 'next_url' not in self.dados:
            raise self.EnvioNaoRealizado(u'As configurações do seu navegador não permitiu o envio dos dados corretos. Por favor, verifique se o JavaScript está habilitado', self.loja_id, self.pedido.numero, dados_envio={}, erros=[u'next_url não está em dados.'])
        dados = self.malote.to_dict()
        self.resultado = {"dados": dados}


class SituacoesDePagamento(servicos.SituacoesDePagamento):
    DE_PARA = {
        'Aprovada': servicos.SituacaoPedido.SITUACAO_PEDIDO_PAGO,
        'Cancelada': servicos.SituacaoPedido.SITUACAO_PEDIDO_CANCELADO,
        'Em andamento': servicos.SituacaoPedido.SITUACAO_AGUARDANDO_PAGTO,
        'Disputa': servicos.SituacaoPedido.SITUACAO_PAGTO_EM_DISPUTA,
        'Devolvida': servicos.SituacaoPedido.SITUACAO_PAGTO_DEVOLVIDO,
        'Chargeback': servicos.SituacaoPedido.SITUACAO_PAGTO_CHARGEBACK,
        '0': servicos.SituacaoPedido.SITUACAO_AGUARDANDO_PAGTO,
        '1': servicos.SituacaoPedido.SITUACAO_PEDIDO_PAGO,
        '2': servicos.SituacaoPedido.SITUACAO_PEDIDO_CANCELADO,
    }


class RegistraResultado(servicos.RegistraResultado):
    def __init__(self, loja_id, dados=None):
        super(RegistraResultado, self).__init__(loja_id, dados)
        self.redirect_para = dados.get('next_url', None)

    @property
    def transacao_id(self):
        return self.dados.get('id_transacao', None) or self.dados.get('transacao_id', None) or self.dados['transacao']

    @property
    def pedido_id(self):
        return self.dados.get('id_pedido', None) or self.dados.get('pedido_id', None) or self.dados['pedido']

    @property
    def status(self):
        return self.dados.get('cod_status', None) or self.dados.get('status', None)

    def monta_dados_pagamento(self):
        if 'id_transacao' in self.dados:
            self.pedido_numero = self.dados["referencia"]
            self.dados_pagamento['identificador_id'] = self.transacao_id
            self.dados_pagamento['transacao_id'] = self.transacao_id
            self.situacao_pedido = SituacoesDePagamento.do_tipo(self.status)
            self.resultado = 'sucesso'
        else:
            self.resultado = 'pendente'


class RegistraNotificacao(servicos.RegistraResultado):
    def __init__(self, loja_id, dados=None):
        super(RegistraNotificacao, self).__init__(loja_id, dados)

    @property
    def transacao_id(self):
        return self.dados.get('id_transacao', None) or self.dados.get('transacao_id', None) or self.dados['transacao']

    @property
    def pedido_id(self):
        return self.dados.get('id_pedido', None) or self.dados.get('pedido_id', None) or self.dados['pedido']

    @property
    def status(self):
        return self.dados.get('cod_status', None) or self.dados.get('status', None)

    def monta_dados_pagamento(self):
        self.pedido_numero = self.pedido_id
        self.dados_pagamento['identificador_id'] = self.transacao_id
        self.dados_pagamento['transacao_id'] = self.transacao_id
        self.situacao_pedido = SituacoesDePagamento.do_tipo(self.status)
        self.resultado = {'resultado': 'OK'}
