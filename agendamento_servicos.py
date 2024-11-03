import os
import re
from datetime import datetime
import json
import time
import oracledb
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

'''
NÃO ESQUEÇA DE CRIAR A TABELA PROF!!

AQUI ESTÁ O SQL DE CRIAÇÃO PARA O SENHOR UTILIZAR NO BANCO:
CREATE TABLE tb_mecanico (
    id_mecanico INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_mecanico VARCHAR(150), 
    especialidade VARCHAR(150), 
    telefone VARCHAR(15), 
    email VARCHAR(50), 
    horarios VARCHAR(500),
    endereco VARCHAR(500)
)

CREATE TABLE tb_servico (
    id_servico INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tema VARCHAR2(100) NOT NULL,
    descricao VARCHAR2(255),
    data_servico DATE,
    hora_servico VARCHAR2(5),
    id_mecanico NUMBER,
    FOREIGN KEY (id_mecanico) REFERENCES tb_mecanico(id_mecanico)
)
'''

with open(r'arquivos_banco/secret.json', 'r') as secret:
    credenciais = json.load(secret)
    
    usr = credenciais['user']
    pwd = credenciais['password']
    dsn = credenciais['dsn']

servicos = []

sender_email = 'faditfiap@gmail.com'
sender_password = 'qxkw ohlj oqdy fwiu'

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
    print("5) Exportar lista de mecânicos para um arquivo JSON")
    print("6) Voltar para o menu principal")
    print("7) Sair do programa")
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
    print("5) Exportar lista de serviços para um arquivo JSON")
    print("6) Voltar para o menu principal")
    print("7) Sair do programa")
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

def validar_cep(texto_input):
    cep = input(texto_input).strip().replace("-", "")
    cep_digito = cep.isdigit()
    while cep_digito == False:
        print("Válido apenas números ou traços!")
        cep = input(texto_input).strip().replace("-", "")
        cep_digito = cep.isdigit()
    return cep.strip()

def consultar_cep(cep):
    try:
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        if response.status_code == 200:
            return response.json()
        else:
            print("Erro ao consultar o CEP.")
    except Exception as e:
        print(f"Erro ao conectar na API de CEP: {e}")
    return None
      
# Funções para as opções do menu dos mecânicos
def adicionar_mecanico():
    campos = []

    nome = validar_nome("Digite o nome completo do novo mecânico: ")
    campos.append(nome)

    especialidade = validar_especialidade("Digite a especialidade do mecânico (ex: Linha Diesel): ")
    campos.append(especialidade)

    telefone = validar_telefone("Digite o telefone do mecânico com o DDD (ex: 11987654321): ")
    campos.append(telefone)

    email = validar_email("Digite o email do mecânico (ex: mecanico@email.com): ")
    campos.append(email)

    print("\nHorario de atendimento disponível:")
    horarios = []
    inserir_horarios(horarios)
    
    horario_string = ''
    for horario in horarios:
        for k, v in horario.items():
            horario_string += f'{k}: {v}, '

    horario_string = horario_string[:-2]
    campos.append(horario_string)

    cep = validar_cep("Digite o CEP do mecânico ou da oficina que se encontra (ex: 00000-000): ")
    endereco = consultar_cep(cep)
    del endereco['unidade']
    del endereco['complemento']
    del endereco['ibge']
    del endereco['gia']
    del endereco['siafi']
        
    endereco_string = ''
    for k, v in endereco.items():
        endereco_string += f'{k}: {v}, '

    endereco_string = endereco_string[:-2]
    campos.append(endereco_string)

    sql_insert_mecanico = '''
    INSERT INTO tb_mecanico (nome_mecanico, especialidade, telefone, email, horarios, endereco)
    VALUES (:1, :2, :3, :4, :5, :6)
    '''

    # Conecta ao banco e executa a inserção
    with oracledb.connect(dsn=dsn, user=usr, password=pwd) as conn:
        cursor_oracle = conn.cursor()
        cursor_oracle.execute(sql_insert_mecanico, campos)
        conn.commit()

    print("\nMecânico adicionado com sucesso!")
    input("\nPressione Enter para continuar...")

