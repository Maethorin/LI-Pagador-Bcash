# -*- coding: utf-8 -*-
import unittest
from datetime import datetime
from decimal import Decimal

from mock import MagicMock, patch
import mock

from pagador_bcash import entidades
from pagador import entidades as pagador_entidades


def gerar_hash_mock(self=None):
    if self:
        self.hash = 'HAAAAASHHHHHHHHHH'
    return 'HAAAAASHHHHHHHHHH'


class GerandoMalote(unittest.TestCase):

    def _cria_item(self, indice):
        item = MagicMock()
        item.sku = 'SKU_{}'.format(indice)
        item.nome = 'Nome Item {}'.format(indice)
        item.quantidade = Decimal('1.00')
        item.preco_venda = Decimal('12.30')
        return item

    def test_gerar_hash_sem_unicode(self):
        configuracao = mock.MagicMock(token='TOKEN')
        pagador_entidades.Pedido._repositorio = MagicMock()
        with patch('pagador_bcash.entidades.md5') as md5_mock:
            hexdig = md5_mock.return_value
            hexdig.hexdigest.return_value = 'HASH'
            malote = entidades.Malote(configuracao)
            malote._gerar_hash()
            malote.hash.should.be.equal('HASH')
            md5_mock.assert_called_with('bairro=None&celular=None&cep=None&cidade=None&complemento=None&desconto=None&email=None&email_loja=None&endereco=None&estado=None&frete=None&id_pedido=None&id_plataforma=None&nome=None&redirect=None&redirect_time=None&telefone=None&tipo_frete=None&tipo_integracao=None&url_aviso=None&url_retorno=NoneTOKEN')

    def test_gerar_hash_com_especial(self):
        configuracao = mock.MagicMock(token='TOKEN')
        pagador_entidades.Pedido._repositorio = MagicMock()
        with patch('pagador_bcash.entidades.md5') as md5_mock:
            hexdig = md5_mock.return_value
            hexdig.hexdigest.return_value = 'HASH'
            malote = entidades.Malote(configuracao)
            malote.bairro = 'São Gonçalo'
            malote._gerar_hash()
            md5_mock.assert_called_with('bairro=S%C3%A3o+Gon%C3%A7alo&celular=None&cep=None&cidade=None&complemento=None&desconto=None&email=None&email_loja=None&endereco=None&estado=None&frete=None&id_pedido=None&id_plataforma=None&nome=None&redirect=None&redirect_time=None&telefone=None&tipo_frete=None&tipo_integracao=None&url_aviso=None&url_retorno=NoneTOKEN')

    def test_gerar_hash_com_unicode(self):
        configuracao = mock.MagicMock(token='TOKEN')
        pagador_entidades.Pedido._repositorio = MagicMock()
        pagador_entidades.Pedido._repositorio = MagicMock()
        with patch('pagador_bcash.entidades.md5') as md5_mock:
            hexdig = md5_mock.return_value
            hexdig.hexdigest.return_value = 'HASH'
            malote = entidades.Malote(configuracao)
            malote.bairro = u'São Gonçalo'
            malote._gerar_hash()
            md5_mock.assert_called_with('bairro=S%C3%A3o+Gon%C3%A7alo&celular=None&cep=None&cidade=None&complemento=None&desconto=None&email=None&email_loja=None&endereco=None&estado=None&frete=None&id_pedido=None&id_plataforma=None&nome=None&redirect=None&redirect_time=None&telefone=None&tipo_frete=None&tipo_integracao=None&url_aviso=None&url_retorno=NoneTOKEN')

    def test_gerar_hash_sem_token(self):
        configuracao = mock.MagicMock(token=None)
        pagador_entidades.Pedido._repositorio = MagicMock()
        with patch('pagador_bcash.entidades.md5') as md5_mock:
            hexdig = md5_mock.return_value
            hexdig.hexdigest.return_value = 'HASH'
            malote = entidades.Malote(configuracao)
            malote._gerar_hash()
            md5_mock.assert_called_with('bairro=None&celular=None&cep=None&cidade=None&complemento=None&desconto=None&email=None&email_loja=None&endereco=None&estado=None&frete=None&id_pedido=None&id_plataforma=None&nome=None&redirect=None&redirect_time=None&telefone=None&tipo_frete=None&tipo_integracao=None&url_aviso=None&url_retorno=None')

    @mock.patch('pagador_bcash.entidades.Malote._gerar_hash', gerar_hash_mock)
    @mock.patch('pagador.repositorios.PedidoRepositorio')
    @mock.patch('pagador_bcash.entidades.settings')
    def test_monta_conteudo_com_pessoa_fisica(self, settings_mock, pedido_repo_mock):
        dados_repositorio = {
            'numero': 23,
            'loja_id': 234,
            'cliente': {'email': 'cliente@teste.com', 'sexo': 'M', 'data_nascimento': datetime(1970, 2, 23)},
            '_valor_envio': 15.60,
            '_valor_desconto': 10.60,
            '_valor_subtotal': 136.40,
            'forma_envio': 'ENVIO',
            'endereco_entrega': {
                'tipo': 'PF',
                'nome': 'Cliente Teste',
                'razao_social': None,
                'cpf': '11122233344', 'rg': '11222333-4',
                'cnpj': None,
                'cep': '22123000',
                'endereco': 'Rua Teste', 'numero': '33', 'complemento': None,
                'bairro': 'Bairro', 'cidade': 'Cidade', 'estado': 'TT'
            },
            'telefone_principal': '2122224444',
            'telefone_celular': '21999987777',
            'itens_no_pedido': [
                {'sku': 'SKU_1', 'nome': 'Item Nome 1', 'quantidade': 1.00, 'preco_venda': 12.30},
                {'sku': 'SKU_2', 'nome': 'Item Nome 2', 'quantidade': 1.00, 'preco_venda': 12.30},
                {'sku': 'SKU_3', 'nome': 'Item Nome 3', 'quantidade': 1.00, 'preco_venda': 12.30},
            ]
        }
        pedido_repo_mock.return_value.obter_com_numero.return_value = dados_repositorio
        pedido = pagador_entidades.Pedido(23, 234)
        configuracao = mock.MagicMock(**{
            'usuario': 'bcash_user',
            'token': 'TOKEN',
            'loja_id': 234
        })
        parametros = {'id_plataforma': 'id_plataforma'}
        settings_mock.BCASH_NOTIFICATION_URL = 'http://bcash.url_retorno.com/{}'
        dados = {
            'next_url': 'http://urlde.redirect.com'
        }
        malote = entidades.Malote(configuracao)
        malote.monta_conteudo(pedido, parametros, dados)
        malote.to_dict().should.be.equal({
            'bairro': 'Bairro',
            'celular': '21999987777',
            'cep': '22123000',
            'cidade': 'Cidade',
            'complemento': '',
            'cpf': '11122233344',
            'data_nascimento': '23/02/1970',
            'desconto': '10.60',
            'email': 'cliente@teste.com',
            'email_loja': 'bcash_user',
            'endereco': u'Rua Teste, 33',
            'estado': 'TT',
            'frete': '15.60',
            'hash': gerar_hash_mock(),
            'id_pedido': 23,
            'id_plataforma': 'id_plataforma',
            'nome': 'Cliente Teste',
            'redirect': 'true',
            'redirect_time': 30,
            'rg': '11222333-4',
            'sexo': 'M',
            'telefone': '2122224444',
            'tipo_frete': 'ENVIO',
            'tipo_integracao': 'PAD',
            'url_aviso': 'http://bcash.url_retorno.com/234/notificacao?referencia=23',
            'url_retorno': 'http://bcash.url_retorno.com/234/resultado?next_url=http://urlde.redirect.com&referencia=23',
            'produto_codigo_1': 'SKU_1',
            'produto_descricao_1': 'Item Nome 1',
            'produto_valor_1': '12.30',
            'produto_qtde_1': 1,
            'produto_codigo_2': 'SKU_2',
            'produto_descricao_2': 'Item Nome 2',
            'produto_qtde_2': 1,
            'produto_valor_2': '12.30',
            'produto_codigo_3': 'SKU_3',
            'produto_descricao_3': 'Item Nome 3',
            'produto_qtde_3': 1,
            'produto_valor_3': '12.30',
        })

    @mock.patch('pagador_bcash.entidades.Malote._gerar_hash', gerar_hash_mock)
    @mock.patch('pagador.repositorios.PedidoRepositorio', mock.MagicMock())
    @mock.patch('pagador_bcash.entidades.settings')
    def test_monta_conteudo_com_pessoa_juridica(self, settings_mock):
        dados_repositorio = {
            'numero': 23,
            'loja_id': 234,
            'cliente': {'email': 'cliente@teste.com', 'sexo': 'M', 'data_nascimento': datetime(1970, 2, 23)},
            '_valor_envio': 15.60,
            '_valor_desconto': 10.60,
            '_valor_subtotal': 136.40,
            'forma_envio': 'ENVIO',
            'endereco_entrega': {
                'tipo': 'PJ',
                'nome': None,
                'razao_social': u'Razão Social Teste S/A',
                'cpf': None,
                'rg': None,
                'cnpj': '12345678901234',
                'cep': '22123000',
                'endereco': 'Rua Teste', 'numero': '33', 'complemento': 'Empresa',
                'bairro': 'Bairro', 'cidade': 'Cidade', 'estado': 'TT'
            },
            'telefone_principal': '2122224444',
            'telefone_celular': '21999987777',
            'itens_no_pedido': [
                {'sku': 'SKU_1', 'nome': 'Item Nome 1', 'quantidade': 1.00, 'preco_venda': 12.30},
                {'sku': 'SKU_2', 'nome': 'Item Nome 2', 'quantidade': 1.00, 'preco_venda': 12.30},
                {'sku': 'SKU_3', 'nome': 'Item Nome 3', 'quantidade': 1.00, 'preco_venda': 12.30},
            ]
        }
        pedido = pagador_entidades.Pedido(23, 234)
        pedido.preencher_com(dados_repositorio)
        configuracao = mock.MagicMock(**{
            'usuario': 'bcash_user',
            'token': 'TOKEN',
            'loja_id': 234
        })
        parametros = {'id_plataforma': 'id_plataforma'}
        settings_mock.BCASH_NOTIFICATION_URL = 'http://bcash.url_retorno.com/{}'
        dados = {
            'next_url': 'http://urlde.redirect.com'
        }
        malote = entidades.Malote(configuracao)
        malote.monta_conteudo(pedido, parametros, dados)
        malote.to_dict().should.be.equal({
            'bairro': 'Bairro',
            'celular': '21999987777',
            'cep': '22123000',
            'cidade': 'Cidade',
            'complemento': 'Empresa',
            'cliente_cnpj': '12345678901234',
            'desconto': '10.60',
            'email': 'cliente@teste.com',
            'email_loja': 'bcash_user', 'endereco': u'Rua Teste, 33',
            'estado': 'TT',
            'frete': '15.60',
            'hash': gerar_hash_mock(),
            'id_pedido': 23,
            'id_plataforma': 'id_plataforma',
            'nome': 'cliente@teste.com',
            'cliente_razao_social': 'Raz\xc3\xa3o Social Teste S/A',
            'redirect': 'true',
            'redirect_time': 30,
            'telefone': '2122224444',
            'tipo_frete': 'ENVIO',
            'tipo_integracao': 'PAD',
            'url_retorno': 'http://bcash.url_retorno.com/234/resultado?next_url=http://urlde.redirect.com&referencia=23',
            'url_aviso': 'http://bcash.url_retorno.com/234/notificacao?referencia=23',
            'produto_codigo_1': 'SKU_1',
            'produto_descricao_1': 'Item Nome 1',
            'produto_valor_1': '12.30',
            'produto_qtde_1': 1,
            'produto_codigo_2': 'SKU_2',
            'produto_descricao_2': 'Item Nome 2',
            'produto_qtde_2': 1,
            'produto_valor_2': '12.30',
            'produto_codigo_3': 'SKU_3',
            'produto_descricao_3': 'Item Nome 3',
            'produto_qtde_3': 1,
            'produto_valor_3': '12.30',
        })


