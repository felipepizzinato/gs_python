import re
import oracledb

#========================================================================================================================

# Funções básicas do sistema 

def obter_string(prompt):
    while True:
        valor = input(prompt).strip()
        if valor:
            return valor
        print("Entrada inválida. O valor não pode ser vazio.")

def obter_opcao_menu(prompt, min, max):
    while True:
        try:
            escolha = int(input(prompt))
            if min <= escolha <= max:
                return escolha
            else:
                print(f'Opção inválida. Por favor, escolha uma opção entre {min} e {max}.')
        except ValueError:
            print('Erro, tipo de entrada inválida. Por favor, insira um número inteiro.')
        
        
def get_conexao():
    return oracledb.connect(user='rm555141', password='140606', dsn='oracle.fiap.com.br/orcl') 

def validar_email(email):
    pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    return re.fullmatch(pattern, email) is not None

def obter_email():
    while True:
        email = input('Insira seu e-mail: ').strip()
        if validar_email(email):
            return email
        print('Formato de e-mail inválido. Por favor, insira um e-mail válido.')
    
def coletar_id_usuario(dados):
    sql = "SELECT id_cliente FROM clientes WHERE email_usuario = :email_usuario"
    try:
        with get_conexao() as con:
            with con.cursor() as cur:
                cur.execute(sql, dados)
                resultado = cur.fetchone()  
                return resultado[0]
    except Exception as e:
        print(f'Ocorreu um erro ao procurar o login: {e}')
        return None
#========================================================================================================================

def apresentando_menu_login_cadastro():
    print("--------------------------------")
    print('|       LOGIN | CADASTRO       |')
    print("--------------------------------\n")
    print('(1) LOGIN')
    print('(2) CADASTRAR')
    print('(3) SAIR')

    return obter_opcao_menu('Escolha uma opção do menu: ', 1, 3)


def coletar_info_login():
    email = obter_string('Insira seu email: ')
    senha = obter_string('Insira sua Senha: ')
    dados_usuario = {
        "email_usuario": email,
        "senha_usuario": senha
    }
    return dados_usuario

def procurar_login_db(dados_usuario):
    sql = "SELECT COUNT(*) FROM t_sf_usuario WHERE email_usuario = :email_usuario AND senha_usuario = :senha_usuario"
    
    try:
        with get_conexao() as con:
            with con.cursor() as cur:
                cur.execute(sql, dados_usuario)
                resultado = cur.fetchone()  
                if resultado and resultado[0] > 0:
                    print('LOGIN REALIZADO!')
                    id = coletar_id_usuario(dados_usuario)
                    return id 
                else:
                    print('USUÁRIO NÃO ENCONTRADO')
                    return None
    except Exception as e:
        print(f'Ocorreu um erro ao procurar o login: {e}')
        return None



def login():
    dados_usuario = coletar_info_login()
    id = procurar_login_db(dados_usuario)
    if id:
        return id
    else:
        return None
    
    
def coleta_info_cadastro():
    nome = obter_string('Insira seu Nome: ')
    email = obter_email()
    senha = obter_string('Insira sua Senha: ')
    dados = {
        "nm_usuario": nome,
        "email_usuario": email,
        "senha_usuario":senha,
    }
    return dados

def usuario_existe(dados):
    email = dados['email_usuario']
    sql = "SELECT COUNT(*) FROM t_usuario WHERE email_usuario = :email_usuario"
    
    try:
        with get_conexao() as con:
            with con.cursor() as cur:
                cur.execute(sql, {"email_usuario": email})
                resultado = cur.fetchone()
                if resultado:
                    return resultado[0] > 0
                else:
                    return False
    except Exception as e:
        print(f'Ocorreu um erro ao verificar a existência do usuário: {e}')
        return False


def cadastrar_usuario(dados):
    email = dados['email_usuario']
    sql = "INSERT INTO t_usuario (nm_usuario, email_usuario, senha_usuario) VALUES (:nm_usuario, :email_usuario, :senha_usuario)"

    try:
        with get_conexao() as con:
            with con.cursor() as cur:
                cur.execute(sql, dados)
                con.commit() 
                print('Usuário cadastrado com sucesso!')
                id = coletar_id_usuario(email)
                return id 
    except Exception as e:
        print(f'Ocorreu um erro ao cadastrar o usuário: {e}')
        return False

    
def cadastro():
    while True:
        info_cadastro = coleta_info_cadastro()
        if usuario_existe(info_cadastro):
            print('Usuário existente, por favor insira os dados navamente com outro usuário')
        else:
            cadastrar_usuario(info_cadastro)
            return info_cadastro
    
    


#========================================================================================================================



def main():
    while True:
        opcao = apresentando_menu_login_cadastro()
        if opcao == 1:
            id = login()
        elif opcao == 2:
            dados_usuario = cadastro()
        else:
            print('Saindo do sistema...')
            break
        if dados_usuario:
            while True:
                opcao = apresentando_menu_principal()
                if opcao == 1:
                    if info_pessoais(dados_usuario):
                        break
                elif opcao == 2:
                    dados_consumo(dados_usuario)
                elif opcao == 3:
                    solucoes()
                else:
                    break
                
    
    
main()