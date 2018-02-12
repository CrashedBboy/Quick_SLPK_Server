#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
QUICK SLPK SERVER
======================

Minimalist web server engine to publish OGC SceneLayerPackage (.slpk) to Indexed 3d Scene Layer (I3S) web service.

How to use:
- Place .SLPK into a folder (default: "./slpk")
- Configure this script:
	- webserver host
	- webserver port
	- slpk folder
- Launch this script 
- Open browser to "host:port"
- Index page let you access your SLPK as I3S services
-  Also provide an intern viewer for test

How to:
- Configure Index page: modify->  views/services_list.tpl
- Configure Viewer page: modify->  views/carte.tpl


Sources:
- python 2.x
- I3S Specifications: https://github.com/Esri/i3s-spec
- BottlePy 0.13+
- Arcgis Javascript API >=4.6


Autor: RIVIERE Romain
Date: 12/02/2018
Licence: GNU GPLv3 

"""

# Import python modules
from bottlepy.bottle import route, run, template, abort, response
from io import BytesIO
import os, sys, json, gzip, zipfile

#User parameter
host='localhost'
port=8080
home=os.path.join(os.path.dirname(os.path.realpath(__file__)),"slpk") #SLPK Folder


#******#
#Script#
#******#

#List available SLPK
slpks=[f for f in os.listdir(home) if os.path.splitext(f)[1].lower()==u".slpk"]

def read(f,slpk):
	"""read gz compressed file from slpk (=zip archive) and output result"""
	if f.startswith("\\"): #remove first \
		f=f[1:]
	with open(os.path.join(home,slpk), 'rb') as file:
		with zipfile.ZipFile(file) as zip:
			if os.path.splitext(f)[1] == ".gz": #unzip GZ
				gz= BytesIO(zip.read(f.replace("\\","/"))) #GZ file  -> convert path sep to zip path sep
				with gzip.GzipFile(fileobj=gz) as gzfile:
					return gzfile.read()
			else:
				return zip.read(f.replace("\\","/")) #Direct read

@route('/')
def list_services():
	""" List all available SLPK, with LINK to I3S service and Viewer page"""
	return template('services_list', slpks=slpks)
	
@route('/<slpk>/SceneServer')
@route('/<slpk>/SceneServer/')
def service_info(slpk):
	""" Service information JSON """
	if slpk not in slpks: #Get 404 if slpk doesn't exists
		abort(404, "Can't found SLPK: %s"%slpk)
	SceneServiceInfo=dict()
	SceneServiceInfo["serviceName"]=slpk
	SceneServiceInfo["name"]=slpk
	SceneServiceInfo["currentVersion"]=10.6
	SceneServiceInfo["serviceVersion"]="1.6"
	SceneServiceInfo["supportedBindings"]=["REST"]
	SceneServiceInfo["layers"] = [json.loads(read("3dSceneLayer.json.gz",slpk))]
	response.content_type = 'application/json'
	return json.dumps(SceneServiceInfo)
	
@route('/<slpk>/SceneServer/layers/0')
@route('/<slpk>/SceneServer/layers/0/')
def layer_info(slpk):
	""" Layer information JSON """
	if slpk not in slpks: #Get 404 if slpk doesn't exists
		abort(404, "Can't found SLPK: %s"%slpk)
	SceneLayerInfo=json.loads(read("3dSceneLayer.json.gz",slpk))
	response.content_type = 'application/json'
	return json.dumps(SceneLayerInfo)

@route('/<slpk>/SceneServer/layers/<layer>/nodes/<node>')
@route('/<slpk>/SceneServer/layers/<layer>/nodes/<node>/')
def node_info(slpk,layer,node):
	""" Node information JSON """
	if slpk not in slpks: #Get 404 if slpk doesn't exists
		abort(404, "Can't found SLPK: %s"%slpk)
	NodeIndexDocument=json.loads(read("nodes/%s/3dNodeIndexDocument.json.gz"%node,slpk))
	response.content_type = 'application/json'
	return json.dumps(NodeIndexDocument)

@route('/<slpk>/SceneServer/layers/<layer>/nodes/<node>/geometries/0')
@route('/<slpk>/SceneServer/layers/<layer>/nodes/<node>/geometries/0/')
def geometry_info(slpk,layer,node):
	""" Geometry information bin """
	if slpk not in slpks: #Get 404 if slpk doesn't exists
		abort(404, "Can't found SLPK: %s"%slpk)
	return read("nodes/%s/geometries/0.bin.gz"%node,slpk)

@route('/<slpk>/SceneServer/layers/<layer>/nodes/<node>/textures/0_0')
@route('/<slpk>/SceneServer/layers/<layer>/nodes/<node>/textures/0_0/')
def textures_info(slpk,layer,node):
	""" Texture information JPG """
	if slpk not in slpks: #Get 404 if slpk doesn't exists
		abort(404, "Can't found SLPK: %s"%slpk)
	try:
		return read("nodes/%s/textures/0_0.jpg"%node,slpk)
	except:
		return ""

@route('/<slpk>/SceneServer/layers/<layer>/nodes/<node>/textures/0_0_1')
@route('/<slpk>/SceneServer/layers/<layer>/nodes/<node>/textures/0_0_1/')
def Ctextures_info(slpk,layer,node):
	""" Compressed texture information """
	if slpk not in slpks: #Get 404 if slpk doesn't exists
		abort(404, "Can't found SLPK: %s"%slpk)
	try:
		return read("nodes/%s/textures/0_0_1.bin.dds.gz"%node,slpk)
	except:
		return ""

@route('/<slpk>/SceneServer/layers/<layer>/nodes/<node>/features/0')
@route('/<slpk>/SceneServer/layers/<layer>/nodes/<node>/features/0/')
def feature_info(slpk,layer,node):
	""" Feature information JSON """
	if slpk not in slpks: #Get 404 if slpk doesn't exists
		abort(404, "Can't found SLPK: %s"%slpk)
	FeatureData=json.loads(read("nodes/%s/features/0.json.gz"%node,slpk))
	response.content_type = 'application/json'
	return json.dumps(FeatureData)

@route('/<slpk>/SceneServer/layers/<layer>/nodes/<node>/Shared')
@route('/<slpk>/SceneServer/layers/<layer>/nodes/<node>/Shared/')
def shared_info(slpk,layer,node):
	""" Shared node information JSON """
	if slpk not in slpks: #Get 404 if slpk doesn't exists
		abort(404, "Can't found SLPK: %s"%slpk)
	try:
		Sharedressource=json.loads(read("nodes/%s/Shared/sharedResource.json.gz"%node,slpk))
		response.content_type = 'application/json'
		return json.dumps(FeatureData)
	except:
		return ""

@route('/<slpk>/SceneServer/layers/<layer>/nodes/<node>/attributes/<attribute>/0')
@route('/<slpk>/SceneServer/layers/<layer>/nodes/<node>/attributes/<attribute>/0/')
def attribute_info(slpk,layer,node,attribute):
	""" Attribute information JSON """
	if slpk not in slpks: #Get 404 if slpk doesn't exists
		abort(404, "Can't found SLPK: %s"%slpk)
	return read("nodes/%s/attributes/%s/0.bin.gz"%(node,attribute),slpk)

@route('/carte/<slpk>')
def carte(slpk):
	""" Preview data on a 3d globe """
	if slpk not in slpks: #Get 404 if slpk doesn't exists
		abort(404, "Can't found SLPK: %s"%slpk)
	return template('carte', slpk=slpk, url="http://%s:%s/%s/SceneServer/layers/0"%(host,port,slpk))

#Run server
run(host=host, port=port)
