from neo4j import GraphDatabase

# Connect to the Neo4j database
uri = "neo4j+s://fdf8e32f.databases.neo4j.io"
driver = GraphDatabase.driver(uri, auth=("neo4j", "0K9KDPJ-dY3E3QAZ1HhGNX0rSIH1VPxPPxXIEl2Sj7o"))

# Run a query
with driver.session() as session:
    result = session.run("MATCH (n) RETURN count(n) AS nodeCount")
    records = list(result)  # Fetch all results into a list

# Process the results
for record in records:
    print(record)

# Close the driver
driver.close()
