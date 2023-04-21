#Importações de bibliotecas
import time
import mysql.connector
import sqlite3

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

def listarHospitais():
    db = conexaobd()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tabelaHospitais")
    hospitais = cursor.fetchall()
    return hospitais

def listarSetores(idHosp):
    db = conexaobd()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tabelaSetores WHERE idHosp=%s", (idHosp,))
    setores = cursor.fetchall()
    return setores

def listarQuartos(idSetor):
    db = conexaobd()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tabelaQuartos WHERE idSetor=%s", (idSetor,))
    quartos = cursor.fetchall()
    return quartos

def listarLeitos(idQuarto):
    db = conexaobd()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tabelaLeitos WHERE idQuarto=%s", (idQuarto,))
    leitos = cursor.fetchall()
    return leitos

def atualizarNumQuarto(idQuarto, novoNumQuarto):
    db = conexaobd()
    cursor = db.cursor()
    cursor.execute("UPDATE tabelaQuartos SET numQuarto=%s WHERE idQuarto=%s", (novoNumQuarto, idQuarto,))
    db.commit()
    return cursor.rowcount

def atualizarDisponibilidade(idLeito, novaDisponibilidade):
    db = conexaobd()
    cursor = db.cursor()
    cursor.execute("UPDATE tabelaLeitos SET disponibilidade=%s WHERE idLeito=%s", (novaDisponibilidade, idLeito,))
    db.commit()
    return cursor.rowcount

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
    criar_borda()
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
    criar_borda()
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
    criar_borda()
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
    criar_borda()
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

# Função para gerenciar os quartos
def gerenciarQuartos():
    while True:
        criar_borda()
        print("GERENCIAMENTO DE LEITOS")
        print("Digite apenas o número da opção desejada:")
        print("1 - Visualizar Quartos")
        print("2 - Adicionar Quarto")
        print("3 - Atualizar Quarto")
        print("4 - Excluir Quarto")
        print("5 - Voltar ao menu anterior")

        opcao = input("Opção escolhida: ")

        if opcao == "1":
            visualizarQuartos()
        elif opcao == "2":
            adicionarQuarto()
        elif opcao == "3":
            atualizarQuarto()
        elif opcao == "4":
            excluirQuarto()
        elif opcao == "5":
            return
        else:
            print("Opção inválida. Tente novamente!")

def visualizarQuartos():
    mydb = conexaobd()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM tabelaHospitais")
    hospitais = mycursor.fetchall()
    for hosp in hospitais:
        print(hosp[0], hosp[1])
    hosp_id = input("Selecione um hospital pelo ID: ")
    mycursor.execute("SELECT * FROM tabelaSetores WHERE idHosp = %s", (hosp_id,))
    setores = mycursor.fetchall()
    for setor in setores:
        print(setor[0], setor[1])
    setor_id = input("Selecione um setor pelo ID: ")
    mycursor.execute("SELECT * FROM tabelaQuartos WHERE idSetor = %s", (setor_id,))
    quartos = mycursor.fetchall()
    for quarto in quartos:
        print(quarto[0], quarto[1])

def adicionarQuarto():
    # Lista hospitais e solicita escolha
    mydb = conexaobd()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM tabelaHospitais")
    hospitais = cursor.fetchall()
    print("Escolha o hospital:")
    for hospital in hospitais:
        print(hospital[0], "-", hospital[1])
    escolha_hospital = input("Digite o número do hospital escolhido: ")
    while not escolha_hospital.isdigit() or int(escolha_hospital) not in range(1, len(hospitais) + 1):
        escolha_hospital = input("Opção inválida, digite novamente: ")
    id_hospital = hospitais[int(escolha_hospital) - 1][0]
    
    # Lista setores do hospital escolhido e solicita escolha
    cursor.execute(f"SELECT * FROM tabelaSetores WHERE idHosp = {id_hospital}")
    setores = cursor.fetchall()
    print("Escolha o setor:")
    for setor in setores:
        print(setor[0], "-", setor[1])
    escolha_setor = input("Digite o número do setor escolhido: ")
    while not escolha_setor.isdigit() or int(escolha_setor) not in range(1, len(setores) + 1):
        escolha_setor = input("Opção inválida, digite novamente: ")
    id_setor = setores[int(escolha_setor) - 1][0]
    
    # Lista quartos do setor escolhido e solicita número do quarto
    cursor.execute(f"SELECT * FROM tabelaQuartos WHERE idSetor = {id_setor}")
    quartos = cursor.fetchall()
    print("Quartos do setor selecionado:")
    for quarto in quartos:
        print(quarto[0], "-", quarto[1])
    numero_quarto = input("Digite o número do novo quarto: ")
    
    # Insere novo quarto na tabelaQuartos
    cursor.execute(f"INSERT INTO tabelaQuartos (nomeQuarto, idSetor) VALUES ('{numero_quarto}', {id_setor})")
    mydb.commit()
    print("Quarto adicionado com sucesso!")
    
    cursor.close()

