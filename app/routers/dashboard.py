from fastapi import APIRouter, Depends, HTTPException

from app.auth import obter_usuario_atual
from app.database import abrir_conexao


router = APIRouter()


@router.get("/overview")
def obter_resumo_dashboard(usuario: dict = Depends(obter_usuario_atual)):
    """Retorna o resumo da empresa vinculada ao usuário autenticado."""

    with abrir_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name
                FROM establishments
                WHERE dashboard_user_id = %s
                """,
                (usuario["id"],),
            )
            empresa = cursor.fetchone()

            if empresa is None:
                raise HTTPException(
                    status_code=404,
                    detail="Nenhuma empresa vinculada a este usuário",
                )

            estabelecimento_id, nome_empresa = empresa

            cursor.execute(
                """
                SELECT
                    COUNT(*) FILTER (
                        WHERE ae.accessed_at >= CURRENT_DATE
                    ) AS acessos_hoje,
                    COUNT(*) FILTER (
                        WHERE ae.accessed_at >= CURRENT_DATE - INTERVAL '6 days'
                    ) AS acessos_ultimos_7_dias,
                    COUNT(ae.id) AS total_acessos,
                    COUNT(*) FILTER (
                        WHERE ae.source = 'qr'
                    ) AS acessos_qr,
                    COUNT(*) FILTER (
                        WHERE ae.source = 'nfc'
                    ) AS acessos_nfc,
                    MAX(ae.accessed_at) AS ultimo_acesso
                FROM qr_codes qc
                LEFT JOIN access_events ae ON ae.qr_code_id = qc.id
                WHERE qc.establishment_id = %s
                """,
                (estabelecimento_id,),
            )
            estatisticas = cursor.fetchone()

            cursor.execute(
                """
                SELECT code, destination_url, is_active
                FROM qr_codes
                WHERE establishment_id = %s
                ORDER BY created_at DESC, id DESC
                LIMIT 1
                """,
                (estabelecimento_id,),
            )
            qr_code = cursor.fetchone()

            cursor.execute(
                """
                SELECT qc.code, ae.source, ae.accessed_at
                FROM access_events ae
                JOIN qr_codes qc ON qc.id = ae.qr_code_id
                WHERE qc.establishment_id = %s
                ORDER BY ae.accessed_at DESC
                LIMIT 10
                """,
                (estabelecimento_id,),
            )
            acessos_recentes = cursor.fetchall()

    (
        acessos_hoje,
        acessos_ultimos_7_dias,
        total_acessos,
        acessos_qr,
        acessos_nfc,
        ultimo_acesso,
    ) = estatisticas

    qr_atual = None
    if qr_code is not None:
        codigo, destino, ativo = qr_code
        qr_atual = {
            "codigo": codigo,
            "destino_url": destino,
            "ativo": ativo,
        }

    return {
        "empresa": {
            "id": estabelecimento_id,
            "nome": nome_empresa,
        },
        "estatisticas": {
            "acessos_hoje": acessos_hoje,
            "acessos_ultimos_7_dias": acessos_ultimos_7_dias,
            "total_acessos": total_acessos,
            "acessos_qr": acessos_qr,
            "acessos_nfc": acessos_nfc,
            "ultimo_acesso": ultimo_acesso,
        },
        "qr_atual": qr_atual,
        "acessos_recentes": [
            {
                "codigo": codigo,
                "origem": origem,
                "acessado_em": acessado_em,
            }
            for codigo, origem, acessado_em in acessos_recentes
        ],
    }
