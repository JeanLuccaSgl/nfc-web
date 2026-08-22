from pathlib import Path

import qrcode


url = "https://nfc-web.onrender.com/q/abc123"

pasta_qrcodes = Path("qrcodes")
pasta_qrcodes.mkdir(exist_ok=True)

nome_arquivo = pasta_qrcodes / "qr_abc123.png"

imagem = qrcode.make(url)
imagem.save(nome_arquivo)

print(f"QR Code criado com sucesso: {nome_arquivo}")
