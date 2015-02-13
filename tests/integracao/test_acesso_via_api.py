# -*- coding: utf-8 -*-
import json
import mock
from li_common.padroes import extensibilidade

from tests.base import TestBase

extensibilidade.SETTINGS.EXTENSOES = {
    'pagamento_digital': 'pagador_bcash.reloaded'
}


class ConfiguracaoMeioDePagamentoDaLoja(TestBase):
    url = '/loja/8/meio-pagamento/pagamento_digital/'

    @mock.patch('pagador_bcash.reloaded.entidades.ConfiguracaoMeioPagamento')
    def test_deve_obter_dados_do_bcash(self, configuracao_mock):
        configuracao = mock.MagicMock()
        configuracao_mock.return_value = configuracao
        configuracao.to_dict.return_value = 'BCASH'
        response = self.app.get(self.url, follow_redirects=True, headers={'authorization': 'chave_aplicacao CHAVE-TESTE'})
        json.loads(response.data).should.be.equal({u'metadados': {u'api': u'API Pagador', u'resultado': u'sucesso', u'versao': u'1.0'}, u'sucesso': {u'configuracao_pagamento': u'BCASH'}})
        response.status_code.should.be.equal(200)
        configuracao_mock.assert_called_with(loja_id=8)

    @mock.patch('pagador_bcash.reloaded.entidades.ConfiguracaoMeioPagamento')
    def test_deve_grava_dados_do_bcash(self, configuracao_mock):
        configuracao = mock.MagicMock()
        configuracao_mock.return_value = configuracao
        configuracao.to_dict.return_value = 'BCASH'
        response = self.app.post(self.url, follow_redirects=True, data={'token': 'ZES'}, headers={'authorization': 'chave_aplicacao CHAVE-TESTE'})
        json.loads(response.data).should.be.equal({u'metadados': {u'api': u'API Pagador', u'resultado': u'sucesso', u'versao': u'1.0'}, u'sucesso': {u'configuracao_pagamento': u'BCASH'}})
        response.status_code.should.be.equal(200)
        configuracao.salvar.assert_called_with({'token': u'ZES'})
