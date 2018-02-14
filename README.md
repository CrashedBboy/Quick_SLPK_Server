QUICK SLPK SERVER
======================

Minimalist web server engine to publish OGC SceneLayerPackage (.slpk) to Indexed 3d Scene Layer (I3S) web service.

Why this projects?  Publishing I3S service to Portal for ArcGIS requires to federated ArcGIS Server ... with this server, you can bypass this step and keep going with your non federated arcgis server.

How to use:
- Place .SLPK into a folder (default: "./slpk")  [You can create SLPK with ArcGIS pro and some other softwares]
- Configure the script (quick_slpk_server.py):
	- webserver host
	- webserver port
	- slpk folder
- Launch this script 
- Open browser to "host:port"
- Index page let you access your SLPK as I3S services
-  Also provide an intern viewer for test

- You can use your I3S services on arcgis online, portal for arcgis, arcgis javascript API, ...  simply use ther service url:
	{host}:{port}/{slpk name .slpk}/SceneServer

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
