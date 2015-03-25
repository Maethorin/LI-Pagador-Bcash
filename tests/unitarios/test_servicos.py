# -*- coding: utf-8 -*-
import unittest

import mock

from pagador_bcash import servicos


class BcashEntregandoPagamento(unittest.TestCase):
    def test_entrega_tem_malote(self):
        entrega = servicos.EntregaPagamento(234)
        entrega.tem_malote.should.be.truthy

    def test_processa_pagamento(self):
        entrega = servicos.EntregaPagamento(234, dados={'next_url', 'url-next'})
        entrega.malote = mock.MagicMock()
        entrega.malote.to_dict.return_value = 'dados'
        entrega.processa_dados_pagamento()
        entrega.resultado.should.be.equal({'dados': 'dados'})

    def test_processa_pagamento_da_erro_sem_next_url(self):
        entrega = servicos.EntregaPagamento(234, dados={})
        entrega.pedido = mock.MagicMock(numero=123)
        entrega.malote = mock.MagicMock()
        entrega.malote.to_dict.return_value = 'dados'
        entrega.processa_dados_pagamento.when.called_with().should.throw(entrega.EnvioNaoRealizado, u'Pedido 123 na Loja Id 234\nAs configurações do seu navegador não permitiu o envio dos dados corretos. Por favor, verifique se o JavaScript está habilitado:\n\tnext_url não está em dados.')


class BcashSituacoesPagamento(unittest.TestCase):
    def test_deve_retornar_aguadando_para_em_andamento(self):
        servicos.SituacoesDePagamento.do_tipo('Em andamento').should.be.equal(servicos.servicos.SituacaoPedido.SITUACAO_AGUARDANDO_PAGTO)

    def test_deve_retornar_aguadando_para_zero(self):
        servicos.SituacoesDePagamento.do_tipo('0').should.be.equal(servicos.servicos.SituacaoPedido.SITUACAO_AGUARDANDO_PAGTO)

    def test_deve_retornar_pago_para_aprovada(self):
        servicos.SituacoesDePagamento.do_tipo('Aprovada').should.be.equal(servicos.servicos.SituacaoPedido.SITUACAO_PEDIDO_PAGO)

    def test_deve_retornar_pago_para_um(self):
        servicos.SituacoesDePagamento.do_tipo('1').should.be.equal(servicos.servicos.SituacaoPedido.SITUACAO_PEDIDO_PAGO)

    def test_deve_retornar_em_disputa_para_disputa(self):
        servicos.SituacoesDePagamento.do_tipo('Disputa').should.be.equal(servicos.servicos.SituacaoPedido.SITUACAO_PAGTO_EM_DISPUTA)

    def test_deve_retornar_devolvido_para_devolvida(self):
        servicos.SituacoesDePagamento.do_tipo('Devolvida').should.be.equal(servicos.servicos.SituacaoPedido.SITUACAO_PAGTO_DEVOLVIDO)

    def test_deve_retornar_cancelado_para_cancelada(self):
        servicos.SituacoesDePagamento.do_tipo('Cancelada').should.be.equal(servicos.servicos.SituacaoPedido.SITUACAO_PEDIDO_CANCELADO)

    def test_deve_retornar_cancelado_para_dois(self):
        servicos.SituacoesDePagamento.do_tipo('2').should.be.equal(servicos.servicos.SituacaoPedido.SITUACAO_PEDIDO_CANCELADO)

    def test_deve_retornar_chargeback_para_chargeback(self):
        servicos.SituacoesDePagamento.do_tipo('Chargeback').should.be.equal(servicos.servicos.SituacaoPedido.SITUACAO_PAGTO_CHARGEBACK)

    def test_deve_retornar_none_para_desconhecido(self):
        servicos.SituacoesDePagamento.do_tipo('zas').should.be.none


class BcashRegistrandoResultado(unittest.TestCase):
    def test_deve_definir_redirect(self):
        registrador = servicos.RegistraResultado(1234, {'next_url': 'url-next'})
        registrador.redirect_para.should.be.equal('url-next')

    def test_deve_montar_dados_pagamento(self):
        registrador = servicos.RegistraResultado(1234, {'next_url': 'url-next', 'referencia': 1234, 'id_transacao': 'transacao-id', 'cod_status': '0'})
        registrador.monta_dados_pagamento()
        registrador.dados_pagamento.should.be.equal({'identificador_id': 'transacao-id', 'transacao_id': 'transacao-id'})

    def test_deve_definir_situacao_pedido(self):
        registrador = servicos.RegistraResultado(1234, {'next_url': 'url-next', 'referencia': 1234, 'id_transacao': 'transacao-id', 'cod_status': '0'})
        registrador.monta_dados_pagamento()
        registrador.situacao_pedido.should.be.equal(servicos.servicos.SituacaoPedido.SITUACAO_AGUARDANDO_PAGTO)

    def test_deve_retornar_resultado_ok(self):
        registrador = servicos.RegistraResultado(1234, {'next_url': 'url-next', 'referencia': 1234, 'id_transacao': 'transacao-id', 'cod_status': '0'})
        registrador.monta_dados_pagamento()
        registrador.resultado.should.be.equal('sucesso')

    def test_deve_retornar_resultado_pendente(self):
        registrador = servicos.RegistraResultado(1234, {'next_url': 'url-next', 'referencia': 1234, 'cod_status': '0'})
        registrador.monta_dados_pagamento()
        registrador.resultado.should.be.equal('pendente')


class BcashRegistrandoNotificacao(unittest.TestCase):
    def test_nao_deve_definir_redirect(self):
        registrador = servicos.RegistraNotificacao(1234, {})
        registrador.redirect_para.should.be.none

    def test_deve_montar_dados_pagamento(self):
        registrador = servicos.RegistraNotificacao(1234, {'id_pedido': 1234, 'id_transacao': 'transacao-id', 'cod_status': '0'})
        registrador.monta_dados_pagamento()
        registrador.dados_pagamento.should.be.equal({'identificador_id': 'transacao-id', 'transacao_id': 'transacao-id'})

    def test_deve_definir_situacao_pedido(self):
        registrador = servicos.RegistraNotificacao(1234, {'id_pedido': 1234, 'id_transacao': 'transacao-id', 'cod_status': '0'})
        registrador.monta_dados_pagamento()
        registrador.situacao_pedido.should.be.equal(servicos.servicos.SituacaoPedido.SITUACAO_AGUARDANDO_PAGTO)

    def test_deve_retornar_resultado_ok(self):
        registrador = servicos.RegistraNotificacao(1234, {'id_pedido': 1234, 'id_transacao': 'transacao-id', 'cod_status': '0'})
        registrador.monta_dados_pagamento()
        registrador.resultado.should.be.equal({'resultado': 'OK'})
