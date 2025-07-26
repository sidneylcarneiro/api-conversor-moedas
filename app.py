from ttkbootstrap import (
    Window, Label, Menubutton, Button, Menu
)
import requests
from tkinter import StringVar
import xml.etree.ElementTree as ET

app = Window(themename="cyborg")
app.geometry("400x400")

moedas_disponiveis = {}
cotacoes_disponiveis = {}
moeda_selecionada = StringVar()
resultado_var = StringVar(value="Clique em Converter")

def carregar_moedas():
    """Carrega a lista de moedas disponíveis"""
    try:
        response = requests.get("https://economia.awesomeapi.com.br/xml/available/uniq")
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for child in root:
                moedas_disponiveis[child.tag] = child.text
            
        response = requests.get("https://economia.awesomeapi.com.br/xml/available")
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for child in root:
                if '-' in child.tag:
                    cotacoes_disponiveis[child.tag] = child.text
            
        menu = Menu(app)
        
        moedas_ordenadas = sorted(moedas_disponiveis.items(), key=lambda x: x[0])
        
        for codigo, nome in moedas_ordenadas:
            par = f"{codigo}-BRL"
            if par in cotacoes_disponiveis:
                menu.add_radiobutton(
                    label=f"{codigo} - {nome}",
                    variable=moeda_selecionada,
                    value=par,
                    command=atualizar_moeda_selecionada
                )
        
        moeda_button['menu'] = menu
        
    except Exception as e:
        resultado_var.set(f"Erro ao carregar moedas: {str(e)}")

def atualizar_moeda_selecionada():
    par = moeda_selecionada.get()
    codigo = par.split('-')[0]
    if codigo in moedas_disponiveis:
        moeda_button.config(text=f"{codigo} - {moedas_disponiveis[codigo]}")
    else:
        moeda_button.config(text="Selecione uma moeda")

def converter_moeda():
    par = moeda_selecionada.get()
    if not par:
        resultado_var.set("Selecione uma moeda primeiro")
        return
    
    try:
        response = requests.get(f"https://economia.awesomeapi.com.br/json/last/{par}")
        if response.status_code == 200:
            data = response.json()

            chave = par.replace("-", "")
            if chave in data:
                cotacao = data[chave]
                valor = float(cotacao['bid'])
                resultado_var.set(f"1 {par.split('-')[0]} = R$ {valor:.2f}")
            else:
                resultado_var.set("Dados de cotação não encontrados")
        else:
            resultado_var.set(f"Erro na API: {response.status_code}")
    except Exception as e:
        resultado_var.set(f"Erro ao obter cotação: {str(e)}")

Label(app, text="Moeda de Origem:").pack(pady=5)
moeda_button = Menubutton(app, text="Selecione uma moeda")
moeda_button.pack(pady=5)

Label(app, text="Resultado:").pack(pady=5)
resultado_entry = Label(
    app, 
    textvariable=resultado_var, 
    font=("Arial", 16, "bold")
)
resultado_entry.pack(pady=10)

Button(
    app, 
    text="Converter", 
    command=converter_moeda
).pack(pady=10)

carregar_moedas()

app.mainloop()