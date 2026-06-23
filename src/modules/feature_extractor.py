import re
from dataclasses import dataclass

@dataclass
class QueryFeatures:
    query_type: str      # coding, math, reasoning, general
    complexity: str      # low, medium, high
    domain: str          # ai, programming, healthcare, finance, education, general
    word_count: int
    complexity_score: float

class FeatureExtractor:
    def __init__(self):
        self.type_keywords = {
            "coding": ["code", "program", "function", "algorithm", "implement",
                      "debug", "python", "java", "class", "loop", "array",
                      "binary search", "sort", "recursion", "sql", "api"],
            "math": ["calculate", "solve", "equation", "integral", "derivative",
                    "matrix", "probability", "statistics", "algebra", "calculus"],
            "reasoning": ["compare", "analyze", "evaluate", "explain why",
                         "difference between", "pros and cons", "which is better",
                         "advantages", "disadvantages", "justify"],
            "general": ["what is", "who is", "when", "where", "how does",
                       "tell me", "explain", "describe", "define"]
        }

        self.domain_keywords = {
            "ai": ["machine learning", "deep learning", "neural network", "nlp",
                  "ai", "artificial intelligence", "model", "training", "dataset"],
            "programming": ["code", "software", "algorithm", "python", "java",
                           "javascript", "database", "api", "git", "docker"],
            "healthcare": ["medicine", "disease", "symptoms", "treatment", "doctor",
                          "hospital", "health", "medical", "patient", "drug"],
            "finance": ["money", "investment", "stock", "market", "bank",
                       "loan", "budget", "tax", "economy", "profit"],
            "education": ["learn", "study", "teach", "school", "university",
                         "course", "exam", "homework", "grade", "student"]
        }

    def extract(self, query: str) -> QueryFeatures:
        query_type = self._classify_type(query)
        complexity, complexity_score = self._analyze_complexity(query)
        domain = self._classify_domain(query)
        word_count = len(query.split())

        return QueryFeatures(
            query_type=query_type,
            complexity=complexity,
            domain=domain,
            word_count=word_count,
            complexity_score=complexity_score
        )

    def _classify_type(self, query: str) -> str:
        query_lower = query.lower()
        scores = {}
        for qtype, keywords in self.type_keywords.items():
            scores[qtype] = sum(1 for k in keywords if k in query_lower)
        if max(scores.values()) == 0:
            return "general"
        return max(scores, key=scores.get)

    def _analyze_complexity(self, query: str) -> tuple:
        score = 0.0
        word_count = len(query.split())

        if word_count > 50:
            score += 0.3
        elif word_count > 20:
            score += 0.2
        elif word_count > 10:
            score += 0.1

        if query.count("?") > 1:
            score += 0.1

        complex_words = ["implement", "design", "optimize", "comprehensive",
                        "advanced", "multiple", "integrate", "compare"]
        for word in complex_words:
            if word in query.lower():
                score += 0.1

        simple_words = ["what is", "define", "simple", "basic", "quick"]
        for word in simple_words:
            if word in query.lower():
                score -= 0.1

        score = max(0.0, min(1.0, score))

        if score >= 0.6:
            label = "high"
        elif score >= 0.3:
            label = "medium"
        else:
            label = "low"

        return label, round(score, 3)

    def _classify_domain(self, query: str) -> str:
        query_lower = query.lower()
        scores = {}
        for domain, keywords in self.domain_keywords.items():
            scores[domain] = sum(1 for k in keywords if k in query_lower)
        if max(scores.values()) == 0:
            return "general"
        return max(scores, key=scores.get)
