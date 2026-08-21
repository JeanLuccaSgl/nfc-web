from app.database import abrir_conexao


codigo = input("Qual o código do QR Code? ").strip()
novo_link = input("Qual será o novo link? ").strip()

with abrir_conexao() as conexao:
    with conexao.cursor() as cursor:
        cursor.execute(
            """
            UPDATE qr_codes
            SET destination_url = %s
            WHERE code = %s
              AND is_active = TRUE
            """,
            (novo_link, codigo),
        )

        if cursor.rowcount == 0:
            print("QR Code não encontrado.")
        else:
            print("Destino alterado com sucesso.")