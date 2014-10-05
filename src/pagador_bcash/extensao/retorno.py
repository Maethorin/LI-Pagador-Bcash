# -*- coding: utf-8 -*-
import json
from pagador import settings
from pagador.retorno.models import SituacaoPedido
from pagador.retorno.registro import RegistroBase
from pagador_pagseguro.extensao.seguranca import ParametrosPagSeguro


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
        self.envio_por_querystring = False

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
    def grava_identificador(self):
        return True

    def __getattr__(self, name):
        if name.startswith("situacao_"):
            if not "cod_status" in self.dados:
                return False
            tipo = name.replace("situacao_", "")
            return self.dados["cod_status"] == SituacoesDePagamento.do_tipo(tipo)
        return object.__getattribute__(self, name)

    @property
    def situacao_do_pedido(self):
        if self.situacao_aguardando:
            return SituacaoPedido.SITUACAO_AGUARDANDO_PAGTO
        if self.situacao_paga:
            return SituacaoPedido.SITUACAO_PEDIDO_PAGO
        if self.situacao_cancelado:
            return SituacaoPedido.SITUACAO_PEDIDO_CANCELADO
        return SituacaoPedido.SITUACAO_PEDIDO_EFETUADO

    @property
    def alterar_situacao(self):
        return True

    @property
    def retorno_de_requisicao(self):
        return self.tipo == "success"

    @property
    def retorno_de_notificacao(self):
        return self.tipo == "retorno"

    @property
    def obter_dados_do_gateway(self):
        return False

    @property
    def redireciona_para(self):
        if "next_url" in self.dados:
            tipo = self.tipo
            if self.situacao_aguardando:
                tipo = 'pending'
            if self.situacao_cancelado:
                tipo = 'failure'
            return "{}?{}=1".format(self.dados["next_url"], tipo)
        return None
