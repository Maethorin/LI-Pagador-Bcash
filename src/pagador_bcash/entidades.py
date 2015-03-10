# -*- coding: utf-8 -*-
from urllib import urlencode
from hashlib import md5

from pagador import settings, entidades
from pagador_bcash import cadastro


CODIGO_GATEWAY = 2


class Malote(entidades.Malote):
    def __init__(self, configuracao):
        super(Malote, self).__init__(configuracao)
        self.id_plataforma = None
        self.tipo_integracao = None
        self.email_loja = None
        self.id_pedido = None
        self.email = None
        self.url_retorno = None
        self.url_aviso = None
        self.redirect = None
        self.redirect_time = None
        self.frete = None
        self.tipo_frete = None
        self.nome = None
        self.telefone = None
        self.celular = None
        self.cep = None
        self.endereco = None
        self.complemento = None
        self.bairro = None
        self.cidade = None
        self.estado = None
        self.desconto = None

    def _cria_item_venda(self, indice, codigo, descricao, qtde, valor):
        indice += 1
        setattr(self, 'produto_codigo_{}'.format(indice), codigo)
        setattr(self, 'produto_descricao_{}'.format(indice), descricao)
        setattr(self, 'produto_qtde_{}'.format(indice), qtde)
        setattr(self, 'produto_valor_{}'.format(indice), valor)

    def _gerar_hash(self):
        valores_formulario = self.to_dict()
        em_ordem = [(k, valores_formulario[k]) for k in sorted(valores_formulario.keys())]
        codificado = []
        for k, v in em_ordem:
            if isinstance(v, unicode):
                v = v.encode('utf-8')
            codificado.append((k, v))
        if self.configuracao.token:
            token = self.configuracao.token.strip()
        else:
            token = ''
        tudo = '{}{}'.format(urlencode(codificado), token)
        self.hash = md5(tudo).hexdigest()

    def monta_conteudo(self, pedido, parametros_contrato=None, dados=None):
        self.id_plataforma = parametros_contrato['id_plataforma']
        self.tipo_integracao = 'PAD'
        self.email_loja = self.configuracao.usuario
        self.id_pedido = pedido.numero
        self.email = pedido.cliente['email']
        self.url_retorno = '{}/resultado?next_url={}&referencia={}'.format(settings.BCASH_NOTIFICATION_URL.format(self.configuracao.loja_id), dados["next_url"], pedido.numero)
        self.url_aviso = '{}/notificacao?referencia={}'.format(settings.BCASH_NOTIFICATION_URL.format(self.configuracao.loja_id), dados["next_url"], pedido.numero)
        self.redirect = 'true'
        self.redirect_time = 30
        self.frete = self.formatador.formata_decimal(pedido.valor_envio)
        self.tipo_frete = pedido.forma_envio
        self.nome = self.formatador.trata_unicode_com_limite((pedido.endereco_entrega['nome'] or pedido.cliente['email']))
        self.telefone = pedido.telefone_principal or ''
        self.celular = pedido.telefone_celular or ''
        self.cep = pedido.endereco_entrega['cep']
        self.endereco = u'{}, {}'.format(pedido.endereco_entrega['endereco'], pedido.endereco_entrega['numero'])
        self.complemento = self.formatador.trata_unicode_com_limite(pedido.endereco_entrega['complemento'])
        self.bairro = self.formatador.trata_unicode_com_limite(pedido.endereco_entrega['bairro'])
        self.cidade = self.formatador.trata_unicode_com_limite(pedido.endereco_entrega['cidade'])
        self.estado = pedido.endereco_entrega['estado']
        self.desconto = self.formatador.formata_decimal(pedido.valor_desconto)
        if pedido.endereco_entrega['tipo'] == 'PF':
            setattr(self, 'cpf', pedido.endereco_entrega['cpf'])
            setattr(self, 'rg', pedido.endereco_entrega['rg'])
            setattr(self, 'sexo', pedido.cliente['sexo'])
            if pedido.cliente['data_nascimento']:
                setattr(self, 'data_nascimento', pedido.cliente['data_nascimento'].strftime('%d/%m/%Y'))
        if pedido.endereco_entrega['tipo'] == 'PJ':
            setattr(self, 'cliente_razao_social', self.formatador.trata_unicode_com_limite(pedido.endereco_entrega['razao_social']))
            setattr(self, 'cliente_cnpj', pedido.endereco_entrega['cnpj'])

        for indice, item in enumerate(pedido.itens):
            self._cria_item_venda(
                indice,
                codigo=self.formatador.trata_unicode_com_limite(item.sku, 100),
                descricao=self.formatador.trata_unicode_com_limite(item.nome, 255),
                qtde=self.formatador.formata_decimal(item.quantidade, como_int=True),
                valor=self.formatador.formata_decimal(item.preco_venda)
            )
        self._gerar_hash()


class ConfiguracaoMeioPagamento(entidades.ConfiguracaoMeioPagamento):
    _campos = ['ativo', 'usuario', 'token', 'valor_minimo_aceitado', 'valor_minimo_parcela', 'mostrar_parcelamento', 'maximo_parcelas', 'parcelas_sem_juros']
    _codigo_gateway = CODIGO_GATEWAY

    def __init__(self, loja_id, codigo_pagamento=None):
        super(ConfiguracaoMeioPagamento, self).__init__(loja_id, codigo_pagamento)
        self.preencher_gateway(self._codigo_gateway, self._campos)
        self.formulario = cadastro.FormularioBcash()
