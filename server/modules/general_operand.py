import os,ast
def get_path():
	#return "/home/serveur/mysite/server/static/"
	return "/Users/sarusman/desktop/server/"

def get_link():
	return "http://localhost:5000/"


def ch_name():
	lst=open("dernier_nom.txt")
	t=lst.read()
	t=t[7:len(t)]
	nom="fichier"+str(int(t)+1)
	lst=open("dernier_nom.txt", "w")
	lst.write(nom)
	lst.close()
	return nom


def clear(value):
	for i in range(len(value)):
		value[i]=value[i][0]
	return value

def public_link(file_id):
	return f"https://drive.google.com/uc?export=view&id={file_id}"

def showable(formats):
	formatable=["pdf", "html", "txt"]
	return formats in formatable


def is_image(ext):
	return ext in ["jpg", "png", "jpeg"]
