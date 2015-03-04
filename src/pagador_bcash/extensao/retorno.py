# -*- coding: utf-8 -*-
from pagador.acesso.externo import FormatoDeEnvio
from pagador.retorno.models import SituacaoPedido
from pagador.retorno.registro import RegistroBase


class SituacoesDePagamento(object):
    aguardando = "0"
    paga = "1"
    cancelado = "2"

    @classmethod
    def do_tipo(cls, tipo):
        return getattr(cls, tipo, None)


class Registro(RegistroBase):
    def __init__(self, dados, tipo="retorno", configuracao=None):
        super(Registro, self).__init__(dados, configuracao)
        self.exige_autenticacao = False
        self.processa_resposta = True
        self.tipo = tipo
        self.formato_envio = FormatoDeEnvio.json

    @property
    def url(self):
        return None

    @property
    def pedido_numero(self):
        if "referencia" in self.dados:
            return self.dados["referencia"]
        elif "id_pedido" in self.dados:
            return self.dados["id_pedido"]
        return None

    @property
    def identificador_id(self):
        if "id_transacao" in self.dados:
            return self.dados["id_transacao"]
        return None

    @property
    def deve_gravar_dados_pagamento(self):
        return True

    def __getattr__(self, name):
        if name.startswith("situacao_"):
            if not "cod_status" in self.dados:
                return False
            tipo = name.replace("situacao_", "")
            return self.dados["cod_status"] == SituacoesDePagamento.do_tipo(tipo)
        return object.__getattribute__(self, name)

    @property
    def situacao_pedido(self):
        if self.situacao_aguardando:
            return SituacaoPedido.SITUACAO_AGUARDANDO_PAGTO
        if self.situacao_paga:
            return SituacaoPedido.SITUACAO_PEDIDO_PAGO
        if self.situacao_cancelado:
            return SituacaoPedido.SITUACAO_PEDIDO_CANCELADO
        return None

    @property
    def alterar_situacao(self):
        return self.situacao_pedido is not None

    @property
    def retorno_requisicao(self):
        return self.tipo == "success"

    @property
    def retorno_notificacao(self):
        return self.tipo == "retorno"

    @property
    def obter_dados_gateway(self):
        return False

    @property
    def redireciona_para(self):
        if self.retorno_requisicao:
            tipo = self.tipo
            if self.situacao_aguardando:
                tipo = 'pending'
            if self.situacao_cancelado:
                tipo = 'failure'
            return "{}?{}=1".format(self.dados["next_url"], tipo)
        return None