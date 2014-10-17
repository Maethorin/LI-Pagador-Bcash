# -*- coding: utf-8 -*-
from urllib import urlencode
from hashlib import md5

from pagador import settings
from pagador.acesso.externo import FormatoDeEnvio
from pagador.envio.requisicao import Enviar
from pagador_bcash.extensao.envio import Checkout
from pagador_bcash.extensao.seguranca import ParametrosBcash


class EnviarPedido(Enviar):
    def __init__(self, pedido, dados, configuracao_pagamento):
        super(EnviarPedido, self).__init__(pedido, dados, configuracao_pagamento)
        self.exige_autenticacao = False
        self.processa_resposta = True
        self.url = None
        self.grava_identificador = False
        self.formato_de_envio = FormatoDeEnvio.json
        for item in range(0, len(self.pedido.itens.all())):
            Checkout.cria_item_venda(item)

    @property
    def chaves_credenciamento(self):
        return ["usuario", "token"]

    def gerar_dados_de_envio(self):
        parametros = ParametrosBcash("bcash", id=self.pedido.conta_id)
        checkout = Checkout(
            id_plataforma=parametros.id_plataforma,
            tipo_integracao='PAD',
            email_loja=self.configuracao_pagamento.usuario,
            id_pedido=self.pedido.numero,
            email=self.pedido.cliente.email,
            url_retorno="{}/success/?next_url={}&referencia={}".format(settings.BCASH_NOTIFICATION_URL.format(self.pedido.conta_id), self.dados["next_url"], self.pedido.numero),
            redirect='true',
            redirect_time=30,
            frete=self.formatador.formata_decimal(self.pedido.valor_envio),
            tipo_frete=self.pedido.pedido_envio.envio.nome,
            nome=unicode((self.pedido.endereco_entrega.nome or self.pedido.cliente.email)),
            telefone=self.pedido.telefone_principal,
            celular=self.pedido.telefone_celular,
            cep=self.pedido.endereco_entrega.cep,
            endereco=u'{}, {}'.format(self.pedido.endereco_entrega.endereco, self.pedido.endereco_entrega.numero),
            complemento=unicode(self.pedido.endereco_entrega.complemento),
            bairro=unicode(self.pedido.endereco_entrega.bairro),
            cidade=unicode(self.pedido.endereco_entrega.cidade),
            estado=self.pedido.endereco_entrega.estado,
            desconto=self.formatador.formata_decimal(self.pedido.valor_desconto)
        )

        if self.pedido.endereco_entrega.tipo == 'PF':
            checkout.define_valor_de_atributo("cpf", {"cpf": self.pedido.endereco_entrega.cpf})
            checkout.define_valor_de_atributo("rg", {"rg": self.pedido.endereco_entrega.rg})
            checkout.define_valor_de_atributo("sexo", {"sexo": self.pedido.cliente.sexo})
            if self.pedido.cliente.data_nascimento:
                data_nascimento = '{}/{}/{}'.format(self.pedido.cliente.data_nascimento.day, self.pedido.cliente.data_nascimento.month, self.pedido.cliente.data_nascimento.year)
                checkout.define_valor_de_atributo("data_nascimento", {"data_nascimento": data_nascimento})
        elif self.pedido.endereco_entrega.tipo == 'PJ':
            checkout.define_valor_de_atributo("cliente_razao_social", {"cliente_razao_social": unicode(self.pedido.endereco_entrega.razao_social)})
            checkout.define_valor_de_atributo("cliente_cnpj", {"cliente_cnpj": self.pedido.endereco_entrega.cnpj})

        for indice, item in enumerate(self.pedido.itens.all()):
            self.define_valor_de_atributo_de_item(checkout, "codigo", indice, unicode(item.sku[:100]))
            self.define_valor_de_atributo_de_item(checkout, "descricao", indice, unicode(item.nome[:255]))
            self.define_valor_de_atributo_de_item(checkout, "qtde", indice, self.formatador.formata_decimal(item.quantidade, como_int=True))
            self.define_valor_de_atributo_de_item(checkout, "valor", indice, self.formatador.formata_decimal(item.preco_venda))

        hasheado = self.gerar_hash(checkout.to_dict())
        checkout.define_valor_de_atributo("hash", {"hash": hasheado})
        return checkout.to_dict()

    def define_valor_de_atributo_de_item(self, checkout, atributo, indice, valor):
        indice += 1
        nome = "produto_{}_{}".format(atributo, indice)
        atributo = "produto_{}_{}".format(atributo, indice)
        checkout.define_valor_de_atributo(nome, {atributo.lower(): valor})

    def obter_situacao_do_pedido(self, status_requisicao):
        return None

    def processar_resposta(self, resposta):
        return {"content": {"dados": self.gerar_dados_de_envio()}, "status": 200}

    def gerar_hash(self, valores_formulario):
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