def listar_mecanicos():
    with oracledb.connect(dsn=dsn, user=usr, password=pwd) as conn:
        cursor_oracle = conn.cursor()
        cursor_oracle.execute("SELECT id_mecanico, nome_mecanico, especialidade, telefone, email, horarios, endereco FROM tb_mecanico")
        mecanicos = cursor_oracle.fetchall()

        if mecanicos:
            print("\n| Mecânicos adicionados |")
            for id_mecanico, nome, especialidade, telefone, email, horarios, endereco in mecanicos:
                print(f"\nMecânico ID: {id_mecanico}")
                print(f"Nome: {nome}")
                print(f"Especialidade: {especialidade}")
                print(f"Telefone: {telefone}")
                print(f"Email: {email}")
                print("\nEndereço:")
                for i in endereco.split(","):
                    print(f"  => {i.strip()}")
                print("\nHorários disponíveis:")
                for horario in horarios.split(','):
                    print(f"  - {horario.strip()}")
            input("\nPressione Enter para continuar...")
        else:
            print("\nNão existem mecânicos adicionados!")
            input("\nPressione Enter para continuar...")
        
def editar_mecanico():
    with oracledb.connect(dsn=dsn, user=usr, password=pwd) as conn:
        cursor_oracle = conn.cursor()
        cursor_oracle.execute("SELECT COUNT(*) FROM tb_mecanico")
        if cursor_oracle.fetchone()[0] == 0:
            print("\nNão existem mecânicos cadastrados!")
            input("\nPressione Enter para continuar...")
            return

    listar_mecanicos()
    mecanico_id = input("\nDigite o ID do mecânico que deseja editar: ")

    with oracledb.connect(dsn=dsn, user=usr, password=pwd) as conn:
        cursor_oracle = conn.cursor()
        
        # Recupera o mecânico selecionado
        cursor_oracle.execute("SELECT nome_mecanico, especialidade, telefone, email, horarios FROM tb_mecanico WHERE id_mecanico = :1", [mecanico_id])
        mecanico = cursor_oracle.fetchone()
        
        if not mecanico:
            print("Mecânico não encontrado.")
            input("\nPressione Enter para continuar...")
            return

        nome, especialidade, telefone, email, horarios = mecanico

        print(f"\n1) Nome: {nome}")
        print(f"2) Especialidade: {especialidade}")
        print(f"3) Telefone: {telefone}")
        print(f"4) Email: {email}")
        print(f"5) Horários: {horarios}")

        campos = input("\nEscolha o número do campo que deseja editar (separado por vírgulas): ").replace(" ", "").split(",")
        novos_valores = []

        for opcao in campos:
            if opcao == '1':
                novo_nome = validar_nome("Digite o novo nome do mecânico: ")
                novos_valores.append(("nome_mecanico", novo_nome))

            elif opcao == '2':
                nova_especialidade = validar_especialidade("Digite a nova especialidade do mecânico: ")
                novos_valores.append(("especialidade", nova_especialidade))

            elif opcao == '3':
                novo_telefone = validar_telefone("Digite o novo telefone do mecânico: ")
                novos_valores.append(("telefone", novo_telefone))

            elif opcao == '4':
                novo_email = validar_email("Digite o novo email do mecânico: ")
                novos_valores.append(("email", novo_email))

            elif opcao == '5':
                novos_horarios = []
                inserir_horarios(novos_horarios)
                horario_string = ', '.join([f"{k}: {v}" for h in novos_horarios for k, v in h.items()])
                novos_valores.append(("horarios", horario_string))

        # Executa a atualização para cada campo alterado
        for campo, valor in novos_valores:
            cursor_oracle.execute(f"UPDATE tb_mecanico SET {campo} = :1 WHERE id_mecanico = :2", [valor, mecanico_id])

        conn.commit()
        print("\nMecânico atualizado com sucesso!")
        input("\nPressione Enter para continuar...")

