from app.database import abrir_conexao


with abrir_conexao() as conexao:
    with conexao.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                e.name,
                q.code,
                COUNT(a.id),
                MAX(a.accessed_at)
            FROM establishments e
            JOIN qr_codes q
                ON q.establishment_id = e.id
            LEFT JOIN access_events a
                ON a.qr_code_id = q.id
            GROUP BY e.name, q.code
            ORDER BY COUNT(a.id) DESC
            """
        )

        resultados = cursor.fetchall()


for empresa, codigo, total_acessos, ultimo_acesso in resultados:
    print(f"Empresa: {empresa}")
    print(f"Código: {codigo}")
    print(f"Total de acessos: {total_acessos}")
    print(f"Último acesso: {ultimo_acesso}")
    print("-" * 30)