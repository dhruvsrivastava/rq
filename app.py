import os
import redis
import requests
import time

from perform_task import perform_task
from rq import Queue
from flask import Flask
from flask import Response , json

app = Flask(__name__)
app.redis = redis.StrictRedis(host = 'localhost' , port = 6379 , db = 0)

q = Queue(connection = redis.StrictRedis())

@app.route('/api/names')
def check():
	data = app.redis.lrange("names" , 0 , -1)
	resp = Response(json.dumps(data) , status = 200 , mimetype = 'application/json')
	print json.dumps(data)
	return resp


@app.route('/api/insert')
def insert_names():
	app.redis.rpush("names" , "A")
	app.redis.rpush("names" , "B")
	app.redis.rpush("names" , "C")
	return '<h1> Insert finished </h1>'

@app.route('/api/enqueue')
def enqueue():
	job = q.enqueue(perform_task , args = (100 , 200))
	if job.result is None:
		return '<h1> Enqueue </h1>'
	resp = Response(json.dumps(job.result) , status = 200 , mimetype = 'application/json)')
	return resp
	
@app.route('/api/active')
def active():
	jobs = q.jobs
	print "number of jobs %d" %(len(q.jobs))
	for job in jobs:
		print job.status
	return '<h1> Active </h1>'	

if __name__ == '__main__':
	app.run(debug = True)
	app.redis.flushdb()