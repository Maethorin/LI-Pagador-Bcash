# -*- coding: utf-8 -*-
import os

from pagador.configuracao.cadastro import CampoFormulario, FormularioBase, CadastroBase, SelecaoBase, TipoDeCampo, caminho_para_template
from pagador.configuracao.cliente import Script, TipoScript


def caminho_arquivo_template(arquivo):
    return caminho_para_template(arquivo, meio_pagamento='pagamento_digital')


class MeioPagamentoCadastro(CadastroBase):
    @property
    def descricao_para_lojista(self):
        script = Script(tipo=TipoScript.html, nome="descricao")
        script.adiciona_linha('<p>Conheça <a href="http://bcash.com.br/para-quem-vende/" target="_blank">Bcash</a>!</p>')
        script.adiciona_linha('<p>Siga os seguintes passos para configurar:</p>')
        script.adiciona_linha('<p>1. Preencha o campo Seu email no Bcash com seu email de cadastro no Bcash;</p>')
        script.adiciona_linha('<p>2. Entre no <a href="https://www.bcash.com.br" target="_blank">Bcash</a>, clique em <strong>Ferramentas -> Código de Integração</strong> e copie <strong>Sua Chave acesso</strong> e cole no campo <strong>Sua Chave acesso</strong>.')
        return script

    @property
    def registro(self):
        script = Script(tipo=TipoScript.html, nome="registro")
        script.adiciona_linha(u'Ainda não tem conta no Bcash?')
        script.adiciona_linha('<a href="https://www.bcash.com.br/criar-conta-vendedor/" title="Criar conta Bcash" class="btn btn-info btn-xs" target="_blank">cadastre-se</a>')
        return script

    def to_dict(self):
        return {
            "html": [
                self.descricao_para_lojista.to_dict(),
                self.registro.to_dict()
            ]
        }

PARCELAS = [(x, x) for x in range(1, 25)]
PARCELAS.insert(0, (24, "Todas"))


class Formulario(FormularioBase):
    usuario = CampoFormulario("usuario", "Seu email no Bcash", requerido=True, tamanho_max=128, ordem=1)
    token = CampoFormulario("token", "Sua chave acesso", requerido=True, tamanho_max=128, ordem=2)
    valor_minimo_aceitado = CampoFormulario("valor_minimo_aceitado", u"Valor mínimo", requerido=False, decimais=2, ordem=3, tipo=TipoDeCampo.decimal, texto_ajuda=u"Informe o valor mínimo para exibir esta forma de pagamento.")
    valor_minimo_parcela = CampoFormulario("valor_minimo_parcela", u"Valor mínimo da parcela", requerido=False, decimais=2, ordem=4, tipo=TipoDeCampo.decimal)
    mostrar_parcelamento = CampoFormulario("mostrar_parcelamento", "Marque para mostrar o parcelamento na listagem e na página do produto.", tipo=TipoDeCampo.boleano, requerido=False, ordem=5)
    maximo_parcelas = CampoFormulario("maximo_parcelas", "Máximo de parcelas", tipo=TipoDeCampo.escolha, requerido=False, ordem=6, texto_ajuda=u"Quantidade máxima de parcelas para esta forma de pagamento.", opcoes=PARCELAS)
    parcelas_sem_juros = CampoFormulario("parcelas_sem_juros", "Parcelas sem juros", tipo=TipoDeCampo.escolha, requerido=False, ordem=7, texto_ajuda=u"Número de parcelas sem juros para esta forma de pagamento.", opcoes=PARCELAS)


class MeioPagamentoEnvio(object):
    @property
    def css(self):
        return Script(tipo=TipoScript.css, caminho_arquivo=caminho_arquivo_template("style.css"))

    @property
    def function_enviar(self):
        return Script(tipo=TipoScript.javascript, eh_template=True, caminho_arquivo=caminho_arquivo_template("javascript.js"))

    @property
    def mensagens(self):
        return Script(tipo=TipoScript.html, caminho_arquivo=caminho_arquivo_template("mensagens.html"))

    def to_dict(self):
        return [
            self.css.to_dict(),
            self.function_enviar.to_dict(),
            self.mensagens.to_dict()
        ]


class MeioPagamentoSelecao(SelecaoBase):
    selecao = Script(tipo=TipoScript.html, nome="selecao", caminho_arquivo=caminho_arquivo_template("selecao.html"), eh_template=True)

    def to_dict(self):
        if not self.aceita_pagamento_no_valor():
            return []
        return [
            self.selecao.to_dict()
        ]
