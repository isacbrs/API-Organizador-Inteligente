# 📄 Documentação Técnica - Feature 3.1: Motor Multimodal e Processamento de Áudio

## 1. Visão Geral
A Feature 3.1 expande a capacidade da API para processar dados não estruturados na forma de ficheiros físicos (Voice-to-JSON). O sistema permite que o utilizador grave áudios descrevendo faturas, sendo estes transcritos e processados em pipeline até à conversão num contrato de dados (DTO) válido.

## 2. Stack Tecnológica
* **Processamento de *Multipart*:** `python-multipart` (Integração FastAPI)
* **Modelo Speech-to-Text (STT):** OpenAI Whisper (via SDK)
* **Padrão Arquitetural:** Pipeline de Encadeamento (Chaining) e I/O Temporário Seguro

## 3. Detalhes de Implementação e Arquitetura

### 3.1. Receção e Validação de Mídia Volátil
A API utiliza as classes `UploadFile` e `File` do FastAPI para lidar com os ficheiros de áudio enviados via `multipart/form-data`. 
* **Sanitização de Entrada:** O *endpoint* verifica ativamente a extensão do ficheiro, permitindo apenas formatos compatíveis com os modelos acústicos (mp3, wav, m4a, ogg). Tentativas de injeção de outros tipos de ficheiros são barradas com `HTTP 400 Bad Request` antes do consumo de memória.

### 3.2. Gestão Segura do Sistema de Ficheiros (I/O)
Uma vez que o modelo Whisper necessita de ler o áudio a partir de um caminho físico no sistema operativo, a arquitetura implementa o módulo `tempfile` da *standard library* do Python.
* O ficheiro é descarregado da memória RAM (`arquivo.read()`) e escrito num ficheiro temporário seguro.
* **Limpeza Garantida:** Para evitar vazamento de memória (Memory Leak) e esgotamento do disco do servidor (Storage Exhaustion), foi implementado um bloco `try-finally`. O bloco garante, de forma determinística, que o ficheiro temporário é apagado do disco (`os.remove`) assim que a inferência do modelo é concluída, independentemente de a API retornar sucesso (200) ou falha (500).

### 3.3. Pipeline de Inferência Encadeada (Chaining)
A arquitetura de *software* evitou redundância de código (DRY) ao adotar um padrão de encadeamento no serviço `llm_service.py`:
1. **Passo 1 (Audio-to-Text):** O áudio físico é enviado para a infraestrutura da nuvem e processado pelo modelo *Whisper*.
2. **Passo 2 (Text-to-JSON):** A *string* da transcrição devolvida é injetada diretamente na função `extrair_dados_fatura()` construída na Feature 2.1. O LLM atua novamente aplicando as políticas de formatação, censura de dados sensíveis e estruturação JSON.

### 3.4. Segurança da Rota
A rota `POST /ia/extrair-audio` herda os *middlewares* de proteção JWT, exigindo que a injeção de dependência confirme o contexto do utilizador via Supabase GoTrue antes de processar o ficheiro multimédia.