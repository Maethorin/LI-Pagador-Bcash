# -*- coding: utf-8 -*-

from pagador.reloaded import servicos


class EntregaPagamento(servicos.EntregaPagamento):
    def __init__(self, loja_id, plano_indice=1):
        super(EntregaPagamento, self).__init__(loja_id, plano_indice)
        self.tem_malote = True

    def processa_dados_de_pagamento(self):
        dados = self.malote.to_dict()
        self.resultado = {"dados": dados}
