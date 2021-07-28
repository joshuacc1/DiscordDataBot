import pandas
import matplotlib.dates
import pandas
import numpy
from bokeh.io import export_png, export_svgs
from bokeh.models import ColumnDataSource, DataTable, TableColumn
import matplotlib.pyplot as plt
import json
import urllib.request
import datetime

def querypoliceshooting(*args):
    iyear=int(args[0])
    fyear=int(args[1])
    df = pandas.read_csv('Data/Police_Shootings_By_Race.csv')
    if len(args) >=3:
        columns=list(args[2:len(args)])
        columns.insert(0,'Year')
        ttable=[x.lower() in [y.lower() for y in columns] for x in df.columns]
        table=df.columns[ttable]
        print(table)
        #if all(x in df.columns for x in columns):
        res = df[table][df['Year']>=iyear][df['Year']<=fyear]
    else:
        res=df[df['Year']>=iyear][df['Year']<=fyear]

    print(res)
    save_df_as_matplotlib_plot(res, 'dataimg.png')
    return res

def query_covid_statistics(country,sdate,edate,columns):
    with urllib.request.urlopen('https://covid.ourworldindata.org/data/owid-covid-data.json') as url:
        data=json.loads(url.read().decode())

    def columnvalue(item,col,default):
        if col in item:
            return item[col]
        else:
            return default
    dataquery={'date':[]}
    for col in columns:
        dataquery[col]=[]
    for x in data[country]['data']:
        date=[int(w) for w in x['date'].split('-')]
        linedate=datetime.datetime(date[0],date[1],date[2])
        if linedate>=sdate and linedate<edate:
            for col in dataquery:
                dataquery[col].append(columnvalue(x,col,None))
    data=pandas.DataFrame(dataquery)
    return data

def save_df_as_matplotlib_plot(df,path):
    fig,ax=plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    ax.table(cellText=df.values,colLabels=df.columns,loc='center',cellLoc='center',colColours=['gray']*len(df.columns))
    fig.tight_layout()
    plt.savefig(path)
    #plt.show()

def save_df_as_matplotlib_graph(df,path):
    fig,ax=plt.subplots()
    fig.patch.set_visible(False)
    daterange = [datetime.datetime.strptime(x, "%Y-%m-%d").date() for x in df['date']]
    for col in df.columns[1:]:
        ax.plot(daterange,[x for x in df[col]],label=col)
    intv=(daterange[-1]-daterange[0])/10
    ax.xaxis.set_major_locator(matplotlib.dates.DayLocator(interval=intv.days))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%m-%d-%Y"))
    ax.tick_params(axis='x',labelrotation=90)
    fig.tight_layout()
    plt.savefig(path)
    #plt.show()
