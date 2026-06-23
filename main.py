import sys
sys.path.insert(0, '.')
from src.utils.router import Router
from src.models.ollama_client import OllamaClient

def run(query: str):
    print("=" * 50)
    print(f"Query: {query}")
    print("=" * 50)

    # Step 1: Route the query
    router = Router()
    result = router.route(query)
    print(result['explanation'])

    # Step 2: Get response from selected model
    print("\nGenerating response...")
    print("-" * 50)
    client = OllamaClient()
    response = client.generate(result['selected_model'], query)

    if response['success']:
        print(f"Response from {response['model']}:\n")
        print(response['response'])
    else:
        print(f"Error: {response['response']}")
    print("=" * 50)

if __name__ == "__main__":
    query = input("Enter your query: ")
    run(query)
