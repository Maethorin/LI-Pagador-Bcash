# -*- coding: utf-8 -*-

from pagador.envio.serializacao import EntidadeSerializavel, Atributo


teste = {'tipo_frete': u'SEDEX', 'data_nascimento': '12/3/1978', 'celular': u'11999999999', 'id_plataforma': 519, 'complemento': u'2 andar', 'tipo_integracao': 'PAD', 'nome': u'Teste Loja Integrada', 'frete': '14.00', 'rg': u'111111111-1', 'email_loja': u'marcio.duarte@lojaintegrada.com.br', 'email': u'marcio.duarte+testeloja@lojaintegrada.com.br', 'redirect': 'true', 'produto_descricao_1': u'Lumin\xe1ria Embutir para 2 L\xe2mpadas sem abas', 'hash': 'a640934d9ee86a0282df86627b4c70bc', 'bairro': u'Botafogo', 'url_retorno': 'http://www.custompaper.com.br/bcash/notificacao', 'sexo': u'm', 'redirect_time': 30, 'produto_codigo_1': 574773, 'produto_qtde_1': 1, 'cep': u'22250040', 'estado': u'RJ', 'produto_valor_1': '500.00', 'cidade': u'Rio de Janeiro', 'cpf': u'16055744651', 'id_pedido': 368073, 'endereco': u'Praia de Botafogo, 518'}


class Checkout(EntidadeSerializavel):
    _atributos = ["id_plataforma", "tipo_integracao", "email_loja", "email", "url_retorno", "redirect", "redirect_time", "id_pedido", "frete", "tipo_frete", "cpf", "rg",
                  "cliente_razao_social", "cliente_cnpj", "data_nascimento", "sexo", "nome", "telefone", "celular", "cep", "endereco", "complemento", "bairro", "cidade", "estado",
                  "desconto", "hash"]
    atributos = [Atributo(atributo) for atributo in _atributos]

    @classmethod
    def cria_item_venda(cls, indice):
        indice += 1
        cls.atributos.append(Atributo("produto_codigo_{}".format(indice)))
        cls.atributos.append(Atributo("produto_descricao_{}".format(indice)))
        cls.atributos.append(Atributo("produto_qtde_{}".format(indice)))
        cls.atributos.append(Atributo("produto_valor_{}".format(indice)))
