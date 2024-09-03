import os
import re

'''
Remover mecânico - Valida pelo nome e isso não é legal, colocar validação por números

Horários disponíveis - Acrescentar validação para horários entre 0 e 60 min

Add serviços - Revisar método inteiro
'''

# Funções para a exibição dos menus
def exibir_menu_principal():
    limpar_terminal()
    # Menu com as opções iniciais para o gerenciamento de serviços do sistema
    print("\n>>>>>>>>>>>>>>> Portal AutoCare - Agendamento de Serviços <<<<<<<<<<<<<<<")
    print("1) Gerenciamento de Mecânicos")
    print("2) Gerenciamento de Serviços")
    print("3) Sair do programa")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    # Requisita a opção que o usuário deseja
    opcao = input("Escolha uma opção: ")
    return opcao

def limpar_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def exibir_menu_mecanicos():
    limpar_terminal()
    # Menu com as opções para o gerenciamento dos mecânicos que serão armazenados no sistema
    print("\n================== Gerenciamento de Mecânicos ==================")
    print("1) Adicionar Mecânico")
    print("2) Listar Mecânicos")
    print("3) Remover Mecânico")
    print("4) Editar Mecânico")
    print("5) Voltar para o menu principal")
    print("6) Sair do programa")
    print("================================================================")

    # Requisita a opção que o usuário deseja
    opcao = input("Escolha uma opção: ")
    return opcao

def exibir_menu_servicos():
    limpar_terminal()
    # Menu com as opções para o gerenciamento dos serviços que os mecânicos farão e serão armazenados no sistema
    print("\n================== Gerenciamento de Serviços ===================")
    print("1) Adicionar Serviço")
    print("2) Listar Serviços")
    print("3) Remover Serviço")
    print("4) Editar Serviço")
    print("5) Voltar para o menu principal")
    print("6) Sair do programa")
    print("================================================================")

    # Requisita a opção que o usuário deseja
    opcao = input("Escolha uma opção: ")
    return opcao

# Listas para armazenar mecanicos e serviços
mecanicos = []
servicos = []

def validar_telefone():
    while True:
        telefone = input("Digite o telefone do mecânico com o DDD (ex: 11987654321): ")
        try:
            if telefone == "":
                raise ValueError("O telefone do mecânico não pode ser vazio!")
            
            int(telefone)
            
            if len(telefone) != 11:
                raise ValueError("O número de telefone deve ter 11 dígitos.")
            
            return str(telefone)
        
        except ValueError as e:
            print(f"\nErro: {e}\n")

def validar_email():
    while True:
        email = input("Digite o email do mecânico (ex: mecanico@email.com): ").strip()
        if email == "":
            print("\nO email não pode ser vazio!\n")
            continue
        
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(regex, email):
            return email
        else:
            print("\nEmail inválido! Tente novamente.\n")

def validar_nome():
    nome = input("\nDigite o nome completo do novo mecânico: ").strip()
    while nome == "":
        print("O nome do mecânico não pode ser vazio!")
        nome = input("Digite o nome completo do novo mecânico: ")
    while len(nome) < 6:
        print("\nTamanho do nome deve ser maior que 5 caracteres!\n")
        nome = input("Digite o nome completo do novo mecânico: ")
    
    return nome.strip().upper()

def validar_especialidade():
    validar = True
    while validar:
        especialidade = input("Digite a especialidade do mecânico (ex: Linha Diesel): ")
        while especialidade == "":
            print("A especialidade do mecânico não pode ser vazia!")
            especialidade = input("Digite a especialidade do mecânico (ex: Linha Diesel): ")
        try:
            int(especialidade)
        except ValueError:
            validar = False
            return especialidade.strip()
        else:
            print("\nEspecialidade inválida!\n")

def inserir_horarios(horarios): # Essa função realiza o processo auxiliar que adiciona um mecânico à lista. Horários não são tão simples quanto nomes, por isso uma função única.
    # Recebe as informações do dia disponível para realizar um atendimento/serviço
    while True:
        dia_semana = input("Digite o dia da semana (ex: Segunda): ").strip().upper()
        dias_validos = ["SEGUNDA", "SEGUNDA-FEIRA", "TERÇA", "TERCA", "TERÇA-FEIRA", "TERCA-FEIRA", "QUARTA", "QUARTA-FEIRA", "QUINTA", "QUINTA-FEIRA", "SEXTA", "SEXTA-FEIRA", "SÁBADO", "SABADO", "DOMINGO"]
        
        if dia_semana not in dias_validos:
            print("\nDia da semana inválido!\n")
            continue

        while True:
            inicio = input("Digite o horário de início (ex: HH:MM): ").strip()
            fim = input("Digite o horário de fim (ex: HH:MM): ").strip()

            try:
                if not inicio or not fim:
                    raise ValueError("O campo horário não pode ser vazio!")
                
                # Validação simples para o formato de horas HH:MM
                if len(inicio) != 5 or len(fim) != 5 or inicio[2] != ':' or fim[2] != ':':
                    raise ValueError("Formato de horário inválido. Use HH:MM.")
                
                if not inicio[:2].isdigit() or not fim[:2].isdigit() or not inicio[3:].isdigit() or not fim[3:].isdigit():
                    raise ValueError("Formato de horário inválido. Use HH:MM.")

                horarios.append({"dia_semana": dia_semana, "inicio": inicio, "fim": fim})
                break  # Sai do loop de horários

            except ValueError as e:
                print(f"\nErro: {e}\n")
        
        # Oferece a opção de adicionar mais horários em diversos dias da semana
        adicionar_mais = input("\nDeseja adicionar mais horários? (s/n): ").lower().strip()
        if adicionar_mais == 'n':
            break

