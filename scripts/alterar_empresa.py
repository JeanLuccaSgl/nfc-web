from app.database import abrir_conexao


codigo = input("Qual o código do QR Code? ").strip()
novo_nome = input("Qual será o novo nome da empresa? ").strip()

if not novo_nome:
    print("O nome não pode ficar vazio.")
    raise SystemExit

with abrir_conexao() as conexao:
    with conexao.cursor() as cursor:
        cursor.execute(
            """
            UPDATE establishments
            SET name = %s
            WHERE id = (
                SELECT establishment_id
                FROM qr_codes
                WHERE code = %s
            )
            RETURNING id, name
            """,
            (novo_nome, codigo),
        )

        empresa = cursor.fetchone()

        if empresa is None:
            print("QR Code não encontrado.")
        else:
            id_empresa, nome_atualizado = empresa
            print(f"Empresa {id_empresa} atualizada para: {nome_atualizado}")