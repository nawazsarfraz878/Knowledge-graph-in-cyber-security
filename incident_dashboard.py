import streamlit as st
from neo4j import GraphDatabase
from pyvis.network import Network
import pandas as pd
import os

# Connect to Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "123456789"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Query Neo4j for incident data
def fetch_incidents():
    query = """
    MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
    RETURN a.name AS Attacker, b.name AS Entity, r.status AS Status
    LIMIT 250
    """
    try:
        with driver.session() as session:
            result = session.run(query)
            return [record.data() for record in result]
    except Exception as e:
        st.error(f"Error fetching incidents: {e}")
        return []

# Generate graph visualization
def generate_graph():
    query = """
    MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
    RETURN a.name AS Source, b.name AS Target, r.status AS Status
    LIMIT 250
    """
    try:
        with driver.session() as session:
            result = session.run(query)
            edges = result.data()

        # Create a PyVis network
        net = Network(height="600px", width="100%", directed=True)
        added_nodes = set()

        for edge in edges:
            source = edge['Source']
            target = edge['Target']
            status = edge['Status']

            if source not in added_nodes:
                net.add_node(source, label=source, color="red")
                added_nodes.add(source)

            if target not in added_nodes:
                net.add_node(target, label=target, color="blue")
                added_nodes.add(target)

            net.add_edge(source, target, label=status)

        # Save the graph as an HTML file
        graph_path = "graph.html"
        net.save_graph(graph_path)
        return graph_path
    except Exception as e:
        st.error(f"Error generating graph: {e}")
        return None

# Streamlit Dashboard
st.title("Incident Response Dashboard")
st.header("Overview of Incidents")

# Fetch data from Neo4j
incidents = fetch_incidents()

if incidents:
    st.write(f"Total Incidents: {len(incidents)}")

    # Display incidents in a table
    df = pd.DataFrame(incidents)
    st.table(df)

    # Filter incidents by status
    status_filter = st.selectbox("Filter by Status", ["All", "In Progress", "Resolved"])
    if status_filter != "All":
        df = df[df['Status'] == status_filter]

    # Display filtered incidents
    st.subheader("Filtered Incidents")
    st.table(df)

    # Add a button to generate a graph visualization
    if st.button("Generate Graph Visualization"):
        graph_path = generate_graph()
        if graph_path and os.path.exists(graph_path):
            st.success("Graph visualization generated below:")
            with open(graph_path, "r", encoding="utf-8") as f:
                graph_html = f.read()
            # Display the graph in the Streamlit app
            st.components.v1.html(graph_html, height=600, scrolling=True)
        else:
            st.error("Failed to generate the graph visualization.")

    # Add report generation and download
    st.subheader("Download Incident Report")
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Report as CSV",
        data=csv,
        file_name="incident_report.csv",
        mime="text/csv"
    )
else:
    st.write("No incidents found.")

# Close the Neo4j driver when the app ends
driver.close()

