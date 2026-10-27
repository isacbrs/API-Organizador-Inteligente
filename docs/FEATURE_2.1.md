# 📄 Documentação Técnica - Feature 2.1: Motor NLP e Integração Nebius AI Cloud

## 1. Visão Geral
A Feature 2.1 introduz o núcleo de Inteligência Artificial do Organizador de Contas. O objetivo arquitetural desta etapa é transformar entradas de texto não estruturadas (linguagem natural) em objetos de dados rigorosamente tipados e estruturados (JSON), prontos para a persistência no banco de dados. 

Para isso, o back-end foi integrado à infraestrutura da **Nebius AI Cloud**, utilizando modelos *open-source* de alto desempenho (família Llama/NVIDIA) atuando como motores de extração de dados (NLP - *Natural Language Processing*).

## 2. Stack Tecnológica
* **Provedor de Infraestrutura de IA:** Nebius AI Cloud
* **Padrão de Comunicação:** SDK AsyncOpenAI (chamadas assíncronas)
* **Engenharia de Prompt:** Zero-shot prompting com restrição de formato de saída
* **Segurança da Rota:** Autenticação JWT via injeção de dependência (`Depends`)

## 3. Detalhes de Implementação e Engenharia de IA

### 3.1. Orquestração Assíncrona e Performance
Para evitar o bloqueio da *Thread* principal do FastAPI (Event Loop) durante o tempo de inferência da IA, a comunicação com a API da Nebius foi implementada utilizando o cliente `AsyncOpenAI`. Isso garante que o servidor continue aceitando requisições de outros usuários de forma concorrente enquanto aguarda o processamento do LLM.

### 3.2. Engenharia de Prompt e Segurança de Dados (Guardrails)
O serviço de LLM (`llm_service.py`) não atua como um *chatbot* genérico, mas como um extrator de dados estrito. A arquitetura do *System Prompt* foi construída com as seguintes restrições:
* **Prevenção de Hallucination e Data Leakage:** A IA possui regras explícitas para censurar PII (*Personally Identificable Information*), ignorando e omitindo CPFs, CNPJs e códigos de barras.
* **Alinhamento de Contrato de Dados:** A IA é forçada a classificar as despesas em categorias pré-aprovadas no banco de dados (`mensal`, `parcelado`, `unico`) e a formatar datas obrigatoriamente no padrão ISO 8601 (YYYY-MM-DD).
* **Parâmetro de Temperatura:** O modelo é invocado com `temperature=0.0`, eliminando a aleatoriedade (criatividade) e garantindo respostas determinísticas e precisas.

### 3.3. Restrição de Saída (JSON Mode)
Para garantir que o front-end receba sempre um contrato válido e parseável, ativamos o `response_format={"type": "json_object"}`. Isso força o LLM no nível da API a responder estritamente em um formato JSON puro, mitigando falhas de *parsing* causadas por injeções de *markdown* ou textos de cortesia ("Aqui está o seu resultado...").

### 3.4. Blindagem do Endpoint
A rota `POST /ia/extrair-texto` reutiliza a mesma arquitetura de segurança (Multitenancy) da Feature 1.3. A requisição exige um Token JWT válido no cabeçalho (*Bearer*), interceptado via injeção de dependência do FastAPI. Usuários não autenticados ou com tokens expirados recebem `HTTP 401 Unauthorized` antes que qualquer processamento de texto ou custo de API seja gerado.

## 4. Fluxo de Execução (Lifecycle)
1. O Front-end dispara um `POST` contendo o texto livre e o JWT do usuário logado.
2. O FastAPI valida o token no Supabase; se autorizado, avança.
3. O controlador repassa o *payload* para o `llm_service.py`.
4. O serviço envelopa a requisição com o *System Prompt* (regras de segurança) e dispara a chamada assíncrona para a Nebius AI Cloud.
5. O LLM da Llama/NVIDIA processa a linguagem natural e extrai os dados alvo.
6. A Nebius retorna uma *string* em formato JSON puro.
7. O Back-end converte o texto (*parsing*) para um dicionário Python e o devolve ao cliente via HTTP 200.