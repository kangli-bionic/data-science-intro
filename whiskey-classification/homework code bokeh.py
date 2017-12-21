# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 13:32:19 2017

@author: Szarzynka
"""

### Lecture

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster.bicluster import SpectralCoclustering

# read in files
whisky = pd.read_csv("whiskies.txt")
whisky["Region"] = pd.read_csv("regions.txt")

#check the content
whisky.head()
whisky.iloc[5:10, 0:5]
whisky.columns

#check the correlation between flavors
flavors = whisky.iloc[:,2:14]
corr_flavors = pd.DataFrame.corr(flavors)
print(corr_flavors)

#plot correlation matrix
plt.figure(figsize=(10,10))
plt.pcolor(corr_flavors)
plt.colorbar()
plt.savefig("corr_flavors.pdf")

#check the correlation between distilleries
corr_whisky = pd.DataFrame.corr(flavors.transpose())
plt.figure(figsize=(10,10))
plt.pcolor(corr_whisky)
plt.axis("tight")
plt.colorbar()
plt.savefig("corr_whisky.pdf")

#cluster whisky based on flavor profile (6 regions)
model = SpectralCoclustering(n_clusters=6, random_state=0)
model.fit(corr_whisky)

#how many observations belong to each cluster
np.sum(model.rows_, axis=1)

#how many clusters belong to each observation - should be 1
np.sum(model.rows_, axis=0)

#interpret - observation number 0 belongs to cluster 5
model.row_labels_

#add group labels from the model
whisky['Group'] = pd.Series(model.row_labels_, index=whisky.index)

#reorder rows in increasing order by group labels
whisky = whisky.ix[np.argsort(model.row_labels_)]
#alternatively
whisky.sort_values('Group', ascending=True, inplace=True)
#reset index
whisky = whisky.reset_index(drop=True)

#check the correlations
correlations = pd.DataFrame.corr(whisky.iloc[:, 2:14].transpose())
correlations = np.array(correlations)

#plot both correlations (over the flavor profiles plus the reordered one with clusters based on region)
#interpret - whiskies from the same cluster (region) may be similar to each other in terms of honey flavor, smokiness etc.
plt.figure(figsize=(14,7))
plt.subplot(121)
plt.pcolor(corr_whisky)
plt.title("Original")
plt.axis("tight")
plt.subplot(122)
plt.pcolor(correlations)
plt.title("Rearranged")
plt.axis("tight")
plt.savefig("correlations.pdf")


### Assignment DataCamp

from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool
from itertools import product

# 2 - create a dictionary
cluster_colors = ["red", "orange", "green", "blue", "purple", "gray"]
regions = ["Speyside", "Highlands", "Lowlands", "Islands", "Campbelltown", "Islay"]

region_colors = {}
for i in range(len(regions)):
    region_colors[regions[i]] = cluster_colors[i]
print(region_colors)

# 3 - define color strength of correlation
distilleries = list(whisky.Distillery)
correlation_colors = []
for i in range(len(distilleries)):
    for j in range(len(distilleries)):
        if correlations[i,j] < 0.7:                                          # if low correlation,
            correlation_colors.append('white')                              # just use white.
        else:                                                               # otherwise,
            if whisky.Group[i] == whisky.Group[j]:                          # if the groups match,
                correlation_colors.append(cluster_colors[whisky.Group[i]])  # color them by their mutual group.
            else:                                                           # otherwise
                correlation_colors.append('lightgray')                      # color them lightgray.
                
                                         
# 4 - make an interactive grid
data = {'x': np.repeat(distilleries, len(distilleries)),
        'y': list(distilleries)*len(distilleries),
        'colors': correlation_colors,
        'alphas': correlations.flatten(),
        'correlations': correlations.flatten(),
        }
source = ColumnDataSource(data)

output_file('Whisky Correlations.html', title='Whisky Correlations')
fig = figure(title='Whisky Correlations', x_axis_location ='above',
             tools='reset,hover,save',
             x_range=list(reversed(distilleries)),
             y_range=distilleries)
fig.grid.grid_line_color = None
fig.axis.axis_line_color = None


def location_plot(title, colors):
    output_file(title+".html")
    location_source = ColumnDataSource(
        data={
        'x': whisky[' Latitude'],
        'y': whisky[' Longitude'],
        'colors': colors,
        'regions': whisky.Region,
        'distilleries': whisky.Distillery
    })

    fig = figure(title=title, x_axis_location='above', tools='reset, hover, save')
    fig.plot_width = 400
    fig.plot_height = 500
    fig.circle('x', 'y', size=9, source=location_source, color='colors', line_color=None)
    fig.axis.major_label_orientation = np.pi / 3
    hover = fig.select(dict(type=HoverTool))
    hover.tooltips = {'Distillery': '@distilerries', 'Location': '(@x, @y)'}
    show(fig)

region_cols = [region_colors[i] for i in list(whisky['Region'])]
classification_cols = [cluster_colors[i] for i in list(whisky['Group'])]

location_plot('Whisky Locations and Regions', region_cols)
location_plot('Whisky Locations and Groups', classification_cols)
