# -*- coding: utf-8 -*-
from urllib import urlencode
from hashlib import md5

from pagador.reloaded import entidades


class Entrega(entidades.Entrega):
    def __init__(self, numero_pedido, id_loja, meio_de_pagamento):
        super(Entrega, self).__init__(numero_pedido, id_loja, meio_de_pagamento)


class Malote(entidades.Malote):
    def __init__(self):
        super(Malote, self).__init__()
        self.id_plataforma = None
        self.tipo_integracao = None
        self.email_loja = None
        self.email = None
        self.url_retorno = None
        self.redirect = None
        self.redirect_time = None
        self.id_pedido = None
        self.frete = None
        self.tipo_frete = None
        self.cpf = None
        self.rg = None
        self.cliente_razao_social = None
        self.cliente_cnpj = None
        self.data_nascimento = None
        self.sexo = None
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
        self.hash = None

    def cria_item_venda(self, indice, codigo, descricao, qtde, valor):
        indice += 1
        setattr(self, "produto_codigo_{}".format(indice), codigo)
        setattr(self, "produto_descricao_{}".format(indice), descricao)
        setattr(self, "produto_qtde_{}".format(indice), qtde)
        setattr(self, "produto_valor_{}".format(indice), valor)

    def _gerar_hash(self, valores_formulario):
        em_ordem = [(k, valores_formulario[k]) for k in sorted(valores_formulario.keys())]
        codificado = []
        for k, v in em_ordem:
            if isinstance(v, unicode):
                v = v.encode('utf-8')
            if isinstance(k, unicode):
                k = k.encode('utf-8')
            codificado.append((k, v))
        if self.configuracao_pagamento.token:
            token = self.configuracao_pagamento.token.strip()
        else:
            token = ''
        tudo = "%s%s" % (urlencode(codificado), token)
        return md5(tudo).hexdigest()

    def monta_conteudo(self, pedido, dados_complementares):
        # parametros = ParametrosBcash("bcash", id=self.pedido.conta_id)
        self.id_plataforma = 'parametros.id_plataforma'
        self.tipo_integracao = 'PAD',
        self.email_loja = self.configuracao_pagamento.usuario,
        self.id_pedido = pedido.numero,
        self.email = pedido.cliente.email,
        self.url_retorno = '{}/success/?next_url={}&referencia={}'.format(settings.BCASH_NOTIFICATION_URL.format(pedido.conta_id), dados_complementares["next_url"], pedido.numero),
        self.redirect = 'true',
        self.redirect_time = 30,
        self.frete = self.formatador.formata_decimal(self.valor_envio),
        self.tipo_frete = pedido.pedido_envio.envio.nome,
        self.nome = self.formatador.trata_unicode_com_limite((pedido.endereco_entrega.nome or pedido.cliente.email)),
        self.telefone = pedido.telefone_principal,
        self.celular = pedido.telefone_celular,
        self.cep = pedido.endereco_entrega.cep,
        self.endereco = u'{}, {}'.format(pedido.endereco_entrega.endereco, pedido.endereco_entrega.numero),
        self.complemento = self.formatador.trata_unicode_com_limite(pedido.endereco_entrega.complemento),
        self.bairro = self.formatador.trata_unicode_com_limite(pedido.endereco_entrega.bairro),
        self.cidade = self.formatador.trata_unicode_com_limite(pedido.endereco_entrega.cidade),
        self.estado = pedido.endereco_entrega.estado,
        self.desconto = self.formatador.formata_decimal(self.valor_desconto)

        if pedido.endereco_entrega.tipo == 'PF':
            self.cpf = pedido.endereco_entrega.cpf
            self.rg = pedido.endereco_entrega.rg
            self.sexo = pedido.cliente.sexo
            if pedido.cliente.data_nascimento:
                self.data_nascimento = '{}/{}/{}'.format(pedido.cliente.data_nascimento.day, pedido.cliente.data_nascimento.month, pedido.cliente.data_nascimento.year)
        elif pedido.endereco_entrega.tipo == 'PJ':
            self.cliente_razao_social = self.formatador.trata_unicode_com_limite(pedido.endereco_entrega.razao_social)
            self.cliente_cnpj = pedido.endereco_entrega.cnpj

        for indice, item in enumerate(pedido.itens.all()):
            self.cria_item_venda(
                indice,
                codigo=self.formatador.trata_unicode_com_limite(item.sku, 100),
                descricao=self.formatador.trata_unicode_com_limite(item.nome, 255),
                qtde=self.formatador.formata_decimal(item.quantidade, como_int=True),
                valor=self.formatador.formata_decimal(item.preco_venda)
            )

        self.hash = self._gerar_hash(self.to_dict())
