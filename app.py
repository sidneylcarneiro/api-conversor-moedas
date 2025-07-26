from ttkbootstrap import Window, Label, Entry, Frame, Button
from ttkbootstrap.constants import *
import requests

app = Window(themename="cyborg")
app.geometry("400x500")
app.title("Conversor de Moedas")

Label(app, text="Conversor de Reais para Euros", font=("Arial", 14)).pack(pady=10)

input_frame = Frame(app)
input_frame.pack(pady=10, fill='x', padx=20)

result_frame = Frame(app)
result_frame.pack(pady=10, fill='x', padx=20)

Label(input_frame, text="Valor R$ ", font=("Arial", 14)).pack(side='left', padx=(0, 10))
input_entry = Entry(input_frame, font=("Arial", 14))
input_entry.pack(side='left', expand=True, fill='x')

Label(result_frame, text="Resultado €: ", font=("Arial", 14)).pack(side='left', padx=(0, 10))
result_label_show = Label(result_frame, font=("Arial", 14))
result_label_show.pack(side='left', expand=True, fill='x')

def buscar_cotacao():
    try:
        response = requests.get("https://economia.awesomeapi.com.br/json/last/EUR-BRL")
        data = response.json()
        cotacao = float(data["EURBRL"]["bid"])
        replaced_entry = input_entry.get().replace(",",".")
        valor_reais = float(replaced_entry or 0)
        valor_euros = valor_reais / cotacao
        result_label_show.config(text=f"{valor_euros:.2f}")
    except Exception as e:
        result_label_show.config(text="Erro ao obter cotação")
        print(f"Erro: {e}")

Button(app, text="Converter", command=buscar_cotacao, bootstyle=PRIMARY).pack(pady=10)

app.mainloop()
