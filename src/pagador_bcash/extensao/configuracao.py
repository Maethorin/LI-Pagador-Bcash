# -*- coding: utf-8 -*-
import os

from pagador.configuracao.cadastro import CampoFormulario, FormularioBase, CadastroBase, SelecaoBase, TipoDeCampo
from pagador.configuracao.cliente import Script, TipoScript


def caminho_do_arquivo_de_template(arquivo):
    diretorio = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(diretorio, "templates", arquivo)


class MeioPagamentoCadastro(CadastroBase):
    @property
    def descricao_para_lojista(self):
        script = Script(tipo=TipoScript.html, nome="descricao")
        script.adiciona_linha('<p>Conheça <a href="http://bcash.com.br/para-quem-vende/" target="_blank">Bcash</a>!</p>')
        script.adiciona_linha('<p>A ferramenta completa que faltava para impulsionar as suas vendas na internet com segurança e rapidez.</p>')
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
PARCELAS.insert(0, (0, "Todas"))


class Formulario(FormularioBase):
    usuario = CampoFormulario("usuario", "Seu e-mail no Bcash", requerido=True, tamanho_max=128, ordem=1)
    token = CampoFormulario("token", "Sua chave de acesso", requerido=True, tamanho_max=128, ordem=2)
    mostrar_parcelamento = CampoFormulario("mostrar_parcelamento", "Marque para mostrar o parcelamento na listagem dos produtos e na página do produto.", tipo=TipoDeCampo.boleano, requerido=False, ordem=3)
    maximo_parcelas = CampoFormulario("maximo_parcelas", "Máximo de parcelas", tipo=TipoDeCampo.escolha, requerido=False, ordem=4, texto_ajuda=u"Quantidade máxima de parcelas para esta forma de pagamento.", opcoes=PARCELAS)
    parcelas_sem_juros = CampoFormulario("parcelas_sem_juros", "Parcelas sem juros", tipo=TipoDeCampo.escolha, requerido=False, ordem=5, texto_ajuda=u"Número de parcelas sem juros para esta forma de pagamento.", opcoes=PARCELAS)


class MeioPagamentoEnvio(object):
    source_fraud_id = Script(tipo=TipoScript.source, conteudo="//resources.koin.{}.br/scripts/koin.min.js".format("net"))

    @property
    def css(self):
        return Script(tipo=TipoScript.css, caminho_arquivo=caminho_do_arquivo_de_template("style.css"))

    @property
    def function_enviar(self):
        return Script(tipo=TipoScript.javascript, eh_template=True, caminho_arquivo=caminho_do_arquivo_de_template("javascript.js"))

    @property
    def mensagens(self):
        return Script(tipo=TipoScript.html, caminho_arquivo=caminho_do_arquivo_de_template("mensagens.html"))

    def to_dict(self):
        return [
            self.css.to_dict(),
            self.source_fraud_id.to_dict(),
            self.function_enviar.to_dict(),
            self.mensagens.to_dict()
        ]


class MeioPagamentoSelecao(SelecaoBase):
    selecao = Script(tipo=TipoScript.html, nome="selecao", caminho_arquivo=caminho_do_arquivo_de_template("selecao.html"), eh_template=True)

    def to_dict(self):
        return [
            self.selecao.to_dict()
        ]
