# Organizador Inteligente de Contas - Back-end API

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.io/)
[![Nebius AI](https://img.shields.io/badge/Nebius_AI_Cloud-000000?style=for-the-badge&logo=nvidia&logoColor=white)](https://nebius.ai/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)

## Sobre o Projeto
API RESTful assíncrona desenvolvida como submissão para o Nebius x NVIDIA Global AI Hackathon. O projeto atua como o motor lógico e de persistência para um Organizador Inteligente de Contas, permitindo que os usuários cadastrem faturas de forma autônoma através de processamento de linguagem natural (texto livre), transcrição acústica (áudio) ou visão computacional (fotografia).

O sistema adota a arquitetura Polyrepo para desacoplamento estrito entre Front-end e Back-end, focado em alta escalabilidade, segurança de dados e integração contínua.

## Arquitetura e Decisões de Engenharia

Para atender a requisitos de software em nível de produção, o back-end foi desenhado com foco nos seguintes pilares:

* **Multitenancy e Zero-Trust:** Implementação estrita de segurança de dados utilizando Row Level Security (RLS) nativo do PostgreSQL (via Supabase). O isolamento de dados financeiros entre usuários é garantido a nível de banco de dados, mitigando falhas na camada de aplicação.
* **Validação Rígida e Contratos (DTOs):** Sanitização de dados de entrada e saída através da biblioteca Pydantic, rejeitando requisições malformadas na borda e respeitando contratos de API rígidos (HTTP 422).
* **Orquestração Multimodal de IA:** Pipeline de inferência estruturado utilizando modelos abertos (Llama e Whisper) atuando na infraestrutura Nebius Cloud via chamadas assíncronas (AsyncOpenAI), evitando bloqueio do Event Loop.
* **I/O Seguro e Stateless Processing:** Processamento de imagens em memória via codificação Base64 (eliminando a necessidade de armazenamento em disco) e gestão segura de I/O temporário para arquivos de áudio, prevenindo vazamentos de memória (Memory Leaks).

## Funcionalidades Implementadas

* **Autenticação e Autorização:** Login e Cadastro com JWT integrados ao GoTrue, com interceptação via injeção de dependências no FastAPI.
* **CRUD Seguro:** Gestão de faturas e contas a pagar atreladas estritamente ao UUID do usuário logado.
* **Motor NLP (Texto):** Extração estruturada (JSON) a partir de descrições financeiras não padronizadas.
* **Motor Acústico (Áudio):** Pipeline de encadeamento (Chaining) convertendo arquivos de voz físicos (mp3, wav, ogg) para JSON.
* **OCR Inteligente (Vision):** Processamento visual de faturas fotografadas utilizando LLM Vision para extração de dados tabulares e datas.

## Documentação Técnica Analítica
Para uma auditoria aprofundada das decisões arquiteturais e fluxos de execução de cada módulo, consulte a documentação técnica oficial:

* [Feature 1.3: CRUD e Multitenancy RLS](./docs/FEATURE_1.3.md)
* [Feature 2.1: Motor NLP e Nebius Cloud](./docs/FEATURE_2.1.md)
* [Feature 3.1: Gestão de Mídia Volátil e Pipeline de Áudio](./docs/FEATURE_3.1.md)
* [Feature 3.2: Motor Multimodal Vision e Codificação Base64](./docs/FEATURE_3.2.md)

## Como Executar o Ambiente Local

1. Clone o repositório:
   ```bash
   git clone [https://github.com/isacbrs/organizador-contas-api.git](https://github.com/isacbrs/organizador-contas-api.git)
2. Instale as dependências do ambiente virtual:
   ```bash
   pip install -r requirements.txt
3. Configure as variáveis de ambiente em um arquivo .env na raiz do projeto:
   ```bash
   SUPABASE_URL="sua_url_do_projeto_supabase"
   SUPABASE_KEY="sua_anon_public_key"
   NEBIUS_API_KEY="sua_api_key_da_nebius_cloud"
   
Desenvolvido por Isac Barros - Engenharia de Software (UCB) |
Nebius x NVIDIA Global AI Hackathon
