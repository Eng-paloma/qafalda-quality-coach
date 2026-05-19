import re
import unicodedata
from typing import List, Dict

KNOWLEDGE: List[Dict[str, str]] = [
    {
        "topic": "Fundamentos do teste",
        "question": "Qual é o objetivo do teste no CTFL 4.0?",
        "answer": "No CTFL, teste existe para avaliar qualidade, reduzir risco, prevenir defeitos e apoiar decisões de release com evidências.",
    },
    {
        "topic": "Fundamentos do teste",
        "question": "Quais são os princípios de teste no CTFL?",
        "answer": "Princípios-chave: teste mostra presença de defeitos, teste exaustivo é impossível, testar cedo gera benefício, defeitos se agrupam, cuidado com paradoxo do pesticida, teste depende de contexto e ausência de erros não garante valor.",
    },
    {
        "topic": "Teste ao longo do ciclo de vida",
        "question": "Como o teste se encaixa no ciclo de vida de desenvolvimento?",
        "answer": "O CTFL reforça atividades de teste em todo o ciclo, com níveis de teste (componente, integração, sistema e aceitação) alinhados a objetivos e riscos do produto.",
    },
    {
        "topic": "Teste ao longo do ciclo de vida",
        "question": "Como aplicar risk-based testing?",
        "answer": "No CTFL, priorização orientada a risco usa probabilidade e impacto para decidir cobertura, esforço e ordem de execução de testes.",
    },
    {
        "topic": "Teste estático",
        "question": "O que é teste estático?",
        "answer": "Teste estático avalia artefatos sem executar software, por exemplo com revisões de requisitos, walkthroughs, inspeções e análise estática de código.",
    },
    {
        "topic": "Teste estático",
        "question": "Qual a diferença entre revisão e análise estática?",
        "answer": "Revisão é atividade humana estruturada sobre artefatos; análise estática é verificação automatizada por ferramenta para detectar padrões de problema.",
    },
    {
        "topic": "Análise e projeto de testes",
        "question": "Quais técnicas de caixa preta aparecem no CTFL 4.0?",
        "answer": "Técnicas clássicas incluem partição de equivalência, análise de valor limite, tabela de decisão e transição de estados para projetar testes por comportamento.",
    },
    {
        "topic": "Análise e projeto de testes",
        "question": "Quais técnicas de caixa branca aparecem no CTFL 4.0?",
        "answer": "No nível Foundation, cobertura de instruções e cobertura de decisões são técnicas estruturais comuns para avaliar partes internas do código.",
    },
    {
        "topic": "Análise e projeto de testes",
        "question": "O que é teste baseado em experiência?",
        "answer": "É o uso de conhecimento prévio do testador para criar testes úteis rapidamente, como adivinhação de erros e teste exploratório.",
    },
    {
        "topic": "Gerenciamento das atividades de teste",
        "question": "Quais atividades de gerenciamento de teste o CTFL cobre?",
        "answer": "Planejamento, monitoramento, controle, encerramento e gestão de comunicação entre partes interessadas, sempre com rastreabilidade e foco em risco.",
    },
    {
        "topic": "Gerenciamento das atividades de teste",
        "question": "Quais métricas de teste são úteis?",
        "answer": "Métricas úteis incluem progresso da execução, cobertura de requisitos, tendências de defeitos e status de risco para apoiar decisões objetivas.",
    },
    {
        "topic": "Gerenciamento das atividades de teste",
        "question": "Como funciona gestão de defeitos?",
        "answer": "Fluxo típico: registrar defeito com evidência, classificar severidade/prioridade, acompanhar correção, retestar e fechar com rastreabilidade.",
    },
    {
        "topic": "Ferramentas de teste",
        "question": "Como o CTFL trata ferramentas de teste?",
        "answer": "O syllabus descreve benefícios, riscos e critérios de adoção de ferramentas para apoiar planejamento, execução, automação, gestão de defeitos e integração contínua.",
    },
    {
        "topic": "Ferramentas de teste",
        "question": "Quando usar automação de testes?",
        "answer": "Automação é mais indicada em cenários repetitivos e estáveis, principalmente regressão e checks rápidos em pipeline; exige manutenção e estratégia clara.",
    },
]


def normalize_text(text: str) -> List[str]:
    text_no_accents = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^a-z0-9\s]", " ", text_no_accents.lower())
    return [word for word in cleaned.split() if word]


def score_match(query: str, text: str) -> float:
    query_tokens = set(normalize_text(query))
    text_tokens = set(normalize_text(text))
    if not query_tokens or not text_tokens:
        return 0.0
    overlap = query_tokens & text_tokens
    return len(overlap) / max(len(text_tokens), 1)


def find_best_knowledge(query: str) -> Dict[str, str]:
    best_item = None
    best_score = 0.0
    for item in KNOWLEDGE:
        score = (
            score_match(query, item["question"]) +
            score_match(query, item["answer"]) +
            score_match(query, item["topic"])
        )
        if score > best_score:
            best_score = score
            best_item = item
    return best_item if best_item else KNOWLEDGE[0]
