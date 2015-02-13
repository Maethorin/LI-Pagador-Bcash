# -*- coding: utf-8 -*-
import unittest
from pagador_bcash.reloaded import cadastro


class FormularioBcash(unittest.TestCase):
    def test_deve_ter_ativo(self):
        formulario = cadastro.FormularioBcash()
        formulario.ativo.nome.should.be.equal('ativo')
        formulario.ativo.ordem.should.be.equal(1)
        formulario.ativo.label.should.be.equal('Pagamento ativo?')
        formulario.ativo.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.boleano)

    def test_deve_ter_usuario(self):
        formulario = cadastro.FormularioBcash()
        formulario.usuario.nome.should.be.equal('usuario')
        formulario.usuario.ordem.should.be.equal(2)
        formulario.usuario.label.should.be.equal('Seu email no Bcash')
        formulario.usuario.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.texto)

    def test_deve_ter_token(self):
        formulario = cadastro.FormularioBcash()
        formulario.token.nome.should.be.equal('token')
        formulario.token.ordem.should.be.equal(3)
        formulario.token.label.should.be.equal('Sua chave acesso')
        formulario.token.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.texto)

    def test_deve_ter_valor_minimo_aceitado(self):
        formulario = cadastro.FormularioBcash()
        formulario.valor_minimo_aceitado.nome.should.be.equal('valor_minimo_aceitado')
        formulario.valor_minimo_aceitado.ordem.should.be.equal(4)
        formulario.valor_minimo_aceitado.label.should.be.equal(u'Valor mínimo')
        formulario.valor_minimo_aceitado.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.decimal)

    def test_deve_ter_valor_minimo_parcela(self):
        formulario = cadastro.FormularioBcash()
        formulario.valor_minimo_parcela.nome.should.be.equal('valor_minimo_parcela')
        formulario.valor_minimo_parcela.ordem.should.be.equal(5)
        formulario.valor_minimo_parcela.label.should.be.equal(u'Valor mínimo da parcela')
        formulario.valor_minimo_parcela.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.decimal)

    def test_deve_ter_mostrar_parcelamento(self):
        formulario = cadastro.FormularioBcash()
        formulario.mostrar_parcelamento.nome.should.be.equal('mostrar_parcelamento')
        formulario.mostrar_parcelamento.ordem.should.be.equal(6)
        formulario.mostrar_parcelamento.label.should.be.equal(u'Marque para mostrar o parcelamento na listagem e na página do produto.')
        formulario.mostrar_parcelamento.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.boleano)

    def test_deve_ter_maximo_parcelas(self):
        formulario = cadastro.FormularioBcash()
        formulario.maximo_parcelas.nome.should.be.equal('maximo_parcelas')
        formulario.maximo_parcelas.ordem.should.be.equal(7)
        formulario.maximo_parcelas.label.should.be.equal(u'Máximo de parcelas')
        formulario.maximo_parcelas.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.escolha)
        formulario.maximo_parcelas.opcoes.should.be.equal(formulario._PARCELAS)

    def test_deve_ter_parcelas_sem_juros(self):
        formulario = cadastro.FormularioBcash()
        formulario.parcelas_sem_juros.nome.should.be.equal('parcelas_sem_juros')
        formulario.parcelas_sem_juros.ordem.should.be.equal(8)
        formulario.parcelas_sem_juros.label.should.be.equal('Parcelas sem juros')
        formulario.parcelas_sem_juros.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.escolha)
