import random
from typing import Optional

from .knowledge import KNOWLEDGE, normalize_text, score_match

GREETINGS = [
    "Olá QA! Que bom te ver por aqui. Sobre qual tema CTFL você quer conversar?",
    "Oi QA! Estou aqui para te ajudar com os temas CTFL. O que você quer aprender agora?",
    "Olá QA! Vamos estudar juntos. Me diga qual tema CTFL você quer explorar.",
]

THANK_YOU = [
    "Fico tão feliz em poder ajudar, QA! Continue testando com dedicação.",
    "Que bom que consegui esclarecer suas dúvidas, QA. Estou sempre aqui!",
    "Foi um prazer ajudar, QA! Você está no caminho certo para se tornar um excelente QA.",
]

GOODBYES = [
    "Até mais, QA! Teste tudo com muito carinho e qualidade.",
    "Tchau QA! Volte sempre que precisar de dicas sobre testes.",
    "Foi ótimo conversar com você, QA! Até a próxima!",
]

FALLBACKS = [
    "Estou aqui para te ajudar com QA de forma bem prática e objetiva. Que tal perguntar sobre testes funcionais, não funcionais ou gestão de qualidade?",
    "Posso explicar conceitos de QA, técnicas de teste, planejamento de testes ou boas práticas. O que mais te interessa?",
    "Vamos conversar sobre qualidade de software! Pergunte sobre casos de teste, cobertura, métricas ou automação de testes.",
]

PERSONALITY_PREFIXES = [
    "Claro, QA. ",
    "Perfeito, QA. ",
    "Vamos lá, QA. ",
]

ENCOURAGEMENTS = [
    "Quer que eu dê um exemplo prático sobre isso?",
    "Continue perguntando, QA! Estou adorando nossa conversa sobre testes.",
    "Você está evoluindo muito bem como QA! Que tal explorar mais esse tema?",
]

SYLLABUS_TOPICS = [
    "Fundamentos do teste",
    "Teste ao longo do ciclo de vida",
    "Teste estático",
    "Análise e projeto de testes",
    "Gerenciamento das atividades de teste",
    "Ferramentas de teste",
]

OUT_OF_SCOPE_MESSAGE = (
    "Esse assunto está fora da minha alçada no momento. "
    "Eu consigo responder apenas temas do syllabus CTFL."
)

TOPIC_GUIDES = {
    "Fundamentos do teste": "foco em objetivo de teste, princípios e risco.",
    "Teste ao longo do ciclo de vida": "foco em níveis, tipos de teste e alinhamento com desenvolvimento.",
    "Teste estático": "foco em revisão e análise sem execução de software.",
    "Análise e projeto de testes": "foco em técnicas de caixa preta, branca e experiência.",
    "Gerenciamento das atividades de teste": "foco em planejamento, monitoramento, métricas e defeitos.",
    "Ferramentas de teste": "foco em adoção de ferramentas e automação com critério.",
}

