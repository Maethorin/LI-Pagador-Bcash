# -*- coding: utf-8 -*-
import unittest
from datetime import datetime
from decimal import Decimal
from mock import MagicMock, patch
import mock

from pagador_bcash.reloaded import entidades
from pagador.reloaded import entidades as pagador_entidades


class GerandoMalote(unittest.TestCase):
    def _cria_item(self, indice):
        item = MagicMock()
        item.sku = 'SKU_{}'.format(indice)
        item.nome = 'Nome Item {}'.format(indice)
        item.quantidade = Decimal('1.00')
        item.preco_venda = Decimal('12.30')
        return item

    def test_gera_hash_sem_unicode(self):
        valores_formulario = {'chave2': 'valor2', 'chave1': 1}
        configuracao = {'token': 'TOKEN'}
        pagador_entidades.Pedido._repositorio = MagicMock()
        with patch('pagador_bcash.reloaded.entidades.md5') as md5_mock:
            hexdig = md5_mock.return_value
            hexdig.hexdigest.return_value = 'HASH'
            malote = entidades.Malote()
            malote._gerar_hash(valores_formulario, configuracao).should.be.equal('HASH')
            md5_mock.assert_called_with('chave1=1&chave2=valor2TOKEN')

    def test_gera_hash_com_especial(self):
        valores_formulario = {'chave2': 'colocação', 'chave1': 1}
        configuracao = {'token': 'TOKEN'}
        pagador_entidades.Pedido._repositorio = MagicMock()
        with patch('pagador_bcash.reloaded.entidades.md5') as md5_mock:
            hexdig = md5_mock.return_value
            hexdig.hexdigest.return_value = 'HASH'
            malote = entidades.Malote()
            malote._gerar_hash(valores_formulario, configuracao).should.be.equal('HASH')
            md5_mock.assert_called_with('chave1=1&chave2=coloca%C3%A7%C3%A3oTOKEN')

    def test_gera_hash_com_unicode(self):
        valores_formulario = {'chave2': u'colocação', 'chave1': 1}
        configuracao = {'token': 'TOKEN'}
        pagador_entidades.Pedido._repositorio = MagicMock()
        with patch('pagador_bcash.reloaded.entidades.md5') as md5_mock:
            hexdig = md5_mock.return_value
            hexdig.hexdigest.return_value = 'HASH'
            malote = entidades.Malote()
            malote._gerar_hash(valores_formulario, configuracao).should.be.equal('HASH')
            md5_mock.assert_called_with('chave1=1&chave2=coloca%C3%A7%C3%A3oTOKEN')

    def test_gera_hash_sem_token(self):
        valores_formulario = {'chave2': u'colocação', 'chave1': 1}
        configuracao = {'token': None}
        pagador_entidades.Pedido._repositorio = MagicMock()
        with patch('pagador_bcash.reloaded.entidades.md5') as md5_mock:
            hexdig = md5_mock.return_value
            hexdig.hexdigest.return_value = 'HASH'
            malote = entidades.Malote()
            malote._gerar_hash(valores_formulario, configuracao).should.be.equal('HASH')
            md5_mock.assert_called_with('chave1=1&chave2=coloca%C3%A7%C3%A3o')

    def test_monta_conteudo_com_pessoa_fisica(self):
        pedido_repositorio = MagicMock()
        pedido_repositorio.cliente.email = 'cliente@teste.com'
        pedido_repositorio.cliente.sexo = 'M'
        pedido_repositorio.cliente.data_nascimento = datetime(1970, 2, 23)
        pedido_repositorio.valor_envio = Decimal('15.60')
        pedido_repositorio.valor_desconto = Decimal('10.60')
        pedido_repositorio.valor_subtotal = Decimal('136.40')
        pedido_repositorio.pedido_envio.envio.nome = 'ENVIO'
        pedido_repositorio.endereco_entrega.tipo = 'PF'
        pedido_repositorio.endereco_entrega.nome = 'Cliente Teste'
        pedido_repositorio.endereco_entrega.razao_social = None
        pedido_repositorio.endereco_entrega.cpf = '11122233344'
        pedido_repositorio.endereco_entrega.cnpj = None
        pedido_repositorio.endereco_entrega.rg = '11222333-4'
        pedido_repositorio.endereco_entrega.endereco = 'Rua Teste'
        pedido_repositorio.endereco_entrega.numero = '33'
        pedido_repositorio.endereco_entrega.complemento = None
        pedido_repositorio.endereco_entrega.bairro = 'Bairro'
        pedido_repositorio.endereco_entrega.cidade = 'Cidade'
        pedido_repositorio.endereco_entrega.estado = 'TT'
        pedido_repositorio.endereco_entrega.cep = '22123000'
        pedido_repositorio.telefone_principal = '2122224444'
        pedido_repositorio.telefone_celular = '21999987777'
        pedido_repositorio.items = [self._cria_item(1), self._cria_item(2), self._cria_item(3)]
        pagador_entidades.Pedido._repositorio = MagicMock()
        pagador_entidades.Pedido._repositorio.obter_unico.return_value = pedido_repositorio
        pedido = pagador_entidades.Pedido(23, 234)
        malote = entidades.Malote()
        configuracao = {
            'usuario': 'bcash_user',
            'token': 'TOKEN'
        }
        dados_complementares = {
            'url_retorno': 'http:\\bcash.url_retorno.com',
            'id_plataforma': 'id_plataforma',
            'next_url': 'http:\\urlde.redirect.com'
        }
        malote._gerar_hash = MagicMock(return_value='HASH')
        malote.monta_conteudo(pedido, configuracao, dados_complementares).should.be.equal({
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
            'hash': 'HASH',
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
            'url_retorno': 'http:\\bcash.url_retorno.com/success/?next_url=http:\\urlde.redirect.com&referencia=23',
            'produto_codigo_1': 'SKU_1',
            'produto_descricao_1': 'Nome Item 1',
            'produto_valor_1': '12.30',
            'produto_qtde_1': 1,
            'produto_codigo_2': 'SKU_2',
            'produto_descricao_2': 'Nome Item 2',
            'produto_qtde_2': 1,
            'produto_valor_2': '12.30',
            'produto_codigo_3': 'SKU_3',
            'produto_descricao_3': 'Nome Item 3',
            'produto_qtde_3': 1,
            'produto_valor_3': '12.30',
        })

    def test_monta_conteudo_com_pessoa_juridica(self):
        pedido_repositorio = MagicMock()
        pedido_repositorio.cliente.email = 'cliente@teste.com'
        pedido_repositorio.cliente.sexo = None
        pedido_repositorio.cliente.data_nascimento = None
        pedido_repositorio.valor_envio = Decimal('15.60')
        pedido_repositorio.valor_desconto = Decimal('10.60')
        pedido_repositorio.valor_subtotal = Decimal('136.40')
        pedido_repositorio.pedido_envio.envio.nome = 'ENVIO'
        pedido_repositorio.endereco_entrega.tipo = 'PJ'
        pedido_repositorio.endereco_entrega.razao_social = u'Razão Social Teste S/A'
        pedido_repositorio.endereco_entrega.nome = None
        pedido_repositorio.endereco_entrega.cpf = None
        pedido_repositorio.endereco_entrega.cnpj = '12345678901234'
        pedido_repositorio.endereco_entrega.rg = None
        pedido_repositorio.endereco_entrega.endereco = 'Rua Teste'
        pedido_repositorio.endereco_entrega.numero = '33'
        pedido_repositorio.endereco_entrega.complemento = 'Empresa'
        pedido_repositorio.endereco_entrega.bairro = 'Bairro'
        pedido_repositorio.endereco_entrega.cidade = 'Cidade'
        pedido_repositorio.endereco_entrega.estado = 'TT'
        pedido_repositorio.endereco_entrega.cep = '22123000'
        pedido_repositorio.telefone_principal = '2122224444'
        pedido_repositorio.telefone_celular = '21999987777'
        pedido_repositorio.items = [self._cria_item(1), self._cria_item(2), self._cria_item(3)]
        pagador_entidades.Pedido._repositorio = MagicMock()
        pagador_entidades.Pedido._repositorio.obter_unico.return_value = pedido_repositorio
        pedido = pagador_entidades.Pedido(23, 234)
        malote = entidades.Malote()
        configuracao = {
            'usuario': 'bcash_user',
            'token': 'TOKEN'
        }
        dados_complementares = {
            'url_retorno': 'http:\\bcash.url_retorno.com',
            'id_plataforma': 'id_plataforma',
            'next_url': 'http:\\urlde.redirect.com'
        }
        malote._gerar_hash = MagicMock(return_value='HASH')
        malote.monta_conteudo(pedido, configuracao, dados_complementares).should.be.equal({
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
            'hash': 'HASH',
            'id_pedido': 23,
            'id_plataforma': 'id_plataforma',
            'nome': 'cliente@teste.com',
            'cliente_razao_social': 'Raz\xc3\xa3o Social Teste S/A',
            'redirect': 'true',
            'redirect_time': 30,
            'telefone': '2122224444',
            'tipo_frete': 'ENVIO',
            'tipo_integracao': 'PAD',
            'url_retorno': 'http:\\bcash.url_retorno.com/success/?next_url=http:\\urlde.redirect.com&referencia=23',
            'produto_codigo_1': 'SKU_1',
            'produto_descricao_1': 'Nome Item 1',
            'produto_valor_1': '12.30',
            'produto_qtde_1': 1,
            'produto_codigo_2': 'SKU_2',
            'produto_descricao_2': 'Nome Item 2',
            'produto_qtde_2': 1,
            'produto_valor_2': '12.30',
            'produto_codigo_3': 'SKU_3',
            'produto_descricao_3': 'Nome Item 3',
            'produto_qtde_3': 1,
            'produto_valor_3': '12.30',
        })


