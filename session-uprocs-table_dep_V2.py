import json
import networkx as nx
from pyvis.network import Network
import streamlit as st
import streamlit.components.v1 as components

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload JSON data", type=["json"])

if uploaded_file is not None:
    data = uploaded_file.getvalue().decode("utf-8")
    json_data = json.loads(data)
else:
    st.warning('Please upload your Json file.')
    st.stop()

# Extract nodes and edges
nodes = []
edges = []

def plot_network_graph():
    # Function to add nodes and edges for inputs and outputs
    def add_input_output_nodes(process_name, inputs, outputs):
        for inp in inputs:
            nodes.append({"id": inp, "title": "", "color": ""})
            edges.append((inp, process_name))
        for out in outputs:
            nodes.append({"id": out, "title": "", "color": ""})
            edges.append((process_name, out))

    # Function to add nodes for table_deps
    def add_table_deps_nodes(uprocs_name, table_deps):
        for table_dep, table_dep_content in table_deps.items():
            if table_dep not in nodes:
                nodes.append({"id": table_dep, "title": table_dep_content, "color": "#00FFFF"}) 
            edges.append((uprocs_name, table_dep))

    # Process each process (uprocs) in the JSON data
    for process_name, process_info in json_data.items():
        nodes.append({"id": process_name, "title": "", "color": ""})
        inputs = process_info.get("inputs", [])
        outputs = process_info.get("outputs", [])
        add_input_output_nodes(process_name, inputs, outputs)

        for uprocs_info in process_info.get("uprocs", []):
            uprocs_name = uprocs_info.get("name")
            uprocs_label = uprocs_info.get("label")
            nodes.append({"id": uprocs_name, "title": "", "color": ""})
            edges.append((process_name, uprocs_name))
            add_table_deps_nodes(uprocs_name, uprocs_info.get("table_deps", {}))

    # Create a graph
    G = nx.DiGraph()

    # Add nodes and edges to the graph
    G.add_nodes_from(node_data["id"] for node_data in nodes)
    G.add_edges_from(edges)

    # Plot the interactive diagram using pyvis
    nt = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True, notebook=True, cdn=True)  
    nt.show_buttons(filter_=['physics'])

    # Define colors for uprocs, input/output nodes, and nodes with table_deps
    uprocs_color = "#FF0000"  # Red for uprocs
    input_output_color = "#00FF00"  # Green for input/output nodes
    table_deps_color = "#00FFFF"  # Cyan for nodes with table_deps

    # Add nodes with attributes to the graph
    for node_data in nodes:
        node_attributes = {}
        node_id = node_data["id"]
        node_attributes["title"] = node_data["title"]  # Use 'title' to set the tooltip text

        # Check if the node is an "uprocs" or an input/output node and update the color accordingly
        if node_id in json_data:
            node_attributes["color"] = uprocs_color
            node_attributes["group"] = "uprocs"  # Add the 'group' attribute for clusters
        else:
            node_attributes["color"] = input_output_color

        # Check if the node has "table_deps" and update the color accordingly
        if node_id in [table_dep["id"] for table_dep in nodes if table_dep["color"] == table_deps_color]:
            node_attributes["color"] = table_deps_color

        nt.add_node(node_id, label=node_id, **node_attributes)

    # Create clusters for sessions and uprocs
    nt.set_options("""{
      "nodes": {
        "borderWidth": 3,
        "font": {
          "size": 30
        },
        "shape": "dot"
      },
      "edges": {
        "arrows": {
          "to": {
            "enabled": true,
            "scaleFactor": 0.5
          }
        }
      },
      "physics": {
        "enabled": true,
        "solver": "repulsion"
      },
      "groups": {
        "uprocs": {
          "color": {
            "background": "#FF0000",
            "border": "#FF0000",
            "highlight": {
              "background": "#FF0000",
              "border": "#FF0000"
            }
          },
          "font": {
            "color": "#FFFFFF"
          }
        },
        "input_output": {
          "color": {
            "background": "#00FF00",
            "border": "#00FF00",
            "highlight": {
              "background": "#00FF00",
              "border": "#00FF00"
            }
          },
          "font": {
            "color": "#FFFFFF"
          }
        }
      }
    }""")

    # Add edges with arrows for dependencies
    for edge in G.edges:
        source, target = edge
        # Check if source node exists, if not create a new node
        if source not in nt.get_nodes():
            nt.add_node(source, label=source, group="input_output")  # Assign the 'input_output' group for input/output nodes
        # Check if target node exists, if not create a new node
        if target not in nt.get_nodes():
            nt.add_node(target, label=target, group="input_output")
        nt.add_edge(source, target, arrows='to', arrowStrikethrough=False, color="#87CEFA")  # Black color for arrows

    # Save the graph to an HTML file
    nt.save_graph(f'data_flow_graph.html')

    # Display the graph using the HTML component in Streamlit
    st.header('Dependency between sessions-uprocs-table_deps')
    HtmlFile = open(f'data_flow_graph.html', 'r', encoding='utf-8')

    # Load HTML into HTML component for display on Streamlit
    components.html(HtmlFile.read(), height=800, width=800)

# Appellez la fonction pour visualiser le graphe lorsque l'application Streamlit est exécutée
if __name__ == "__main__":
    st.title("Orange Kenobi")
    plot_network_graph()
