import sys
sys.path.insert(0, ".")
from src.utils.router import Router
from src.models.ollama_client import OllamaClient
import time
import json

def evaluate(queries):
    router = Router()
    client = OllamaClient()
    results = []

    for query in queries:
        print(f"Testing: {query[:50]}...")
        start = time.time()
        route_result = router.route(query)
        selected = route_result["selected_model"]
        response = client.generate(selected, query)
        end = time.time()

        results.append({
            "query": query,
            "selected_model": selected,
            "scores": route_result["scores"],
            "response_time": round(end - start, 2),
            "success": response["success"]
        })

    return results

test_queries = [
    "Write a Python binary search program",
    "Compare CNN and RNN neural networks",
    "Calculate the derivative of x squared",
    "What is machine learning",
    "Implement a linked list in Python"
]

print("Starting evaluation...")
results = evaluate(test_queries)

print("\nEvaluation Results:")
print("=" * 60)
for r in results:
    print(f"Query   : {r['query'][:45]}...")
    print(f"Model   : {r['selected_model']}")
    print(f"Time    : {r['response_time']}s")
    print(f"Success : {r['success']}")
    print("-" * 60)

with open("data/results/evaluation.json", "w") as f:
    json.dump(results, f, indent=2)
print("Results saved to data/results/evaluation.json")