# Funções para as opções do menu dos mecânicos
def adicionar_mecanico(): # Essa função realiza o processo que adiciona um mecânico à lista. Ainda não tem integração com algum banco.
    # Recebendo as informações pessoais do mecânico
    nome = validar_nome()
    especialidade = validar_especialidade()
    telefone = validar_telefone()
    email = validar_email()

    # Chama a função "inserir_horarios()" recebendo essa lista de horários para o mecânico.
    print("\nHorario de atendimento disponível:")
    horarios = []
    inserir_horarios(horarios)

    # Constrói um mecânico novo à partir dos dados inseridos.
    mecanicos.append({"nome": nome, "especialidade": especialidade, "telefone": telefone.strip(), "email": email.strip(), "horarios": horarios})

    # Validação do processo
    print("\nMecânico adicionado com sucesso!")
    input("\nPressione Enter para continuar...")

def listar_mecanicos(): # Essa função lista os mecânicos existentes. 
    # Verifica se existem mecânicos e exibe uma lista deles
    if mecanicos:
        print("\n| Mecânicos adicionados |")
        contador = 1
        for mecanico in mecanicos:
            print(f"\nMecânico {contador}:")
            print(f"Nome: {mecanico['nome']}")
            print(f"Especialidade: {mecanico['especialidade']}")
            print(f"Telefone: {mecanico['telefone']}")
            print(f"Email: {mecanico['email']}")
            print("Horários disponíveis:")
            for horario in mecanico['horarios']:
                print(f"  - {horario['dia_semana']}: Das {horario['inicio']} às {horario['fim']}")
            contador += 1
    # Caso não existam, faz a validação
    else:
        print("\nNão existem mecânicos adicionados!")
        input("\nPressione Enter para continuar...")
    
    input("\nPressione Enter para continuar...")
        
def editar_mecanico(mecanico): # Essa função permite editar qualquer um dos mecânicos existentes (recebido via parâmetro).
    # Exibe as informações atuais do mecânico
    print(f"\nMecânico: {mecanico['nome']}")
    print(f"Especialidade: {mecanico['especialidade']}")
    print(f"Telefone: {mecanico['telefone']}")
    print(f"Email: {mecanico['email']}")
    print("Horários disponíveis:")
    for horario in mecanico['horarios']:
        print(f"  - {horario['dia_semana']}: Das {horario['inicio']} às {horario['fim']}")

    # Permite a alteração de cada informação pessoal
    novo_nome = input("\nDigite o novo nome do mecânico (ou deixe vazio para manter o atual): ")
    if novo_nome:
        mecanico['nome'] = novo_nome

    nova_especialidade = input("Digite a nova especialidade do mecânico (ou deixe vazio para manter a atual): ")
    if nova_especialidade:
        mecanico['especialidade'] = nova_especialidade

    novo_telefone = input("Digite o novo telefone do mecânico (ou deixe vazio para manter o atual): ")
    if novo_telefone:
        mecanico['telefone'] = novo_telefone

    novo_email = input("Digite o novo email do mecânico (ou deixe vazio para manter o atual): ")
    if novo_email:
        mecanico['email'] = novo_email

    # Faz a validação
    print("\nServiço atualizado com sucesso!")
    input("\nPressione Enter para continuar...")

def remover_mecanico(): # Essa função permite remover qualquer um dos mecânicos existentes.
    # Se existerem mecânicos pede o nome do mecânico à ser removido
    if mecanicos:
        nome = input("\nDigite o nome do mecânico a ser removido: ")

        # Procura o nome do mecânico na lista
        for mecanico in mecanicos:
            if mecanico['nome'] == nome:
                
                # Remove e valida
                mecanicos.remove(mecanico)
                print("\nMecânico removido com sucesso!")
                input("\nPressione Enter para continuar...")
                return
            
        # Caso não encontre o nome
        print("\nMecânico não encontrado!")
        input("\nPressione Enter para continuar...")
    
    # Caso não existam, faz a validação
    else:
        print("\nNão existem mecânicos adicionados!")
        input("\nPressione Enter para continuar...")

