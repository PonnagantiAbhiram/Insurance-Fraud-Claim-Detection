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
    """
    Extract graph features using NetworkX and return
    graph metrics + nodes/edges for frontend visualization.
    """

    if insurance_graph is None:
        raise RuntimeError("Graph model is not loaded.")

    city = claim_data.get('incidentCity', 'Unknown')
    state = claim_data.get('policyState', 'Unknown')
    relationship = claim_data.get('insuredRelationship', 'Unknown')
    incident_type = claim_data.get('incidentType', 'Unknown')

    # --------------------------------------------------
    # Graph Metrics
    # --------------------------------------------------
    nodes_to_check = [city, state, relationship, incident_type]

    degrees = []
    connected_nodes = 0

    for node in nodes_to_check:
        if insurance_graph.has_node(node):
            degrees.append(insurance_graph.degree(node))
            connected_nodes += len(
                list(insurance_graph.neighbors(node))
            )
        else:
            degrees.append(0)

    avg_degree = (
        sum(degrees) / len(degrees)
        if degrees else 0
    )

    graph_features = {
        "graph_avg_degree": float(avg_degree),
        "graph_connected_entities": float(connected_nodes)
    }

    # --------------------------------------------------
    # Nodes for React Flow
    # --------------------------------------------------
    nodes = [
        {
            "id": "claim",
            "label": "Current Claim",
            "type": "claim"
        },
        {
            "id": "city",
            "label": city,
            "type": "city"
        },
        {
            "id": "state",
            "label": state,
            "type": "state"
        },
        {
            "id": "relationship",
            "label": relationship,
            "type": "relationship"
        },
        {
            "id": "incident",
            "label": incident_type,
            "type": "incident"
        }
    ]

    edges = [
        {
            "source": "claim",
            "target": "city"
        },
        {
            "source": "claim",
            "target": "state"
        },
        {
            "source": "claim",
            "target": "relationship"
        },
        {
            "source": "claim",
            "target": "incident"
        }
    ]

    # --------------------------------------------------
    # Risk Metrics
    # --------------------------------------------------
    relationship_strength = min(
        0.99,
        avg_degree / 10
    )

    risk_pattern = (
        "Detected Ring"
        if connected_nodes > 10
        else "Normal Cluster"
    )

    graph_frontend_data = {
        "connectedEntities": connected_nodes + 4,
        "relationshipStrength": round(
            relationship_strength,
            2
        ),
        "riskPattern": risk_pattern,

        # React Flow data
        "nodes": nodes,
        "edges": edges
    }

    return graph_features, graph_frontend_data