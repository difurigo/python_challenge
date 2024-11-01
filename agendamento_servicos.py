import os
import re
from datetime import datetime
import json
import time

# Tratamento dos dados
with open(r'Base-Mecânicos/mecanicos.json', 'r', encoding='utf-8') as arquivo_json:
    mecanicos = json.load(arquivo_json)

for mecanico in mecanicos:
    nome_alterado = mecanico['nome'].upper()
    mecanico['nome'] = nome_alterado

servicos = []

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

def sair_do_programa():
        print("\nSaindo do programa...")
        time.sleep(1.2)
        print("Volte sempre!")

# Funcionalidades do programa
def validar_telefone(texto_input):
    while True:
        telefone = input(texto_input)
        try:
            if telefone == "":
                raise ValueError("O telefone do mecânico não pode ser vazio!")
            
            int(telefone)
            
            if len(telefone) != 11:
                raise ValueError("O número de telefone deve ter 11 dígitos.")
            
            telefone = str(telefone)
            telefone_formatado = f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
            return telefone_formatado
        
        except ValueError as e:
            print(f"\nErro: {e}\n")

def validar_email(texto_input):
    while True:
        email = input(texto_input).strip()
        if email == "":
            print("\nO email não pode ser vazio!\n")
            continue
        
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(regex, email):
            return email
        else:
            print("\nEmail inválido! Tente novamente.\n")

def validar_nome(texto_input):
    nome = input(f"\n{texto_input}").strip()
    while nome == "":
        print("O nome do mecânico não pode ser vazio!")
        nome = input()
    while len(nome) < 6:
        print("\nTamanho do nome deve ser maior que 5 caracteres!\n")
        nome = input(texto_input)
    while nome.isdigit():
        print("\nO nome do mecânico não podem ser números.\n")
        nome = input(texto_input)
    
    return nome.strip().upper()

def validar_especialidade(texto_input):
    validar = True
    while validar:
        especialidade = input(texto_input)
        while especialidade == "":
            print("A especialidade do mecânico não pode ser vazia!")
            especialidade = input(texto_input)
        while especialidade.isdigit():
            print("\nA especialidade do mecânico não pode ser números.\n")
            especialidade = input(texto_input)
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
        
        horas_validas = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
        
        minutos_validos = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
        
        if dia_semana not in dias_validos:
            print("\nDia da semana inválido!\n")
            continue

        while True:
            try:
                inicio = input("Digite o horário de início (ex: HH:MM): ").strip()
                fim = input("Digite o horário de fim (ex: HH:MM): ").strip()
                
                if not inicio[:2] in horas_validas or not fim[:2] in horas_validas:
                    raise ValueError('Horários inválidos. Insira horários possíveis.')
                
                if not inicio[3:] in minutos_validos or not fim[3:] in minutos_validos:
                    raise ValueError('Horários inválidos. Insira horários possíveis.')

                if not inicio or not fim:
                    raise ValueError("O campo horário não pode ser vazio!")
                
                # Validação simples para o formato de horas HH:MM
                if len(inicio) != 5 or len(fim) != 5 or inicio[2] != ':' or fim[2] != ':':
                    raise TypeError("Algun(s) formato(s) de horário inválido(s). Use HH:MM.")
                
                if not inicio[:2].isdigit() or not fim[:2].isdigit() or not inicio[3:].isdigit() or not fim[3:].isdigit():
                    raise TypeError("Algun(s) formato(s) de horário inválido(s). Use HH:MM.")

                horarios.append({"dia_semana": dia_semana, "inicio": inicio, "fim": fim})
                break  # Sai do loop de horários

            except Exception as e:
                print(f"\nErro: {e}\n")
        
        # Oferece a opção de adicionar mais horários em diversos dias da semana
        adicionar_mais = input("\nDeseja adicionar mais horários? (s/n): ").lower().strip()
        if adicionar_mais == 'n':
            break

