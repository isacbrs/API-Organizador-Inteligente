from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from app.services.llm_service import extrair_dados_fatura, transcrever_e_extrair_audio
from app.api.dependencies import get_current_user_client

router = APIRouter(prefix="/ia", tags=["Processamento de IA"])

class TextoInput(BaseModel):
    texto: str

@router.post("/extrair-texto", summary="Extrai dados de fatura a partir de texto livre")
async def processar_texto(
    payload: TextoInput,
    supabase = Depends(get_current_user_client) 
):
    try:
        dados_json = await extrair_dados_fatura(payload.texto)
        return dados_json
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar IA: {str(e)}")

# --- NOVA ROTA AQUI ---
@router.post("/extrair-audio", summary="Extrai dados de fatura a partir de um ficheiro de áudio")
async def processar_audio(
    arquivo: UploadFile = File(..., description="Ficheiro de áudio (mp3, wav, m4a)"),
    supabase = Depends(get_current_user_client)
):
    # Validações de segurança e formato
    extensao = arquivo.filename.split(".")[-1].lower()
    formatos_permitidos = ["mp3", "wav", "m4a", "ogg"]
    
    if extensao not in formatos_permitidos:
        raise HTTPException(status_code=400, detail="Formato de áudio não suportado.")
        
    try:
        # Lê o ficheiro para a memória RAM
        audio_bytes = await arquivo.read()
        
        # Envia para a camada de serviço processar
        dados_json = await transcrever_e_extrair_audio(audio_bytes, extensao)
        return dados_json
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento de áudio: {str(e)}")