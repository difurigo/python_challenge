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
                    agendamento_servicos.editar_mecanico()
                elif opcao_mecanicos == '5':
                    agendamento_servicos.exportar_mecanicos_para_json()
                elif opcao_mecanicos == '6':
                    break
                elif opcao_mecanicos == '7':
                    agendamento_servicos.sair_do_programa()
                    exit()
                else:
                    print("\nOpção inválida!")
                    input("\nPressione Enter para retornar...")

        elif opcao == '2':
            while True:
                opcao_servicos = agendamento_servicos.exibir_menu_servicos()
                if opcao_servicos == '1':
                    agendamento_servicos.adicionar_servico()
                elif opcao_servicos == '2':
                    agendamento_servicos.listar_servicos()
                elif opcao_servicos == '3':
                    agendamento_servicos.remover_servico()
                elif opcao_servicos == '4':
                    agendamento_servicos.editar_servico()
                elif opcao_servicos == '5':
                    agendamento_servicos.exportar_servicos_para_json()
                elif opcao_servicos == '6':
                    break
                elif opcao_servicos == '7':
                    agendamento_servicos.sair_do_programa()
                    exit()
                else:
                    print("\nOpção inválida!")
                    input("\nPressione Enter para retornar...")

        elif opcao == '3':
            agendamento_servicos.sair_do_programa()
            break
        else:
            quantidade_opcoes_menu_principal = 3
            print(f"\nOpção inválida! Selecione uma das {quantidade_opcoes_menu_principal} opcões.")
            input("\nPressione Enter para retornar...")
            
if __name__ == '__main__':
    menu()
