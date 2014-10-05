# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac

import time
from datetime import datetime
from pagador.seguranca.autenticador import TipoAutenticacao
from pagador.seguranca.instalacao import Parametros
from pagador_koin import settings
from pagador.seguranca import autenticador


class ParametrosBcash(Parametros):
    @property
    def chaves(self):
        return ["id_plataforma"]


class Credenciador(autenticador.Credenciador):
    def __init__(self, configuracao):
        self.conta_id = configuracao.conta_id
        self.token = str(getattr(configuracao, "token", ""))
        self.tipo = TipoAutenticacao.query_string

    @property
    def chave(self):
        return ["token"]

    def obter_credenciais(self):
        return self.token

    def esta_valido(self):
        return True
