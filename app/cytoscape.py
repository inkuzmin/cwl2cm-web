import uuid
import json


class Elements:
    def __init__(self, nodes=[], edges=[]):
        self.nodes = nodes
        self.edges = edges

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def toJSON(self, outfile=None):
        export = {
            'nodes': [node.export() for node in self.nodes],
            'edges': [edge.export() for edge in self.edges]
        }
        if outfile:
            with open(outfile, 'w') as o:
                json.dump(export, o)

        return json.dumps(export)


class Node:
    count = 0

    def __init__(self, uid=None, nodeType="", position={}):
        Node.count += 1

        if uid:
            self.id = uid
        else:
            self.id = "node-{}".format(Node.count)

        self.type = nodeType
        self.position = position
        self.name = None

        self.edam = None

    def export(self):
        export = {
            'data': {
                'id': self.id,
                'type': self.type,
                'color': 'grey',
                'name': self.name,  # or self.id,
                'requiredText': '',
                'description': self.name or "",
            },
            'position': self.position,

            "group": "nodes",
            "removed": False,
            "selected": False,
            "selectable": True,
            "locked": False,
            "grabbable": True,
            "classes": self.type
        }

        if self.edam:
            if self.type == 'operation':
                export['data'][self.type] = self.edam
            elif self.type == 'data':
                export['data']['formats'] = [self.edam]

        return export


class Edge:
    def __init__(self, source, target):
        self.id = str(uuid.uuid1())
        self.source = source
        self.target = target

    def export(self):
        export = {
            'data': {
                'source': self.source,
                'target': self.target,
                'id': self.id
            },
            "position": {},
            "group": "edges",
            "removed": False,
            "selected": False,
            "selectable": True,
            "locked": False,
            "grabbable": True,
            "classes": "required"
        }
        return export
