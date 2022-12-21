# nsj-rest-test-util
Utilitário para geração e execução de testes em APIs Rest

Esta biblioteca não se propõe a testar método e sim requisições.
A criação dos testes é automatizada, só é necessário preencher qual a requisição e qual a resposta esperada.

A biblioteca possui dois passos: a Criação e a Execução

A Criação de caso de teste é o processo que realiza um dump das informações no banco ele gera um csv com as informações do banco no momento da criação do teste e também realiza a requisção para a api que será testada para gerar assim o retorno que será comparado na hora de executar o teste.

A Execução do teste é realizada pelo pytest na pasta api/casos_de_teste
neste ponto ele carregará no banco os dados do csv criado na criação do teste e fará uma requisição para a api no tenant que foi configurado nas variaveis de ambiente.

# Variaveis de ambiente

DATABASE_HOST - Host do banco 
DATABASE_PASS - Senha do banco
DATABASE_PORT - Porta do banco
DATABASE_NAME - Nome da base de dados
DATABASE_USER - Usuario do banco

SERVER_PORT - porta da aplicação que será testada
TESTS_TENANT - tenant que será usado para inserção de dados de teste
TESTS_URL_BASE - url base da aplicação que será 


# Criação de caso de teste




    
 em src/util/tcase_tools altere o chamamento da função TCaseTools.criar_caso_teste_padrao no método main
     TCaseTools.criar_caso_teste_padrao(
        1,                          # Tenant que será feita a requisição ara montar o teste
        "/recursos",                # Rota que será feira a requisição
        "1234",                     # Codigo mope para a rota
        HTTPMethod.GET,             # Metodo HTTP que será feita a requisição
        204,                        # Código esperado para o retorno
        "exemplo1",                 # Nome que será usado para se referir ao teste
        JsonUtil().decode(""""""),  # Corpo da requisição em caso de POST, em caso de GET e DELETE são os parametros na url
        True,                       # Esse parametro é para saber se deseja executar o teste e gerar a saída, por 
                                    padrão passamos true
        True                        # esse paramentro é para se o teste já existir ao executar novamente será sobrescrito
                                    seus arquivos
    )