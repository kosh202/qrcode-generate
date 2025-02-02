import tkinter as tk
from tkinter import ttk, filedialog
import qrcode
from PIL import Image, ImageTk
import io

caminho_imagem = "./t.jpg"

# Sugestões de coisas que podem ser adicionadas para o QR Code
sugestoes_texto = (

    "Exemplos de coisas para adicionar ao QR Code:\n"

    "- URL\n"

    "- Texto\n"

    "- Endereço de Email\n"

    "- Número de Telefone\n"

    "- Contato VCard\n"

)

# Função para gerar o QR Code

def gerar_qrcode():

    # Obtém o texto da entrada de texto

    dados = entrada_texto.get()

    # Cria um objeto QRCode

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    # Adiciona o texto ao QRCode

    qr.add_data(dados)

    qr.make(fit=True)

    # Cria uma imagem do QRCode

    # img = qr.make_image(fill_color="#0986b2", back_color="black")
    img = qr.make_image(fill_color="#070707", back_color="white")

    # Abrir a imagem que será colocada no meio do QR Code
    img_logo = Image.open(caminho_imagem)

    # Redimensionar a imagem do logo
    tamanho_logo = 50  # Tamanho do logo em pixels
    img_logo = img_logo.resize((tamanho_logo, tamanho_logo))

    # Calcular a posição para centralizar o logo
    posicao = ((img.size[0] - img_logo.size[0]) // 2, (img.size[1] - img_logo.size[1]) // 2)

    # Colocar a imagem do logo no QR Code
    img.paste(img_logo, posicao, img_logo.convert("RGBA"))  # Usar RGBA para preservar a transparência

    # Converte a imagem em um formato de bytes

    img_byte_array = io.BytesIO()

    img.save(img_byte_array, format="PNG")

    img_byte_array = img_byte_array.getvalue()

    # Cria uma imagem PhotoImage a partir dos bytes

    img_bytes = Image.open(io.BytesIO(img_byte_array))

    qr_image = ImageTk.PhotoImage(img_bytes)

    # Exibe a imagem em uma etiqueta

    qr_label.config(image=qr_image)

    qr_label.image = qr_image

    # Salva a imagem como um arquivo PNG

    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Arquivos PNG", "*.png")])

    if file_path:

        with open(file_path, 'wb') as f:

            f.write(img_byte_array)

        status_label.config(text=f"QR Code gerado e salvo como '{file_path}'.")

# Cria a janela principal

janela = tk.Tk()

janela.title("Gerador de QR Code")

# Cria um estilo para melhorar a aparência dos widgets

style = ttk.Style()

style.configure('TButton', foreground="blue", font=('Helvetica', 12))

# Cria uma etiqueta com informações úteis e sugestões

info_label = ttk.Label(janela, text="Digite o texto abaixo e clique em 'Gerar QR Code'.", font=('Helvetica', 12))

info_label.pack(pady=10)

sugestoes_label = ttk.Label(janela, text=sugestoes_texto, font=('Helvetica', 12))

sugestoes_label.pack()

# Cria uma entrada de texto

entrada_texto = ttk.Entry(janela, font=('Helvetica', 12))

entrada_texto.pack()

# Cria um botão para gerar o QR Code

botao_gerar = ttk.Button(janela, text="Gerar QR Code", command=gerar_qrcode)

botao_gerar.pack(pady=10)

# Cria uma etiqueta para exibir o QR Code gerado

qr_label = ttk.Label(janela)

qr_label.pack()

# Cria uma etiqueta para exibir informações de status

status_label = ttk.Label(janela, text="", font=('Helvetica', 12))

status_label.pack()

# Inicia o loop da interface gráfica

janela.mainloop()