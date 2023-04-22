##BIBLIOTECAS
import mysql.connector
import os
import time

##FUNÇÕES GLOBAIS
def conexaoBD():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="pL"
    )
    return db

def headerMenu(title, subtitle):
    os.system('cls' if os.name == 'nt' else 'clear')
    border = 60*"="
    title_length = len(title)
    subtitle_length = len(subtitle)
    title_spaces = int((40 - title_length)/2)
    subtitle_spaces = int((40 - subtitle_length)/2)
    print(f"{border}\n{' '*title_spaces}{title}\n{' '*subtitle_spaces}{subtitle}\n{border}")
    print()
    time.sleep(0.5)

##FUNÇÔES ESPECIFICAS
def mostrar_hospitais():
    db = conexaoBD()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tbHospitais")
    hospitais = cursor.fetchall()
    print("ID\tNome do Hospital")
    for hospital in hospitais:
        print(f"{hospital[0]}\t{hospital[1]}")
    db.close()

def mostrar_setores(hospital_id):
    db = conexaoBD()
    cursor = db.cursor()
    cursor.execute("SELECT nomeSetor FROM tbSetores WHERE hospSetor = (SELECT nomeHosp FROM tbHospitais WHERE idHosp = %s)", (hospital_id,))
    setores = cursor.fetchall()
    db.close()
    print("Setores disponíveis:")
    for setor in setores:
        print(f"- {setor[0]}")



##MENUS
#MENU INICIAL
def menuInicial():
    headerMenu("Bem-vindo ao PyLeitos!", "Um sistema para gerenciamento de leitos hospitalares.")

    while True:
        print("Selecione uma opção:")
        print("1 - Iniciar plantão")
        print("2 - Transferência Interna")
        print("3 - Remanejamento")
        print("4 - Fila de Espera")
        print("5 - Configurações")
        print("6 - Fechar plantão\n")

        opcao = input("Opção escolhida: ")

        if opcao == "1":
            iniciarPlantao()
        elif opcao == "2":
            transferenciaInterna()
        elif opcao == "3":
            remanejamentoInterno()
        elif opcao == "4":
            filaDeEspera()
        elif opcao == "5":
            configuracoes()
        elif opcao == "6":
            fecharPlantao()
        else:
            print("Opção inválida. Tente novamente.\n")

def configuracoes():
    headerMenu("MENU - CONFIGURAÇÕES", "Altere dados sobre hospitais, setores, quartos e leitos")

    while True:
        print("Selecione uma opção:")
        print("1 - Adicionar Hospital/Setor/Quarto/Leito")
        print("2 - Atualizar Hospital/Setor/Quarto/Leito")
        print("3 - Excluir Hospital/Setor/Quarto/Leito")
        print("4 - Visualizar Hospital/Setor/Quarto/Leito")
        print("5 - Voltar ao menu anterior")

        opcao = input("Opção escolhida: ")

        if opcao == "1":
            headerMenu("Adicionar", "Selecione o que você quer adicionar")
            print("1 - Adicionar Hospital")
            print("2 - Adicionar Setor")
            print("3 - Adicionar Quarto")
            print("4 - Adicionar Leito")
            print("5 - Voltar ao menu anterior")
            opcao = input("Opção escolhida: ")

            if opcao == "1":
                headerMenu("Hospitais", "Insira os dados para adicionar um novo hospital")
                db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="pL"
                )
                cursor = db.cursor()
                nome_hospital = input("Digite o nome completo do hospital: ")
                sql = "INSERT INTO tbHospitais (nomeHosp) VALUES (%s)"
                val = (nome_hospital,)
                cursor.execute(sql, val)
                db.commit()
                print(cursor.rowcount, "registro(s) adicionado(s) com sucesso.")

            elif opcao == "2":
                headerMenu("Setores", "Insira os dados para adicionar um novo setor")
                while True:
                    mostrar_hospitais()
                    hospital_id = input("Selecione o ID do hospital: ")
                    setor_nome = input(f"Digite o nome do setor para adicionar no hospital de ID '{hospital_id}': ")
                    db = conexaoBD()
                    cursor = db.cursor()
                    cursor.execute("SELECT nomeHosp FROM tbHospitais WHERE idHosp = %s", (hospital_id,))
                    result = cursor.fetchone()
                    if result is None:
                        print("ID do hospital inválido.")
                    else:
                        hosp_nome = result[0]
                        cursor.execute("INSERT INTO tbSetores (hospSetor, nomeSetor) VALUES (%s, %s)", (hosp_nome, setor_nome))
                        db.commit()
                        print("Setor adicionado com sucesso!")
                    db.close()
                    opcao = input("Deseja adicionar outro setor para este hospital? (S/N) ")
                    if opcao.lower() != "s":
                        break
            elif opcao == "3":
                headerMenu("Quartos", "Insira os dados para adicionar um novo quarto")
                mostrar_hospitais()
                hospital_id = input("Selecione o ID do hospital: ")
                db = conexaoBD()
                cursor = db.cursor()
                cursor.execute("SELECT nomeHosp FROM tbHospitais WHERE idHosp = %s", (hospital_id,))
                result = cursor.fetchone()
                if result is None:
                    print("ID do hospital inválido.")
                    db.close()
                    continue
                hospital_nome = result[0]
                mostrar_setores(hospital_id)
                setor_id = input("Selecione o ID do setor: ")
                cursor.execute("SELECT nomeSetor FROM tbSetores WHERE idSetor = %s", (setor_id,))
                result = cursor.fetchone()
                if result is None:
                    print("ID do setor inválido.")
                    db.close()
                    continue
                setor_nome = result[0]
                quarto_nome = input(f"Digite o nome do quarto para adicionar em '{hospital_nome} - {setor_nome}': ")
                cursor.execute("INSERT INTO tbQuartos (hospQuarto, setorQuarto, nomeQuarto) VALUES (%s, %s, %s)", (hospital_nome, setor_nome, quarto_nome))
                db.commit()
                print("Quarto adicionado com sucesso!")
                db.close()
                opcao = input("Deseja adicionar outro quarto para este setor? (S/N) ")
                if opcao.lower() != "s":
                    break


            elif opcao == "3":
                adQuarto()
            elif opcao == "4":
                filaDeEspera()
            elif opcao == "5":
                configuracoes()
            elif opcao == "6":
                fecharPlantao()
            else:
                print("Opção inválida. Tente novamente.\n")

        elif opcao == "2":
            print("1 - Atualizar Hospital")
            print("2 - Atualizar Setor")
            print("3 - Atualizar Quarto")
            print("4 - Atualizar Leito")
            print("5 - Voltar ao menu anterior")
        elif opcao == "3":
            print("1 - Excluir Hospital")
            print("2 - Excluir Setor")
            print("3 - Excluir Quarto")
            print("4 - Excluir Leito")
            print("5 - Voltar ao menu anterior")
        elif opcao == "4":
            print("1 - Excluir Hospital")
            print("2 - Excluir Setor")
            print("3 - Excluir Quarto")
            print("4 - Excluir Leito")
            print("5 - Voltar ao menu anterior")
        elif opcao == "5":
            return
        else:
            print("Opção inválida. Tente novamente.\n")

menuInicial()