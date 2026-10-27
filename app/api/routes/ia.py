from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.llm_service import extrair_dados_fatura
from app.api.dependencies import get_current_user_client

router = APIRouter(prefix="/ia", tags=["Processamento de IA"])

# DTO para a entrada de texto
class TextoInput(BaseModel):
    texto: str

@router.post("/extrair-texto", summary="Extrai dados de fatura a partir de texto livre")
async def processar_texto(
    payload: TextoInput,
    # Injetamos a segurança para garantir que a IA não seja usada por quem não está logado
    supabase = Depends(get_current_user_client) 
):
    try:
        dados_json = await extrair_dados_fatura(payload.texto)
        return dados_json
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao processar IA na Nebius: {str(e)}"
        )