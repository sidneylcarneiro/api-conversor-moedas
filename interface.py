from ttkbootstrap import Window, Label, Entry, Frame, Button, Combobox
from ttkbootstrap.constants import *
from converter import obter_cotacao, salvar_historico

app = Window(themename="cyborg")
app.geometry("400x250")
app.title("Conversor de Moedas")

Label(app, text="Conversor de Moedas", font=("Arial", 16)).pack(pady=10)

moedas = ["BRL", "USD", "EUR", "JPY", "GBP", "ARS", "CHF", "AUD"]

moeda_frame = Frame(app)
moeda_frame.pack(pady=10, padx=20, fill='x')

Label(moeda_frame, text="De: ", font=("Arial", 12)).pack(side="left")
combo_origem = Combobox(moeda_frame, values=moedas, font=("Arial", 12), width=5)
combo_origem.set("BRL")
combo_origem.pack(side="left", padx=5)

Label(moeda_frame, text="Para: ", font=("Arial", 12)).pack(side="left")
combo_destino = Combobox(moeda_frame, values=moedas, font=("Arial", 12), width=5)
combo_destino.set("EUR")
combo_destino.pack(side="left", padx=5)

input_frame = Frame(app)
input_frame.pack(pady=10, padx=20, fill='x')

Label(input_frame, text="Valor: ", font=("Arial", 14)).pack(side="left", padx=(0, 10))
input_entry = Entry(input_frame, font=("Arial", 14))
input_entry.pack(side="left", expand=True, fill="x")

result_frame = Frame(app)
result_frame.pack(pady=10, padx=20, fill='x')

Label(result_frame, text="Resultado: ", font=("Arial", 14)).pack(side="left", padx=(0, 10))
result_label = Label(result_frame, font=("Arial", 14))
result_label.pack(side="left", expand=True, fill="x")

def converter_moeda():
    origem = combo_origem.get()
    destino = combo_destino.get()
    valor_txt = input_entry.get().replace(",", ".")
    try:
        valor_origem = float(valor_txt)
        cotacao = obter_cotacao(origem, destino)
        valor_convertido = valor_origem / cotacao
        result_label.config(text=f"{valor_convertido:.2f}")
        salvar_historico(origem, destino, valor_origem, valor_convertido)
    except Exception as e:
        result_label.config(text="Erro na conversão")
        print(e)

Button(app, text="Converter", command=converter_moeda, bootstyle=PRIMARY).pack(pady=10)

app.mainloop()
