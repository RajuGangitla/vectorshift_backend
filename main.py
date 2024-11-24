from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import networkx as nx

# Define the request payload model
class PipelineData(BaseModel):
    nodes: list
    edges: list

app = FastAPI()

# CORS setup to allow the frontend (React) to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post('/pipelines/parse')
def parse_pipeline(pipeline_data: PipelineData):
    nodes = pipeline_data.nodes
    edges = pipeline_data.edges
    
    # Calculate number of nodes and edges
    num_nodes = len(nodes)
    num_edges = len(edges)
    
    # Create a directed graph to check if it's a DAG
    G = nx.DiGraph()
    
    # Add nodes to the graph
    G.add_nodes_from([node['id'] for node in nodes])
    
    # Add edges to the graph
    G.add_edges_from([(edge['source'], edge['target']) for edge in edges])
    
    # Check if the graph is a DAG
    is_dag = nx.is_directed_acyclic_graph(G)
    
    return {'num_nodes': num_nodes, 'num_edges': num_edges, 'is_dag': is_dag}
