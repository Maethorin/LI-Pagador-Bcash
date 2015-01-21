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

    def _cria_item_venda(self, retorno, indice, codigo, descricao, qtde, valor):
        indice += 1
        retorno['produto_codigo_{}'.format(indice)] = codigo
        retorno['produto_descricao_{}'.format(indice)] = descricao
        retorno['produto_qtde_{}'.format(indice)] = qtde
        retorno['produto_valor_{}'.format(indice)] = valor

    def _gerar_hash(self, valores_formulario, configuracao):
        em_ordem = [(k, valores_formulario[k]) for k in sorted(valores_formulario.keys())]
        codificado = []
        for k, v in em_ordem:
            if isinstance(v, unicode):
                v = v.encode('utf-8')
            codificado.append((k, v))
        if configuracao['token']:
            token = configuracao['token'].strip()
        else:
            token = ''
        tudo = '{}{}'.format(urlencode(codificado), token)
        return md5(tudo).hexdigest()

    def monta_conteudo(self, pedido, configuracao=None, dados_complementares=None):
        retorno = {
            'id_plataforma': dados_complementares['id_plataforma'],
            'tipo_integracao': 'PAD',
            'email_loja': configuracao['usuario'],
            'id_pedido': pedido.numero,
            'email': pedido.cliente['email'],
            'url_retorno': '{}/success/?next_url={}&referencia={}'.format(dados_complementares["url_retorno"], dados_complementares["next_url"], pedido.numero),
            'redirect': 'true',
            'redirect_time': 30,
            'frete': self.formatador.formata_decimal(self.valor_envio(pedido)),
            'tipo_frete': pedido.forma_envio,
            'nome': self.formatador.trata_unicode_com_limite((pedido.endereco_entrega['nome'] or pedido.cliente['email'])),
            'telefone': pedido.telefone_principal,
            'celular': pedido.telefone_celular,
            'cep': pedido.endereco_entrega['cep'],
            'endereco': u'{}, {}'.format(pedido.endereco_entrega['endereco'], pedido.endereco_entrega['numero']),
            'complemento': self.formatador.trata_unicode_com_limite(pedido.endereco_entrega['complemento']),
            'bairro': self.formatador.trata_unicode_com_limite(pedido.endereco_entrega['bairro']),
            'cidade': self.formatador.trata_unicode_com_limite(pedido.endereco_entrega['cidade']),
            'estado': pedido.endereco_entrega['estado'],
            'desconto': self.formatador.formata_decimal(self.valor_desconto(pedido)),
        }
        if pedido.endereco_entrega['tipo'] == 'PF':
            retorno['cpf'] = pedido.endereco_entrega['cpf']
            retorno['rg'] = pedido.endereco_entrega['rg']
            retorno['sexo'] = pedido.cliente['sexo']
            if pedido.cliente['data_nascimento']:
                retorno['data_nascimento'] = pedido.cliente['data_nascimento'].strftime('%d/%m/%Y')
        if pedido.endereco_entrega['tipo'] == 'PJ':
            retorno['cliente_razao_social'] = self.formatador.trata_unicode_com_limite(pedido.endereco_entrega['razao_social'])
            retorno['cliente_cnpj'] = pedido.endereco_entrega['cnpj']

        for indice, item in enumerate(pedido.items):
            self._cria_item_venda(
                retorno,
                indice,
                codigo=self.formatador.trata_unicode_com_limite(item['sku'], 100),
                descricao=self.formatador.trata_unicode_com_limite(item['nome'], 255),
                qtde=self.formatador.formata_decimal(item['quantidade'], como_int=True),
                valor=self.formatador.formata_decimal(item['preco_venda'])
            )

        retorno['hash'] = self._gerar_hash(retorno, configuracao)
        return retorno
