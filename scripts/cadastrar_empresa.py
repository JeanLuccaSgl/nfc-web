from pathlib import Path
import qrcode
import secrets

from app.database import abrir_conexao

nome_empresa = input("Qual o nome da empresa?")
link_avaliacao = input("Qual o link de avaliação da empresa?")

codigo_qr = secrets.token_urlsafe(8)
url_publica = f"https://nfc-web.onrender.com/q/{codigo_qr}"

print(f"Nome da empresa: {nome_empresa}")
print(f"Link de avaliação: {link_avaliacao}")
print(f"Código QR: {codigo_qr}")
print(f"URL pública: {url_publica}")

with abrir_conexao() as conexao:
    with conexao.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO establishments (name)
            VALUES (%s)
            RETURNING id
            """,
            (nome_empresa,),
        )

        resultado = cursor.fetchone()
        id_empresa = resultado[0]

        cursor.execute(
            """
            INSERT INTO qr_codes (code, destination_url, establishment_id)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (codigo_qr, link_avaliacao, id_empresa),
        )

        resultado_qr = cursor.fetchone()
        id_qr_code = resultado_qr[0] if resultado_qr else None

pasta_qrcodes = Path("qrcodes")
pasta_qrcodes.mkdir(exist_ok=True)

nome_arquivo = pasta_qrcodes / f"qr_{codigo_qr}.png"

imagem = qrcode.make(url_publica)
imagem.save(nome_arquivo)

print(f"Imagem criada: {nome_arquivo}")
print(f"Empresa criada com ID: {id_empresa}")
