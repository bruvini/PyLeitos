#Importações de bibliotecas
import time
import mysql.connector

#Definição das funções

# Função para criar uma borda na tela
def criar_borda():
    print("=" * 60)

# Função para pausar a tela
def pausar_tela():
    time.sleep(1)
    print("\n")

#conexão com o banco de dados mysql
def conexaobd():
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="pyleitos"
    )
    return db

#gerenciar hospitais
def gerenciarHospitais():
    while True:
        criar_borda()
        print("GERENCIAR HOSPITAIS\n")
        print("Digite apenas o número da opção desejada: ")
        print("1 - Visualizar hospitais")
        print("2 - Adicionar um hospital")
        print("3 - Atualizar um hospital")
        print("4 - Excluir um hospital")
        print("5 - Voltar ao menu anterior")
        criar_borda()

        opcao = input("Opção escolhida: ")

        if opcao == "1":
            criar_borda()
            print("VISUALIZAR HOSPITAIS\n")
            db = conexaobd()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM tabelaHospitais")
            result = cursor.fetchall()
            contador = 0
            for row in result:
                print(row)
            cursor.close()
            db.close()
            pausar_tela()
            
        elif opcao == "2":
            criar_borda()
            print("ADICIONAR HOSPITAL\n")
            nomeHospital = input("Digite o nome do hospital sem abreviações: ")
            db = conexaobd()
            cursor = db.cursor()
            cursor.execute("INSERT INTO tabelaHospitais (nomeHospital) VALUES (%s)", (nomeHospital,))
            db.commit()
            print(cursor.rowcount, "Registro adicionado")
            cursor.close()
            db.close()
            pausar_tela()

        elif opcao == "3":
            criar_borda()
            print("ATUALIZAR HOSPITAL\n")
            db = conexaobd()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM tabelaHospitais")
            result = cursor.fetchall()
            for row in result:
                print(row)
            hospital_id = input("Selecione o ID do hospital que quer atualizar: ")
            hospital_novoNome = input("Digite o novo nome para esse Hospital: ")
            cursor.execute("UPDATE tabelaHospitais SET nomeHospital=%s WHERE idHosp=%s", (hospital_novoNome, hospital_id))
            db.commit()
            print(cursor.rowcount, "Registro atualizado")
            cursor.close()
            db.close()
            pausar_tela()
        
        elif opcao == "4":
            criar_borda()
            print("EXCLUIR HOSPITAL\n")
            db = conexaobd()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM tabelaHospitais")
            result = cursor.fetchall()
            for row in result:
                print(row)
            idHospital = input("Selecione o ID do hospital que quer excluir: ")
            cursor.execute("DELETE FROM tabelaHospitais WHERE idHosp=%s", (idHospital,))
            db.commit()
            print(cursor.rowcount, "Registro deletado")
            cursor.close()
            db.close()
            pausar_tela()
        
        elif opcao == "5":
            print("Voltando para o menu anterior\n")
            return
        
        else:
            criar_borda()
            print("Opção inválida. Tente novamente!\n")
            pausar_tela()

# Função para gerenciar os setores
def gerenciarSetores():
    while True:
        criar_borda()
        print("GERENCIAMENTO DE SETORES")
        print("Digite apenas o número da opção desejada:")
        print("1 - Visualizar Setores")
        print("2 - Adicionar Setor")
        print("3 - Atualizar Setor")
        print("4 - Excluir Setor")
        print("5 - Voltar ao menu anterior")

        opcao = input("Opção escolhida: ")

        if opcao == "1":
            visualizarSetores()
        elif opcao == "2":
            adicionarSetor()
        elif opcao == "3":
            atualizarSetor()
        elif opcao == "4":
            excluirSetor()
        elif opcao == "5":
            return
        else:
            print("Opção inválida. Tente novamente!")

def visualizarSetores():
    db = conexaobd()
    cursor = db.cursor()
    cursor.execute("SELECT tabelaHospitais.nomeHospital, tabelaSetores.idSetor, tabelaSetores.nomeSetor FROM tabelaHospitais INNER JOIN tabelaSetores ON tabelaHospitais.idHosp = tabelaSetores.idHosp ORDER BY tabelaHospitais.nomeHospital, tabelaSetores.nomeSetor")
    result = cursor.fetchall()

    if not result:
        print("Não há setores cadastrados!")
    else:
        hosp_antigo = ""
        for hosp, idSetor, nomeSetor in result:
            if hosp != hosp_antigo:
                print(f"{hosp}:")
                hosp_antigo = hosp
            print(f"ID Setor: {idSetor} | Nome Setor: {nomeSetor}")
        pausar_tela()

def adicionarSetor():
    nomeSetor = input("Digite o nome do setor a ser adicionado: ")
    db = conexaobd()
    cursor = db.cursor()
    cursor.execute("SELECT idHosp, nomeHospital FROM tabelaHospitais")
    result = cursor.fetchall()

    if not result:
        print("Não há hospitais cadastrados!")
    else:
        print("Hospitais disponíveis:")
        for idHosp, nomeHosp in result:
            print(f"ID Hospital: {idHosp} | Nome Hospital: {nomeHosp}")
        idHosp = input("Digite o ID do hospital ao qual o setor será vinculado: ")

        db = conexaobd()
        cursor = db.cursor()
        cursor.execute("INSERT INTO tabelaSetores (nomeSetor, idHosp) VALUES (%s, %s)", (nomeSetor, idHosp))
        db.commit()
        print("Setor adicionado com sucesso!")
        pausar_tela()

