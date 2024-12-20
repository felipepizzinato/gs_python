import re
import oracledb
import matplotlib.pyplot as plt
import numpy as np
from colorama import Fore, Back, Style, init
import datetime
import csv
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
    return oracledb.connect(user='rm555462', password='131005', dsn='oracle.fiap.com.br/orcl') 

def validar_email(email):
    pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    return re.fullmatch(pattern, email) is not None

def obter_email():
    while True:
        email = input('Insira seu e-mail: ').strip()
        if validar_email(email):
            return email
        print('Formato de e-mail inválido. Por favor, insira um e-mail válido.')
    

def obter_kwh():
    while True:
        try:
            kwh = float(input('Insira quanto de KWh teve de consumo: ').strip())
            if kwh > 0:
                return kwh
            print('Valor de KWh inválido. Por favor, insira um número válido maior que zero.')
        except ValueError:
            print('Erro, tipo de entrada inválida. Por favor, insira um número.')
   
def obter_inteiro(prompt):
    while True:
        try:
            opcao = int(input(prompt))
            if opcao > 0:
                return opcao
            print('Valor inválido. Por favor, insira um número inteiro válido maior que zero.')
        except ValueError:
            print('Erro, tipo de entrada inválida. Por favor, insira um número.')
              
    
def coletar_id_usuario(email):
    sql = "SELECT id_usuario FROM t_usuario WHERE email_usuario = :email_usuario"
    try:
        with get_conexao() as con:
            with con.cursor() as cur:
                cur.execute(sql, {"email_usuario": email})
                resultado = cur.fetchone()  
                return resultado[0]
    except Exception as e:
        print(f'Ocorreu um erro ao procurar o login: {e}')
        return None

def validar_mes():
    meses = {
        "janeiro", "fevereiro", "março", "abril",
        "maio", "junho", "julho", "agosto",
        "setembro", "outubro", "novembro", "dezembro"
    }
    while True:
        mes_usuario = obter_string('Insira o mês do consumo que deseja registrar: ').lower()
        for mes in meses:
            if mes_usuario == mes:
                return mes_usuario
        print('Mês inválido! Insira novamente um mês válido')

def validar_ano():
    ano_minimo=2015
    ano_atual = datetime.datetime.now().year
    while True:
        ano = obter_inteiro('Insira o ano do consumo que deseja registrar: ')
        if ano_minimo <= ano <= ano_atual:
            return ano
        else:
            print(f"Ano inválido! O ano deve estar entre {ano_minimo} e {ano_atual}.")
        
        
def realizar_media_kwh(kwh):
    media = kwh / 30
    if media <= 5:
        print( Fore.GREEN + "Consumo Baixo. Parabéns! Seu consumo está em um nível sustentável." + Style.RESET_ALL)
    elif media >= 5 and media <= 10:
        print( Fore.YELLOW + "Consumo Moderado. Atenção! Você está consumindo de forma moderada.Considere otmizar o uso de alguns aparelhos." + Style.RESET_ALL)
    else:
        print( Fore.RED + "Consumo Alto. Alerta! Seu consumo está alto. Reduza o uso de energia para ajudar o planeta e economizar." + Style.RESET_ALL)
    return None
        
def selecionar_indice_dados_consumo(dados):
    while True: 
        opcao = obter_inteiro('Insira o indíce do consumo: ')
        if opcao < 1 or opcao > len(dados):
            print("Índice inválido! Por favor, insira um número válido.")
        else:
            break
    return opcao

def apresentar_consumo_selecionado(indice, dados, id_usuario):
    dados_consumo = {"ano_consumo": dados[indice-1][0],
                     "mes_consumo": dados[indice-1][1],
                     "id_usuario": id_usuario}
    print(f"(1)Ano consumo: {dados[indice-1][0]} \n(2)Mês consumo: {dados[indice-1][1]} \n(3)Kwh: {dados[indice-1][2]}")
    return dados_consumo

