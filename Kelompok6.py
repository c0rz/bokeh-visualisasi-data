# -*- coding: utf-8 -*-
"""Visdat_HDI.ipynb

Import library yang dibutuhkan
"""
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.models.widgets import Tabs, Panel
from bokeh.layouts import row, widgetbox

import pandas as pd

"""Load data"""

df = pd.read_excel('HDI.xlsx')

"""Data Exploration"""

# df.shape

"""Melihat 5 data teratas"""

# df.head()

"""Melihat info setiap kolom, terutama melihat missing value"""

# df.info()

"""## Data Preprocessing

Hanya mengambil data nasional
"""

df = df[df['Level'] == 'National']
# df.shape

df.drop(columns=['ISO_Code', 'Level', 'GDLCODE', 'Region'], inplace=True)


"""Mengganti index menjadi Country"""

df.set_index('Country', inplace=True)


"""Melakukan transpos"""

df = df.transpose()


"""Mengubah tipe data indeks dari int menjadi str"""

df.index = df.index.map(str)

"""Melakukan reset index sehingga Year menjadi kolom baru dan melihat tipe data kolom Year yang baru dibuat tersebut"""

df = df.reset_index().rename(columns={'index': 'Year'})
# df.dtypes['Year']

"""Menghilangkan 'Country' dari index"""

df.columns.name = None


"""Melihat info dengan banyak float64 ada 186 dan object sebanyak 1"""

# df.info()

"""Visualisasi Bokeh"""

"""Membuat Column Data Source"""

# CDS Source 1 untuk Visualisasi Line/Scatter Pertama
source1 = ColumnDataSource(data={
    'x': df['Year'],
    'y': df['Indonesia']
})

# CDS Source 2 untuk Visualisasi Line/Scatter Kedua
source2 = ColumnDataSource(data={
    'x': df['Year'],
    'y': df['Singapore']
})

"""Mengatur Tooltips untuk Hover (Jika menggerakan mouse ke gambar, menampilkan data)"""

tooltips = [
    ('Year', '$x{0}'),
    ('HDI', '$y'),
]

"""Tools yang dipakai di sebelah kanan"""

select_tools = ['pan', 'wheel_zoom', 'save', 'reset']

"""Panel 1 Berisi Visualisasi Garis/Line"""

# Mengatur Figure
fig_garis = figure(title='Membandingkan HDI Antara 2 Negara',
                   plot_height=550, plot_width=1000,
                   x_axis_label='Tahun', y_axis_label='HDI',
                   tools=select_tools)

# Negara 1
fig_garis.line(x='x', y='y',
               color='salmon',
               line_width=4,
               source=source1,
               legend_label='Negara 1')

# Negara 2
fig_garis.line(x='x', y='y',
               color='royalblue',
               line_width=4,
               source=source2,
               legend_label='Negara 2')

# Lokasi Legend
fig_garis.legend.location = 'top_left'

# Menambahkan Hover
fig_garis.add_tools(HoverTool(tooltips=tooltips))

"""Panel 2 Berisi Visualisasi Scatter / Titik"""

# Membuat Figure
fig_titik = figure(title='Membandingkan HDI Antara 2 Negara',
                   plot_height=550, plot_width=1000,
                   x_axis_label='Tahun', y_axis_label='HDI',
                   tools=select_tools)

# Negara 1
fig_titik.scatter(x='x', y='y',
                  color='salmon',
                  size=10,
                  source=source1,
                  legend_label='Negara 1')

# Negara 2
fig_titik.scatter(x='x', y='y',
                  color='royalblue',
                  size=10,
                  source=source2,
                  legend_label='Negara 2')

# Lokasi Legend
fig_titik.legend.location = 'top_left'

# Menambahkan Hover
fig_titik.add_tools(HoverTool(tooltips=tooltips))

"""Function untuk mengupdate saat terjadi interaksi"""


def update_plot(attr, old, new):
    nilai_negara1 = select1.value
    nilai_negara2 = select2.value

    new_data1 = {
        'x': df['Year'],
        'y': df[nilai_negara1]
    }

    new_data2 = {
        'x': df['Year'],
        'y': df[nilai_negara2]
    }

    source1.data = new_data1
    source2.data = new_data2


"""Mengatur Select"""

# Pilihan pada Select berupa List Seluruh Negara
option = df.columns.to_list()
del option[0]

# Select 1 untuk pilihan Negara 1
select1 = Select(
    options=option,
    title='Pilih Negara 1 (Berwarna Merah)',
    value='Indonesia'
)

# Select 2 untuk pilihan Negara 2
select2 = Select(
    options=option,
    title='Pilih Negara 2 (Berwarna Biru)',
    value='Singapore'
)

# Jika Select dipilih
select1.on_change('value', update_plot)
select2.on_change('value', update_plot)

"""Mengatur Layout, Panel, dan Tabs"""

# Membuat layout dengan widget di sebelah kiri
layout1 = row(widgetbox(select1, select2,), fig_garis)
layout2 = row(widgetbox(select1, select2,), fig_titik)

# Membuat 2 Panel
garis_panel = Panel(child=layout1, title='Visualisasi Garis (Line)')
titik_panel = Panel(child=layout2, title='Visualisasi Titik (Scatter)')

# Menggabungkan Panel menjadi Tab
tabs = Tabs(tabs=[garis_panel, titik_panel])

curdoc().add_root(tabs)
