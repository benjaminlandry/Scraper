from treelib import Node, Tree
from anytree import Node, RenderTree, AnyNode
from anytree.exporter import JsonExporter, DictExporter
from anytree.importer import JsonImporter
import pymongo
from pymongo import MongoClient

importer = JsonImporter()
with open('testsuites.json') as f1:
    data = f1.read()
    root = importer.import_(data)
    # print(RenderTree(root))

def get_leaf_nodes():
    leafs = []
    def _get_leaf_nodes(node):
        if node is not None:
            if len(node.children) == 0:
                leafs.append(node)
            for n in node.children:
                _get_leaf_nodes(n)
    _get_leaf_nodes(root)
    return leafs

list_leafs = get_leaf_nodes() 
exporter = DictExporter()  
exported_result = exporter.export(root)
print(type(exported_result))

## Post the Dictionary Results to Mongodb
def postToMongo(self, mongoIP, database, collection, log):
    client = MongoClient(mongoIP, 27017) # connects client with the mongoserver
    db = client[database] # create/connect to a database
    col = db[collection]  # create/connect to a collection

    col.insert_one(log)  # insert log document in a collection

postToMongo('http://142.133.174.148:8888/', 'localhost', 'RBT', 'filter_tests', exported_result)


