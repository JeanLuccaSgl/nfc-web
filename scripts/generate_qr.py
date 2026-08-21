import qrcode


url = "https://nfc-web.onrender.com/q/abc123"

imagem = qrcode.make(url)
imagem.save("qr_abc123.png")

print("QR Code criado com sucesso.")