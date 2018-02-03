import os
import sys
import glob
import h5py
import numpy as np
import pandas as pd
import sqlite3
import seaborn as sns
import matplotlib as mpl
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, contains_eager

from bokeh.layouts import row, widgetbox
from bokeh.plotting import curdoc, figure, show
from bokeh.models import Select, ColumnDataSource, HoverTool, OpenURL, TapTool

# custom markup for plot marker tooltips with thumbnails and metadata
hover = HoverTool(
    tooltips="""
    <div>
        <div height="100px" width="130px">
            <img
              src="@thumb" alt="@thumb"
              style="float: center; margin: 0px 15px 15px 0px; width: 100px; height: 100px"
              border="2"
            ></img>
        </div>
        <div>
            <span style="font-size: 17px; font-weight: bold; color: #990000;">Class</span>
            <span style="font-size: 15px;">@Main</span>
        </div>
        <div>
            <span style="font-size: 15px; color: #990000;">Image Code</span>
            <span style="font-size: 10px;">@key</span>
        </div>
        <div>
            <span style="font-size: 15px; color: #990000;">Mag</span>
            <span style="font-size: 10px;">@mag</span>
        </div>
    </div>
"""
)

def get_db():
    """ Get database of specific collection"""
    conn = sqlite3.connect('./static/info/info.sqlite')
    cursor = conn.cursor()
    sql = "select * from info"
    df = pd.read_sql(sql, conn)
    collection = ['al', 'ci', 'cs', 'cu', 'ti']
    entry = df[(df.main.isin(collection))]
    x_tsne = np.load('./static/info/x_tsne.npy')
    return (entry, x_tsne)

entry, x_tsne = get_db()
N = len(entry)

root_path = 'static/Micrographs_scaled/'
path_main = ['{}/'.format(main) for main in entry['main'].values]
path_id = ['{}_h.png'.format(key) for key in entry['Image_Code'].values]
thumb = [root_path + path_main[i] + path_id[i] for i in range(N)]


collection_dic={}
collection_dic['al']='dodgerblue'
collection_dic['ci']='palegreen'
collection_dic['cs']='orange'
collection_dic['cu']='blueviolet'
collection_dic['ti']='hotpink'
c=[collection_dic[i] for i in entry['main'].values]

source = ColumnDataSource(
    data=dict(
        key=entry['Image_Code'].values,
        x=x_tsne[:, 0],
        y=x_tsne[:, 1],
        thumb=thumb,
        main=entry['main'].values,
        Main=np.array([entry['main'].values[i].capitalize() for i in range(N)]),
        size=10 * np.ones(entry.index.size),
        color=c,
        alpha=0.8 * np.ones(entry.index.size),
        mag=entry['Original_magnification'].values
    )
)

p = figure(plot_height=800, plot_width=800, title='ASM t-SNE Visualization Explorer',
           tools=['crosshair', 'pan', 'reset', 'save', 'wheel_zoom', 'tap', hover])
clrcles = p.circle(source=source,
                   x='x', y='y',
                   size='size', alpha='alpha', color='color',
                   line_color='black', line_alpha=0.3)
p.toolbar.active_scroll = 'auto'


url_for_entry = "micrographs/@key"
taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url=url_for_entry)

curdoc().add_root(row(p))
curdoc().title = "ASMDB: a microstructure explorer"

show(p)
