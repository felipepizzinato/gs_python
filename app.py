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
    

#========================================================================================================================

def apresentando_menu_login_cadastro():
    print("--------------------------------")
    print('|       LOGIN | CADASTRO       |')
    print("--------------------------------\n")
    print('(1) LOGIN')
    print('(2) CADASTRAR')
    print('(3) SAIR')

    return obter_opcao_menu('Escolha uma opção do menu: ', 1, 3)






def main():
    while True:
        opcao = apresentando_menu_login_cadastro()
        if opcao == 1:
            dados_usuario = login()
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