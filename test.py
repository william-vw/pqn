import rdflib

g = rdflib.Graph()
g.parse("log-bnodes.rdf", format="n3")

# with open("test-bnodes.sparql", 'r') as qfile:
#     query = qfile.read()
#     print(query)
query = """
PREFIX tr: <http://example.org/trace#>
PREFIX : <http://example.org#>
SELECT ?t
WHERE { 
    # why doesn't this work? 
    [ tr:from :a1 ; tr:to :a2 ] tr:in ?t .
    # ?x tr:from :a1 ; tr:to :a2 ; tr:in ?t .
}"""
qres = g.query(query)
for row in qres:
    print(row)