# -*- coding: utf-8 -*-
import unittest
import mock
from pagador_bcash.reloaded import servicos


class EntregandoPagamento(unittest.TestCase):
    def test_resultado_no_padrao(self):
        resultado = servicos.Resultado({'chave': 'valor'})
        resultado.sucesso.should.be.truthy
        resultado.conteudo.should.be.equal({'dados': {'chave': 'valor'}})

    def test_entrega_tem_malote(self):
        entrega = servicos.EntregaPagamento(234)
        entrega.tem_malote.should.be.truthy

    def test_envia_pagamento(self):
        entrega = servicos.EntregaPagamento(234)
        entrega.malote = mock.MagicMock()
        entrega.malote.to_dict.return_value = 'dados'
        entrega.enviar_pagamento()
        entrega.resultado.sucesso.should.be.truthy
        entrega.resultado.conteudo.should.be.equal({'dados': 'dados'})