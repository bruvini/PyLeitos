#Importações de bibliotecas
import time
import mysql.connector

#Definição das funções

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
def gerenciarHospitais ():
    while True:
        print("Digite apenas o número da opção desejada: ")
        print("1 - Visualizar hospitais")
        print("2 - Adicionar um hospital")
        print("3 - Atualizar um hospital")
        print("4 - Excluir um hospital")
        print("5 - Voltar ao menu anterior")


        opcao = input("Opção escolhida: ")

        if opcao == "1":
            print("Essa é a lista de hospitais já cadastrados: \n")

            db = conexaobd()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM tabelaHospitais")
            result = cursor.fetchall()
            contador = 0
            for row in result:
                print(row)
            cursor.close()
            db.close()
            return
            
        elif opcao == "2":
            nomeHospital = input("Digite o nome do hospital sem abreviações: ")
            db = conexaobd()
            cursor = db.cursor()
            cursor.execute("INSERT INTO tabelaHospitais (nomeHospital) VALUES (%s)", (nomeHospital,))
            db.commit()
            print(cursor.rowcount, "Registro adicionado")
            cursor.close()
            db.close()
            return

        elif opcao == "3":
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
            return
        
        elif opcao == "4":
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
            return
        
        elif opcao == "5":
            print("Voltando para o menu anterior\n")
            return
        
        else:
            print("Opção inválida. Tente novamente!\n")

#gerenciar as configurações
def menuConfiguracao ():
    while True:
        print("Digite apenas o número da opção desejada: ")
        print("1 - Gerenciar Hospitais")
        print("2 - Gerenciar Setores")
        print("3 - Gerenciar Leitos")
        print("4 - Voltar ao menu principal")

        opcao = input("Opção escolhida: ")

        if opcao == "1":
            gerenciarHospitais ()
        elif opcao == "2":
            print("Abrindo gerenciamento dos setores\n")
        elif opcao == "3":
            print("Abrindo gerenciamento dos leitos\n")
        elif opcao == "4":
            print("Voltando para o menu principal\n")
            return
        else:
            print("Opção inválida. Tente novamente!\n")

print ("Olá, seja bem-vindo ao Sistema PyLeitos")
print ("Um sistema para gerenciamento de leitos no CHT")
time.sleep(0.5)

while True:
    print("Digite apenas o número da opção desejada: ")
    print("1 - Iniciar Plantão")
    print("2 - Transferir paciente")
    print("3 - Remanejar paciente")
    print("4 - Fechar plantão")
    print("5 - Configurações")

    opcao = input("Opção escolhida: ")

    if opcao == "1":
        print("Vamos iniciar o plantão\n")
    elif opcao == "2":
        print("Vamos transferir um paciente\n")
    elif opcao == "3":
        print("Vamos remanejar um paciente\n")
    elif opcao == "4":
        print("Vamos fechar o plantão\n")
    elif opcao == "5":
        print("Abrindo menu de configuração\n")
        menuConfiguracao()
    else:
        print("Opção inválida. Tente novamente!\n")