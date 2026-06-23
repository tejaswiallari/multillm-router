from src.modules.feature_extractor import FeatureExtractor, QueryFeatures
from src.models.model_profiles import get_all_models, ModelProfile

class Router:
    def __init__(self):
        self.extractor = FeatureExtractor()
        self.models = get_all_models()

    def route(self, query: str) -> dict:
        features = self.extractor.extract(query)
        scores = {}

        for model_name, profile in self.models.items():
            score = self._calculate_score(features, profile)
            scores[model_name] = round(score, 2)

        best_model = max(scores, key=scores.get)
        explanation = self._explain(features, best_model, scores)

        return {
            "query": query,
            "features": features,
            "scores": scores,
            "selected_model": best_model,
            "explanation": explanation
        }

    def _calculate_score(self, features: QueryFeatures, profile: ModelProfile) -> float:
        # Match query type to model strength
        type_score = {
            "coding": profile.coding,
            "math": profile.math,
            "reasoning": profile.reasoning,
            "general": profile.general
        }.get(features.query_type, profile.general)

        # Complexity weight - prefer faster models for simple queries
        complexity_weight = {
            "low": profile.speed * 0.3,
            "medium": type_score * 0.2,
            "high": type_score * 0.3
        }.get(features.complexity, 0)

        # Cost weight - free models get a bonus
        cost_bonus = 1.0 if profile.cost == 0 else 0.0

        final_score = (type_score * 0.6) + complexity_weight + cost_bonus
        return final_score

    def _explain(self, features: QueryFeatures, best_model: str, scores: dict) -> str:
        profile = self.models[best_model]
        explanation = f"""
Selected Model : {profile.name}
Query Type     : {features.query_type}
Complexity     : {features.complexity}
Domain         : {features.domain}
Final Score    : {scores[best_model]}

All Scores:"""
        for model, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            explanation += f"\n  {model}: {score}"
        return explanation