def atualizarQuarto():
    # Conecta ao banco de dados
    db = conexaobd()
    cursor = db.cursor()

    # Seleciona um hospital
    cursor.execute("SELECT idHosp, nomeHospital FROM tabelaHospitais")
    hospitais = cursor.fetchall()
    print("Selecione um hospital:")
    for hospital in hospitais:
        print(f"{hospital[0]} - {hospital[1]}")
    idHosp = int(input("Digite o ID do hospital desejado: "))

    # Seleciona um setor do hospital escolhido
    cursor.execute("SELECT idSetor, nomeSetor FROM tabelaSetores WHERE idHosp = %s", (idHosp,))
    setores = cursor.fetchall()
    print("Selecione um setor:")
    for setor in setores:
        print(f"{setor[0]} - {setor[1]}")
    idSetor = int(input("Digite o ID do setor desejado: "))

    # Seleciona os quartos do setor escolhido
    cursor.execute("SELECT idQuarto, nomeQuarto FROM tabelaQuartos WHERE idSetor = %s", (idSetor,))
    quartos = cursor.fetchall()
    print("Selecione um quarto:")
    for quarto in quartos:
        print(f"{quarto[0]} - {quarto[1]}")
    idQuarto = int(input("Digite o ID do quarto desejado: "))

    # Altera o nome do quarto selecionado
    novoNome = input("Digite o novo nome do quarto: ")
    cursor.execute("UPDATE tabelaQuartos SET nomeQuarto = %s WHERE idQuarto = %s", (novoNome, idQuarto))

    # Confirma a alteração no banco de dados
    db.commit()

    # Fecha a conexão
    cursor.close()
    db.close()

    print("Quarto atualizado com sucesso!")

def excluirQuarto():
    # Conectando ao banco de dados
    db = conexaobd()    
    # Criando o cursor
    cursor = db.cursor()
    
    # Listando os hospitais
    cursor.execute("SELECT * FROM tabelaHospitais")
    hospitais = cursor.fetchall()
    
    # Verificando se existem hospitais cadastrados
    if not hospitais:
        print("Nenhum hospital cadastrado.")
        return
    
    # Exibindo a lista de hospitais e solicitando a seleção do usuário
    print("Selecione um hospital:")
    for hospital in hospitais:
        print(f"{hospital[0]}. {hospital[1]}")
    idHosp = int(input("Digite o ID do hospital desejado: "))
    
    # Listando os setores deste hospital
    cursor.execute("SELECT * FROM tabelaSetores WHERE idHosp=%s", (idHosp,))
    setores = cursor.fetchall()
    
    # Verificando se existem setores cadastrados para este hospital
    if not setores:
        print("Nenhum setor cadastrado para este hospital.")
        return
    
    # Exibindo a lista de setores e solicitando a seleção do usuário
    print("Selecione um setor:")
    for setor in setores:
        print(f"{setor[0]}. {setor[1]}")
    idSetor = int(input("Digite o ID do setor desejado: "))
    
    # Listando os quartos deste setor
    cursor.execute("SELECT * FROM tabelaQuartos WHERE idSetor=%s", (idSetor,))
    quartos = cursor.fetchall()
    
    # Verificando se existem quartos cadastrados para este setor
    if not quartos:
        print("Nenhum quarto cadastrado para este setor.")
        return
    
    # Exibindo a lista de quartos e solicitando a seleção do usuário
    print("Selecione um quarto:")
    for quarto in quartos:
        print(f"{quarto[0]}. {quarto[1]}")
    idQuarto = int(input("Digite o ID do quarto desejado: "))
    
    # Verificando se existem leitos vinculados a este quarto
    cursor.execute("SELECT * FROM tabelaLeitos WHERE idQuarto=%s", (idQuarto,))
    leitos = cursor.fetchall()
    
    if leitos:
        # Se existirem leitos, perguntar ao usuário se deseja apagar todos os leitos deste quarto
        print(f"O quarto selecionado possui {len(leitos)} leitos vinculados.")
        confirm = input("Deseja apagar todos os leitos deste quarto? (s/n): ")
        
        if confirm.lower() == "s":
            # Apagando todos os leitos deste quarto
            cursor.execute("DELETE FROM tabelaLeitos WHERE idQuarto=%s", (idQuarto,))
            db.commit()
            print(f"{len(leitos)} leitos apagados.")
        else:
            # Caso contrário, não é possível excluir o quarto
            print("Operação cancelada pelo usuário.")
            return
    
    # Excluindo o quarto selecionado
    cursor.execute("DELETE FROM tabelaQuartos WHERE idQuarto=%s", (idQuarto,))
    db.commit()
    print("Quarto excluído com sucesso.")

