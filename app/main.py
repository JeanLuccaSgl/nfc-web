from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from app.database import abrir_conexao

app = FastAPI()

@app.get("/")
def inicio():
    return {"mensagem": "API funcionando corretamente."}

@app.get("/q/{codigo}")
def acessar_qr_code(codigo: str):
    with abrir_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, destination_url
                FROM qr_codes
                WHERE code = %s AND is_active = TRUE
                """,
                (codigo,),
            )

            qr_code = cursor.fetchone()

            if qr_code is None:
                raise HTTPException(
                    status_code=404,
                    detail="QR Code não encontrado",
                )

            qr_code_id, destination_url = qr_code

            cursor.execute(
                """
                INSERT INTO access_events (qr_code_id)
                VALUES (%s)
                """,
                (qr_code_id,),
            )

    return RedirectResponse(
        url=destination_url,
        status_code=302,
    )