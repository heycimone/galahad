#!/usr/bin/python
import rethinkdb as r
r.connect("172.30.93.138",28015).repl()

r.db('routing').table('galahad').insert([{
	'function':'virtue',
	'host':'test1',
	'address':'172.30.87.99',
	'guestnet':'10.91.0.11'}]).run()