# Função para gerenciar os leitos
def gerenciarLeitos():
    while True:
        criar_borda()
        print("GERENCIAMENTO DE LEITOS")
        print("Digite apenas o número da opção desejada:")
        print("1 - Visualizar Leitos")
        print("2 - Adicionar Leitos")
        print("3 - Atualizar Leitos")
        print("4 - Excluir Leitos")
        print("5 - Voltar ao menu anterior")

        opcao = input("Opção escolhida: ")

        if opcao == "1":
            visualizarLeitos()
        elif opcao == "2":
            adicionarLeito()
        elif opcao == "3":
            atualizarLeito()
        elif opcao == "4":
            excluirLeito()
        elif opcao == "5":
            return
        else:
            print("Opção inválida. Tente novamente!")

def adicionarLeito():
    hospitais = listarHospitais()
    if not hospitais:
        print("Nenhum hospital cadastrado.")
        return
    
    print("Selecione um hospital:")
    for hospital in hospitais:
        print(f"{hospital[0]}. {hospital[1]}")
    idHosp = int(input("Digite o ID do hospital desejado: "))
    
    setores = listarSetores(idHosp)
    if not setores:
        print("Nenhum setor cadastrado para este hospital.")
        return
    
    print("Selecione um setor:")
    for setor in setores:
        print(f"{setor[0]}. {setor[1]}")
    idSetor = int(input("Digite o ID do setor desejado: "))
    
    quartos = listarQuartos(idSetor)
    if not quartos:
        print("Nenhum quarto cadastrado para este setor.")
        return
    
    print("Selecione um quarto:")
    for quarto in quartos:
        print(f"{quarto[0]}. {quarto[1]}")
    idQuarto = int(input("Digite o ID do quarto desejado: "))
    
    while True:
        numLeito = input("Digite o número do leito: ")
        disponibilidade = input("O quarto está ativo? (s/n): ")
        if disponibilidade.lower() == "s":
            disponibilidade = "ATIVO"
        else:
            disponibilidade = "INATIVO"
        
        db = conexaobd()
        cursor = db.cursor()
        cursor.execute("INSERT INTO tabelaLeitos (numLeito, disponibilidade, idQuarto) VALUES (%s, %s, %s)", (numLeito, disponibilidade, idQuarto))
        db.commit()
        print("Leito adicionado com sucesso!")
        
        resposta = input("Deseja adicionar mais um leito? (s/n): ")
        if resposta.lower() != "s":
            break

def visualizarLeitos():
    hospitais = listarHospitais()
    if not hospitais:
        print("Nenhum hospital cadastrado.")
        return
    
    for hospital in hospitais:
        print(f"Hospital: {hospital[1]}")
        idHosp = hospital[0]
        
        setores = listarSetores(idHosp)
        if not setores:
            print("\tNenhum setor cadastrado para este hospital.")
            continue
        
        for setor in setores:
            print(f"\tSetor: {setor[1]}")
            idSetor = setor[0]
            
            quartos = listarQuartos(idSetor)
            if not quartos:
                print("\t\tNenhum quarto cadastrado para este setor.")
                continue
            
            for quarto in quartos:
                print(f"\t\tQuarto: {quarto[1]}")
                idQuarto = quarto[0]
                
                db = conexaobd()
                cursor = db.cursor()
                cursor.execute("SELECT * FROM tabelaLeitos WHERE idQuarto=%s ORDER BY numLeito ASC", (idQuarto,))
                leitos = cursor.fetchall()
                
                if not leitos:
                    print("\t\t\tNenhum leito cadastrado para este quarto.")
                    continue
                
                for leito in leitos:
                    print(f"\t\t\tLeito: {leito[1]} | Disponibilidade: {leito[2]}")
                
    return

