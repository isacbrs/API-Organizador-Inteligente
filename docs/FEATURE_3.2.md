# 📄 Documentação Técnica - Feature 3.2: Motor Multimodal Vision (OCR Inteligente)

## 1. Visão Geral
A Feature 3.2 conclui a suíte multimodal da aplicação ao integrar processamento de imagens (OCR) com Extração Estruturada. O sistema recebe *scans* ou fotografias de faturas/boletos e, utilizando a Nebius AI Cloud, converte diretamente os *pixels* da imagem num DTO JSON limpo e inserível na base de dados.

## 2. Stack Tecnológica
* **Modelo Visual:** LLM Vision Instruct (Infraestrutura Nebius)
* **Gestão de *Payload*:** Codificação Base64 (*Data URI*)
* **Sanitização de Entrada:** FastAPI UploadFile com validação MIME-type

## 3. Detalhes de Arquitetura e Engenharia

### 3.1. *Stateless Processing* via Base64
Ao contrário do processamento acústico (Feature 3.1) que exige gestão de I/O em disco, a arquitetura da extração visual opera *in-memory* (*stateless*).
* O ficheiro é lido nativamente em RAM e imediatamente codificado para *Base64*.
* O modelo LLM Vision consome diretamente a *Data URI*, eliminando operações de leitura/escrita (*I/O operations*) em disco, reduzindo a latência do *endpoint* e anulando o risco de armazenamento excessivo de imagens temporárias no servidor.

### 3.2. Engenharia de *Prompt* Multimodal
O *payload* da requisição combina texto instrucional com o *buffer* de imagem.
* O parâmetro `detail: "high"` força a API de IA a particionar a imagem em blocos de alta resolução, crucial para a deteção precisa de dígitos pequenos (como cêntimos, taxas ou datas de vencimento borradas).
* A temperatura determinística (`temperature=0.0`) e o modo JSON (`json_object`) garantem que o modelo atue como um classificador analítico rígido, e não como um gerador de legendas de imagens criativo.