my_list = [
    {
        'id': '111',
        'pid': '0',
        'name': 'A1'
    },
    {
        'id': '222',
        'pid': '111',
        'name': 'A-B1'
    },
    {
        'id': '223',
        'pid': '111',
        'name': 'A-B2'
    },
    {
        'id': '224',
        'pid': '111',
        'name': 'A-B3'
    },
    {
        'id': '333',
        'pid': '223',
        'name': 'A-B2-C1'
    },
    {
        'id': '444',
        'pid': '333',
        'name': 'A-B2-C1-D1'
    }
]
node = my_list[0]


def printList(id, my_list, node):
    for x in my_list:
        if x['pid'] == id:
            new_node = printList(x['id'], my_list, x)
            if 'child' in node:
                node['child'].append(new_node)
            else:
                node['child'] = [new_node]
    return node


printList('111', my_list, node)
print(node)