# Funções para as opções do menu dos mecânicos
def adicionar_mecanico(): # Essa função realiza o processo que adiciona um mecânico à lista. Ainda não tem integração com algum banco.
    # Recebendo as informações pessoais do mecânico
    nome = validar_nome("Digite o nome completo do novo mecânico: ")
    especialidade = validar_especialidade("Digite a especialidade do mecânico (ex: Linha Diesel): ")
    telefone = validar_telefone("Digite o telefone do mecânico com o DDD (ex: 11987654321): ")
    email = validar_email("Digite o email do mecânico (ex: mecanico@email.com): ")

    # Chama a função "inserir_horarios()" recebendo essa lista de horários para o mecânico.
    print("\nHorario de atendimento disponível:")
    horarios = []
    inserir_horarios(horarios)

    # Constrói um mecânico novo à partir dos dados inseridos.
    mecanicos.append({"nome": nome, "especialidade": especialidade, "telefone": telefone.strip(), "email": email.strip(), "horarios": horarios})

    # Validação do processo
    print("\nMecânico adicionado com sucesso!")
    input("\nPressione Enter para continuar...")

    # with open(r'Base-Mecânicos/mecanicos.json', 'w', encoding='utf-8') as arquivo_json:
    #     json.dump(mecanicos, arquivo_json)

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
        
        input("\nPressione Enter para continuar...")

    # Caso não existam, faz a validação
    else:
        print("\nNão existem mecânicos adicionados!")
        input("\nPressione Enter para continuar...")
        
def editar_mecanico(mecanico): # Essa função permite editar qualquer um dos mecânicos existentes (recebido via parâmetro).
    # Exibe as informações atuais do mecânico
    print(f"\n1) Mecânico: {mecanico['nome']}")
    print(f"2) Especialidade: {mecanico['especialidade']}")
    print(f"3) Telefone: {mecanico['telefone']}")
    print(f"4) Email: {mecanico['email']}")
    print("Horários disponíveis:")
    for horario in mecanico['horarios']:
        print(f" - {horario['dia_semana']}: Das {horario['inicio']} às {horario['fim']}")

    print("\nEscolha o número do campo que deseja editar (Para mais de um campo, separe por vírgulas")
    campos = input("Campo(s): ")
    campos = campos.replace(" ", "")

    if "," in campos:
        campos = campos.split(",")

    if not isinstance(campos, list):
        list(campos)

    for opcao in campos:
        if opcao == '1':
            # Permite a alteração de cada informação pessoal
            novo_nome = validar_nome("Digite o novo nome do mecânico: ")
            mecanico['nome'] = novo_nome

        elif opcao == '2':
            nova_especialidade = validar_especialidade("Digite a nova especialidade do mecânico: ")
            mecanico['especialidade'] = nova_especialidade

        elif opcao == '3':
            novo_telefone = validar_telefone("Digite o novo telefone do mecânico: ")
            mecanico['telefone'] = novo_telefone

        elif opcao == '4':
            novo_email = validar_email("Digite o novo email do mecânico: ")
            mecanico['email'] = novo_email
        
        else:
            print("Opção inválida. Escolha uma opção válida.")

    # Faz a validação
    print("\nServiço atualizado com sucesso!")
    input("\nPressione Enter para continuar...")

    # with open(r'Base-Mecânicos/mecanicos.json', 'w', encoding='utf-8') as arquivo_json:
    #     json.dump(mecanicos, arquivo_json)

def remover_mecanico(): # Essa função permite remover qualquer um dos mecânicos existentes.
    # Se existerem mecânicos pede o nome do mecânico à ser removido
    if mecanicos:
        print("\nMecânicos disponíveis:")
        contador = 1
        for mecanico in mecanicos:
            print(f"    => Mecânico {contador} - {mecanico['nome']}")
            contador += 1
        while True:
            escolha_mecanico = input("\nDigite o número do mecânico que deseja remover: ")
            if escolha_mecanico.isdigit():
                escolha_mecanico = int(escolha_mecanico)
                if 1 <= escolha_mecanico <= len(mecanicos):
                    mecanico_escolhido = mecanicos[escolha_mecanico - 1]
                    mecanicos.remove(mecanico_escolhido)
                    print("\nMecânico removido com sucesso!")
                    input("\nPressione Enter para continuar...")

                    # with open(r'Base-Mecânicos/mecanicos.json', 'w', encoding='utf-8') as arquivo_json:
                    #     json.dump(mecanicos, arquivo_json)
                    return
                else:
                    print("\nOpção inválida. Digite um número válido da lista.")
            else:
                print("\nEntrada inválida. Digite apenas números inteiros.")
    else:
        print("\nNão existem mecânicos cadastrados!")
        input("\nPressione Enter para continuar...") 

