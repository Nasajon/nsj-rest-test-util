from nsj_rest_test_util.util.json_util import JsonUtil


class ExcecaoLancadaManualmente(Exception):
    def __init__(self, mensagem, detalhes=None):
        self.mensagem = mensagem
        self.detalhes = detalhes

    def __dict__(self):
        if self.detalhes is not None:
            return {
                "erro": self.mensagem,
                "detalhes": self.detalhes
            }
        else:
            return {
                "erro": self.mensagem
            }


class ExcecaoInterna(Exception):
    pass


class ExcecaoDataForaDaCompetencia(ExcecaoLancadaManualmente):
    pass


class MissingAttributeException(ExcecaoLancadaManualmente):
    pass


class WrongTypeException(ExcecaoLancadaManualmente):
    pass


class InvalidValueException(ExcecaoLancadaManualmente):
    pass


class ContabilidadeRealizadaException(ExcecaoLancadaManualmente):
    def __init__(self, mensagem):
        self.mensagem = mensagem

    def __dict__(self):
        return {
            "erro": "Esta operação não pode ser realizada pois altera um movimento contábil já realizado de forma definitiva",
            "detalhes": self.mensagem}


class ValidacaoContabilException(ExcecaoLancadaManualmente):

    def __dict__(self):
        return {
            "erro": "Erro contabil",
            "detalhes": self.detalhes}


class RecursoJaExisteException(ExcecaoLancadaManualmente):
    def __init__(self, nome_recurso, valor):
        self.nome_recurso = nome_recurso
        self.valor = valor

    def __str__(self):
        return f"Já existe um recurso <{self.nome_recurso}> com identificação {self.valor}"

    def __dict__(self):
        return {
            "erro": str(self)
        }


class RecursoNaoExisteException(ExcecaoLancadaManualmente):
    def __init__(self, nome_recurso, valor):
        self.nome_recurso = nome_recurso
        self.valor = valor

    def __str__(self):
        return f"Erro: Não existe um recurso do tipo [{self.nome_recurso}] com identificação {self.valor}"

    def __dict__(self):
        return {
            "erro": str(self)
        }


class IdentificacaoAmbiguaException(ExcecaoLancadaManualmente):
    def __init__(self, nome_recurso, nome_identificador, valor, opcoes):
        self.nome_recurso = nome_recurso
        self.nome_identificador = nome_identificador
        self.valor = valor
        self.opcoes = opcoes

    def __str__(self):
        return JsonUtil().encode(self.__dict__())

    def __dict__(self):
        return {
            "msg": "O identificador [" + self.nome_identificador + "] com valor [" + self.valor + \
                   "] é ambíguo para o recurso [" + self.nome_recurso + "].",
            "opcoes-disponiveis": self.opcoes}
