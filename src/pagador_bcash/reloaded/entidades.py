# -*- coding: utf-8 -*-
from urllib import urlencode
from hashlib import md5
from li_common.padroes import cadastro

from pagador.reloaded import entidades


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


class Formulario(cadastro.Formulario):
    PARCELAS = [(x, x) for x in range(1, 24)]
    PARCELAS.insert(0, (24, "Todas"))
    usuario = cadastro.CampoFormulario("usuario", "Seu email no Bcash", requerido=True, tamanho_max=128, ordem=1)
    token = cadastro.CampoFormulario("token", "Sua chave acesso", requerido=True, tamanho_max=128, ordem=2)
    valor_minimo_aceitado = cadastro.CampoFormulario("valor_minimo_aceitado", u"Valor mínimo", requerido=False, decimais=2, ordem=3, tipo=cadastro.TipoDeCampo.decimal, texto_ajuda=u"Informe o valor mínimo para exibir esta forma de pagamento.")
    valor_minimo_parcela = cadastro.CampoFormulario("valor_minimo_parcela", u"Valor mínimo da parcela", requerido=False, decimais=2, ordem=4, tipo=cadastro.TipoDeCampo.decimal)
    mostrar_parcelamento = cadastro.CampoFormulario("mostrar_parcelamento", "Marque para mostrar o parcelamento na listagem e na página do produto.", tipo=cadastro.TipoDeCampo.boleano, requerido=False, ordem=5)
    maximo_parcelas = cadastro.CampoFormulario("maximo_parcelas", "Máximo de parcelas", tipo=cadastro.TipoDeCampo.escolha, requerido=False, ordem=6, texto_ajuda=u"Quantidade máxima de parcelas para esta forma de pagamento.", opcoes=PARCELAS)
    parcelas_sem_juros = cadastro.CampoFormulario("parcelas_sem_juros", "Parcelas sem juros", tipo=cadastro.TipoDeCampo.escolha, requerido=False, ordem=7, texto_ajuda=u"Número de parcelas sem juros para esta forma de pagamento.", opcoes=PARCELAS)


class ConfiguracaoMeioPagamento(entidades.ConfiguracaoMeioPagamento):
    _campos = ['ativo', 'usuario', 'token', 'valor_minimo_aceitado', 'valor_minimo_parcela', 'mostrar_parcelamento', 'maximo_parcelas', 'parcelas_sem_juros']
    _codigo_gateway = 2

    def __init__(self, loja_id):
        super(ConfiguracaoMeioPagamento, self).__init__(loja_id)
        self.preencher_do_gateway(self._codigo_gateway, self._campos)
        self.formulario = Formulario().to_dict()
