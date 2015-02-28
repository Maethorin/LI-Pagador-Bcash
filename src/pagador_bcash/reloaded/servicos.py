# -*- coding: utf-8 -*-

from pagador.reloaded import servicos


class Resultado(object):
    def __init__(self, dados):
        self.sucesso = True
        self.conteudo = {"dados": dados}


class EntregaPagamento(servicos.EntregaPagamento):
    def __init__(self, loja_id, plano_indice=1):
        super(EntregaPagamento, self).__init__(loja_id, plano_indice)
        self.tem_malote = True

    def enviar_pagamento(self, tentativa=1):
        dados = self.malote.to_dict()
        self.resultado = Resultado(dados)
