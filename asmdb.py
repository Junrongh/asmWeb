import os
import numpy as np
import pandas as pd
import sqlite3
import scipy.spatial.distance as distance
from flask import Flask, render_template, request, url_for
from bokeh.client import pull_session
from bokeh.embed import autoload_server


def get_db():
	""" Get database of specific collection """
	conn = sqlite3.connect('./static/info/info.sqlite')
	cursor = conn.cursor()
	sql = "select * from info"
	df = pd.read_sql(sql, conn)
	collection = ['al', 'ci', 'cs', 'cu', 'ti']
	entry = df[(df.main.isin(collection))]
	entry = entry.reset_index(drop = True)
	return entry


def df2dic(df, idx):
	""" Turn dataframe into dictionary """
	total = []
	for i in idx:
		dic = {}
		for j in df:
			try:
				dic[j] = df.loc[i][j].encode('utf-8').decode('utf-8')
			except AttributeError:
				if df.loc[i][j] == None:
					dic[j] = 'Not Mentioned'
				continue
		total.append(dic)
	return total


def paginate(results, page, PER_PAGE):
	""" The infomation in one page for Livriary Content """
	start = (page - 1) * PER_PAGE
	if start < 0 or start > len(results):
		return []
	end = min(start + PER_PAGE, len(results))
	page_data = {'prev_num': page - 1, 'next_num': page + 1,
				 'has_prev': True, 'has_next': True}
	if page_data['prev_num'] <= 0:
		page_data['has_prev'] = False
	if end >= len(results):
		page_data['has_next'] = False
	return results[start:end], page_data

app = Flask(__name__)

################################ Home Page ####################################

@app.route('/')
@app.route('/index')
@app.route('/imagesearch')
def index():
	return render_template('index.html')

################################ Write Up #####################################

@app.route('/<filename>')  
def download(filename):  
    return None 

########################## Interactive t-SNE Map ##############################

@app.route('/visualize')
def bokeh_plot():
	bokeh_script = autoload_server(
		None, url="file:///Users/Junrongh/flasky/asmdbweb/visualize.html")
	return render_template('visualize.html', bokeh_script=bokeh_script)

############################# Libriary Content ################################

@app.route('/entries')
@app.route('/entries/<int:page>')
def entries(page=1):
	db = get_db()
	items = 24
	entry_perpage, page_data = paginate(db, page, items)
	dic = []
	for i in range(0, len(entry_perpage)):
		dic.append(entry_perpage.iloc[i])
	return render_template('entries.html', entries=dic, pg=page_data)

############################ Micrograph Details ###############################

@app.route('/micrographs/<imagecode>')
def micrographs(imagecode):
	db = get_db()
	entry = db[(db.Image_Code == imagecode)]
	idx = list(entry.index)
	dic = df2dic(entry, idx)[0]
	return render_template('micrographdetail.html', dic=dic)

########################### Similar Micrographs ###############################

@app.route('/findsimilar/<imagecode>')
def visualquery(imagecode):
	db = get_db()
	x_tsne = np.load('./static/info/x_tsne.npy')
	items = 16
	entry = db[(db.Image_Code == imagecode)]
	idx = list(entry.index)
	dic = df2dic(entry, idx)[0]
	dist = distance.pdist(x_tsne)
	dist = distance.squareform(dist)
	similar_idx = np.argsort(dist[idx[0]])
	similar = []
	for i in range(1, items + 1):
		similar.append(db.iloc[similar_idx[i]])
	return render_template('similar.html', dic=dic, similar=similar)

############################ Searching Results ################################

@app.route('/search/keywords=<key>')
@app.route('/search/keywords=<key>/page=<int:page>')
def search(key, page=1):
	PER_PAGE = 20
	item = [i for i in db]
	result = pd.DataFrame(columns=item)
	dic = []
	info = key.split(' ')
	for i in info:
		idx = db['main'].str.contains(i)
	for i in item:
		try:
			for k in info:
				idx = idx | db[i].str.contains(k)
		except (AttributeError, ValueError):
			continue
	result = db[idx]
	n_result = len(result)

	entry_perpage, page_data = paginate(result, page, PER_PAGE)
	for i in range(0, len(entry_perpage)):
		dic.append(entry_perpage.iloc[i])

	return render_template('search.html', n=n_result, key=key, entries=dic, pg=page_data)


@app.route('/search', methods = ['POST'])
def search_r(page=1):
	key = request.values.get('keywords')
	PER_PAGE = 20
	db = get_db()
	item = [i for i in db]
	result = pd.DataFrame(columns=item)
	dic = []
	info = key.split(' ')
	for i in info:
		idx = db['main'].str.contains(i)
	for i in item:
		try:
			for k in info:
				idx = idx | db[i].str.contains(k)
		except (AttributeError, ValueError):
			continue
	result = db[idx]
	n_result = len(result)

	entry_perpage, page_data = paginate(result, page, PER_PAGE)
	for i in range(0, len(entry_perpage)):
		dic.append(entry_perpage.iloc[i])

	return render_template('search.html', n=n_result, key=key, entries=dic, pg=page_data)


######################### End Webpage functions ###############################


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=54455,debug=True)
