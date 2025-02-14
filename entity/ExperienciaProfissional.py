from datetime import datetime

class ExperienciaProfissional:
    def __init__(self, id, titulo, data_inicio, data_fim, descricao):
        self._id = id
        self._titulo = titulo
        self._dataInicio = data_inicio
        self._dataFim = data_fim
        self._descricao = descricao

    # Getters
    @property
    def id(self):
        return self._id

    @property
    def titulo(self):
        return self._titulo

    @property
    def dataInicio(self):
        return self._dataInicio

    @property
    def dataFim(self):
        return self._dataFim

    @property
    def descricao(self):
        return self._descricao

    # Setters
    @id.setter
    def id(self, value):
        self._id = value

    @titulo.setter
    def titulo(self, value):
        self._titulo = value

    @dataInicio.setter
    def dataInicio(self, value):
        self._dataInicio = value

    @dataFim.setter
    def dataFim(self, value):
        self._dataFim = value

    @descricao.setter
    def descricao(self, value):
        self._descricao = value

    # @staticmethod
    # def _verificar_datas(data_inicio, data_fim):
    #     formato = "%d/%m/%Y"
    #     try:
    #         data_inicio_dt = datetime.strptime(data_inicio, formato)
    #         data_fim_dt = datetime.strptime(data_fim, formato)
    #     except ValueError:
    #         raise ValueError("As datas devem estar no formato dd/mm/aaaa")
    #     if data_inicio_dt >= data_fim_dt:
    #         raise ValueError("A data de início deve ser menor que a data de fim")

    def cadastraExperienciaProfissional(self):
        pass