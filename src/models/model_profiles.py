from dataclasses import dataclass

@dataclass
class ModelProfile:
    name: str
    provider: str        # ollama or api
    model_id: str        # actual model name to call
    coding: float        # score out of 10
    reasoning: float
    math: float
    general: float
    speed: float
    cost: float          # 0 = free, higher = more expensive

MODEL_PROFILES = {
    "llama3.2": ModelProfile(
        name="Llama 3.2",
        provider="ollama",
        model_id="llama3.2",
        coding=8.0,
        reasoning=8.5,
        math=7.0,
        general=8.0,
        speed=9.0,
        cost=0.0
    ),
    "mistral": ModelProfile(
        name="Mistral",
        provider="ollama",
        model_id="mistral",
        coding=7.5,
        reasoning=7.0,
        math=8.0,
        general=8.5,
        speed=7.0,
        cost=0.0
    ),

    "gemma2": ModelProfile(
        name="Gemma 2",
        provider="ollama",
        model_id="gemma2",
        coding=7.0,
        reasoning=8.0,
        math=8.5,
        general=9.0,
        speed=8.0,
        cost=0.0
    ),
}

def get_model_profile(model_name: str) -> ModelProfile:
    return MODEL_PROFILES.get(model_name)

def get_all_models() -> dict:
    return MODEL_PROFILES