# Funcionalidades do programa
def validar_tema(texto_input):  
    validar = True
    while validar:
        tema = input(f"\n{texto_input}")
        while tema == "":
            print("O tema do serviço não pode ser vazio!")
            tema = input(f"\n{texto_input}")
        while tema.isdigit():
            print("\nO tema do serviço não pode ser números.")
            tema = input(f"\n{texto_input}")
        try:
            int(tema)
        except ValueError:
            validar = False
            return tema.strip().upper()
        else:
            print("\nTema inválido!")

def validar_descricao(texto_input):
    validar = True
    while validar:
        descricao = input(f"\n{texto_input}")
        while descricao == "":
            print("A descrição do serviço não pode ser vazia!")
            descricao = input(f"\n{texto_input}")
        while descricao.isdigit():
            print("\nA descrição do serviço não pode ser números.")
            descricao = input(f"\n{texto_input}")
        try:
            int(descricao)
        except ValueError:
            validar = False
            return descricao.strip()
        else:
            print("\nDescrição inválida!")

def validar_data(texto_input):
    while True:
        data = input(texto_input).strip()
        
        if not data:
            print("A data do serviço não pode ser vazia!")
            continue
        
        try:
            data_validada = datetime.strptime(data, "%d/%m/%Y")
            return data_validada.strftime("%d/%m/%Y")
        except ValueError:
            print("\nData inválida. Certifique-se de seguir o formato DD/MM/AAAA e que a data seja válida.\n")

def validar_hora(texto_input):
    hora = input(texto_input)
    horas_validas = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
        
    minutos_validos = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']

    while True:
        try:
            hora = input("Digite o horário de início (ex: HH:MM): ").strip()
                
            if not hora[:2] in horas_validas :
                raise ValueError('Horários inválidos. Insira horários possíveis.')
                
            if not hora[3:] in minutos_validos:
                 raise ValueError('Horários inválidos. Insira horários possíveis.')
            
            if not hora:
                raise ValueError("O campo horário não pode ser vazio!")
                
            # Validação simples para o formato de horas HH:MM
            if len(hora) != 5 or hora[2] != ':':
                raise TypeError("Algun(s) formato(s) de horário inválido(s). Use HH:MM.")
                
            if not hora[:2].isdigit() or not hora[3:].isdigit():
                raise TypeError("Algun(s) formato(s) de horário inválido(s). Use HH:MM.")
            
            return hora.strip()

        except Exception as e:
            print(f"\nErro: {e}\n")

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
        tema = validar_tema("Digite o tema do serviço à realizar (ex: Troca de Bicos): ")  
        descricao = validar_descricao("Digite a descrição do serviço à realizar: ")
        data = validar_data("Digite a data da realização do serviço (ex: DD/MM/AAAA): ")
        hora = validar_hora("Digite a hora da realização do serviço (ex: HH:MM): ")

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

            input("\nPressione Enter para continuar...")

    # Caso não existam, faz a validação
    else:
        print("\nNão existem serviços adicionados!")
        input("\nPressione Enter para continuar...")

def editar_servico(servico): # Essa função permite editar qualquer um dos serviços existentes (recebido via parâmetro).
    # Exibe as informações atuais do serviço
    print(f"\n1) Serviço: {servico['tema']}")
    print(f"2) Descrição: {servico['descricao']}")
    print(f"3) Data: {servico['data']}")
    print(f"4) Hora: {servico['hora']}")
    print(f"5) Mecânico responsável: {servico['mecanico']['nome']}")

    print("\nEscolha o número do campo que deseja editar (Para mais de um campo, separe por vírgulas")
    campos = input("Campo(s): ")
    campos = campos.replace(" ", "")
    
    if "," in campos:
        campos = campos.split(",")

    if not isinstance(campos, list):
        list(campos)

    for opcao in campos:
        if opcao == '1':
            # Permite a alteração de cada campo
            novo_tema = validar_tema("Digite o novo tema do serviço: ")
            servico['tema'] = novo_tema

        elif opcao == '2':
            nova_descricao = validar_descricao("Digite a nova descrição do serviço: ")
            servico['descricao'] = nova_descricao

        elif opcao == '3':
            nova_data = validar_data("Digite a nova data do serviço: ")
            servico['data'] = nova_data
        
        elif opcao == '4':
            nova_hora = validar_hora("Digite a nova data do serviço: ")
            servico['hora'] = nova_hora

        else:
            print("Opção inválida. Escolha uma opção válida.")
        
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