def remover_mecanico():
    with oracledb.connect(dsn=dsn, user=usr, password=pwd) as conn:
        cursor_oracle = conn.cursor()

        cursor_oracle.execute("SELECT COUNT(*) FROM tb_mecanico")
        if cursor_oracle.fetchone()[0] == 0:
            print("\nNão existem mecânicos cadastrados para remover!")
            input("\nPressione Enter para continuar...")
            return

        listar_mecanicos()
        mecanico_id = input("\nDigite o ID do mecânico que deseja remover: ")
        confirmacao = input("Tem certeza que deseja remover este mecânico? (s/n): ").strip().lower()

        if confirmacao == 's':
            cursor_oracle.execute("DELETE FROM tb_servico WHERE id_mecanico = :1", [mecanico_id])
            cursor_oracle.execute("DELETE FROM tb_mecanico WHERE id_mecanico = :1", [mecanico_id])
            conn.commit()
            print("\nMecânico e seus serviços removidos com sucesso!")
        else:
            print("\nOperação de remoção cancelada.")

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
        descricao = input(f"{texto_input}")
        while descricao == "":
            print("A descrição do serviço não pode ser vazia!")
            descricao = input(f"{texto_input}")
        while descricao.isdigit():
            print("\nA descrição do serviço não pode ser números.")
            descricao = input(f"{texto_input}")
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
    horas_validas = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
        
    minutos_validos = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']

    while True:
        try:
            hora = input(texto_input).strip()
                
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
def adicionar_servico():
    with oracledb.connect(dsn=dsn, user=usr, password=pwd) as conn:
        cursor_oracle = conn.cursor()
        
        # Listar mecânicos disponíveis
        cursor_oracle.execute("SELECT id_mecanico, nome_mecanico, email FROM tb_mecanico")
        mecanicos = cursor_oracle.fetchall()
        
        if mecanicos:
            print("\nMecânicos disponíveis:")
            for id, (id_mecanico, nome, email) in enumerate(mecanicos, start=1):
                print(f"    => Mecânico {id} - {nome} (Email: {email})")
            
            # Solicita a escolha do mecânico
            while True:
                escolha_mecanico = input("\nDigite o número do mecânico escolhido: ")
                if escolha_mecanico.isdigit() and 1 <= int(escolha_mecanico) <= len(mecanicos):
                    id_mecanico_escolhido = mecanicos[int(escolha_mecanico) - 1][0]
                    nome = mecanicos[int(escolha_mecanico) - 1][1]
                    email_mecanico = mecanicos[int(escolha_mecanico) - 1][2]
                    break
                else:
                    print("\nOpção inválida. Digite um número válido da lista.")
        
            # Recebe os dados do serviço
            tema = validar_tema("Digite o tema do serviço à realizar (ex: Troca de Bicos): ")  
            descricao = validar_descricao("Digite a descrição do serviço à realizar: ")
            data = validar_data("Digite a data da realização do serviço (ex: DD/MM/AAAA): ")
            hora = validar_hora("Digite a hora da realização do serviço (ex: HH:MM): ")

            # Insere o serviço no banco
            cursor_oracle.execute(""" 
                INSERT INTO tb_servico (tema, descricao, data_servico, hora_servico, id_mecanico) 
                VALUES (:tema, :descricao, TO_DATE(:data, 'DD/MM/YYYY'), :hora, :id_mecanico) 
            """, [tema, descricao, data, hora, id_mecanico_escolhido])

            conn.commit()
            print("\nServiço adicionado com sucesso!")

            # Enviar e-mail ao mecânico
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email_mecanico
            msg['Subject'] = f"Novo Serviço Agendado: {tema}"

            body = f"""
            Olá, {nome}!

            Você tem um novo serviço agendado:
            Tema: {tema}
            Descrição: {descricao}
            Data: {data}
            Hora: {hora}

            Atenciosamente,
            Portal AutoCare
            """
            msg.attach(MIMEText(body, 'plain'))

            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.send_message(msg)
                print("Notificação de e-mail enviada ao mecânico!")
                input("\nPressione Enter para continuar...")
            except Exception as e:
                print(f"Erro ao enviar e-mail: {e}")
                input("\nPressione Enter para continuar...")
        
        else:
            print("\nNão existem mecânicos cadastrados!")
            input("\nPressione Enter para continuar...")

