class SugestaoNovoProfessor:
    def __init__(self, data_sugestao, nome_professor):
        self._data_sugestao = data_sugestao
        self._nome_professor = nome_professor

    # Getters
    @property
    def id(self):
        return self._id

    @property
    def data_sugestao(self):
        return self._data_sugestao

    @property
    def nome_professor(self):
        return self._nome_professor

    # Setters
    @id.setter
    def id(self, value):
        self._id = value

    @data_sugestao.setter
    def data_sugestao(self, value):
        self._data_sugestao = value

    @nome_professor.setter
    def nome_professor(self, value):
        self._nome_professor = value

