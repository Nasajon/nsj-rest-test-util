
class TestesFactory:
  
    @staticmethod
    def getTestesRepository():
        from tests.src.repository.testes_repository import TestesRepository
        return TestesRepository()