def calculo_emissao_co2(kwh):
    print(f"Emissão Total de CO2:{kwh * 0.0125} Kg CO2e")
    print('obs: Cálculo realizado de acordo com a calculado de CO2 de SOSMATAATLANTICA e carbonlifecycle')
    


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
    sql = "SELECT COUNT(*) FROM t_usuario WHERE email_usuario = :email_usuario AND senha_usuario = :senha_usuario"
    
    try:
        with get_conexao() as con:
            with con.cursor() as cur:
                cur.execute(sql, dados_usuario)
                resultado = cur.fetchone()  
                if resultado and resultado[0] > 0:
                    print('LOGIN REALIZADO!')
                    email = dados_usuario["email_usuario"]
                    id_usuario = coletar_id_usuario(email)
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
    required_keys = {'nm_usuario', 'email_usuario', 'senha_usuario'}
    if not required_keys.issubset(dados):
        print("Erro: Dicionário de dados está faltando uma ou mais chaves obrigatórias.")
        return False

    email = dados['email_usuario']
    sql = "INSERT INTO t_usuario (nm_usuario, email_usuario, senha_usuario) VALUES (:nm_usuario, :email_usuario, :senha_usuario)"

    try:
        with get_conexao() as con:
            with con.cursor() as cur:
                cur.execute(sql, dados)
                con.commit() 
                print('Usuário cadastrado com sucesso!')
                id_usuario = coletar_id_usuario(email)
                if id_usuario is None:
                    print("Erro: `coletar_id_usuario` retornou None.")
                    return False
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
    print('(2) MONITORAR DADOS DE CONSUMO')
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
    sql = "SELECT * FROM t_usuario WHERE id_usuario = :id_usuario"
    with get_conexao() as con:
        try: 
            with con.cursor() as cur:
                cur.execute(sql, {"id_usuario": id_usuario})
                dados = cur.fetchall()
                print(f'(1) Nome: {dados[0][1]}')
                print(f'(2) Email: {dados[0][2]}')
                print(f'(3) Senha: {dados[0][3]}')
            return True
        except Exception as e:
            print(f'Erro ao exibir dados: {e}')
            
            
def alterar_usuario(id_usuario, campo, novo_valor):
    sql = f'UPDATE t_usuario SET {campo} = :novo_valor WHERE id_usuario = :id_usuario'
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
                break
    elif escolha == 3:
        nova_senha = obter_string('Digite a nova senha: ')
        alterar_usuario(id_usuario, 'senha_usuario', nova_senha)       
    else:
        print('Operação cancelada.')
        
def sql_deletar_usuario(id_usuario):
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
        sql_deletar_usuario(id_usuario)
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

def apresentar_dados_consumo(id_usuario):
    sql = "SELECT ano_consumo, mes_consumo, kwh_consumo FROM t_dados_consumo WHERE id_usuario = :id_usuario"
    try:
        with get_conexao() as con:
            with con.cursor() as cur:
                cur.execute(sql, {"id_usuario": id_usuario})
                dados = cur.fetchall()
                if not dados:
                    print("Nenhum dado de consumo encontrado para este usuário.")
                    return
                print("Consumo do usuário:")

                for indice, dado in enumerate(dados, start=1): 
                    ano_consumo = dado[0]
                    mes_consumo = dado[1]
                    kwh_consumo = dado[2]
                    print(f"{indice} :\nAno consumo: {ano_consumo}\nMês consumo: {mes_consumo}\nKWH: {kwh_consumo}\nCategoria de consumo:")
                    realizar_media_kwh(kwh_consumo)
                    calculo_emissao_co2(kwh_consumo)

                return dados
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
 
def validar_cadastro_consumo(dados_consumo):
    dados_consumo = {
        "id_usuario": dados_consumo.get("id_usuario"),
        "ano_consumo": dados_consumo.get("ano_consumo"),
        "mes_consumo": dados_consumo.get("mes_consumo")
    }
    sql = "SELECT COUNT(*) FROM t_dados_consumo WHERE id_usuario = :id_usuario AND ano_consumo = :ano_consumo  AND mes_consumo = :mes_consumo"
    try:
        with get_conexao() as con:
            with con.cursor() as cur:
                cur.execute(sql, dados_consumo)
                resultado = cur.fetchone()
                if resultado:
                    return resultado[0] > 0
                else:
                    return False
    except Exception as e:
        print(f"Erro ao verificar consumo: {e}")
        return None
   


def realizar_cadastro_consumo(dados_consumo):
    sql = "INSERT INTO t_dados_consumo (id_usuario, ano_consumo, mes_consumo, kwh_consumo) VALUES (:id_usuario, :ano_consumo, :mes_consumo, :kwh_consumo)"
    try:
        with get_conexao() as con:
            with con.cursor() as cur:
                cur.execute(sql, dados_consumo)
                con.commit()
                return True
    except Exception as e:
        print(f'Erro ao inserir os dados na tabela: {e}')
        return None

    
def obter_dados_consumo(id_usuario):
    ano_consumo = validar_ano()  
    mes_consumo = validar_mes()    
    kwh_consumo = obter_kwh()  
    dados_consumo = {
        "id_usuario": id_usuario,
        "ano_consumo": ano_consumo,
        "mes_consumo": mes_consumo,
        "kwh_consumo": kwh_consumo  
    }
    
    return dados_consumo
    
