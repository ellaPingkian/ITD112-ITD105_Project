from flask import Flask, render_template
import numpy as np
import pandas as pd
from math import pi

import random
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LabelSet, Label, BasicTickFormatter, HoverTool

from bokeh.plotting import figure, ColumnDataSource
from bokeh.tile_providers import get_provider, Vendors
from bokeh.palettes import RdYlGn
from bokeh.transform import linear_cmap,factor_cmap
from bokeh.layouts import row, column
from bokeh.models import ColorBar, NumeralTickFormatter
from bokeh.transform import cumsum



app = Flask(__name__)

@app.route('/')
def dengue_cases():

  data = pd.read_csv('static\dataset\doh-epi-dengue-data-2016-2021.csv')
  cdata = data.dropna()

  # 1 line graph - Total number of recorded dengue cases and deaths by location + mortality rate per region
  # 	Options: By specific location
  # 		       By region
  reg = cdata['Region'].unique()

  reg_lst = []
  csum_lst = []
  dsum_lst = []
  mrate_lst = []

  for i in reg:
    reg_lst.append(str(i))
    dsum = int(cdata[(cdata['Region'] == i)][["deaths"]].sum())       #sum of all deaths per region
    dsum_lst.append(int(dsum))

    csum = int(cdata[(cdata['Region'] == i)][["cases"]].sum())       #sum of all cases per region
    csum_lst.append(int(csum))
    
    #mortality rate
    if csum == 0:
        mrate = 0
    else:
        mrate = round((dsum/csum)*100, 2)
        mrate = str(str(mrate) + "%")
        mrate_lst.append(mrate)

  source1 = ColumnDataSource(data=dict(
                            reg_lst=reg_lst,
                            csum_lst=csum_lst,
                            dsum_lst=dsum_lst,
                            mrate_lst=mrate_lst
                            ))

  p1 = figure(
        x_range=reg_lst,
        sizing_mode="stretch_width",
        # title="DEATHS RECORDED PER REGION",
        x_axis_label='REGIONS', 
        y_axis_label='RECORDED CASES & DEATHS',
        )
  
  l1 = LabelSet(x='reg_lst', y='csum_lst', text='csum_lst', text_color="black",
                    x_offset=5, y_offset=5, source=source1)

  citation = Label(x=900, y=280, x_units='screen', y_units='screen',
                  text='Highest recorded cases: R IV-A Calabarzon (163,117)\nHighest recorded deaths:  NCR (4009/116,147)\nLowest mortality rate: R I Ilocos Region (0.26%)',
                  background_fill_color='beige',
                  text_color="black"
                  )
  
  p1.line(reg_lst, csum_lst, line_width=6, color="teal", legend_label="cases recorded")
  p1.xgrid.grid_line_color = None
  p1.y_range.start = 0
  p1.add_layout(l1)
  p1.add_layout(citation)
  p1.xaxis.major_label_orientation = pi/4
  p1.xaxis.major_label_text_font_size= "11pt"
  p1.yaxis.major_label_text_font_size= "11pt"
  p1.xaxis.axis_label_text_font_size = "12pt"
  p1.xaxis.axis_label_text_font_style = "bold"
  p1.yaxis.axis_label_text_font_size = "12pt"
  p1.yaxis.axis_label_text_font_style = "bold"
  p1.yaxis.formatter = BasicTickFormatter(use_scientific=False)


  l2 = LabelSet(x='reg_lst', y='dsum_lst', text='dsum_lst', text_color="red",
                    x_offset=-10, y_offset=10, source=source1)
  
  l3 = LabelSet(x='reg_lst', y='dsum_lst', text='mrate_lst',
                    x_offset=-10, y_offset=24, source=source1)

  p1.line(reg_lst, dsum_lst, line_width=5, color='red', legend_label='deaths recorded')
  p1.add_layout(l2)
  p1.add_layout(l3)


  # 2. Line graph + Bar graph - reported dengue cases in the Philippines (col2, r2)
  # 	Options: By year
  # 		       By year by location
  # 		       By month (2016-2021) - this could further determine when is the season where mosquitos breed
  #scraping unique years from dataset
  data['DATE'] = pd.to_datetime(data['DATE'], format="%m/%d/%Y")

  year_lst = []
  deaths_pY = []
  cases_pY = []
  ymrate_lst = []
  cdata = data.dropna()                           # droping null value in dataset
  years = cdata['DATE'].dt.year.unique()          # unique list of years

  for i in years:
    year_lst.append(str(i))
    dPy = int(cdata[(cdata['DATE'].dt.year == i)][["deaths"]].sum())              # deaths per year
    deaths_pY.append(dPy)
    cPy = int(cdata[(cdata['DATE'].dt.year == i)][["cases"]].sum())              # deaths per year
    cases_pY.append(cPy)
  
    ymrate = round((dPy/cPy)*100, 2)
    ymrate = str("("+str(ymrate) + "%"+")")
    ymrate_lst.append(ymrate)

  source2 = ColumnDataSource(data=dict(
                            year_lst=year_lst,
                            deaths_pY=deaths_pY,
                            cases_pY=cases_pY,
                            ymrate_lst=ymrate_lst
                            ))

  p2 = figure(
        x_range=year_lst,
        sizing_mode="stretch_width",
        x_axis_label='YEARS', 
        y_axis_label='RECORDED CASES & DEATHS',
        )
  
  l11 = LabelSet(x='year_lst', y='cases_pY', text='cases_pY', text_color="black",
                    x_offset=-10, y_offset=5, source=source2)

  citation = Label(x=1000, y=300, x_units='screen', y_units='screen',
                  text='Highest recorded cases: 2019 (441,902)\nHighest recorded deaths:  2016 (8,127/209,544)\nHighest mortality rate: 2016 (3.88%)',
                  background_fill_color='beige',
                  text_color="black"
                  )
  
  p2.vbar(year_lst, top = cases_pY, width=0.5, color="teal", legend_label="cases recorded")
  p2.xgrid.grid_line_color = None
  p2.y_range.start = 0
  p2.add_layout(l11)
  p2.add_layout(citation)
  p2.yaxis.major_label_orientation = pi/4
  p2.xaxis.major_label_text_font_size= "11pt"
  p2.yaxis.major_label_text_font_size= "12pt"
  p2.xaxis.axis_label_text_font_size = "14pt"
  p2.xaxis.axis_label_text_font_style = "bold"
  p2.yaxis.axis_label_text_font_size = "12pt"
  p2.yaxis.axis_label_text_font_style = "bold"
  p2.yaxis.formatter = BasicTickFormatter(use_scientific=False)


  l22 = LabelSet(x='year_lst', y='deaths_pY', text='deaths_pY', text_color="black",
                    x_offset=-10, y_offset=10, source=source2)
  
  l33 = LabelSet(x='year_lst', y='deaths_pY', text='ymrate_lst', text_color="red",
                    x_offset=-15, y_offset=24, source=source2)

  p2.line(year_lst, deaths_pY, line_width=5, color='red', legend_label='deaths recorded')
  p2.add_layout(l22)
  p2.add_layout(l33)



  script1, div1 = components(p1)
  script2, div2 = components(p2)


  return render_template('index.html', script=[script1, script2], div=[div1, div2],)


