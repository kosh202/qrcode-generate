#version 0.0.2
import tkinter as tk
from tkinter import ttk, filedialog, colorchooser
import qrcode
from PIL import Image, ImageTk
import io

# Sugestões para o QR Code
sugestoes_texto = (
    "Exemplos de coisas para adicionar ao QR Code:\n"
    "- URL\n"
    "- Texto\n"
    "- Endereço de Email\n"
    "- Número de Telefone\n"
    "- Contato VCard\n"
)

cor_qrcode = "#070707"  # Cor padrão do QR Code
cor_fundo_qrcode = "#FFFFFF"  # Cor padrão do fundo
caminho_imagem = None  # Armazena a imagem escolhida
img_byte_array = None  # Armazena o QR Code gerado


def escolher_cor():
    global cor_qrcode
    cor = colorchooser.askcolor()[1]
    if cor:
        cor_qrcode = cor
        label_cor.config(text=f"Cor do QR Code: {cor}", bg=cor)


def escolher_cor_fundo():
    global cor_fundo_qrcode
    cor = colorchooser.askcolor()[1]
    if cor:
        cor_fundo_qrcode = cor
        label_cor_fundo.config(text=f"Cor de Fundo: {cor}", bg=cor)


def escolher_imagem():
    global caminho_imagem
    caminho_imagem = filedialog.askopenfilename(
        title="Escolher uma imagem",
        filetypes=[("Imagens", "*.jpg;*.jpeg;*.png;*.gif;*.bmp;*.tiff;*.webp")]
    )


def gerar_qrcode():
    global caminho_imagem, img_byte_array

    dados = entrada_texto.get()
    if not dados:
        status_label.config(text="Por favor, insira um texto para gerar o QR Code.", foreground="red")
        return

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(dados)
    qr.make(fit=True)

    img = qr.make_image(fill_color=cor_qrcode, back_color=cor_fundo_qrcode)

    if caminho_imagem:
        try:
            img_logo = Image.open(caminho_imagem)
            tamanho_logo = 50
            img_logo = img_logo.resize((tamanho_logo, tamanho_logo))
            posicao = ((img.size[0] - img_logo.size[0]) // 2, (img.size[1] - img_logo.size[1]) // 2)
            img.paste(img_logo, posicao, img_logo.convert("RGBA"))
        except Exception as e:
            status_label.config(text=f"Erro ao adicionar logo: {str(e)}", foreground="red")

    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format="PNG")
    img_byte_array = img_byte_array.getvalue()

    img_bytes = Image.open(io.BytesIO(img_byte_array))
    qr_image = ImageTk.PhotoImage(img_bytes)

    qr_label.config(image=qr_image)
    qr_label.image = qr_image
    status_label.config(text="QR Code gerado com sucesso!", foreground="green")


def salvarqr():
    global img_byte_array
    if img_byte_array is None:
        status_label.config(text="Nenhum QR Code para salvar. Gere um primeiro!", foreground="red")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Arquivos PNG", "*.png")])
    if file_path:
        with open(file_path, 'wb') as f:
            f.write(img_byte_array)
        status_label.config(text=f"QR Code salvo como '{file_path}'.", foreground="green")


def limpar_imagem():
    global caminho_imagem
    caminho_imagem = None
    status_label.config(text="Imagem removida. Gere o QR Code novamente.", foreground="blue")
    qr_label.config(image='')


def interface():
    global entrada_texto, status_label, qr_label, label_cor, label_cor_fundo

    janela = tk.Tk()
    janela.title("Gerador de QR Code")

    style = ttk.Style()
    style.configure('TButton', foreground="blue", font=('Helvetica', 12))

    ttk.Label(janela, text="Digite o texto abaixo e clique em 'Gerar QR Code'.", font=('Helvetica', 12)).pack(pady=10)
    ttk.Label(janela, text=sugestoes_texto, font=('Helvetica', 12)).pack()

    entrada_texto = ttk.Entry(janela, font=('Helvetica', 12), width=40)
    entrada_texto.pack(pady=5)

    frame_botoes = ttk.Frame(janela)
    frame_botoes.pack(pady=10)

    ttk.Button(frame_botoes, text="Gerar QR Code", command=gerar_qrcode).grid(row=0, column=0, padx=5)
    ttk.Button(frame_botoes, text="Escolher Imagem", command=escolher_imagem).grid(row=0, column=1, padx=5)
    ttk.Button(frame_botoes, text="Limpar Imagem", command=limpar_imagem).grid(row=0, column=2, padx=5)
    ttk.Button(frame_botoes, text="Escolher Cor", command=escolher_cor).grid(row=0, column=3, padx=5)
    ttk.Button(frame_botoes, text="Escolher Cor de Fundo", command=escolher_cor_fundo).grid(row=0, column=4, padx=5)
    ttk.Button(frame_botoes, text="Salvar QR Code", command=salvarqr).grid(row=0, column=5, padx=5)

    label_cor = tk.Label(janela, text="Cor do QR Code: Preto", width=30, height=2)
    label_cor.pack(pady=5)

    label_cor_fundo = tk.Label(janela, text="Cor de Fundo: Branco", width=30, height=2)
    label_cor_fundo.pack(pady=5)

    qr_label = ttk.Label(janela)
    qr_label.pack()

    status_label = ttk.Label(janela, text="Gerador de QR Code", font=('Helvetica', 12), foreground="black")
    status_label.pack(pady=5)

    janela.mainloop()


def main():
    interface()


main()
