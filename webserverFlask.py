import uuid 
from flask import Flask, request, jsonify, abort

# initialize Flask server
app = Flask(__name__)

# create unique ID for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = str(uuid.uuid4())
todo_2_id = str(uuid.uuid4())
todo_3_id = str(uuid.uuid4())
todo_4_id = str(uuid.uuid4())

# define internal data structures with example data
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
    {'id': todo_4_id, 'name': 'Auto reinigen', 'description': '', 'list': todo_list_1_id},
]

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PATCH'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


# define endpoint for adding a new list
@app.route('/list', methods=['POST'])
def add_new_list():
    # make JSON from POST data (even if content type is not set correctly)
    new_list = request.get_json(force=True)
    print('Got new list to be added: {}'.format(new_list))
    # create ID for new list, save it and return the list with ID
    new_list['id'] = uuid.uuid4()
    todo_lists.append(new_list)
    return jsonify(new_list), 200


# define endpoint for getting all lists
@app.route('/lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists)


# define endpoint for getting and deleting existing todo lists
@app.route('/list/<list_id>', methods=['GET', 'DELETE', 'PATCH'])
def handle_list(list_id):
    # find todo list depending on given list ID
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list ID is invalid, return status code 404
    if not list_item:
        abort(404)
    if request.method == 'GET':
        # find all todo entries for the todo list with the given ID
        print('Returning todo list...')
        return jsonify([i for i in todos if i['list'] == list_id])
    elif request.method == 'DELETE':
        # delete the list with given ID
        print('Deleting todo list...')
        todo_lists.remove(list_item)
        return 'list deleted', 200


# define endpoint for bind item to list
@app.route('/list/<list_id>/item', methods=['POST'])
def item_add(list_id):
    print(list_id)
    if request.method == 'POST':
        dict = {
            'id': str(uuid.uuid4()),
            'name': request.form.get('name'),
            'list': list_id
        }
        for i in todo_lists:
            if list_id == i['id']:
               
               try:
                    todo_lists.insert(len(todo_lists)+1, dict)
                    return jsonify({'message': 'Eintrag '+dict.get('id')+' erfolgreich angelegt.'}), 200
               except Exception as e:
                   return jsonify({'message': 'Fehler beim Erstellen des Eintrags', 'error': str(e)}), 500
    else:
        abort(402)


# define endpoint for creating new item in specific list
@app.route('/list/<list_id>/item/<item_id>', methods=['DELETE', 'PATCH'])
def handle_item(list_id, item_id):
    if request.method == "DELETE" :
        for i in todos:
            if i['id'] == item_id:
                if i['list'] == list_id :
                    print('Deleting todo item...')
                    todos.remove(item_id)
                    return '', 200
    elif request.method == 'PATCH' :
        if list_id in todo_lists and item_id in todos[list_id]:
            try:
                request_data = request.get_json()
                todo_lists[list_id][item_id]['name'] = request_data.get('name', todo_lists[list_id][item_id]['name'])
                todo_lists[list_id][item_id]['beschreibung'] = request_data.get('beschreibung', todo_lists[list_id][item_id]['description'])
                return jsonify(todo_lists[list_id][item_id]), 200
            except Exception as e:
                return jsonify({'message': 'Fehler beim Aktualisieren des Eintrags', 'error': str(e)}), 500
        else:
            return jsonify({'message': 'Eine der IDs existiert nicht'}), 404
    else:
        abort(404)

if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