@app.route('/world-dataset')
def world():
  
    wdata = pd.read_csv('static\dataset\philvolcs_2022_filtered.csv')
    wdata.dropna()

    # Define coord as tuple (lat,long)
    def x_coord(x, y):
    
        lat = x
        lon = y
        
        r_major = 6378137.000
        x = r_major * np.radians(lon)
        scale = x/lon
        y = 180.0/np.pi * np.log(np.tan(np.pi/4.0 + 
            lat * (np.pi/180.0)/2.0)) * scale
        return (x, y)

    # Define coord as tuple (lat,long)
    wdata['coords'] = list(zip(wdata['lat'], wdata['long']))
    # Obtain list of mercator coordinates
    mercators = [x_coord(x, y) for x, y in wdata['coords'] ]

    # Create mercator column in our wdata
    wdata['mercator'] = mercators
    # Split that column out into two separate columns - mercator_x and mercator_y
    wdata[['mercator_x', 'mercator_y']] = wdata['mercator'].apply(pd.Series)
    

    # Select tile set to use
    chosentile = get_provider(Vendors.CARTODBPOSITRON)

    # Choose palette
    palette = RdYlGn[11]

    # Tell Bokeh to use df as the source of the data
    source = ColumnDataSource(data=wdata)

    # Define color mapper - which column will define the colour of the data points
    color_mapper = linear_cmap(field_name = 'magnitude', palette = palette, low = wdata['magnitude'].min(), high = wdata['magnitude'].max())

    # Set tooltips - these appear when we hover over a data point in our map, very nifty and very useful
    tooltips = [("Magnitude","@magnitude"), ("Location","@loc"), ("Date","@date_time")]

    # Create figure
    p = figure(x_axis_type="mercator", y_axis_type="mercator", x_axis_label = 'Longitude', y_axis_label = 'Latitude', width=800, height=940, tooltips = tooltips)


    p.add_tile(chosentile)    # Add map tile
    p.circle(x = 'mercator_x', y = 'mercator_y', color = color_mapper, source=source, size=10, fill_alpha = 0.7)    # Add points using mercator coordinates

    #Defines color bar
    color_bar = ColorBar(color_mapper=color_mapper['transform'], 
                        formatter = NumeralTickFormatter(format='0.0[0000]'), 
                        label_standoff = 13, width=13, location=(0,0),
                        major_label_text_font_size = '15px')

    # Set color_bar location
    p.add_layout(color_bar, 'right')
    p.xaxis.major_label_text_font_size= "12pt"
    p.yaxis.major_label_text_font_size= "12pt"
    p.xaxis.axis_label_text_font_size = "14pt"
    p.xaxis.axis_label_text_font_style = "bold"
    p.yaxis.axis_label_text_font_size = "14pt"
    p.yaxis.axis_label_text_font_style = "bold"


    script4, div4 = components(p)
    return render_template('world.html', script=[script4], div=[div4],)


if __name__ == "__main__":
  app.run(debug=True)