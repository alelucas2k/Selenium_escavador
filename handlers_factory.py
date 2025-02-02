from driver_handlers import OpenSiteHandler, SearchProfessorHandler, ClickProfileHandler, SaveResumeHandler

class HandlerFactory:
    @staticmethod
    def criar_cadeia():
        return OpenSiteHandler(SearchProfessorHandler(ClickProfileHandler(SaveResumeHandler())))
