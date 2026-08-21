import qrcode


url = "http://127.0.0.1:8000/q/abc123"

imagem = qrcode.make(url)
imagem.save("qr_abc123.png")

print("QR Code criado com sucesso.")