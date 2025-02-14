import requests

class Perfil:
    def __init__(self, id, nome, curso, email_institucional):
        self._id = id
        self._nome = nome
        self._curso = curso
        self._email_institucional = email_institucional

    # Getters
    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def curso(self):
        return self._curso

    @property
    def email_institucional(self):
        return self._email_institucional

    # Setters
    @id.setter
    def id(self, value):
        self._id = value

    @nome.setter
    def nome(self, value):
        self._nome = value

    @curso.setter
    def curso(self, value):
        self._curso = value

    @email_institucional.setter
    def email_institucional(self, value):
        self._email_institucional = value

    @staticmethod
    def obter_dominio(email):
        dominio = email.split('@')[1]
        return dominio == 'academico.ifpb.edu.br'

    @staticmethod
    def verifica_email_institucional(email_institucional):
        try:
            client = emailable.Client('test_ae3408af24bd480f6ab3')
            response = client.verify(email_institucional)

            if response.state == 'deliverable' and Perfil.obter_dominio(email_institucional):
                return True
            else:
                return False
        except Exception as e:
            raise ValueError(f"Erro ao verificar o e-mail: {e}")

    # def cadastraPerfil(self):
    #     pass

# # Exemplo de uso
# perfil = Perfil("João", "Engenharia", "livia.meira@academico.ifpb.edu.br")
# print(f"Perfil criado com sucesso! Nome: {perfil.nome}, Curso: {perfil.curso}, Email: {perfil.email_institucional}")
