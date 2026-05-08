from pathlib import Path
import textwrap

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


SOURCE = "Dormitory #14"
TARGET = "4th Building LPNU"
OUTPUT_FILE = Path(__file__).with_name("graph_visualization.png")


def build_graph() -> nx.Graph:
	graph = nx.Graph()

	edges = [
		("Dormitory #14", "Avalon Lux", 133.56),
		("Dormitory #14", "Silpo", 445.09),
		("Silpo", "Nova Post #19", 165.74),
		("Avalon Lux", "Nova Post #19", 301.67),
		("Nova Post #19", "Medic", 360.22),
		("Medic", "Church of Saint Clement", 358.33),
		("Medic", "Kotlyarevskiy street intersection", 293.67),
		("Medic", "Stanislava Lema Square", 406.91),
		("Church of Saint Clement", "Sosnovskiy Palace", 148.78),
		("Kotlyarevskiy street intersection", "Kyivska street intersection", 316.25),
		("Stanislava Lema Square", "Tocha (tea store)", 253.11),
		("Sosnovskiy Palace", "Kyivska street intersection", 136.77),
		("Tocha (tea store)", "Simi", 124.81),
		("Sosnovskiy Palace", "Galya Baluvana", 145.42),
		("Kyivska street intersection", "Blizenko", 240.77),
		("Galya Baluvana", "Unitas", 97.21),
		("Simi", "Central Building LPNU", 67.58),
		("Blizenko", "Architector's street", 62.40),
		("Architector's street", "2nd Building LPNU", 78.08),
		("Central Building LPNU", "2nd Building LPNU", 159.02),
		("Unitas", "KaVa", 95.45),
		("Unitas", "Starytskiy street", 77.59),
		("KaVa", "7th Building LPNU", 95.45),
		("Starytskiy street", "7th Building LPNU", 106.17),
		("7th Building LPNU", "4th Building LPNU", 200.91),
		("2nd Building LPNU", "4th Building LPNU", 68.62),
	]

	for left, right, weight in edges:
		graph.add_edge(left, right, weight=weight)

	return graph


def classify_node(node: str) -> str:
	lower = node.lower()

	if node == SOURCE:
		return "source"
	if node == TARGET:
		return "target"
	if "lpnu" in lower:
		return "campus"
	if "street" in lower or "intersection" in lower:
		return "route"
	return "landmark"


def wrap_label(label: str, width: int = 16) -> str:
	return textwrap.fill(label, width=width)


def main() -> None:
	graph = build_graph()
	weighted_path = nx.shortest_path(graph, source=SOURCE, target=TARGET, weight="weight", methid="dijkstra")
	total_weight = nx.path_weight(graph, weighted_path, weight="weight")

	positions = nx.spring_layout(graph, seed=42, k=1.15, iterations=300)

	node_palette = {
		"source": "#e76f51",
		"target": "#2a9d8f",
		"campus": "#264653",
		"route": "#8d99ae",
		"landmark": "#f4a261",
	}

	path_nodes = set(weighted_path)

	fig, ax = plt.subplots(figsize=(18, 12), facecolor="#f8fafc")
	ax.set_facecolor("#f8fafc")
	ax.set_title(
		"Dormitory #14 to 4th Building LPNU\nWeighted shortest path highlighted",
		fontsize=20,
		fontweight="bold",
		color="#1f2937",
		pad=20,
	)

	# draw the full network
	nx.draw_networkx_edges(
		graph,
		positions,
		ax=ax,
		edge_color="#cbd5e1",
		width=1.6,
		alpha=0.45,
	)

	# shortest path
	for left, right in zip(weighted_path, weighted_path[1:]):
		nx.draw_networkx_edges(
			graph,
			positions,
			edgelist=[(left, right)],
			ax=ax,
			edge_color="#ef4444",
			width=4.2,
			alpha=0.95,
		)

	# draw nodes by category
	for category in ["landmark", "route", "campus", "source", "target"]:
		nodes = [node for node in graph.nodes if classify_node(node) == category]
		if not nodes:
			continue

		nx.draw_networkx_nodes(
			graph,
			positions,
			nodelist=nodes,
			node_size=[1650 if node in (SOURCE, TARGET) else 950 if node in path_nodes else 780 for node in nodes],
			node_color=node_palette[category],
			edgecolors=["#111827" if node in path_nodes else "#ffffff" for node in nodes],
			linewidths=[2.8 if node in (SOURCE, TARGET) else 2.0 if node in path_nodes else 1.2 for node in nodes],
			ax=ax,
		)

	#  labels
	wrapped_labels = {node: wrap_label(node) for node in graph.nodes}
	nx.draw_networkx_labels(
		graph,
		positions,
		labels=wrapped_labels,
		font_size=9.5,
		font_weight="semibold",
		font_color="#0f172a",
		bbox={"boxstyle": "round,pad=0.25", "fc": "#ffffff", "ec": "#e2e8f0", "alpha": 0.92},
		ax=ax,
	)

	path_edge_labels = {
		(left, right): f"{graph[left][right]['weight']:.2f}"
		for left, right in zip(weighted_path, weighted_path[1:])
	}
	nx.draw_networkx_edge_labels(
		graph,
		positions,
		edge_labels=path_edge_labels,
		font_size=9,
		font_color="#b91c1c",
		rotate=False,
		label_pos=0.5,
		bbox={"boxstyle": "round,pad=0.18", "fc": "#fff1f2", "ec": "#fecdd3", "alpha": 0.95},
		ax=ax,
	)

	legend_handles = [
		Patch(facecolor=node_palette["source"], edgecolor="#111827", label="Source"),
		Patch(facecolor=node_palette["target"], edgecolor="#111827", label="Target"),
		Patch(facecolor=node_palette["campus"], edgecolor="#111827", label="Campus building"),
		Patch(facecolor=node_palette["route"], edgecolor="#111827", label="Street / intersection"),
		Patch(facecolor=node_palette["landmark"], edgecolor="#111827", label="Landmark / stop"),
		Line2D([0], [0], color="#ef4444", lw=4.2, label="Shortest path"),
	]
	ax.legend(
		handles=legend_handles,
		loc="upper right",
		frameon=True,
		fancybox=True,
		framealpha=0.95,
		facecolor="white",
		edgecolor="#e2e8f0",
		fontsize=10,
	)

	fig.text(
		0.5,
		0.02,
		f"Shortest route: {' → '.join(weighted_path)}    |    Total cost: {total_weight:.2f} seconds. I.e {total_weight / 60:.2f} minutes",
		ha="center",
		va="bottom",
		fontsize=11,
		color="#334155",
		bbox={"boxstyle": "round,pad=0.35", "fc": "#ffffff", "ec": "#cbd5e1", "alpha": 0.96},
	)

	ax.axis("off")
	fig.tight_layout(rect=(0, 0.05, 1, 1))
	fig.savefig(OUTPUT_FILE, dpi=220, bbox_inches="tight")
	plt.close(fig)

	print(f"Shortest path: {weighted_path}")
	print(f"Total distance: {total_weight:.2f}")
	print(f"Saved visualization to: {OUTPUT_FILE}")


if __name__ == "__main__":
	main()
