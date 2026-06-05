import React from 'react';
import ReactFlow from 'reactflow';
import 'reactflow/dist/style.css';
import styles from './GraphSection.module.css';

const GraphSection = ({ data }) => {

  console.log("GRAPH DATA:", data);

  if (!data) return null;
  const nodes = data.nodes.map((node, index) => ({
    id: node.id,
    data: {
      label: node.label
    },
    position: {
      x: index === 0 ? 350 : 150 * index,
      y: index === 0 ? 50 : 250
    }
  }));

  const edges = data.edges.map((edge, index) => ({
    id: `e${index}`,
    source: edge.source,
    target: edge.target,
    animated: true
  }));

  return (
    <div className={`card ${styles.container}`}>
      <h2 className="section-title">
        Claim Relationship Analysis
      </h2>

      <p className="section-subtitle">
        Graph-based feature extraction for network analysis
      </p>

      <div
        style={{
          height: "450px",
          borderRadius: "12px",
          overflow: "hidden",
          border: "1px solid #e5e7eb"
        }}
      >
        <ReactFlow
          nodes={nodes}
          edges={edges}
          fitView
        />
      </div>

      <div className={styles.graphInsights}>
        <div className={styles.insightBox}>
          <h4 className={styles.insightTitle}>
            Connected Entities
          </h4>

          <p className={styles.insightValue}>
            {data.connectedEntities}
          </p>
        </div>

        <div className={styles.insightBox}>
          <h4 className={styles.insightTitle}>
            Relationship Strength
          </h4>

          <p className={styles.insightValue}>
            {data.relationshipStrength}
          </p>
        </div>

        <div className={styles.insightBox}>
          <h4 className={styles.insightTitle}>
            Risk Pattern
          </h4>

          <p
            className={styles.insightValue}
            style={{
              color:
                data.riskPattern === "Detected Ring"
                  ? "var(--fraud-alert)"
                  : "var(--success)"
            }}
          >
            {data.riskPattern}
          </p>
        </div>
      </div>
    </div>
  );
};

export default GraphSection;