def listar_servicos():
    with oracledb.connect(dsn=dsn, user=usr, password=pwd) as conn:
        cursor_oracle = conn.cursor()
        
        cursor_oracle.execute("""
            SELECT s.id_servico, s.tema, s.descricao, TO_CHAR(s.data_servico, 'DD/MM/YYYY'), s.hora_servico, m.nome_mecanico 
            FROM tb_servico s
            INNER JOIN tb_mecanico m 
            ON s.id_mecanico = m.id_mecanico
        """)
        servicos = cursor_oracle.fetchall()
        
        if servicos:
            print("\n| Serviços adicionados |")
            for id_servico, tema, descricao, data, hora, nome_mecanico in servicos:
                print(f"\nServiço ID: {id_servico}")
                print(f"Tema: {tema}")
                print(f"Descrição: {descricao}")
                print(f"Dia {data} às {hora}")
                print(f"Mecânico responsável: {nome_mecanico}")
            input("\nPressione Enter para continuar...")
        
        else:
            print("\nNão existem serviços adicionados!")
            input("\nPressione Enter para continuar...")

def editar_servico():
    with oracledb.connect(dsn=dsn, user=usr, password=pwd) as conn:
        cursor_oracle = conn.cursor()
        
        # Verifica se há serviços cadastrados
        cursor_oracle.execute("SELECT COUNT(*) FROM tb_servico")
        if cursor_oracle.fetchone()[0] == 0:
            print("\nNão existem serviços cadastrados!")
            input("\nPressione Enter para continuar...")
            return

    listar_servicos()  # Exibe a lista de serviços existentes
    servico_id = input("\nDigite o ID do serviço que deseja editar: ")

    with oracledb.connect(dsn=dsn, user=usr, password=pwd) as conn:
        cursor_oracle = conn.cursor()
        
        # Recupera o serviço selecionado
        cursor_oracle.execute("""
            SELECT tema, descricao, TO_CHAR(data_servico, 'DD/MM/YYYY'), hora_servico, id_mecanico 
            FROM tb_servico 
            WHERE id_servico = :1
        """, [servico_id])
        servico = cursor_oracle.fetchone()
        
        if not servico:
            print("\nServiço não encontrado.")
            input("\nPressione Enter para continuar...")
            return

        tema, descricao, data, hora, id_mecanico = servico

        print(f"\n1) Tema: {tema}")
        print(f"2) Descrição: {descricao}")
        print(f"3) Data: {data}")
        print(f"4) Hora: {hora}")
        print(f"5) Mecânico responsável (ID): {id_mecanico}")

        campos = input("\nEscolha o número do campo que deseja editar (separado por vírgulas): ").replace(" ", "").split(",")
        novos_valores = []

        for opcao in campos:
            if opcao == '1':
                tema = validar_tema("Digite o novo tema do serviço: ")
                novos_valores.append(("tema", tema))
            elif opcao == '2':
                descricao = validar_descricao("Digite a nova descrição do serviço: ")
                novos_valores.append(("descricao", descricao))
            elif opcao == '3':
                data = validar_data("Digite a nova data do serviço (DD/MM/AAAA): ")
                novos_valores.append(("data_servico", data))
            elif opcao == '4':
                hora = validar_hora("Digite a nova hora do serviço (HH:MM): ")
                novos_valores.append(("hora_servico", hora))
            elif opcao == '5':
                listar_mecanicos()
                id_mecanico = input("Digite o novo ID do mecânico responsável: ")
                novos_valores.append(("id_mecanico", id_mecanico))

        # Executa a atualização para cada campo alterado
        for campo, valor in novos_valores:
            cursor_oracle.execute(f"UPDATE tb_servico SET {campo} = :1 WHERE id_servico = :2", [valor, servico_id])

        conn.commit()
        print("\nServiço atualizado com sucesso!")

        # Atualiza o e-mail com as informações novas
        cursor_oracle.execute("SELECT email FROM tb_mecanico WHERE id_mecanico = :1", [id_mecanico])
        email_mecanico = cursor_oracle.fetchone()[0]

        # Prepare o e-mail com os dados atualizados
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email_mecanico
        msg['Subject'] = f"Serviço Editado: {tema}"

        body = f"""
        Olá!

        O serviço foi editado:
        Tema: {tema}
        Descrição: {descricao}
        Nova Data: {data}
        Nova Hora: {hora}

        Atenciosamente,
        Portal AutoCare
        """
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
            print("Notificação de e-mail enviada ao mecânico!")
            input("\nPressione Enter para continuar...")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            input("\nPressione Enter para continuar...")