def logica_cadastrar_consumo(id_usuario):
    while True:
        dados_consumo = obter_dados_consumo(id_usuario)
        if validar_cadastro_consumo(dados_consumo):
            print('Já existe um cadastro de consumo para este mês, por favor insira os dados novamente para outro mês')
            
        else:
            realizar_cadastro_consumo(dados_consumo)
            print('Dados de consumo registrado com sucesso')
            break
                
def sql_alterar_dados_consumo(novo_valor, id_usuario,campo, dados_consumo):
    parametros = {
    "novo_valor": novo_valor,
    "id_usuario": id_usuario,
    "ano_consumo": dados_consumo["ano_consumo"],
    "mes_consumo": dados_consumo["mes_consumo"]
}

    sql = f"UPDATE t_dados_consumo SET {campo} = :novo_valor WHERE id_usuario = :id_usuario AND ano_consumo = :ano_consumo AND mes_consumo = :mes_consumo"
    with get_conexao() as con:
        with con.cursor() as cur:
            try:
                cur.execute(sql, parametros)
                con.commit()
                print("Ano_consumo atualizado com sucesso!")
            except Exception as e:
                print(f"Ocorreu um erro ao atualizar ano_consumo: {e}")

def logica_alterar_dados_consumo(id_usuario):
    dados = apresentar_dados_consumo(id_usuario)
    indice = selecionar_indice_dados_consumo(dados)
    dados_consumo_antigo = apresentar_consumo_selecionado(indice, dados, id_usuario)
    escolha = obter_opcao_menu('Insira qual dado você deseja alterar (digite 4 para cancelar a operação): ', 1, 4)

    if escolha == 1:
        while True:
            novo_ano = validar_ano()
            dados_consumo = dados_consumo_antigo.copy()
            dados_consumo["ano_consumo"] = novo_ano
            if validar_cadastro_consumo(dados_consumo):
                print('Já existe um cadastro de consumo para este mês, por favor insira outra data')
            else:
                sql_alterar_dados_consumo(novo_ano, id_usuario, 'ano_consumo', dados_consumo_antigo)
                break
    elif escolha == 2:
        while True:
            novo_mes = validar_mes()
            dados_consumo = dados_consumo_antigo.copy()
            dados_consumo["mes_consumo"] = novo_mes
            if validar_cadastro_consumo(dados_consumo):
                    print('Já existe um cadastro de consumo para este mês, por favor insira outra data')
            else:
                sql_alterar_dados_consumo(novo_mes, id_usuario, 'mes_consumo', dados_consumo_antigo)
                break
    elif escolha == 3:
        kwh_consumo = obter_kwh() 
        sql_alterar_dados_consumo(kwh_consumo, id_usuario, 'kwh_consumo', dados_consumo_antigo)    
    else:
        print('Operação cancelada.')

def sql_deletar_dados_consumo(id_usuario, dados,indice):
    sql = "DELETE FROM t_dados_consumo WHERE id_usuario = :id_usuario AND ano_consumo = :ano_consumo AND mes_consumo = :mes_consumo"
    try:
        with get_conexao() as con:
            with con.cursor() as cur:
                dados_consumo = {
                    "id_usuario": id_usuario,
                    "ano_consumo" : dados[indice - 1][0],
                    "mes_consumo": dados[indice - 1][1]
                }
                cur.execute(sql, dados_consumo)
                con.commit()
                print("Consumo excluído com sucesso!")
                return True
    except Exception as e:
        print(f'Erro ao deletar os dados na tabela: {e}')
        return None
def exportar_arquivo_csv(id_usuario):
    sql = "SELECT ano_consumo, mes_consumo, kwh_consumo FROM t_dados_consumo WHERE id_usuario = :id_usuario"
    try:
        with get_conexao() as con:
            with con.cursor() as cur:
                cur.execute(sql, {"id_usuario": id_usuario})
                dados = cur.fetchall()
                if not dados:
                    print("Nenhum dado de consumo encontrado para este usuário.")
                    return
                colunas = [desc[0] for desc in cur.description]
                nome_arquivo = f'dados_consumo_usuario_{id_usuario}.csv'
                
                with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
                    escritor = csv.writer(arquivo_csv)

                    escritor.writerow(colunas)

                    escritor.writerows(dados)

                print(f"Dados exportados com sucesso para '{nome_arquivo}'")
                
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    
    
def logica_deletar_dados_consumo(id_usuario):
    dados = apresentar_dados_consumo(id_usuario)
    indice = selecionar_indice_dados_consumo(dados)
    print('Você realmente deseja apagar este dado de consumo ?')
    print('(1) Sim')
    print('(2) Não')
    opcao = obter_opcao_menu('Escolha uma opção do menu de cadastro: ', 1, 2)
    if opcao == 1:
        sql_deletar_dados_consumo(id_usuario, dados, indice)
        return True
    else:
        print('Operação cancelada.')
        return None