class ConfiguracaoMeioPagamento(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ConfiguracaoMeioPagamento, self).__init__(*args, **kwargs)
        self.campos = ['ativo', 'usuario', 'token', 'valor_minimo_aceitado', 'valor_minimo_parcela', 'mostrar_parcelamento', 'maximo_parcelas', 'parcelas_sem_juros']
        self.codigo_gateway = 2

    def test_deve_ter_os_campos_especificos_na_classe(self):
        entidades.ConfiguracaoMeioPagamento._campos.should.be.equal(self.campos)

    def test_deve_ter_codigo_gateway(self):
        entidades.ConfiguracaoMeioPagamento._codigo_gateway.should.be.equal(self.codigo_gateway)

    @mock.patch('pagador_bcash.reloaded.entidades.ConfiguracaoMeioPagamento.preencher_do_gateway', autospec=True)
    def test_deve_preencher_do_gateway_na_inicializacao(self, preencher_mock):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        preencher_mock.assert_called_with(configuracao, self.codigo_gateway, self.campos)

    @mock.patch('pagador_bcash.reloaded.entidades.ConfiguracaoMeioPagamento.preencher_do_gateway', autospec=True)
    def test_deve_definir_formulario_na_inicializacao(self, preencher_mock):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.formulario.should.be.a('pagador_bcash.reloaded.cadastro.FormularioBcash')
