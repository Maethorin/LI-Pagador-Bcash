# -*- coding: utf-8 -*-

from pagador.envio.serializacao import EntidadeSerializavel, Atributo


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
