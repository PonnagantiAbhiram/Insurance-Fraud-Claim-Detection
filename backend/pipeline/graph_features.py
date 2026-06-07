import os
import pickle
import networkx as nx

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

insurance_graph = None

def load_graph_model():
    global insurance_graph
    try:
        with open(os.path.join(MODELS_DIR, 'insurance_graph.pkl'), 'rb') as f:
            insurance_graph = pickle.load(f)
        print("Graph model loaded successfully.")
    except Exception as e:
        print(f"Error loading Graph model: {e}")

load_graph_model()

def extract_graph_features(claim_data):
    if insurance_graph is None:
        raise RuntimeError("Graph model is not loaded.")

    city         = claim_data.get('incidentCity', 'Unknown')
    state        = claim_data.get('policyState', 'Unknown')
    relationship = claim_data.get('insuredRelationship', 'Unknown')
    incident_type= claim_data.get('incidentType', 'Unknown')

    nodes_to_check = [city, state, relationship, incident_type]
    degrees = []
    connected_nodes = 0

    for node in nodes_to_check:
        try:
            if insurance_graph.has_node(node):
                degrees.append(insurance_graph.degree(node))
                connected_nodes += len(list(insurance_graph.neighbors(node)))
            else:
                degrees.append(0)
        except Exception as e:
            print(f"Warning: Graph node {node}: {e}")
            degrees.append(0)

    avg_degree = sum(degrees) / len(degrees) if degrees else 0

    # -------------------------------------------------------
    # FIX: model expects graph_degree_centrality,
    # graph_clustering_coeff, graph_pagerank
    # (not graph_avg_degree / graph_connected_entities)
    # -------------------------------------------------------
    num_nodes = insurance_graph.number_of_nodes()
    degree_centrality = avg_degree / (num_nodes - 1) if num_nodes > 1 else 0.0

    # Compute clustering coefficient for known nodes only
    known_nodes = [n for n in nodes_to_check if insurance_graph.has_node(n)]
    if known_nodes:
        clustering = nx.average_clustering(insurance_graph, nodes=known_nodes)
    else:
        clustering = 0.0

    # Approximate pagerank from pre-computed graph
    try:
        pr = nx.pagerank(insurance_graph, max_iter=50)
        pagerank_vals = [pr.get(n, 0.0) for n in nodes_to_check]
        avg_pagerank = sum(pagerank_vals) / len(pagerank_vals)
    except Exception:
        avg_pagerank = 0.0

    graph_features = {
        "graph_degree_centrality": float(degree_centrality),
        "graph_clustering_coeff":  float(clustering),
        "graph_pagerank":          float(avg_pagerank),
    }

    # Frontend visualisation data (unchanged)
    nodes = [
        {"id": "claim",        "label": "Current Claim",  "type": "claim"},
        {"id": "city",         "label": city,              "type": "city"},
        {"id": "state",        "label": state,             "type": "state"},
        {"id": "relationship", "label": relationship,      "type": "relationship"},
        {"id": "incident",     "label": incident_type,     "type": "incident"},
    ]
    edges = [
        {"source": "claim", "target": "city"},
        {"source": "claim", "target": "state"},
        {"source": "claim", "target": "relationship"},
        {"source": "claim", "target": "incident"},
    ]

    relationship_strength = min(0.99, avg_degree / 10)
    risk_pattern = "Detected Ring" if connected_nodes > 10 else "Normal Cluster"

    graph_frontend_data = {
        "connectedEntities":    connected_nodes + 4,
        "relationshipStrength": round(relationship_strength, 2),
        "riskPattern":          risk_pattern,
        "nodes":                nodes,
        "edges":                edges,
    }

    return graph_features, graph_frontend_data