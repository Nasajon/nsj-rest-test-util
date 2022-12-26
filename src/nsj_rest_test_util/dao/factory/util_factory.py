
class TestesFactory:
  
    @staticmethod
    def getTestesRepository():
        from nsj_rest_test_util.dao.repository.testes_repository import TestesRepository
        return TestesRepository()