# Funções para as opções do menu de serviços
def adicionar_servico(): # Essa função realiza o processo que relaciona um novo serviço à um mecânico e adiciona o serviço à lista. Ainda não tem integração com algum banco.
    # Verifica se há mecânicos e faz inicia exibindo resumidamente cada um
    if mecanicos:
        print("\nMecânicos disponíveis:")
        contador = 1
        for mecanico in mecanicos:
            print(f"    => Mecânico {contador} - {mecanico['nome']}")
            contador += 1
        
        # Depois pede para o usuário escolher um e verifica se a escolha faz sentido
        while True:
            escolha_mecanico = input("\nDigite o número do mecânico escolhido: ")
            if escolha_mecanico.isdigit():
                escolha_mecanico = int(escolha_mecanico)
                if 1 <= escolha_mecanico <= len(mecanicos):
                    mecanico_escolhido = mecanicos[escolha_mecanico - 1]
                    break
                else:
                    print("\nOpção inválida. Digite um número válido da lista.")
            else:
                print("\nEntrada inválida. Digite um número inteiro.")

        # Inicia o processo de recebimento das informações do novo serviço
        tema = input("\nDigite o tema do serviço à realizar (ex: Troca de Bicos): ")
        while tema == "":
            print("O tema do serviço não pode ser vazio!")
            tema = input("Digite o tema do serviço à realizar (ex: Troca de Bicos): ")
        
        descricao = input("Digite a descrição do serviço à realizar: ")
        while descricao == "":
            print("A descrição do serviço não pode ser vazia!")
            descricao = input("Digite a descrição do serviço à realizar: ")

        data = input("Digite a data da realização do serviço (ex: DD/MM/AAAA): ")
        while data == "":
            print("A data do serviço não pode ser vazia!")
            data = input("Digite a data da realização do serviço (ex: DD/MM/AAAA): ")
        
        hora = input("Digite a hora da realização do serviço (ex: HH:MM): ")
        while hora == "":
            print("A hora do serviço não pode ser vazia!")
            hora = input("Digite a hora da realização do serviço (ex: HH:MM): ")

        # Adiciona na lista o novo serviço
        servicos.append(
            {"tema": tema, 
            "descricao": descricao, 
            "data": data, 
            "hora": hora,
            "mecanico": mecanico_escolhido})

        # Realiza a validação
        print("\nServiço adicionado com sucesso!")
        input("\nPressione Enter para continuar...")

    # Caso não existam mecânicos para adicionar o serviço
    else:
        print("\nNão existem mecânicos cadastrados!")
        input("\nPressione Enter para continuar...")

def listar_servicos(): # Essa função lista os serviços existentes.
    # Verifica se existem mecânicos e exibe uma lista deles
    if servicos:
        print("\n| Serviços adicionados |")
        contador = 1
        for servico in servicos:
            print(f"\nServiço {contador}:")
            print(f"Tema: {servico['tema']}")
            print(f"Descrição: {servico['descricao']}")
            print(f"Dia {servico['data']} às {servico['hora']}")
            print(f"Mecânico responsável: {servico['mecanico']['nome']}")
            contador += 1
    # Caso não existam, faz a validação
    else:
        print("\nNão existem serviços adicionados!")
        input("\nPressione Enter para continuar...")
    
    input("\nPressione Enter para continuar...")

def editar_servico(servico): # Essa função permite editar qualquer um dos serviços existentes (recebido via parâmetro).
    # Exibe as informações atuais do serviço
    print(f"\nServiço: {servico['tema']}")
    print(f"Descrição: {servico['descricao']}")
    print(f"Data: {servico['data']}")
    print(f"Hora: {servico['hora']}")
    print(f"Mecânico responsável: {servico['mecanico']['nome']}")

    # Permite a alteração de cada campo
    novo_tema = input("\nDigite o novo tema do serviço (ou deixe vazio para manter o atual): ")
    if novo_tema:
        servico['tema'] = novo_tema

    nova_descricao = input("Digite a nova descrição do serviço (ou deixe vazio para manter a atual): ")
    if nova_descricao:
        servico['descricao'] = nova_descricao

    nova_data = input("Digite a nova data do serviço (ou deixe vazio para manter a atual): ")
    if nova_data:
        servico['data'] = nova_data
    
    nova_hora = input("Digite a nova data do serviço (ou deixe vazio para manter a atual): ")
    if nova_hora:
        servico['hora'] = nova_hora

    # Realiza a validação
    print("\nServiço atualizado com sucesso!")
    input("\nPressione Enter para continuar...")

def remover_servico(): # Essa função permite remover qualquer um dos serviços existentes.
    # Se existerem serviços, chama a função "listar_serviços()" e pede o número correspondendente ao serviço
    if servicos:
        listar_servicos()
        opcao = int(input("\nDigite o numero correspondente ao serviço a ser removido: "))
        if 1 <= opcao <= len(servicos):

            # Se a escolha estiver dentro da lista, faz a remoção do serviço e valida
            servicos.pop(opcao - 1)
            print("\nServiço removido com sucesso!")
            input("\nPressione Enter para continuar...")
            return
        
        # Caso o que foi recebido não esteja na lista
        else:
            print("\nServiço não encontrado!")
            input("\nPressione Enter para continuar...")
    
    # Caso não existam serviços na lista
    else:
        print("\nNão existem serviços adicionados!")
        input("\nPressione Enter para continuar...")