'''
import streamlit as st
from neo4j import GraphDatabase
from pyvis.network import Network
import pandas as pd
import os

# Connect to Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "123456789"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Query Neo4j for incident data
def fetch_incidents():
    query = """
    MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
    RETURN a.name AS Attacker, b.name AS Entity, r.status AS Status
    LIMIT 250
    """
    try:
        with driver.session() as session:
            result = session.run(query)
            return [record.data() for record in result]
    except Exception as e:
        st.error(f"Error fetching incidents: {e}")
        return []

# Generate graph visualization
def generate_graph():
    query = """
    MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
    RETURN a.name AS Source, b.name AS Target, r.status AS Status
    LIMIT 250
    """
    try:
        with driver.session() as session:
            result = session.run(query)
            edges = result.data()

        # Create a PyVis network
        net = Network(height="600px", width="100%", directed=True)
        added_nodes = set()

        for edge in edges:
            source = edge['Source']
            target = edge['Target']
            status = edge['Status']

            if source not in added_nodes:
                net.add_node(source, label=source, color="red")
                added_nodes.add(source)

            if target not in added_nodes:
                net.add_node(target, label=target, color="blue")
                added_nodes.add(target)

            net.add_edge(source, target, label=status)

        # Save the graph as an HTML file
        graph_path = "graph.html"
        net.save_graph(graph_path)
        return graph_path
    except Exception as e:
        st.error(f"Error generating graph: {e}")
        return None

# Streamlit Dashboard
st.title("Incident Response Dashboard")
st.header("Overview of Incidents")

# Fetch data from Neo4j
incidents = fetch_incidents()

if incidents:
    st.write(f"Total Incidents: {len(incidents)}")

    # Display incidents in a table
    df = pd.DataFrame(incidents)
    st.table(df)

    # Filter incidents by status
    status_filter = st.selectbox("Filter by Status", ["All", "Detected", "Resolved"])
    if status_filter != "All":
        df = df[df['Status'] == status_filter]

    # Display filtered incidents
    st.subheader("Filtered Incidents")
    st.table(df)

    # Add a button to generate a graph visualization
    if st.button("Generate Graph Visualization"):
        graph_path = generate_graph()
        if graph_path and os.path.exists(graph_path):
            st.success("Graph visualization generated below:")
            with open(graph_path, "r", encoding="utf-8") as f:
                graph_html = f.read()
            # Display the graph in the Streamlit app
            st.components.v1.html(graph_html, height=600, scrolling=True)
        else:
            st.error("Failed to generate the graph visualization.")

    # Add report generation and download
    st.subheader("Download Incident Report")
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Report as CSV",
        data=csv,
        file_name="incident_report.csv",
        mime="text/csv"
    )
else:
    st.write("No incidents found.")

# Close the Neo4j driver when the app ends
driver.close()

'''