#========================================================================================================================

def consultar_dados(id_usuario):
    query = "SELECT ano_consumo, mes_consumo, kwh_consumo FROM t_dados_consumo WHERE id_usuario = :id_usuario ORDER BY ano_consumo, mes_consumo "
    
    try:
        with get_conexao() as con:
            with con.cursor() as cur:
                cur.execute(query, {"id_usuario": id_usuario})
                dados = cur.fetchall()
                return dados
    except Exception as e:
        print(f"Erro ao executar consulta: {e}")
        return []

def processar_dados(dados):
    anos = []
    meses = []
    kwh = []

    meses_numericos = {
        "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4,
        "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
        "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12
    }

    for dado in dados:
        anos.append(dado[0])
        meses.append(meses_numericos[dado[1].lower()])  
        kwh.append(dado[2])

    return anos, meses, kwh

def criar_grafico_comparativo(anos, meses, kwh):
    anos_unicos = sorted(set(anos))
    cores = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    legenda = []

    nomes_meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    plt.figure(figsize=(12, 6))  

    for i, ano in enumerate(anos_unicos):
        meses_ano = [mes for j, mes in enumerate(meses) if anos[j] == ano]
        kwh_ano = [valor for j, valor in enumerate(kwh) if anos[j] == ano]

        meses_ano, kwh_ano = zip(*sorted(zip(meses_ano, kwh_ano)))

        plt.plot(meses_ano, kwh_ano, marker='o', linestyle='-', color=cores[i % len(cores)], label=f'Ano {ano}')
        legenda.append(f'Ano {ano}')

    plt.title('Comparativo de Consumo de Energia por Mês e Ano', fontsize=16)
    plt.xlabel('Mês', fontsize=12)
    plt.ylabel('kWh Consumido', fontsize=12)

    plt.xticks(np.arange(1, 13), nomes_meses, rotation=45) 

    plt.legend()
    plt.grid(True)
    plt.tight_layout()  
    plt.show()

def grafico_mes_consumo(id_usuario):
    dados = consultar_dados(id_usuario)
    anos, meses, kwh = processar_dados(dados)
    criar_grafico_comparativo(anos, meses, kwh)
    return None
#========================================================================================================================
    


def processar_dados_anuais(dados):
    consumo_anual = {}

    for dado in dados:
        ano = dado[0]
        kwh = dado[2]
        if ano in consumo_anual:
            consumo_anual[ano] += kwh
        else:
            consumo_anual[ano] = kwh

    return consumo_anual

def criar_grafico_consumo_anual(consumo_anual):
    anos = list(map(int, consumo_anual.keys()))
    total_kwh = list(consumo_anual.values())

    plt.figure(figsize=(10, 6))
    plt.bar(anos, total_kwh, color='skyblue', edgecolor='black')

    plt.title('Consumo Total Anual de Energia', fontsize=16)
    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('kWh Consumido', fontsize=12)

    for i, valor in enumerate(total_kwh):
        plt.text(anos[i], valor + 10, f'{valor}', ha='center', fontsize=10)

    plt.xticks(anos, fontsize=10)  
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def grafico_consumo_total_anual(id_usuario):
    dados = consultar_dados(id_usuario)  
    if not dados:
        print("Nenhum dado encontrado para o usuário.")
        return None

    consumo_anual = processar_dados_anuais(dados) 
    criar_grafico_consumo_anual(consumo_anual)    

#========================================================================================================================
def dados_consumo(id_usuario):

    while True: 
        
        print('(1) LISTAR DADOS DE CONSUMO')
        print('(2) ADICIONAR DADOS DE CONSUMO')
        print('(3) EXCLUIR DADOS DE CONSUMO')
        print('(4) ALTERAR DADOS DE CONSUMO')
        print('(5) GRÁFICO COMPARAÇÃO MÊS CONSUMO')
        print('(6) GRÁFICO CONSUMO TOTAL POR ANO')
        print('(7) EXPORTAR PARA ARQUIVO .csv')
        print('(8) VOLTAR AO MENU PRINCIPAL')
        opcao = obter_opcao_menu('Escolha uma opção: ', 1, 8)
        if opcao == 1:
            apresentar_dados_consumo(id_usuario)
        if opcao == 2:
            logica_cadastrar_consumo(id_usuario)
        elif opcao == 3:
            logica_deletar_dados_consumo(id_usuario)
        elif opcao == 4:
            logica_alterar_dados_consumo(id_usuario)
        elif opcao == 5:
            grafico_mes_consumo(id_usuario)
        elif opcao == 6:
            grafico_consumo_total_anual(id_usuario)
        elif opcao == 7:
            exportar_arquivo_csv(id_usuario)
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