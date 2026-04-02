# Rafael - AgeTech & HealthTech Ecosystem

**Rafael** não é apenas um software; é uma infraestrutura de cuidado contínuo, focado em atuar como um "Filho Digital" e um acompanhante inteligente para a terceira idade. Nosso objetivo é combater a solidão crônica, resolver a barreira de exclusão digital e prover uma rotina preventiva de saúde com integração IOT e IA generativa.

## 🎯 A Visão Macro

Rafael atua com empatia e inteligência em 3 Grandes Pilares:
1. **O Ecossistema de Voz (A Interface do Idoso):** O "Modo Totem", funcionando sem intervenção mecânica (Zero Interface UI). Uma interface proativa e animada por IA que puxa assunto, avisa sobre remédios e reage a estados emocionais.
2. **Saúde Preditiva (A Clínica Invisível):** Dados colhidos por voz ou wearables para formar um histórico sólido, identificando distúrbios sorrateiros precocemente (ex: insônia, alteração de humor).
3. **Dashboard Definitivo (Para Familiares/Médicos):** O "Painel de Tranquilidade" — que condensa tudo em uma linha do tempo clara para o cuidador/filho saber que "tudo está bem" sem precisar ligar com medo do pior, e alertas de emergência (Queda, AVC).

## 💻 Estrutura do Repositório (MVP)

A arquitetura inicial do repositório está subdividida em Backend e Frontend separadamente, para garantir escabilidade:

- `/rafael-app`: **Frontend SPA (Single Page Application)**
  - Construído com `React.js` (Vite) e `Tailwind CSS v4`.
  - Interfaces fiéis ao Design System (Mobile-First Dashboard UI & Totem UI).
  - Animações reativas fluidas com `Framer Motion` ("Esfera Viva").
- `/Backend`: **Inteligência Artificial & Fluxo Funcional**
  - Integrações utilizando `LangChain` via Python (como `Mente.py`) e orquestração dos serviços TTS locales como `Kokoro`.

## 🚀 Como Executar o Frontend Localmente

O Front-end do MVP é responsivo e roda com ambiente node. No diretório `rafael-app`, execute:

```bash
# Entre no diretório do front-end
cd rafael-app

# Instale os pacotes (na primeira vez)
npm install

# Rode o servidor de dev local
npm run dev
```

Pronto! Acesse preferencialmente http://localhost:5173 para explorar as interfaces de *Modo Painel* e o *Modo Totem*.