class BcashConfiguracaoMeioPagamento(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BcashConfiguracaoMeioPagamento, self).__init__(*args, **kwargs)
        self.campos = ['ativo', 'usuario', 'token', 'valor_minimo_aceitado', 'valor_minimo_parcela', 'mostrar_parcelamento', 'maximo_parcelas', 'parcelas_sem_juros']
        self.codigo_gateway = 2

    @mock.patch('pagador_bcash.entidades.ConfiguracaoMeioPagamento.preencher_gateway', mock.MagicMock())
    def test_deve_ter_os_campos_especificos_na_classe(self):
        entidades.ConfiguracaoMeioPagamento(234).campos.should.be.equal(self.campos)

    @mock.patch('pagador_bcash.entidades.ConfiguracaoMeioPagamento.preencher_gateway', mock.MagicMock())
    def test_deve_ter_codigo_gateway(self):
        entidades.ConfiguracaoMeioPagamento(234).codigo_gateway.should.be.equal(self.codigo_gateway)

    @mock.patch('pagador_bcash.entidades.ConfiguracaoMeioPagamento.preencher_gateway', autospec=True)
    def test_deve_preencher_gateway_na_inicializacao(self, preencher_mock):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        preencher_mock.assert_called_with(configuracao, self.codigo_gateway, self.campos)

    @mock.patch('pagador_bcash.entidades.ConfiguracaoMeioPagamento.preencher_gateway', mock.MagicMock())
    def test_deve_definir_formulario_na_inicializacao(self):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.formulario.should.be.a('pagador_bcash.cadastro.FormularioBcash')

    @mock.patch('pagador_bcash.entidades.ConfiguracaoMeioPagamento.preencher_gateway', mock.MagicMock())
    def test_deve_ser_aplicacao(self):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.eh_aplicacao.should.be.falsy