class QAfalda:
    def __init__(self):
        self.name = "QAfalda"
        self.style = """
QAfalda: inteligente, curiosa e acolhedora. Ela lembra a Mafalda, mas fala sobre qualidade de teste.
"""
        self.syllabus_items = [item for item in KNOWLEDGE if item["topic"] in SYLLABUS_TOPICS]
        self.topic_keywords = {
            "Fundamentos do teste": {"fundamento", "fundamentos", "principio", "principios", "objetivo", "risco", "qualidade"},
            "Teste ao longo do ciclo de vida": {"ciclo", "vida", "nivel", "niveis", "integracao", "sistema", "aceitacao", "risk", "based"},
            "Teste estático": {"estatico", "revisao", "inspecao", "walkthrough", "analise", "codigo"},
            "Análise e projeto de testes": {"caixa", "preta", "branca", "equivalencia", "limite", "decisao", "estado", "experiencia", "exploratorio"},
            "Gerenciamento das atividades de teste": {"planejamento", "monitoramento", "controle", "metrica", "metricas", "defeito", "triagem", "prioridade"},
            "Ferramentas de teste": {"ferramenta", "ferramentas", "automacao", "pipeline", "ci", "gestao", "suporte"},
        }

    def respond(self, question: str) -> str:
        return self.respond_with_context(question)["text"]

    def respond_with_context(self, question: str, context: Optional[dict] = None) -> dict:
        ctx = context or {}
        text = question.strip()
        if not text:
            return {
                "text": "Olá QA. Me conte qual tema você quer explorar.",
                "topic": None,
                "actions": self._actions_for_topic(None),
                "context": {"last_topic": None},
            }

        normalized = normalize_text(text)
        detected_topic = self._detect_topic_from_text(normalized)
        best_item, best_score = self._find_best_syllabus_item(text)

        if "estudo" in normalized and "caso" in normalized:
            if detected_topic:
                item = self._find_item_by_topic(detected_topic)
            elif best_score >= 0.20:
                item = best_item
            elif ctx.get("last_topic"):
                item = self._find_item_by_topic(ctx["last_topic"])
            else:
                return {
                    "text": "Claro, QA. Para montar estudo de caso, primeiro escolha um dos temas CTFL disponíveis.",
                    "topic": None,
                    "actions": self._actions_for_topic(None),
                    "context": ctx,
                }
            return {
                "text": self._build_case_study(item),
                "topic": item["topic"],
                "actions": self._actions_for_topic(item["topic"]),
                "context": {"last_topic": item["topic"]},
            }

        if any(word in normalized for word in ["passo", "roteiro", "como", "aplicar"]):
            target_topic = detected_topic or ctx.get("last_topic")
            if target_topic:
                return {
                    "text": self._build_step_by_step(target_topic),
                    "topic": target_topic,
                    "actions": self._actions_for_topic(target_topic),
                    "context": {"last_topic": target_topic},
                }

        if ("outro" in normalized and "assunto" in normalized) or ("outro" in normalized and "tema" in normalized):
            return {
                "text": self._topic_guidance_message(full=True),
                "topic": None,
                "actions": self._actions_for_topic(None),
                "context": {"last_topic": None},
            }

        if any(word in normalized for word in ["olá", "oi", "bom", "boa", "hello", "eai"]):
            return {
                "text": "Olá QA. " + self._topic_guidance_message(),
                "topic": None,
                "actions": self._actions_for_topic(None),
                "context": ctx,
            }

        if any(word in normalized for word in ["obrigado", "valeu", "brigado", "thanks"]):
            return {
                "text": random.choice(THANK_YOU),
                "topic": ctx.get("last_topic"),
                "actions": self._actions_for_topic(ctx.get("last_topic")),
                "context": ctx,
            }

        if any(word in normalized for word in ["tchau", "até", "adeus", "bye", "see"]):
            return {
                "text": random.choice(GOODBYES),
                "topic": None,
                "actions": [],
                "context": {"last_topic": None},
            }

        if any(word in normalized for word in ["lista", "tópico", "topico", "sintese", "resuma", "temas", "conteudo"]):
            return {
                "text": self._topic_guidance_message(full=True),
                "topic": None,
                "actions": self._actions_for_topic(None),
                "context": ctx,
            }

        if any(word in normalized for word in ["mafalda", "qafalda", "persona", "personagem"]):
            return {
                "text": (
                    "Eu sou a QAfalda, uma persona inspirada na Mafalda. "
                    "Meu papel é tirar dúvidas sobre qualidade de teste e incentivar quem estuda QA."
                ),
                "topic": None,
                "actions": self._actions_for_topic(None),
                "context": ctx,
            }

        if detected_topic:
            topic_item = self._find_item_by_topic(detected_topic)
            response = self._compose_topic_response(topic_item)
            return {
                "text": response,
                "topic": topic_item["topic"],
                "actions": self._actions_for_topic(topic_item["topic"]),
                "context": {"last_topic": topic_item["topic"]},
            }

        if best_score > 0.22:
            response = self._compose_topic_response(best_item)
            return {
                "text": response,
                "topic": best_item["topic"],
                "actions": self._actions_for_topic(best_item["topic"]),
                "context": {"last_topic": best_item["topic"]},
            }

        return {
            "text": OUT_OF_SCOPE_MESSAGE + "\n\n" + self._topic_guidance_message(full=True),
            "topic": None,
            "actions": self._actions_for_topic(None),
            "context": {"last_topic": None},
        }

    def _compose_topic_response(self, item: dict) -> str:
        guide = TOPIC_GUIDES.get(item["topic"], "foco em aplicação prática para QA.")
        return (
            f"Entendi, QA. Vamos falar de {item['topic']}.\n"
            f"Resumo prático: {item['answer']}\n"
            f"Direção de estudo: {guide}\n\n"
            "Quer seguir com estudo de caso ou com passo a passo?"
        )

    def _build_step_by_step(self, topic: str) -> str:
        return (
            f"Perfeito, QA. Passo a passo para {topic}:\n"
            "1) Defina o objetivo do teste e o risco principal.\n"
            "2) Escolha os cenários críticos do fluxo.\n"
            "3) Escreva casos com resultado esperado claro.\n"
            "4) Execute, registre evidências e defeitos.\n"
            "5) Reavalie risco e avance para regressão."
        )

    def _estimate_relevance(self, question: str, item: dict) -> float:
        from .knowledge import score_match

        return (
            score_match(question, item["question"]) * 0.6 +
            score_match(question, item["answer"]) * 0.3 +
            score_match(question, item["topic"]) * 0.1
        )

    def _friendly_fallback(self, question: str) -> str:
        normalized = normalize_text(question)
        if any(word in normalized for word in ["por", "que", "porque", "pq"]):
            return (
                "Às vezes a melhor resposta é um exemplo. "
                "Tente me perguntar sobre um tipo específico de teste ou um caso prático de QA."
            )
        return random.choice(FALLBACKS)

    def _topic_guidance_message(self, full: bool = False) -> str:
        if full:
            return "Escolha um tema CTFL para começarmos:\n- " + "\n- ".join(SYLLABUS_TOPICS)
        return "Escolha um tema CTFL para começarmos."

    def _build_case_study(self, item: dict) -> str:
        return (
            f"Perfeito, QA. Estudo de caso prático para {item['topic']}:\n"
            "Exemplo 1: um checkout começou a falhar após atualização.\n"
            "Ação: priorizar o risco crítico, executar cenários essenciais, registrar evidências e validar correção.\n\n"
            "Exemplo 2: release semanal aumentou defeitos em produção.\n"
            "Ação: aplicar técnica do tema para selecionar testes de maior impacto antes do deploy e medir resultado no ciclo seguinte.\n\n"
            f"Base técnica do tema: {item['answer']}"
        )

    def _actions_for_topic(self, topic: Optional[str]) -> list[dict]:
        if topic:
            return [
                {"label": "Estudo de caso", "prompt": f"Quero um estudo de caso sobre {topic}"},
                {"label": "Escolher outro assunto", "prompt": "Quero escolher outro assunto"},
            ]
        return [{"label": topic_name, "prompt": topic_name} for topic_name in SYLLABUS_TOPICS]

    def suggest_topics(self, question: str) -> list[str]:
        _ = question
        return SYLLABUS_TOPICS

    def _find_best_syllabus_item(self, question: str) -> tuple[dict, float]:
        best_item = self.syllabus_items[0]
        best_score = 0.0
        for item in self.syllabus_items:
            score = (
                score_match(question, item["question"]) * 0.55 +
                score_match(question, item["answer"]) * 0.30 +
                score_match(question, item["topic"]) * 0.15
            )
            if score > best_score:
                best_score = score
                best_item = item
        return best_item, best_score

    def _find_item_by_topic(self, topic: str) -> dict:
        for item in self.syllabus_items:
            if item["topic"] == topic:
                return item
        return self.syllabus_items[0]

    def _detect_topic_from_text(self, normalized_tokens: list[str]) -> Optional[str]:
        token_set = set(normalized_tokens)
        best_topic = None
        best_overlap = 0
        for topic, keywords in self.topic_keywords.items():
            overlap = len(token_set & keywords)
            if overlap > best_overlap:
                best_overlap = overlap
                best_topic = topic
        return best_topic if best_overlap > 0 else None

    def _get_topic_suggestions(self, current_topic: str) -> list[str]:
        """Retorna sugestões de assuntos relacionados ao tópico atual."""
        topic_suggestions = {
            "Fundamentos de Teste": ["Casos de Teste", "Cenários de Teste", "Planejamento de Testes"],
            "Técnicas de Teste": ["Teste de Caixa Preta", "Teste de Caixa Branca", "Teste de Integração"],
            "Gestão de Testes": ["Métricas de Teste", "Relatórios de Teste", "Gestão de Defeitos"],
            "Ferramentas de Teste": ["Automação de Testes", "Ferramentas de Gerenciamento", "Teste de Performance"],
            "Qualidade de Software": ["Processos de QA", "Padrões de Qualidade", "Certificações"],
        }

        # Retorna sugestões relacionadas ou uma seleção aleatória se não encontrar
        if current_topic in topic_suggestions:
            return random.sample(topic_suggestions[current_topic], min(2, len(topic_suggestions[current_topic])))

        # Fallback: retorna alguns tópicos gerais
        all_topics = ["Fundamentos de Teste", "Técnicas de Teste", "Gestão de Testes", "Ferramentas de Teste"]
        return random.sample(all_topics, 2)