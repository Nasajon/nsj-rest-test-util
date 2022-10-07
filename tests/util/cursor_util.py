class CursorUtil:
    @staticmethod
    def fetchall(cursor):
        fetch =  cursor.fetchall()
        retorno = []
        for f in fetch:
            linha ={}
            for key in f.keys():
                linha[key] = f[key]
            retorno.append(linha)
        return retorno

    @staticmethod
    def fetchone(cursor):
        if cursor is not None:
            dados = cursor.fetchall()
            if len(dados) > 0:
                return dados[0]