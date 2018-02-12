<html>
<head>
<title>Quick SLPK Server</title>
</head>
<body>
<b>Liste des services disponibles:</b>
<ul>
	% for slpk in slpks:
		<li><a href="{{slpk}}/SceneServer">{{slpk}}</a><a href="carte/{{slpk}}"> [visualiser]</a></li>
	% end
</ul>
</body>
</html>