# -*- coding: utf-8 -*-
import unittest
from pagador_bcash.reloaded import entidades


class SerializandoMalote(unittest.TestCase):
    def _cria_item_de_venda(self, malote, indice):
        malote.cria_item_venda(indice, 'produto_codigo_{}'.format(indice), 'produto_descricao_{}'.format(indice), 'produto_qtde_{}'.format(indice), 'produto_valor_{}'.format(indice))

    def test_retorna_dicionario_com_valores_preenchidos(self):
        malote = entidades.Malote()
        malote.id_plataforma = 'plataforma'
        malote.tipo_integracao = 'tipo_integracao'
        malote.email_loja = 'email_loja'
        malote.email = 'email'
        malote.url_retorno = 'url_retorno'
        malote.redirect = 'redirect'
        malote.redirect_time = 'redirect_time'
        malote.id_pedido = 'id_pedido'
        malote.frete = 'frete'
        malote.tipo_frete = 'tipo_frete'
        malote.cpf = 'cpf'
        malote.rg = 'rg'
        malote.cliente_razao_social = 'cliente_razao_social'
        malote.cliente_cnpj = 'cliente_cnpj'
        malote.data_nascimento = 'data_nascimento'
        malote.sexo = 'sexo'
        malote.nome = 'nome'
        malote.telefone = 'telefone'
        malote.celular = '2199999999'
        malote.cep = '22250040'
        malote.endereco = 'endereco'
        malote.complemento = 'complemento'
        malote.bairro = 'bairro'
        malote.cidade = 'cidade'
        malote.estado = 'estado'
        malote.desconto = 'desconto'
        malote.hash = 'hash'
        self._cria_item_de_venda(malote, 1)
        self._cria_item_de_venda(malote, 2)
        malote.to_dict().should.be.equal(
            {
                'bairro': 'bairro',
                'celular': '2199999999',
                'cep': '22250040',
                'cidade': 'cidade',
                'cliente_cnpj': 'cliente_cnpj',
                'cliente_razao_social': 'cliente_razao_social',
                'complemento': 'complemento',
                'cpf': 'cpf',
                'data_nascimento': 'data_nascimento',
                'desconto': 'desconto',
                'email': 'email',
                'email_loja': 'email_loja',
                'endereco': 'endereco',
                'estado': 'estado',
                'frete': 'frete',
                'hash': 'hash',
                'id_pedido': 'id_pedido',
                'id_plataforma': 'plataforma',
                'nome': 'nome',
                'redirect': 'redirect',
                'redirect_time': 'redirect_time',
                'rg': 'rg',
                'sexo': 'sexo',
                'telefone': 'telefone',
                'tipo_frete': 'tipo_frete',
                'tipo_integracao': 'tipo_integracao',
                'url_retorno': 'url_retorno',
                'produto_codigo_2': 'produto_codigo_1',
                'produto_codigo_3': 'produto_codigo_2',
                'produto_descricao_2': 'produto_descricao_1',
                'produto_descricao_3': 'produto_descricao_2',
                'produto_qtde_2': 'produto_qtde_1',
                'produto_qtde_3': 'produto_qtde_2',
                'produto_valor_2': 'produto_valor_1',
                'produto_valor_3': 'produto_valor_2'
            }
        )