def remover_servico():
    with oracledb.connect(dsn=dsn, user=usr, password=pwd) as conn:
        cursor_oracle = conn.cursor()
        
        # Verifica se há serviços cadastrados
        cursor_oracle.execute("SELECT COUNT(*) FROM tb_servico")
        if cursor_oracle.fetchone()[0] == 0:
            print("\nNão existem serviços cadastrados!")
            input("\nPressione Enter para continuar...")
            return

    listar_servicos()  # Exibe a lista de serviços existentes
    servico_id = input("\nDigite o ID do serviço que deseja remover: ")

    with oracledb.connect(dsn=dsn, user=usr, password=pwd) as conn:
        cursor_oracle = conn.cursor()
        
        # Verifica se o serviço existe antes de tentar removê-lo
        cursor_oracle.execute("SELECT COUNT(*) FROM tb_servico WHERE id_servico = :1", [servico_id])
        if cursor_oracle.fetchone()[0] == 0:
            print("\nServiço não encontrado!")
            input("\nPressione Enter para continuar...")
            return

        # Remove o serviço
        cursor_oracle.execute("DELETE FROM tb_servico WHERE id_servico = :1", [servico_id])
        conn.commit()

        print("\nServiço removido com sucesso!")
        input("\nPressione Enter para continuar...")

# Exportar para Json
def exportar_mecanicos_para_json():
    with oracledb.connect(dsn=dsn, user=usr, password=pwd) as conn:
        cursor_oracle = conn.cursor()
        cursor_oracle.execute("SELECT id_mecanico, nome_mecanico, especialidade, telefone, email, horarios FROM tb_mecanico")
        mecanicos = cursor_oracle.fetchall()
        
        if mecanicos:
            lista_mecanicos = []
            for id_mecanico, nome, especialidade, telefone, email, horarios in mecanicos:
                mecanico_dict = {
                    "id_mecanico": id_mecanico,
                    "nome": nome,
                    "especialidade": especialidade,
                    "telefone": telefone,
                    "email": email,
                    "horarios": horarios.split(',')
                }
                lista_mecanicos.append(mecanico_dict)

            # Salva a lista de mecânicos em um arquivo JSON
            with open('mecanicos.json', 'w') as json_file:
                json.dump(lista_mecanicos, json_file, indent=4)
                
            print("\nDados dos mecânicos exportados com sucesso para 'mecanicos.json'!")
            input("\nPressione Enter para continuar...")
        else:
            print("\nNão existem mecânicos para exportar!")
            input("\nPressione Enter para continuar...")

def exportar_servicos_para_json():
    with oracledb.connect(dsn=dsn, user=usr, password=pwd) as conn:
        cursor_oracle = conn.cursor()
        
        # Consulta todos os serviços com os dados do mecânico
        cursor_oracle.execute("""
            SELECT s.id_servico, s.tema, s.descricao, TO_CHAR(s.data_servico, 'DD/MM/YYYY'), s.hora_servico, m.nome_mecanico 
            FROM tb_servico s
            INNER JOIN tb_mecanico m 
            ON s.id_mecanico = m.id_mecanico
        """)
        servicos = cursor_oracle.fetchall()
        
        if servicos:
            lista_servicos = []
            for id_servico, tema, descricao, data, hora, nome_mecanico in servicos:
                servico_dict = {
                    "id_servico": id_servico,
                    "tema": tema,
                    "descricao": descricao,
                    "data": data,
                    "hora": hora,
                    "mecanico_responsavel": nome_mecanico
                }
                lista_servicos.append(servico_dict)

            # Salva a lista de serviços em um arquivo JSON
            with open('servicos.json', 'w') as json_file:
                json.dump(lista_servicos, json_file, indent=4)
                
            print("\nDados dos serviços exportados com sucesso para 'servicos.json'!")
            input("\nPressione Enter para continuar...")
        else:
            print("\nNão existem serviços para exportar!")
            input("\nPressione Enter para continuar...")
