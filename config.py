from neo4j import GraphDatabase


driver = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "connect"))
session_db = driver.session()