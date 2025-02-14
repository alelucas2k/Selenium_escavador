from datetime import datetime


class Projeto:
    def __init__(self, id, nome, data_inicio, data_fim, descricao, eh_pesquisa, eh_extensao):
        self._id = id
        self._nome = nome
        self._data_inicio = data_inicio
        self._data_fim = data_fim
        self._descricao = descricao
        self._eh_pesquisa = eh_pesquisa
        self._eh_extensao = eh_extensao
        self._professores = []
        self._alunos = []
        self._grandes_areas = []

    # @staticmethod
    # def verificar_datas(data_inicio, data_fim):
    #     formato = "%d/%m/%Y"
    #     try:
    #         data_inicio_dt = datetime.strptime(data_inicio, formato)
    #         data_fim_dt = datetime.strptime(data_fim, formato)
    #     except ValueError:
    #         raise ValueError("As datas devem estar no formato dd/mm/aaaa")
    #     if data_inicio_dt >= data_fim_dt:
    #         raise ValueError("A data de início deve ser menor que a data de fim")

    # Getters
    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def data_inicio(self):
        return self._data_inicio

    @property
    def data_fim(self):
        return self._data_fim

    @property
    def descricao(self):
        return self._descricao

    @property
    def eh_pesquisa(self):
        return self._eh_pesquisa

    @property
    def eh_extensao(self):
        return self._eh_extensao

    # Setters
    @id.setter
    def id(self, value):
        self._id = value

    @nome.setter
    def nome(self, value):
        self._nome = value

    @data_inicio.setter
    def data_inicio(self, value):
        self._data_inicio = value

    @data_fim.setter
    def data_fim(self, value):
        self._data_fim = value

    @descricao.setter
    def descricao(self, value):
        self._descricao = value

    @eh_pesquisa.setter
    def eh_pesquisa(self, value):
        self._eh_pesquisa = value

    @eh_extensao.setter
    def eh_extensao(self, value):
        self._eh_extensao = value

    @property
    def professores(self):
        return self._professores

    @property
    def alunos(self):
        return self._alunos

    @property
    def grandes_areas(self):
        return self
