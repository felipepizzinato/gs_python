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
                    id_usuario = coletar_id_usuario(dados_usuario)
                    return id_usuario 
                else:
                    print('USUÁRIO NÃO ENCONTRADO')
                    return None
    except Exception as e:
        print(f'Ocorreu um erro ao procurar o login: {e}')
        return None




    
    

    
def login():
    dados_usuario = coletar_info_login()
    id_usuario = procurar_login_db(dados_usuario)
    if id_usuario:
        return id_usuario
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
                id_usuario = coletar_id_usuario(email)
                return id_usuario 
    except Exception as e:
        print(f'Ocorreu um erro ao cadastrar o usuário: {e}')
        return False

    
def cadastro():
    while True:
        info_cadastro = coleta_info_cadastro()
        if usuario_existe(info_cadastro):
            print('Usuário existente, por favor insira os dados navamente com outro usuário')
        else:
            id_usuario = cadastrar_usuario(info_cadastro)
            return id_usuario
    
    


#========================================================================================================================


def apresentando_menu_principal():
    print("-------------------------------")
    print('|        MENU PRINCIPAL        |')
    print("-------------------------------\n")
    print('(1) INFORMAÇÕES PESSOAIS')
    print('(2) ANALISAR DADOS DE CONSUMO')
    print('(3) SUGESTÕES')
    print('(4) VOLTAR AO MENU DE LOGIN | CADASTRO')

    return obter_opcao_menu('Escolha uma opção do menu de cadastro: ', 1, 4)


def apresentando_menu_info_pessoais():
    print("-------------------------------------------")
    print('|        MENU INFORMAÇÕES PESSOAIS        |')
    print("-------------------------------------------\n")
    print('(1) VER MEUS DADOS DE CADASTRO')
    print('(2) ALTERAR DADOS DE CADASTRO')
    print('(3) EXCLUIR CADASTRO')
    print('(4) VOLTAR AO MENU PRINCIPAL')

    return obter_opcao_menu('Escolha uma opção do menu de cadastro: ', 1, 4)


def exibir_dados(id_usuario):
    sql = "SELECT * FROM t_sf_usuario WHERE id_usuario = :id_usuario"
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, {"id_usuario": id_usuario})
            dados = cur.fetchall()
            print(f'(1) Nome: {dados[0][1]}')
            print(f'(2) Email: {dados[0][2]}')
            print(f'(3) Senha: {dados[0][3]}')
        return True

def alterar_usuario(id_usuario, campo, novo_valor):
    sql = f'UPDATE t_sf_usuario SET {campo} = :novo_valor WHERE id_usuario = :id_usuario'
    with get_conexao() as con:
        with con.cursor() as cur:
            try:
                cur.execute(sql, {'novo_valor': novo_valor, 'id_usuario': id_usuario})
                con.commit()
                print(f'{campo.capitalize()} atualizado com sucesso!')
                return True
            except Exception as e:
                print(f'Ocorreu um erro ao atualizar {campo}: {e}')

def alterar_dados(id_usuario):
    exibir_dados(id_usuario)
    escolha = obter_opcao_menu('Insira qual dado você deseja alterar (digite 4 para cancelar a operação): ', 1, 4)

    if escolha == 1:
        novo_nome = obter_string('Digite o novo nome: ')
        alterar_usuario(id_usuario, 'nm_usuario', novo_nome)
    elif escolha == 2:
        while True:
            novo_email = obter_email()
            dados = {
                "email_usuario":novo_email
                }
            
            
            if usuario_existe(dados):
                print('Erro: O usuário já existe. Escolha outro nome de usuário.')
            else:
                alterar_usuario(id_usuario, 'email_usuario', novo_email)
    elif escolha == 3:
        nova_senha = obter_string('Digite a nova senha: ')
        alterar_usuario(id_usuario, 'senha_usuario', nova_senha)       
    else:
        print('Operação cancelada.')
        
def deletar(id_usuario):
    sql = "DELETE FROM t_usuario WHERE id_usuario = :id_usuario"
    try:
        with get_conexao() as con:
            with con.cursor() as cur:
                cur.execute(sql, {"id_usuario": id_usuario})
                con.commit() 
                print('Usuário excluído com sucesso!')
    except Exception as e:
        print(f'Ocorreu um erro ao excluir o usuário: {e}')

def deletar_usuario(id_usuario):
    print('Você realmente deseja apagar sua conta?')
    print('(1) Sim')
    print('(2) Não')
    opcao = obter_opcao_menu('Escolha uma opção do menu de cadastro: ', 1, 2)
    if opcao == 1:
        deletar(id_usuario)
        return True
    else:
        print('Operação cancelada.')
        return None

def info_pessoais(id_usuario):
    while True:
        opcao = apresentando_menu_info_pessoais()
        if opcao == 1:
            exibir_dados(id_usuario)
        elif opcao == 2:
            alterar_dados(id_usuario)
        elif opcao == 3:
            if deletar_usuario(id_usuario):
                return True
                
        else:
            break
        
#========================================================================================================================


def solucoes():
    sql = "SELECT tema_sugestao, ds_sugestao FROM t_sugestoes"
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql)
            dados = cur.fetchall()
            for tema, sugestao in dados:
                print(f"Tema: {tema} - Sugestão: {sugestao}")       
        return True
#========================================================================================================================


def main():
    while True:
        opcao = apresentando_menu_login_cadastro()
        if opcao == 1:
            id_usuario = login()
        elif opcao == 2:
            id_usuario = cadastro()
        else:
            print('Saindo do sistema...')
            break
        if id_usuario:
            while True:
                opcao = apresentando_menu_principal()
                if opcao == 1:
                    if info_pessoais(id_usuario):
                        break
                elif opcao == 2:
                    dados_consumo(id_usuario)
                elif opcao == 3:
                    solucoes()
                else:
                    break
                
    
    
main()