def atualizarLeito():
    # Seleciona um hospital
    hospitais = listarHospitais()
    print("Selecione um hospital:")
    for hospital in hospitais:
        print(hospital[0], "-", hospital[1])
    idHosp = input("Digite o ID do hospital desejado: ")
    
    # Seleciona um setor do hospital selecionado
    setores = listarSetores(idHosp)
    print("\nSelecione um setor:")
    for setor in setores:
        print(setor[0], "-", setor[1])
    idSetor = input("Digite o ID do setor desejado: ")
    
    # Lista todos os quartos do setor selecionado
    quartos = listarQuartos(idSetor)
    print("\nQuartos do setor selecionado:")
    for quarto in quartos:
        print(quarto[0], "-", quarto[1])
        
        # Lista todos os leitos do quarto selecionado
        leitos = listarLeitos(quarto[0])
        for leito in leitos:
            print("\tLeito", leito[1], "-", leito[2])
            
            # Solicita qual leito deseja atualizar
            idLeito = leito[0]
            escolha = input("Deseja atualizar o leito " + str(leito[1]) + "? (S/N)")
            if escolha.upper() == "S":
                alterarQuarto = False
                alterarDisp = False
                
                # Verifica se deseja alterar o número do quarto
                escolha = input("Deseja alterar o número do quarto? (S/N)")
                if escolha.upper() == "S":
                    novoNumQuarto = input("Digite o novo número do quarto: ")
                    atualizarNumQuarto(idQuarto=quarto[0], novoNumQuarto=novoNumQuarto)
                    alterarQuarto = True
                
                # Verifica se deseja alterar a disponibilidade
                escolha = input("Deseja alterar a disponibilidade? (S/N)")
                if escolha.upper() == "S":
                    disponibilidade = "ATIVO" if leito[2] == "INATIVO" else "INATIVO"
                    atualizarDisponibilidade(idLeito=idLeito, novaDisponibilidade=disponibilidade)
                    alterarDisp = True
                
                if alterarQuarto and alterarDisp:
                    print("Leito atualizado com sucesso! (Número do quarto e disponibilidade)")
                elif alterarQuarto:
                    print("Leito atualizado com sucesso! (Número do quarto)")
                elif alterarDisp:
                    print("Leito atualizado com sucesso! (Disponibilidade)")
                else:
                    print("Nenhuma alteração realizada.")

def excluirLeito():
    # Listar hospitais e pedir para usuário selecionar um
    hospitais = listarHospitais()
    print("Selecione um hospital para continuar: ")
    for hosp in hospitais:
        print(f"{hosp[0]} - {hosp[1]}")
    idHosp = int(input("Digite o ID do hospital desejado: "))
    
    # Listar setores do hospital selecionado e pedir para usuário selecionar um
    setores = listarSetores(idHosp)
    print("\nSelecione um setor para continuar: ")
    for setor in setores:
        print(f"{setor[0]} - {setor[1]}")
    idSetor = int(input("Digite o ID do setor desejado: "))
    
    # Listar quartos do setor selecionado e pedir para usuário selecionar um
    quartos = listarQuartos(idSetor)
    print("\nSelecione um quarto para continuar: ")
    for quarto in quartos:
        print(f"{quarto[0]} - {quarto[1]}")
    idQuarto = int(input("Digite o ID do quarto desejado: "))
    
    # Listar leitos do quarto selecionado e pedir para usuário selecionar um
    leitos = listarLeitos(idQuarto)
    print("\nSelecione um leito para excluir: ")
    for leito in leitos:
        print(f"{leito[0]} - {quarto[1]}-{leito[1]} - {leito[2]}")
    idLeito = int(input("Digite o ID do leito desejado: "))
    
    # Excluir leito selecionado
    db = conexaobd()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tabelaLeitos WHERE idLeito=%s", (idLeito,))
    db.commit()
    
    print("Leito excluído com sucesso!")


# Função para o menu de configuração
def menuConfiguracao():
    while True:
        criar_borda()
        print("                 MENU DE CONFIGURAÇÃO                ")
        criar_borda()
        print("Digite apenas o número da opção desejada: ")
        print("1 - Gerenciar Hospitais")
        print("2 - Gerenciar Setores")
        print("3 - Gerenciar Quartos")
        print("4 - Gerenciar Leitos")
        print("5 - Voltar ao menu principal")
        opcao = input("Opção escolhida: ")

        if opcao == "1":
            gerenciarHospitais()
        elif opcao == "2":
            gerenciarSetores()
        elif opcao == "3":
            gerenciarQuartos()
        elif opcao == "4":
            gerenciarLeitos()
        elif opcao == "5":
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