# QAfalda Quality Coach

QAfalda é um assistente em Python inspirado na Mafalda, com objetivo de tirar dúvidas e incentivar quem estuda qualidade de teste. Ela foi criada para ajudar com conteúdos do syllabus BSQTB-CTFL 4.0 em uma interface minimalista e leve.

## O que está incluído

- `main.py`: ponto de entrada para interface gráfica ou modo texto
- `web.py`: ponto de entrada da versão web com Flask
- `qafalda/`: pacote com a lógica da persona, base de conhecimento, interface e web app
- `README.md`: instruções de uso

## O que há de novo

- Respostas mais naturais e com tom incentivador
- Base de conhecimento ampliada para mais temas de qualidade de teste
- Interface web em Flask com layout leve e responsivo
- Fallback para modo texto em ambientes sem display gráfico
- **Novas páginas web:**
  - `/temas`: explore temas em cards interativos
  - `/dicas`: receba dicas diárias inspiradoras
  - `/quiz`: teste seus conhecimentos com mini quiz

## Como usar

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar interface gráfica ou texto

```bash
python main.py
```

- Se houver display, abre a janela Tkinter.
- Se não houver display, inicia em modo texto.

### Executar versão web

```bash
python web.py
```

Depois, abra no navegador:

```text
http://127.0.0.1:5000
```

## Sobre a QAfalda

- Responde a perguntas sobre fundamentos de teste, técnicas, gestão de defeitos, métricas, automação e muito mais.
- Tem uma interface minimalista e acolhedora, tanto na versão desktop quanto na web.
- Foi pensada para ser simples, prática e inspiradora para quem estuda qualidade de software.
- Usa um tom amigável e direto, sempre chamando o usuário de "QA" para criar identificação.
- Base de conhecimento abrangente com 31 tópicos do syllabus BSQTB-CTFL 4.0.

## Requisitos

- Python 3.10 ou superior
- Flask
- Tkinter para a interface desktop (normalmente já instalado com Python)
