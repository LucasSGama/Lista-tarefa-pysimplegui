import PySimpleGUI as sg

# Função para calcular a expressão matemática
def calcular(expressao):
    try:
        # Avalia a expressão matemática e retorna o resultado
        return str(eval(expressao))
    except Exception as e:
        return "Erro"

# Layout da interface
layout = [
    [sg.Input(key='-DISPLAY-', size=(20, 1), justification='right', font=('Arial', 18))],
    [sg.Button('7'), sg.Button('8'), sg.Button('9'), sg.Button('/')],
    [sg.Button('4'), sg.Button('5'), sg.Button('6'), sg.Button('*')],
    [sg.Button('1'), sg.Button('2'), sg.Button('3'), sg.Button('-')],
    [sg.Button('0'), sg.Button('.'), sg.Button('+'), sg.Button('=')],
    [sg.Button('C')]
]

# Cria a janela
window = sg.Window('Calculadora', layout)

# Loop principal da aplicação
while True:
    event, values = window.read()

    # Fechar a janela
    if event == sg.WIN_CLOSED:
        break

    # Se o evento for um número ou operador, atualiza a tela
    if event in '0123456789.+-*/':
        current_text = values['-DISPLAY-']
        window['-DISPLAY-'].update(current_text + event)

    # Se o evento for '=' (igual), calcula o resultado
    elif event == '=':
        expression = values['-DISPLAY-']
        result = calcular(expression)
        window['-DISPLAY-'].update(result)

    # Se o evento for 'C', limpa a tela
    elif event == 'C':
        window['-DISPLAY-'].update('')

# Fecha a janela
window.close()