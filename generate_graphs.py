import sys
sys.path.insert(0, ".")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import json

# Data from our evaluation
models = ["llama3.2", "mistral", "gemma2"]
query_types = ["Coding", "Math", "Reasoning", "General"]

# Model scores per query type
scores = {
    "llama3.2": [8.0, 7.0, 8.5, 8.0],
    "mistral":  [7.5, 8.0, 7.0, 8.5],
    "gemma2":   [7.0, 8.5, 8.0, 9.0]
}

# Graph 1: Model scores by query type
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("Multi-LLM Router - Evaluation Results", fontsize=16, fontweight="bold")

# Bar chart - scores by query type
x = np.arange(len(query_types))
width = 0.25
ax1 = axes[0]
for i, model in enumerate(models):
    ax1.bar(x + i*width, scores[model], width, label=model)
ax1.set_xlabel("Query Type")
ax1.set_ylabel("Score")
ax1.set_title("Model Scores by Query Type")
ax1.set_xticks(x + width)
ax1.set_xticklabels(query_types)
ax1.legend()
ax1.set_ylim(0, 10)

# Graph 2: Response times
query_labels = ["Binary\nSearch", "Derivative", "ML\nDefinition", "CNN vs\nRNN", "Linked\nList"]
response_times = [26.95, 3.08, 15.91, 26.98, 17.14]
ax2 = axes[1]
colors = ["#2196F3", "#4CAF50", "#FF9800", "#F44336", "#9C27B0"]
bars = ax2.bar(query_labels, response_times, color=colors)
ax2.set_xlabel("Query")
ax2.set_ylabel("Response Time (seconds)")
ax2.set_title("Response Time per Query")
for bar, time in zip(bars, response_times):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f"{time}s", ha="center", va="bottom", fontsize=9)

# Graph 3: Routing distribution
routing_counts = {"llama3.2": 3, "mistral": 0, "gemma2": 2}
ax3 = axes[2]
ax3.pie(routing_counts.values(), labels=routing_counts.keys(),
        autopct="%1.1f%%", startangle=90,
        colors=["#2196F3", "#4CAF50", "#FF9800"])
ax3.set_title("Model Selection Distribution")

plt.tight_layout()
plt.savefig("data/results/evaluation_graphs.png", dpi=150, bbox_inches="tight")
print("Graphs saved to data/results/evaluation_graphs.png")
