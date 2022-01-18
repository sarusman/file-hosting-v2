from . import general_operand
import os

def generator(nom, poid, formats, img, file_id, showable):
	print(file_id)
	if img:
		return f"<h2>{extension_telecharger(nom, file_id)} <br> Format : {formats} <br><br> Poids : {poid}<br>{extention_supprimmer(file_id)} <hr /><img style='width:50%; height:70%' src='{general_operand.public_link(file_id)}'></h2>"
	elif showable:
		return f"<h2>{extension_telecharger(nom, file_id)} <br> Format : {formats} <br><br> Poids : {poid}<br> {extention_supprimmer(file_id)} <hr /><pre class='brush' : {nom}> <iframe src='{general_operand.public_link(file_id)}' style='width:50%; height:50%'; frameborder='0'></iframe></h2>"
	else:
		return f"<h2>{extension_telecharger(nom, file_id)} <br> Format : {formats} <br><br> Poids : {poid}<br> {extention_supprimmer(file_id)}<hr /> <pre class='brush' : {nom}> </h2>"
def extension_telecharger(domaine, file_id):
	return f'<br><a href="{general_operand.get_link()}/telecharge/{domaine}/{file_id}"> Télécharger</a><br>'

def extention_supprimmer(file_id):
	return '<br><a href="'+general_operand.get_link()+'/suprimme/'+file_id+'">Supprimer</a><br><br>'



def extension_home():
	return '<br><a href="'+general_operand.get_link()+'">Retour</a><br>'



