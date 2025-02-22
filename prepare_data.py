import json
import csv

# Open and load the JSON file
with open('entity&relationship.json', 'r', encoding='utf-8') as file:
    # Load the entire JSON content as a list of dictionaries
    data = json.load(file)

# Create lists to store entities and relationships
entities = []
relationships = []

# Extract entities and relationships from each object
for item in data:
    output = item.get('output', '')
    if output:
        # Extract Named Entities
        if "Named Entities:" in output:
            entities_part = output.split("Named Entities:")[1].split("\n")[0].strip()
            for entity in entities_part.split("), "):
                entity = entity.strip("()")
                if "," in entity:
                    entity_parts = entity.split(", ")
                    if len(entity_parts) == 2:
                        entities.append({
                            "name": entity_parts[0].strip(),
                            "type": entity_parts[1].strip()
                        })

        # Extract Relationships
        if "Relationships:" in output:
            relationships_part = output.split("Relationships:")[1].strip()
            for relationship in relationships_part.split("), "):
                relationship = relationship.strip("()")
                if "," in relationship:
                    relationship_parts = relationship.split(", ")
                    if len(relationship_parts) == 3:
                        relationships.append({
                            "source": relationship_parts[0].strip(),
                            "relationship": relationship_parts[1].strip(),
                            "target": relationship_parts[2].strip()
                        })

# Write entities to a CSV file
with open('nodes.csv', 'w', newline='', encoding='utf-8') as node_file:
    writer = csv.writer(node_file)
    writer.writerow(['name', 'type'])
    for entity in entities:
        writer.writerow([entity['name'], entity['type']])

# Write relationships to a CSV file
with open('relationships.csv', 'w', newline='', encoding='utf-8') as rel_file:
    writer = csv.writer(rel_file)
    writer.writerow(['source', 'relationship', 'target'])
    for relationship in relationships:
        writer.writerow([relationship['source'], relationship['relationship'], relationship['target']])

print("CSV files created successfully!")
