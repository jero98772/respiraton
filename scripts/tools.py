def writetxt(name,content):
	content = str(content)
	with open(name, 'w') as file:
		file.write(content)
		file.close()