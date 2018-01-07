import sys
import time
import os
import contextlib

import db
from web_connection import the_https_request
from fs_connection import the_resource_path

def fetchServices(node_id=None):
	"""
    Fetches all active services.

    Parameters: 
        none
    Returns:
        Returns a list of active service location dictionaries.
	"""
	resList = []
	sql = '''SELECT id, fqdn FROM node WHERE active=:act;'''
	args = {"act": 1}
	nodes = db.query(sql, args)

	for node in nodes:
		sql = '''SELECT id, uri, proto FROM service WHERE active=:act and node_id=:node_id;'''
		args = {"act": 1, "node_id": node[0]}
		resources = db.query(sql, args)

	 	for resource in resources:
			resList.append({'fqdn': node[1], 'uri': resource[1], 'proto': resource[2], 'node_id': node[0], 
							'service_id': resource[0]})
	return resList


def fetchResource(**resDict):
	"""
    Fetches a resource according to the dictionary provided.

    Parameters: 
        resourceDict: {'fqdn': string, 'uri': string, 'proto': string}
    Returns:
        Returns binary resource.
    """
	with contextlib.closing(the_https_request) as req:
		res = req.open(resDict['proto'] + "://" + resDict['fqdn'] + "/" + resDict['uri']).read()
		#print resDict['proto'] + "://" + resDict['fqdn'] + "/" + resDict['uri']
		return res


def storeFile(resDict):
	"""
    Stores a resource on the filesystem according to the dictionary provided.

    Parameters: 
        resourceDict: {'node_id': int, 'service_id': int, 'res_bin' string, 'res_time': string}
    Returns:
        Returns fully qualified filename, false on error.
    """
	path = the_resource_path + str(resDict['node_id']) + "/" + str(resDict['service_id'])
	if not os.path.exists(path):
		try:
			os.makedirs(path, 0755)
			print path
		except Exception as error:
			print('caught this error: ' + repr(error))
			return False

	if os.path.exists(path):
		try:
			file = path + "/" + str(resDict['res_time']) + ".jpg"
			output = open(file, "wb")
			output.write(resDict['res_bin'])
			output.close()
			return file
		except Exception as error:
			print('caught this error: ' + repr(error))
			return False			


def storeDB(resDict):
	"""
    Stores resource metadata in the database according to the dictionary provided.

    Parameters: 
        resourceDict: {'res_time': string, 'res_file': string, 'service_id' int}
    Returns:
        Returns true if successful, false on error.
    """
	sql = '''INSERT INTO resource(date,path,service_id) VALUES(?,?,?);'''
	args = (resDict['res_time'], resDict['res_file'], resDict['service_id'])
	print db.query(sql, args)
	# TODO: error handling on exit--check number of lines inserted via query function?


myServices = fetchServices()

# Testpad
for service in myServices:
	print sys.getsizeof(service)

	service.update({'res_bin': fetchResource(**service), 'res_time': int(time.time())})

	print sys.getsizeof(service['res_bin'])
	print service['res_time']

	service.update({'res_file': storeFile(service)})
	storeDB(service)
	print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(service['res_time']))

# resDict: {'fqdn': string, 'uri': string, 'proto': string, 'node_id': int, 
#				 'service_id': int, 'res_bin': string, 'res_time': string }
