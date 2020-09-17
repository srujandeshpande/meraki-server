import pymongo
from bson.json_util import dumps
import json
from flask import Flask, request, render_template, session, redirect, url_for, flash, Response, abort, render_template_string, send_from_directory
from flask_cors import CORS
import requests


app = Flask(__name__)
application = app
CORS(app)


client = pymongo.MongoClient(
    "mongodb+srv://dbAdmin:dbPassword@cluster0.rxwsz.azure.mongodb.net/merakidb?retryWrites=true&w=majority")
db = pymongo.database.Database(client, 'merakidb')


@app.route('/api')
def hello_world():
    return 'Hello, World!'


@app.route('/api/story', methods=['GET'])
def get_stories():
    Story = pymongo.collection.Collection(db, 'Story')
    data = json.loads(dumps(Story.find()))
    rdata = dict()
    rdata['count'] = len(data)
    rdata['data'] = data
    return rdata


@app.route('/api/story', methods=['POST'])
def create_story():
    inputData = request.json
    Story = pymongo.collection.Collection(db, 'Story')
    Story.insert_one(inputData)
    return "Story Created"


@app.route('/api/story', methods=['PUT'])
def update_story():
    inputData = request.json
    Story = pymongo.collection.Collection(db, 'Story')
    uid = inputData['uid']
    # Story.remove({uid:uid})
    Story.update_one({"uid": uid}, {"$set": inputData})
    return "Story Updated"


@app.route('/api/story', methods=['DELETE'])
def delete_story():
    inputData = request.json
    Story = pymongo.collection.Collection(db, 'Story')
    Story.delete_one({"uid": inputData['uid']})
    return "Story Deleted"
