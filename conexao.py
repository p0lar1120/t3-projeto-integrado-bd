import os
from getpass import getpass
from mysql.connector import connect, Error


def usar_conexao(acao):
    """Abre a conexão com o MySQL e executa `acao(connection)`.

    Se existir ~/.my.cnf (seção [client]) ele é usado; caso contrário,
    usuário e senha são solicitados no terminal.
    """
    try:
        cnf = os.path.expanduser("~/.my.cnf")
        if os.path.exists(cnf):
            parametros = {"option_files": cnf}
        else:
            parametros = {
                "user": input("Usuário: "),       # Solicita ao usuário o nome de login
                "password": getpass("Senha: "),   # Solicita a senha de forma oculta
            }
        with connect(host="localhost", **parametros) as connection:
            print("Conexão estabelecida:", connection)
            return acao(connection)
    except Error as e:
        print("Ocorreu um erro ao conectar com o BD: ", e)
