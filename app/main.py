from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


from ruamel.yaml import YAML
import json
import uuid

import cytoscape as cy
import gxformat2

yaml = YAML()
scaleX = 2
scaleY = 0.5
with open('edam.2.json') as edamDataFile:
    edamData = json.load(edamDataFile)


def relByTermId(termId):
    [_, type_uid] = termId.split(':')
    [edamType, uid] = type_uid.split('_')

    relIds = [x[0] for x in edamData['data'][edamType] if x[1] == uid]
    if len(relIds) > 0:
        return relIds[0]
    else:
        return '-1'


def transform(a):
    b = []
    if isinstance(a, dict):
        for key, value in a.items():
            if isinstance(value, dict):
                item = {
                    'id': str(key),
                    **value
                }
                if 'source' not in value:
                    item['source'] = str(key)
                if 'type' not in item:
                    item['type'] = ''
            elif isinstance(value, type("string")):
                item = {
                    'id': str(key),
                    'type': '',
                    'source': str(value)
                }
            b.append(item)
    elif isinstance(a, list):
        for item in a:
            if isinstance(item, dict):
                if 'source' not in item:
                    if 'id' in item:
                        item['source'] = item['id']
                    elif 'name' in item:
                        item['source'] = item['name']
                        item['id'] = item['name']
                    elif 'tool_id' in item:
                        item['id'] = item['tool_id']
                    else:
                        raise Error()
                        item['id'] = str(uuid.uuid1())
                    if 'type' not in item:
                        item['type'] = ''
                b.append(item)
            elif isinstance(item, type("string")):
                item = {
                    'id': str(item),
                    'type': '',
                    'source': str(item),
                }
                b.append(item)
    return b


def convert_(format, input):
    """Script that converts CWL and Galaxy to ConceptMaps"""
    if format == 'galaxy':
        galaxyWorkflow = json.loads(input)
        format2fromGalaxy = gxformat2.from_galaxy_native(galaxyWorkflow, json_wrapper=True)
        cwl = yaml.load(format2fromGalaxy['yaml_content'])
    elif format == 'cwl':
        cwl = yaml.load(input)

    elements = cy.Elements([], [])

    inputs = transform(cwl['inputs'])
    outputs = transform(cwl['outputs'])
    steps = transform(cwl['steps'])

    all_data = {}

    for inp in inputs:
        if inp['type'].startswith('File') or inp['type'].startswith('Dir'):
            if inp['id'] not in all_data:  # also ids could be keys in dict
                if 'sbg:x' in inp and 'sbg:y' in inp:
                    position = {
                        'x': inp['sbg:y'] * scaleX,
                        'y': inp['sbg:x'] * scaleY
                    }
                else:
                    position = {}
                node = cy.Node(uid=inp['id'], nodeType='data', position=position)
                all_data[inp['id']] = node

                if 'format' in inp:
                    node.edam = relByTermId(inp['format'])

    for out in outputs:
        if out['type'].startswith('File') or out['type'].startswith('Dir'):
            if out['id'] not in all_data:
                if 'sbg:x' in out and 'sbg:y' in out:
                    position = {
                        'x': out['sbg:y'] * scaleX,
                        'y': out['sbg:x'] * scaleY
                    }
                else:
                    position = {}
                node = cy.Node(uid=out['id'], nodeType='data', position=position)
                all_data[out['id']] = node

                if 'format' in out:
                    node.edam = relByTermId(out['format'])

    for step in steps:
        k = False
        if 'outputs' in step:
            k = 'outputs'
        elif 'out' in step:
            k = 'out'

        if k:
            outs = transform(step[k])
            for out in outs:
                if out['id'] not in all_data:
                    node = cy.Node(uid=out['id'], nodeType='data')
                    all_data[out['id']] = node

                    if 'format' in out:
                        node.edam = relByTermId(out['format'])

    #
    for key, node in all_data.items():
        elements.addNode(node)
    #

    for step in steps:
        if 'sbg:x' in step and 'sbg:y' in step:
            position = {
                'x': step['sbg:y'] * scaleX,
                'y': step['sbg:x'] * scaleY
            }
        else:
            position = {}

        operationNode = cy.Node(nodeType='operation', position=position)
        operationNode.name = step['id']
        elements.addNode(operationNode)

        if 'format' in step:
            operationNode.edam = relByTermId(step['format'])

        ins = transform(step['in'])

        k = False
        if 'outputs' in step:
            k = 'outputs'
        elif 'out' in step:
            k = 'out'

        if k:
            outs = transform(step[k])

            for inp in ins:
                # if inp['id'] in all_data:
                #     dataNode = all_data[inp['id']]
                #     edge = cy.Edge(dataNode.id, operationNode.id)
                #     elements.addEdge(edge)

                if len(inp['source'].split('/')) > 0 and inp['source'].split('/')[-1] in all_data:
                    dataNode = all_data[inp['source'].split('/')[-1]]
                    dataNode.name = inp['id']
                    edge = cy.Edge(dataNode.id, operationNode.id)
                    elements.addEdge(edge)

            for out in outs:
                if out['id'] in all_data:
                    dataNode = all_data[out['id']]
                    edge = cy.Edge(operationNode.id, dataNode.id)
                    elements.addEdge(edge)

    return elements.toJSON()


@app.route("/")
def hello():
    return app.send_static_file('index.html')


@app.route("/convert", methods=['GET', 'POST'])
def convert():
    data = request.form['data']
    format = request.form['format']
    result = convert_(format, data)
    print(result)
    return result

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