def atualizarSetor():
    # mostra a lista de hospitais
    db = conexaobd()
    cursor = db.cursor()
    cursor.execute("SELECT idHosp, nomeHospital FROM tabelaHospitais")
    hospitais = cursor.fetchall()
    if hospitais:
        print("Selecione o hospital:")
        for hospital in hospitais:
            print(f"{hospital[0]} - {hospital[1]}")
        idHosp = input("ID do hospital selecionado: ")
        # mostra a lista de setores do hospital selecionado
        cursor.execute("SELECT idSetor, nomeSetor FROM tabelaSetores WHERE idHosp = %s", (idHosp,))
        setores = cursor.fetchall()
        if setores:
            print("Selecione o setor:")
            for setor in setores:
                print(f"{setor[0]} - {setor[1]}")
            idSetor = input("ID do setor selecionado: ")
            novoNomeSetor = input("Digite o novo nome do setor: ")
            # atualiza o nome do setor
            cursor.execute("UPDATE tabelaSetores SET nomeSetor = %s WHERE idSetor = %s", (novoNomeSetor, idSetor))
            db.commit()
            if cursor.rowcount == 0:
                print("ID de setor não encontrado. Nenhum setor foi atualizado.")
            else:
                print("Setor atualizado com sucesso!")
        else:
            print("Não há setores cadastrados para este hospital.")
    else:
        print("Não há hospitais cadastrados.")
    pausar_tela()

def excluirSetor():
    db = conexaobd()
    cursor = db.cursor()

    # mostra a lista de hospitais
    cursor.execute("SELECT idHosp, nomeHospital FROM tabelaHospitais")
    hospitais = cursor.fetchall()
    if hospitais:
        print("Selecione o hospital:")
        for hospital in hospitais:
            print(f"{hospital[0]} - {hospital[1]}")
        idHosp = input("ID do hospital selecionado: ")
        # mostra a lista de setores do hospital selecionado
        cursor.execute("SELECT idSetor, nomeSetor FROM tabelaSetores WHERE idHosp = %s", (idHosp,))
        setores = cursor.fetchall()
        if setores:
            print("Selecione o setor a ser excluído:")
            for setor in setores:
                print(f"{setor[0]} - {setor[1]}")
            idSetor = input("ID do setor selecionado: ")
            # confirmação da exclusão
            confirmacao = input("Tem certeza que deseja excluir o setor selecionado? (S/N): ")
            if confirmacao.upper() == "S":
                cursor.execute("DELETE FROM tabelaSetores WHERE idSetor = %s", (idSetor,))
                db.commit()
                if cursor.rowcount == 0:
                    print("ID de setor não encontrado. Nenhum setor foi excluído.")
                else:
                    print("Setor excluído com sucesso!")
            else:
                print("Operação cancelada pelo usuário.")
        else:
            print("Não há setores cadastrados para este hospital.")
    else:
        print("Não há hospitais cadastrados.")
    pausar_tela()

# Função para gerenciar os leitos
def gerenciarLeitos():
    print("Gerenciando leitos...\n")
    # Adicione aqui o código para gerenciar os leitos

# Função para o menu de configuração
def menuConfiguracao():
    while True:
        criar_borda()
        print("                 MENU DE CONFIGURAÇÃO                ")
        criar_borda()
        print("Digite apenas o número da opção desejada: ")
        print("1 - Gerenciar Hospitais")
        print("2 - Gerenciar Setores")
        print("3 - Gerenciar Leitos")
        print("4 - Voltar ao menu principal")
        opcao = input("Opção escolhida: ")

        if opcao == "1":
            gerenciarHospitais()
        elif opcao == "2":
            gerenciarSetores()
        elif opcao == "3":
            gerenciarLeitos()
        elif opcao == "4":
            print("Voltando para o menu principal...\n")
            return
        else:
            print("Opção inválida. Tente novamente!\n")
        pausar_tela()

# Função para o menu principal
def menuPrincipal():
    while True:
        criar_borda()
        print("               SISTEMA PYLEITOS - MENU PRINCIPAL               ")
        criar_borda()
        print("Digite apenas o número da opção desejada: ")
        print("1 - Iniciar Plantão")
        print("2 - Transferir paciente")
        print("3 - Remanejar paciente")
        print("4 - Fila de espera")
        print("5 - Fechar plantão")
        print("6 - Configurações")
        opcao = input("Opção escolhida: ")

        if opcao == "1":
            print("Iniciando plantão...\n")
        elif opcao == "2":
            print("Transferindo paciente...\n")
        elif opcao == "3":
            print("Remanejando paciente...\n")
        elif opcao == "4":
            print("Abrindo fila de espera...\n")
        elif opcao == "5":
            print("Fechando plantão...\n")
        elif opcao == "6":
            print("Abrindo menu de configuração...\n")
            menuConfiguracao()
        else:
            print("Opção inválida. Tente novamente!\n")
        pausar_tela()

# Programa principal
criar_borda()
print("             SISTEMA PYLEITOS - BEM-VINDO             ")
criar_borda()
print("Um sistema para gerenciamento de leitos no CHT")
pausar_tela()

menuPrincipal()