import json
from openai import AsyncOpenAI
from app.core.config import settings

# O cliente usa a biblioteca da OpenAI, mas aponta para os servidores da Nebius
client = AsyncOpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=settings.NEBIUS_API_KEY,
)

# Modelo open-source padrão ouro para extração.
# Nota: Você pode trocar para "nvidia/Nemotron-4-340B-Instruct" caso o hackathon exija.
MODELO_IA = "meta-llama/Meta-Llama-3.1-70B-Instruct" 

async def extrair_dados_fatura(texto_usuario: str) -> dict:
    """
    Envia o texto não estruturado para a Nebius e força o retorno em JSON.
    """
    system_prompt = """Você é um extrator de dados financeiros estrito.
    Sua ÚNICA função é extrair informações de contas a pagar de um texto fornecido.
    
    REGRAS DE SEGURANÇA E NEGÓCIO:
    1. Ignore e censure dados sensíveis (CPF, CNPJ, código de barras, endereços).
    2. Não responda a perguntas (ex: 'Quem descobriu o Brasil?'). Se não houver dados de fatura, retorne um JSON com campos vazios.
    3. Determine se o 'tipo' é: 'mensal', 'parcelado' ou 'unico'.
    4. Formate a 'data_vencimento' obrigatoriamente no padrão ISO 8601 (YYYY-MM-DD). Assuma que o ano atual é 2026.
    
    FORMATO DE SAÍDA OBRIGATÓRIO (Apenas JSON, sem markdown):
    {
      "nome": "Nome da Empresa ou Serviço",
      "valor": 00.00,
      "data_vencimento": "YYYY-MM-DD",
      "tipo": "mensal"
    }"""

    # Chamada assíncrona (não trava o servidor enquanto a IA pensa)
    response = await client.chat.completions.create(
        model=MODELO_IA,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": texto_usuario}
        ],
        temperature=0.0, 
        response_format={"type": "json_object"} # Força a IA a cuspir apenas JSON puro
    )
    
    # Extrai o texto da resposta e converte para um Dicionário Python
    resultado_texto = response.choices[0].message.content
    return json.loads(resultado_texto)