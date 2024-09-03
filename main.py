import agendamento_servicos

def menu():
    while True:
        opcao = agendamento_servicos.exibir_menu_principal()

        if opcao == '1':
            while True:
                opcao_mecanicos = agendamento_servicos.exibir_menu_mecanicos()
                if opcao_mecanicos == '1':
                    agendamento_servicos.adicionar_mecanico()
                elif opcao_mecanicos == '2':
                    agendamento_servicos.listar_mecanicos()
                elif opcao_mecanicos == '3':
                    agendamento_servicos.remover_mecanico()
                elif opcao_mecanicos == '4':
                    if agendamento_servicos.mecanicos:
                        print("\nMecânicos disponíveis:")
                        contador = 1
                        for mecanico in agendamento_servicos.mecanicos:
                            print(f"    => Mecânico {contador} - {mecanico['nome']}")
                            contador += 1
                        while True:
                            escolha_mecanico = input("\nDigite o número do mecânico que deseja editar: ")
                            if escolha_mecanico.isdigit():
                                escolha_mecanico = int(escolha_mecanico)
                                if 1 <= escolha_mecanico <= len(agendamento_servicos.mecanicos):
                                    mecanico_escolhido = agendamento_servicos.mecanicos[escolha_mecanico - 1]
                                    agendamento_servicos.editar_mecanico(mecanico_escolhido)
                                    break
                                else:
                                    print("\nOpção inválida. Digite um número válido da lista.")
                            else:
                                print("\nEntrada inválida. Digite um número inteiro.")
                    else:
                        print("\nNão existem mecânicos cadastrados!")
                        input("\nPressione Enter para continuar...")
                elif opcao_mecanicos == '5':
                    break
                elif opcao_mecanicos == '6':
                    print("\nSaindo do programa...")
                    exit()
                else:
                    print("\nOpção inválida!")

        elif opcao == '2':
            while True:
                agendamento_servicos.mecanicos
                opcao_servicos = agendamento_servicos.exibir_menu_servicos()
                if opcao_servicos == '1':
                    agendamento_servicos.adicionar_servico()
                elif opcao_servicos == '2':
                    agendamento_servicos.listar_servicos()
                elif opcao_servicos == '3':
                    agendamento_servicos.remover_servico()
                elif opcao_servicos == '4':
                    if agendamento_servicos.servicos:
                        print("\nServiços disponíveis:")
                        contador = 1
                        for servico in agendamento_servicos.servicos:
                            print(f"    => Serviço {contador} - {servico['tema']}")
                            print(f"    Descrição: {servico['descricao']}")
                            print(f"    Mecânico responsável: {servico['mecanico']['nome']}")
                            contador += 1
                        while True:
                            escolha_servico = input("\nDigite o número do serviço que deseja editar: ")
                            if escolha_servico.isdigit():
                                escolha_servico = int(escolha_servico)
                                if 1 <= escolha_servico <= len(agendamento_servicos.servicos):
                                    servico_escolhido = agendamento_servicos.servicos[escolha_servico - 1]
                                    agendamento_servicos.editar_servico(servico_escolhido)
                                    break
                                else:
                                    print("\nOpção inválida. Digite um número válido da lista.")
                            else:
                                print("\nEntrada inválida. Digite um número inteiro.")
                    else:
                        print("\nNão existem serviços adicionados!")
                        input("\nPressione Enter para continuar...")
                elif opcao_servicos == '5':
                    break
                elif opcao_servicos == '6':
                    print("\nSaindo do programa...")
                    exit()
                else:
                    print("\npção inválida!")

        elif opcao == '3':
            print("\nSaindo do programa...")
            break
        else:
            quantidade_opcoes_menu_principal = 3
            print(f"\nOpção inválida! Selecione uma das {quantidade_opcoes_menu_principal} opcões.")

if __name__ == '__main__':
    menu()
