import PySimpleGUI as sg
import json # Biblioteca para trabalhar com arquivo json
import os # Biblioteca que fornece funcionalidades para interagir com o sistema operacional, usado para verificar arquivo

# Salvando o caminho do arquivo de tarefas
ARQUIVO_TAREFAS = 'Tarefas.json'

# Função para carregar as tarefas
def carregar_tarefas():
    """Carrega as tarefas do arquivo JSON"""
    # Checando se existe o arquivo Tarefas.json
    if os.path.exists(ARQUIVO_TAREFAS):
        # Abrindo o arquivo Tarefas.json no modo r(read) ou seja, modo leitura e salva na variavel f
        with open(ARQUIVO_TAREFAS, 'r') as f:
            try:
                # Então ele vai salvar o conteudo de leitura encontrado no json e salvar na variavel tarefas
                tarefas = json.load(f)
                return tarefas
            # Captura uma exeção caso o arquivo estaja invalido
            except json.JSONDecodeError:
                return []  # Retorna uma lista vazia se o JSON estiver vazio ou inválido
    return [{'texto': 'Tarefa padrão', 'marcado': False}]  # Caso não exista um arquivo Tarefas.json ele cria esse arquivo com uma lista com tendo uma tarefa padrão

# Função para salvar tarefas passando como argumento as tarefas que estão na interface
def salvar_tarefas(tarefas):
    """Salva as tarefas no arquivo JSON"""
    # Abrindo o arquivo Tarefas.json no modo w(write) ou seja, modo escrita e salva na variavel f
    with open(ARQUIVO_TAREFAS, 'w') as f:
            # Aqui ele abre o json no modo escrita passado pela f, indenta a escrita para 4 linhas para se tornar mais legivel, e pega as tarefas passada pelo parametro para passar no json
        json.dump(tarefas, f, indent=4)

# Criando o layout
def criar_janela_inicial(tarefas):
    # Define o tema da interface
    sg.theme('DarkBlue4')
    layout = [
        [sg.Frame('Tarefas', layout=[
            #  Aqui cria um check box com o texte da tarefa, que por padrão quando é criado ele vem marcaod como false e recebe uma chave que é o nome da tarefa mais o 'tarefa_' no começo
            # E abilita que os eventos sejam gerando quando o checkbox mudar
            [sg.Checkbox(tarefa['texto'], default=tarefa.get('marcado', False), key=f'tarefa_{tarefa["texto"]}', enable_events=True)]
            # Aqui ele cria um checkbox para cada tarefa do arquivo json
            for tarefa in tarefas
        ], key='container')],
        # Botões para adicionar uma nova tarefa e resetar a lista de tarefas
        [sg.Button('Nova Tarefa'), sg.Button('Resetar')]
    ]
    # retorna  criando a janela com o layout definido, tamanho ajustavel e finalize serve garantir que todos os elementos sejam finalizados e prontos para uso
    return sg.Window('Todo List', layout=layout, size=(800, 600), resizable=True, finalize=True)



# EXECUÇÃO DA APLICAÇÃO

# Salva todas as tarefas ja salvas no arquivo em uma variavel para carregar na tela
tarefas = carregar_tarefas()

# Criar a janela com as tarefas carregadas
janela = criar_janela_inicial(tarefas)

# Loop infinito que mantem a aplicação em execução atá a janela ser fechada
while True:
    # Leitor de eventos e valor dos elementos da janela
    event, values = janela.read()
    # Se a janela for fechada sai do loop
    if event == sg.WIN_CLOSED:
        break
    # Verifica se o botão Nova Tarefa foi pressionado
    if event == 'Nova Tarefa':
        # Exibe um pop up para o usuario inserir a nova tarefa, e salva na variavel nova_tarefa
        nova_tarefa = sg.popup_get_text('Digite o texto da nova tarefa:')
        # Verifica se o usario escreveu algum texto
        if nova_tarefa:
            # Adicione a nova tarefa dinamicamente no layout container
            janela.extend_layout(janela['container'], [[sg.Checkbox(nova_tarefa, key=f'tarefa_{nova_tarefa}', enable_events=True)]])
            # Atualizar a lista de tarefas que aparece na tela
            tarefas.append({'texto': nova_tarefa, 'marcado': False})
            # Salvar as tarefas no arquivo json após adicionar uma nova tarefa
            salvar_tarefas(tarefas)

            # Atualização do Estado de uma Tarefa

    # Verifica se o evento está relaiconado com a checkbocx de alguma tarefa
    elif event.startswith('tarefa_'):
        # Extrai o texto da tarefa a partir do nome do evento
        texto = event[len('tarefa_'):]
        # Leitura sobre toda a lista de tarefas
        for tarefa in tarefas:
            # if para encontrar a tarefa correspondente
            if tarefa['texto'] == texto:
                # Expressão ternária (valor_se_verdadeiro if condição else valor_se_falso)
                tarefa['marcado'] = True if values[event] else False  # Atualizar o valor de marcado para True ou False
                break
        # Salvar as tarefas após alterar o estado do checkbox
        salvar_tarefas(tarefas)
    elif event == 'Resetar':
        # Deletar o arquivo JSON
        if os.path.exists(ARQUIVO_TAREFAS):
            os.remove(ARQUIVO_TAREFAS)
        # Fechar a janela
        janela.close()
        break

janela.close()