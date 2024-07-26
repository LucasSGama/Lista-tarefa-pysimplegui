import PySimpleGUI as sg
import json
import os

# Caminho do arquivo de tarefas
ARQUIVO_TAREFAS = 'Tarefas.json'

def carregar_tarefas():
    """Carrega as tarefas do arquivo JSON"""
    if os.path.exists(ARQUIVO_TAREFAS):
        with open(ARQUIVO_TAREFAS, 'r') as f:
            try:
                tarefas = json.load(f)
                return tarefas
            except json.JSONDecodeError:
                return []  # Retorna uma lista vazia se o JSON estiver vazio ou inválido
    return [{'texto': 'Tarefa padrão', 'marcado': False}]  # Retorna uma lista com uma tarefa padrão

def salvar_tarefas(tarefas):
    """Salva as tarefas no arquivo JSON"""
    with open(ARQUIVO_TAREFAS, 'w') as f:
        json.dump(tarefas, f, indent=4)

# Função para converter os valores dos Checkboxes em uma lista de tarefas
def extrair_tarefas(values):
    tarefas = []
    if values:
        for key, value in values.items():
            if key.startswith('tarefa_'):
                texto = key[len('tarefa_'):]
                marcado = value
                tarefas.append({'texto': texto, 'marcado': marcado})
    return tarefas

# Criando o layout
def criar_janela_inicial(tarefas):
    sg.theme('DarkBlue4')
    layout = [
        [sg.Frame('Tarefas', layout=[
            [sg.Checkbox(tarefa['texto'], default=tarefa.get('marcado', False), key=f'tarefa_{tarefa["texto"]}', enable_events=True)]
            for tarefa in tarefas
        ], key='container')],
        [sg.Button('Nova Tarefa'), sg.Button('Resetar')]
    ]
    return sg.Window('Todo List', layout=layout, size=(800, 600), resizable=True, finalize=True)

# Carregar tarefas do arquivo
tarefas = carregar_tarefas()

# Criar a janela com as tarefas carregadas
janela = criar_janela_inicial(tarefas)

while True:
    event, values = janela.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Nova Tarefa':
        nova_tarefa = sg.popup_get_text('Digite o texto da nova tarefa:')
        if nova_tarefa:
            janela.extend_layout(janela['container'], [[sg.Checkbox(nova_tarefa, key=f'tarefa_{nova_tarefa}', enable_events=True)]])
            # Atualizar a lista de tarefas
            tarefas.append({'texto': nova_tarefa, 'marcado': False})
            # Salvar as tarefas após adicionar uma nova tarefa
            salvar_tarefas(tarefas)
    elif event.startswith('tarefa_'):
        # Atualizar o estado do checkbox
        texto = event[len('tarefa_'):]
        for tarefa in tarefas:
            if tarefa['texto'] == texto:
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