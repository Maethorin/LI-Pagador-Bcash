# -*- coding: utf-8 -*-
import unittest
import mock
from pagador_bcash.reloaded import servicos


class BcashEntregandoPagamento(unittest.TestCase):
    def test_entrega_tem_malote(self):
        entrega = servicos.EntregaPagamento(234)
        entrega.tem_malote.should.be.truthy

    def test_processa_pagamento(self):
        entrega = servicos.EntregaPagamento(234)
        entrega.malote = mock.MagicMock()
        entrega.malote.to_dict.return_value = 'dados'
        entrega.processa_dados_de_pagamento()
        entrega.resultado.should.be.equal({'dados': 'dados'})