'''
import streamlit as st
from neo4j import GraphDatabase
from pyvis.network import Network
import pandas as pd

# Connect to Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "123456789"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Query Neo4j for incident data
def fetch_incidents():
    query = """
    MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
    RETURN a.name AS Attacker, b.name AS Entity, r.status AS Status;
    LIMIT 50;
    """
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]

# Generate graph visualization
def generate_graph():
    query = """
    MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
    RETURN a.name AS Source, b.name AS Target, r.status AS Status;
    LIMIT 50;
    """
    with driver.session() as session:
        result = session.run(query)
        edges = result.data()

    # Create a PyVis network
    net = Network(height="600px", width="100%", directed=True)
    added_nodes = set()

    for edge in edges:
        source = edge['Source']
        target = edge['Target']
        status = edge['Status']

        if source not in added_nodes:
            net.add_node(source, label=source, color="red")
            added_nodes.add(source)

        if target not in added_nodes:
            net.add_node(target, label=target, color="blue")
            added_nodes.add(target)

        net.add_edge(source, target, label=status)

    # Save and display the graph
    net.save_graph("graph.html")

# Streamlit Dashboard
st.title("Incident Response Dashboard")
st.header("Overview of Incidents")

# Fetch data from Neo4j
incidents = fetch_incidents()

if incidents:
    st.write(f"Total Incidents: {len(incidents)}")

    # Display incidents in a table
    df = pd.DataFrame(incidents)
    st.table(df)

    # Filter incidents by status
    status_filter = st.selectbox("Filter by Status", ["All", "Identified", "In Progress", "Resolved"])
    if status_filter != "All":
        df = df[df['Status'] == status_filter]

    # Display filtered incidents
    st.subheader("Filtered Incidents")
    st.table(df)

    # Add a button to generate a graph visualization
    if st.button("Generate Graph Visualization"):
        generate_graph()
        st.success("Graph visualization generated! Click below to view.")
        st.markdown("[View Graph Visualization](graph.html)", unsafe_allow_html=True)

    # Add report generation and download
    st.subheader("Download Incident Report")
    if st.button("Generate Report"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Report as CSV",
            data=csv,
            file_name="incident_report.csv",
            mime="text/csv"
        )
else:
    st.write("No incidents found.")
'''
'''
import streamlit as st
from neo4j import GraphDatabase
import pandas as pd
import matplotlib.pyplot as plt

# Connect to Neo4j
uri = "bolt://localhost:7687"  # Update if needed
username = "neo4j"
password = "123456789"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Fetch incidents with caching
@st.cache_data
def fetch_incidents_cached():
    query = """
    MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
    RETURN a.name AS Attacker, b.name AS Entity, r.status AS Status
    LIMIT 50;
    """
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]

# Streamlit Dashboard
st.title("Incident Response Dashboard")
st.header("Overview of Incidents")

# Fetch data from Neo4j
try:
    incidents = fetch_incidents_cached()
    st.write("Fetched Data:", incidents)  # Debugging output

    # Check if any incidents were returned
    if incidents:
        # Create a DataFrame from the fetched data
        if "Status" in incidents[0]:
            df = pd.DataFrame(incidents)
            st.write(f"Total Incidents: {len(df)}")

            # Display incidents in a table
            st.subheader("All Incidents")
            st.table(df)

            # Filter incidents by status
            if "Status" in df.columns:
                status_filter = st.selectbox("Filter by Status", ["All"] + list(df["Status"].unique()))
                if status_filter != "All":
                    df = df[df["Status"] == status_filter]

            # Display filtered incidents
            st.subheader("Filtered Incidents")
            st.table(df)

            # Generate a bar chart for incident counts by status
            st.subheader("Incident Status Distribution")
            if "Status" in df.columns:
                status_counts = df["Status"].value_counts()
                plt.bar(status_counts.index, status_counts.values, color="skyblue")
                plt.xlabel("Status")
                plt.ylabel("Count")
                plt.title("Incident Status Distribution")
                st.pyplot(plt)
            else:
                st.write("No 'Status' field found in the data.")
        else:
            st.write("The fetched data does not include a 'Status' field.")
    else:
        st.write("No incidents found in the database.")

except Exception as e:
    st.error(f"Error fetching or processing data: {e}")
    st.stop()


from pyvis.network import Network

def visualize_graph():
    query = """
    MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
    RETURN a.name AS Source, b.name AS Target, r.status AS Status;
    """
    with driver.session() as session:
        results = session.run(query)
        edges = [{"source": record["Source"], "target": record["Target"], "status": record["Status"]} for record in results]

    # Create a PyVis Network
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")
    for edge in edges:
        net.add_node(edge["source"], label=edge["source"])
        net.add_node(edge["target"], label=edge["target"])
        net.add_edge(edge["source"], edge["target"], title=edge["status"])
    
    # Save and display the graph
    net.save_graph("graph.html")
    st.components.v1.html(open("graph.html", "r").read(), height=700)

# Call the visualization function in Streamlit
st.header("Graph Visualization")
visualize_graph()


import pandas as pd

def generate_report():
    query = """
    MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
    RETURN a.name AS Attacker, b.name AS Entity, r.status AS Status;
    """
    with driver.session() as session:
        results = session.run(query)
        data = [{"Attacker": record["Attacker"], "Entity": record["Entity"], "Status": record["Status"]} for record in results]

    # Convert to DataFrame
    df = pd.DataFrame(data)
    # Save to CSV
    report_path = "incident_report.csv"
    df.to_csv(report_path, index=False)
    st.success(f"Report generated: {report_path}")
    st.download_button(
        label="Download Report",
        data=open(report_path, "rb"),
        file_name="incident_report.csv",
        mime="text/csv",
    )

# Call the report generation function in Streamlit
st.header("Report Generation")
if st.button("Generate Incident Report"):
    generate_report()
'''
'''
import streamlit as st
from neo4j import GraphDatabase
import pandas as pd
import matplotlib.pyplot as plt
from pyvis.network import Network
import os

# Connect to Neo4j
uri = "bolt://localhost:7687"  # Update if needed
username = "neo4j"
password = "123456789"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Fetch incidents with caching
@st.cache_data
def fetch_incidents_cached():
    query = """
    MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
    RETURN a.name AS Attacker, b.name AS Entity, r.status AS Status
    LIMIT 50;
    """
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]

# Streamlit Dashboard
st.title("Incident Response Dashboard")
st.header("Overview of Incidents")

# Fetch data from Neo4j
try:
    incidents = fetch_incidents_cached()
    st.write("Fetched Data:", incidents)  # Debugging output

    # Check if any incidents were returned
    if incidents:
        # Create a DataFrame from the fetched data
        if "Status" in incidents[0]:
            df = pd.DataFrame(incidents)
            st.write(f"Total Incidents: {len(df)}")

            # Display incidents in a table
            st.subheader("All Incidents")
            st.table(df)

            # Filter incidents by status
            if "Status" in df.columns:
                status_filter = st.selectbox("Filter by Status", ["All"] + list(df["Status"].unique()))
                if status_filter != "All":
                    df = df[df["Status"] == status_filter]

            # Display filtered incidents
            st.subheader("Filtered Incidents")
            st.table(df)

            # Generate a bar chart for incident counts by status
            st.subheader("Incident Status Distribution")
            if "Status" in df.columns:
                status_counts = df["Status"].value_counts()
                plt.bar(status_counts.index, status_counts.values, color="skyblue")
                plt.xlabel("Status")
                plt.ylabel("Count")
                plt.title("Incident Status Distribution")
                st.pyplot(plt)
            else:
                st.write("No 'Status' field found in the data.")
        else:
            st.write("The fetched data does not include a 'Status' field.")
    else:
        st.write("No incidents found in the database.")

except Exception as e:
    st.error(f"Error fetching or processing data: {e}")
    st.stop()

# Graph Visualization Function
def visualize_graph():
    query = """
    MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
    RETURN a.name AS Source, b.name AS Target, r.status AS Status;
    """
    with driver.session() as session:
        results = session.run(query)
        edges = [{"source": record["Source"], "target": record["Target"], "status": record["Status"]} for record in results]

    # Create a PyVis Network
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")
    for edge in edges:
        net.add_node(edge["source"], label=edge["source"])
        net.add_node(edge["target"], label=edge["target"])
        net.add_edge(edge["source"], edge["target"], title=edge["status"])
    
    # Save and display the graph
    output_path = os.path.join(os.getcwd(), "graph.html")
    try:
        # Ensure the output path is valid and forward-compatible
        output_path = output_path.replace("\\", "/")
        net.save_graph(output_path)
        with open(output_path, "r", encoding="utf-8") as f:
            graph_html = f.read()
        st.components.v1.html(graph_html, height=700)
    except Exception as e:
        st.error(f"Error creating or displaying graph: {e}")


# Report Generation Function
def generate_report():
    query = """
    MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
    RETURN a.name AS Attacker, b.name AS Entity, r.status AS Status;
    """
    with driver.session() as session:
        results = session.run(query)
        data = [{"Attacker": record["Attacker"], "Entity": record["Entity"], "Status": record["Status"]} for record in results]

    # Convert to DataFrame
    df = pd.DataFrame(data)
    # Save to CSV
    report_path = os.path.join(os.getcwd(), "incident_report.csv")
    try:
        df.to_csv(report_path, index=False)
        st.success(f"Report generated: {report_path}")
        with open(report_path, "rb") as f:
            st.download_button(
                label="Download Report",
                data=f,
                file_name="incident_report.csv",
                mime="text/csv",
            )
    except Exception as e:
        st.error(f"Error generating report: {e}")

# Call the report generation function in Streamlit
st.header("Report Generation")
if st.button("Generate Incident Report"):
    generate_report()
'''
'''
import streamlit as st
from neo4j import GraphDatabase
import pandas as pd
import matplotlib.pyplot as plt
import os
from pyvis.network import Network

# Connect to Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "123456789"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Fetch incidents with caching
@st.cache_data
def fetch_incidents_cached():
    query = """
    MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
    RETURN a.name AS Attacker, b.name AS Entity, r.status AS Status
    LIMIT 500;
    """
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]

# Streamlit Dashboard
st.title("Incident Response Dashboard")
st.header("Overview of Incidents")

# Fetch data from Neo4j
try:
    incidents = fetch_incidents_cached()

    # Check if any incidents were returned
    if incidents:
        df = pd.DataFrame(incidents)
        st.write(f"Total Incidents: {len(df)}")

        # Display incidents in a table
        st.subheader("All Incidents")
        st.table(df)

        # Filter incidents by status
        status_filter = st.selectbox("Filter by Status", ["All"] + list(df["Status"].unique()))
        if status_filter != "All":
            df = df[df["Status"] == status_filter]

        # Display filtered incidents
        st.subheader("Filtered Incidents")
        st.table(df)

        # Generate a bar chart for incident counts by status
        st.subheader("Incident Status Distribution")
        if "Status" in df.columns:
            status_counts = df["Status"].value_counts()
            plt.bar(status_counts.index, status_counts.values, color="skyblue")
            plt.xlabel("Status")
            plt.ylabel("Count")
            plt.title("Incident Status Distribution")
            st.pyplot(plt)
    else:
        st.write("No incidents found in the database.")

except Exception as e:
    st.error(f"Error fetching or processing data: {e}")
    st.stop()
''''''
# Graph Visualization
st.header("Graph Visualization")

import os
import tempfile
from pyvis.network import Network

import os
import tempfile
from pyvis.network import Network

import os
import tempfile
from pyvis.network import Network

def visualize_graph():
    query = """
    MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
    RETURN a.name AS Source, b.name AS Target, r.status AS Status;
    """
    with driver.session() as session:
        results = session.run(query)
        edges = [{"source": record["Source"], "target": record["Target"], "status": record["Status"]} for record in results]

    # Check if we have any data
    if not edges:
        st.error("No data returned for the graph visualization.")
        return

    # Debug: Print edges to make sure they are being added correctly
    st.write("Edges:", edges)

    # Create a PyVis Network
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")

    # Add nodes and edges to the network
    for edge in edges:
        st.write(f"Adding edge: {edge['source']} -> {edge['target']}, Status: {edge['status']}")
        net.add_node(edge["source"], label=edge["source"], color="lightblue")
        net.add_node(edge["target"], label=edge["target"], color="orange")
        net.add_edge(edge["source"], edge["target"], title=edge["status"])

    # Save the graph to a temporary directory
    try:
        # Use tempfile to create a temporary path
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, "temp_graph.html")

        # Save the graph in HTML format
        net.save_graph(temp_path)

        # Debug: Check the saved file path
        st.write(f"Graph saved to: {temp_path}")

        # Display the graph in an iframe
        st.components.v1.html(f'<iframe src="file:///{temp_path}" width="100%" height="700px"></iframe>', height=700)

    except Exception as e:
        st.error(f"Error creating or displaying graph: {e}")





# Call the visualization function
visualize_graph()
''''''
# Report Generation
st.header("Report Generation")

def generate_report():
    query = """
    MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
    RETURN a.name AS Attacker, b.name AS Entity, r.status AS Status;
    """
    with driver.session() as session:
        results = session.run(query)
        data = [{"Attacker": record["Attacker"], "Entity": record["Entity"], "Status": record["Status"]} for record in results]

    # Convert to DataFrame
    df = pd.DataFrame(data)
    # Save to CSV
    report_path = "incident_report.csv"
    df.to_csv(report_path, index=False)
    st.success(f"Report generated: {report_path}")
    st.download_button(
        label="Download Report",
        data=open(report_path, "rb"),
        file_name="incident_report.csv",
        mime="text/csv",
    )

if st.button("Generate Incident Report"):
    generate_report()'''