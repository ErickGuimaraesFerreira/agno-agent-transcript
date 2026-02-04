# 🎬 Transcripter AI

Sistema inteligente de transcrição de vídeos e geração de conteúdo para Reels, utilizando IA para analisar e modelar o estilo de criadores de conteúdo.

## ✨ Funcionalidades

- **Transcrição Automática de Vídeos** - Suporta Groq (Whisper) e Google Gemini
- **Agente Copywriter IA** - Cria roteiros de Reels modelando o estilo de criadores
- **Pesquisa Web Integrada** - Utiliza Tavily para buscar informações atualizadas
- **Interface Web (Agent UI)** - Interface interativa para comunicação com o agente
- **Memória Persistente** - Histórico de conversas salvo em SQLite

## 🛠️ Tecnologias

| Categoria | Tecnologia |
|-----------|------------|
| Framework de Agentes | [Agno](https://github.com/agno-ai/agno) |
| LLM | Google Gemini 2.5 Flash/Pro |
| Transcrição | Groq Whisper / Gemini |
| Pesquisa Web | Tavily |
| Backend | FastAPI + Uvicorn |
| Package Manager | UV |

## 📁 Estrutura do Projeto

```
transcripter-ai/
├── agent.py                 # Agente copywriter principal
├── transcripter.py          # Transcrição com Groq/Whisper
├── transcripter_gemini.py   # Transcrição com Gemini
├── transcription_reader.py  # Ferramentas de leitura do banco
├── prompts/
│   └── copywriter.md        # Instruções do agente
├── gemini-transcripter/
│   └── transcriptions.json  # Banco de transcrições
├── agent-ui/                # Interface web
├── kallaway/                # Vídeos do creator Kallaway
├── jeffnippard/             # Vídeos do creator Jeff Nippard
└── rourkeheath/             # Vídeos do creator Rourke Heath
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.13+
- [UV](https://github.com/astral-sh/uv) (gerenciador de pacotes)

### Setup

```bash
# Clone o repositório
git clone (https://github.com/ErickGuimaraesFerreira/agno-agent-transcript)
cd transcripter-ai

# Instale as dependências
uv sync

# Configure as variáveis de ambiente
cp .env.example .env
```

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GROQ_API_KEY=sua_chave_groq
GOOGLE_API_KEY=sua_chave_google
TAVILY_API_KEY=sua_chave_tavily
```

## 📖 Uso

### 1. Transcrever Vídeos

**Com Groq (Whisper):**
```bash
uv run python transcripter.py
```

**Com Gemini:**
```bash
uv run python transcripter_gemini.py
```

> Os vídeos devem estar nas pastas `kallaway/`, `jeffnippard/` ou `rourkeheath/`

### 2. Iniciar o Agente Copywriter

```bash
uv run python agent.py
```

O agente estará disponível em `http://localhost:8000`

### 3. Usar a Interface Web

```bash
cd agent-ui
npm install
npm run dev
```

## 🤖 Como o Agente Funciona

1. **Pesquisa** - O agente busca informações sobre o tema solicitado
2. **Seleção de Creator** - Você escolhe qual criador modelar
3. **Geração de Hooks** - São gerados 10+ hooks baseados no estilo do creator
4. **Criação do Roteiro** - O Reel final é escrito imitando o formato do creator

## 🎯 Criadores Disponíveis

- **Kallaway** - Estilo motivacional e produtividade
- **Jeff Nippard** - Conteúdo fitness baseado em ciência
- **Rourke Heath** - Lifestyle e desenvolvimento pessoal

## 📝 Licença

MIT License

---

Desenvolvido com ❤️ usando [Agno](https://github.com/agno-ai/agno) e Google Gemini


