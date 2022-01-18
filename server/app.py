from flask import Flask, render_template, request, redirect, session
import sqlite3, os, requests
from flask import send_file
from modules import general_operand, extention_generator
from modules import google
from database import database_op

app = Flask(__name__)
google_engine=google.Google()
app.secret_key=os.urandom(431)
database=database_op.Database()

@app.route('/')
def index():
	return render_template("index.html", link=general_operand.get_link()+"uploader", available=str(15-total_quota()/1000)[0:5], files=get_len())


def total_quota():
	values=general_operand.clear(database.select("size"))
	total=0
	for size in values:
		total+=float(size.split(" ")[0])
	return total
def get_len():
	return len(general_operand.clear(database.select("size")))


@app.route('/recherche', methods=['POST'])
def rechercher():
	nom=request.form['sherch']
	return redirect('/'+nom)


@app.route('/suprimme/<file_id>')
def supprimer(file_id):
	google_engine.delete(file_id)
	database.delete(file_id)
	return f"<center><h1>Le fichier a été supprimé</h1></center>{extention_generator.extension_home()}"




def download_fast(file_id, nom, pos):
	google_engine.downloader(file_id, nom, pos)


def get_site(nom):
	if exist(nom):
		return database.select_file("", nom)
	else:
		return False


@app.route('/<nom>')
def show_file(nom):
	site=get_site(nom)
	if not site:
		return f"<h1>Fichier {nom} inexistant {extention_generator.extension_home()}</h1>"
	file_format=site[0].split(".")[-1]
	file_id=site[1]
	file_size=site[2]
	img=general_operand.is_image(file_format)
	if img:
		return extention_generator.generator(nom, file_size, file_format, img, file_id, True)
	else:
		if general_operand.showable(file_format):
			return extention_generator.generator(nom, file_size, file_format, img, file_id, True)
		else:
			return f"{extention_generator.generator(nom, file_size, file_format, img, file_id, False)}<br>Affichage impossible <br>"




@app.route('/telecharge/<domaine>/<file_id>')
def download(domaine, file_id):
	return redirect(f"https://docs.google.com/uc?export=download&id={file_id}")



def exist(nom):
	values=database.select("name")
	return nom in general_operand.clear(values)



def saver(nom, file_id, size):
	database.insert(("name", "file_id", "size"), (nom, file_id, size))


def get_tt():
	fichiers=database.select("name")
	if len(fichiers)==0:
		return "<center>Aucun Fichier</center>"
	else:
		l_b=""
		for i in fichiers:
			l_b+="<center><h2><a href='"+general_operand.get_link()+i[0]+"'>"+i[0]+"</a><br></h2></center>"
		l_b+="</center>"
	return l_b



@app.route('/server')
def serve():
	return get_tt()



def save_file(file, path, name):
	file.save(path)
	data=google_engine.uploader(path, name)
	os.remove(path)
	return data



@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		try:
			file=request.files['file']
			nom=request.form['nom']
		except:
			return redirect('/')
		if nom=='' or file.filename=='':
			return redirect('/')

		dmn=file.filename.split('.')
		dmn=nom+"."+dmn[len(dmn)-1]
		dmn=dmn.replace('?', '-')

		if not exist(dmn):
			if general_operand.is_image(dmn.split(".")[1]):
				path=general_operand.get_path()+'static/'+dmn
			else:
				path=general_operand.get_path()+'templates/'+ dmn

			data_file=save_file(file, path, dmn)

			saver(dmn, data_file['id'], data_file["size"])
			return render_template('uploaded_site.html', domaine=dmn,nom_site=dmn, lien=general_operand.get_link()+dmn)
		else:
			return "<h1>Le nom est déja utilisé.</h1>"+general_operand.extension_home()

if __name__ == '__main__':
   app.run(debug=True)

