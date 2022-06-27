from neo4j import GraphDatabase

driver = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "connect"))
session = driver.session()

query = "MATCH (n) RETURN n.name"
result = session.run(query)

print(result)

for i in result:
    print("La valeur de i : ",i)