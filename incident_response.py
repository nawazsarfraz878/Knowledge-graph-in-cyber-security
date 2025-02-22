from neo4j import GraphDatabase

# Connect to Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "123456789"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Function to run a Cypher query
def run_query(query):
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]
    
def update_status(attacker, entity_name, status):
    query = f"""
    MATCH (a:Entity {{name: '{attacker}'}})-[r:RELATES_TO]->(b:Entity {{name: '{entity_name}'}})
    SET r.status = '{status}'
    RETURN r.status AS Status;
    """
    with driver.session() as session:
        result = session.run(query)
        for record in result:
            print(f"Updated status to '{status}' for {attacker} -> {entity_name}")


# Define response actions based on entity type
def get_response(entity_type, entity_name):
    responses = {
        'malware': f"Quarantine the system and block the malware '{entity_name}' using antivirus tools.",
        'technique': f"Implement mitigations for the technique '{entity_name}' and monitor logs for suspicious activity.",
        'vulnerability': f"Patch the vulnerability '{entity_name}' and monitor for exploitation attempts."
    }
    return responses.get(entity_type, f"No specific response defined for {entity_type} '{entity_name}'.")

# Query to extract incidents from Neo4j
query = """
MATCH (a:Entity)-[:RELATES_TO]->(b:Entity)
WHERE a.type = 'attacker' AND b.type IN ['malware', 'technique', 'vulnerability']
RETURN a.name AS Attacker, b.type AS RelatedEntity, b.name AS RelatedName;
"""

# Run the query
incidents = run_query(query)

# Process and respond to incidents
for incident in incidents:
    attacker = incident['Attacker']
    entity_type = incident['RelatedEntity']
    entity_name = incident['RelatedName']

    # Get the response for the related entity
    response = get_response(entity_type, entity_name)

    print(f"Incident detected: Attacker '{attacker}' is related to {entity_type} '{entity_name}'.")
    print(f"Suggested Response: {response}")

    # Update the relationship status to "In Progress"
    update_status(attacker, entity_name, "In Progress")

    # Simulate completing the response (for demonstration purposes)
    print(f"Executing response action for '{entity_name}'...")
    update_status(attacker, entity_name, "Resolved")
    print("-" * 50)
