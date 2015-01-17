#!/usr/bin/env python

import binascii, os

import bottle
from bottle import response, request

@bottle.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@bottle.get('/')
def health():
    response.content_type = 'text/plain'
    if os.path.isdir("./tasks"):
        return 'ok'
    else:
        return 'tasks directory does not exist'

@bottle.post('/task')
def create_task():
    response.content_type = 'text/plain'

    task_id = binascii.hexlify(os.urandom(8))
    with open('./tasks/' + task_id + '.status', 'a') as f:
        f.write('queued')

    return task_id

@bottle.get('/tasks')
def list_tokens():
    return ' '.join(os.listdir('./tasks'))

@bottle.get('/task/<name>')
def get_task(name):
    with open ('./tasks/' + name + '.status', 'r') as f:
        return '\n'.join(f.readlines())

bottle.run(host='localhost', port=8080, debug=True)