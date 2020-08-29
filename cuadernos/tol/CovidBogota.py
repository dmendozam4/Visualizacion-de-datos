import pandas as pd
import matplotlib.pyplot as plt
from ipywidgets import interact, interactive
import ipywidgets as widgets
import numpy as np
import datetime
from IPython.core.display import HTML, display

linea='*'*100
hoy= pd.to_datetime('today')
ayer= hoy - datetime.timedelta(days=1)
ayer=ayer.strftime('%d%m%Y')

url="https://datosabiertos.bogota.gov.co/dataset/44eacdb7-a535-45ed-be03-16dbbea6f6da/resource/b64ba3c4-9e41-41b8-b3fd-2da21d627558/download/osb_enftransm-covid-19_"
url= url + ayer + ".csv"

#url="Covid.csv"

df=pd.read_csv(url,sep=';',encoding='latin1')
reg=df["Fecha de inicio de síntomas"].count()
dfcovid=df.drop(range(reg-2,reg +1  , 1),axis=0)
dfcovid['Estado'] = dfcovid['Estado'].replace("Fallecido No aplica No causa Directa","FallecidoOtrasCausas")
dfcovid['Ubicación'] = dfcovid['Ubicación'].replace("Fallecido No aplica No causa Directa","FallecidoOtrasCausas")
FechaSeparada=dfcovid['Fecha de diagnóstico'].str.split("/", n=2, expand=True)
dfcovid['DíaDiagnóstico']=pd.to_numeric(FechaSeparada[0])
dfcovid['MesDiagnóstico']=FechaSeparada[1]
dfcovid['MesDiagnóstico'] = dfcovid['MesDiagnóstico'].replace("03","Marzo")
dfcovid['MesDiagnóstico'] = dfcovid['MesDiagnóstico'].replace("04","Abril")
dfcovid['MesDiagnóstico'] = dfcovid['MesDiagnóstico'].replace("05","Mayo")
dfcovid['MesDiagnóstico'] = dfcovid['MesDiagnóstico'].replace("06","Junio")
dfcovid['MesDiagnóstico'] = dfcovid['MesDiagnóstico'].replace("07","Julio")
dfcovid['MesDiagnóstico'] = dfcovid['MesDiagnóstico'].replace("08","Agosto")

###Primer widget

def f(sexo):
    df2=dfcovid[dfcovid["Sexo"]==sexo].groupby("Ubicación").count()
    df2["Orden"]=[1,2,3,4,5]
    #df2["Orden"]=[1,3,4,5,2]
    df2=df2.sort_values(by="Orden")
    ind=df2.index
    data=df2["Sexo"]
    fig, ax = plt.subplots(figsize=(6, 5), subplot_kw=dict(aspect="equal"))
    #Explode sirve para separar de la torta cada variable
    wedges, texts = ax.pie(data,wedgeprops=dict(width=0.5), explode=(0,0,-0.1,0.5,-0.1),                        
                                      startangle=-40)
    pct=["{:.2%}".format(da/sum(data)) for da in data]
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")
    
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))        
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(ind[i]+"  "+pct[i], xy=(x, y),
                    xytext=(2.5*np.sign(x), 2.4*y),
                    horizontalalignment=horizontalalignment, **kw)
    ax.set_title("Participación de casos en el sexo "+ sexo +
                 "\n\n"+" {:,} casos confirmados".format(sum(data)) +"\n")

    plt.show()
    return
df2=dfcovid.groupby("Sexo").count().index
Wid1=interactive(f, sexo=widgets.Dropdown(options=df2,value="F", 
                                       description="Sexo:", 
                                       disabled=False,))

##Segundo widget
def filtromes(MesDiagnóstico):    
    
    if MesDiagnóstico== 1:
        MesDiagnóstico='Abril'
    elif MesDiagnóstico== 2:
        MesDiagnóstico='Agosto'
    elif MesDiagnóstico== 3:
        MesDiagnóstico='Julio'
    elif MesDiagnóstico== 4:
        MesDiagnóstico='Junio'
    elif MesDiagnóstico== 5:
        MesDiagnóstico='Marzo'
    else:    
        MesDiagnóstico='Mayo'
    
    Casos=dfcovid[dfcovid['MesDiagnóstico']==MesDiagnóstico].groupby('DíaDiagnóstico')['Ubicación'].count().reset_index(name='NumCasos')
    #ylabels=Casos['DíaDiagnóstico'].unique()
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Una función para poner la cantidad de casos
    def autolabel(rects):
        for rect in rects:
            width = rect.get_width()
            ax.annotate('{:,}'.format(width),
                        xy=(width,rect.get_y() + rect.get_height() / 2),
                        xytext=(3,0),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='left', va='center')

    rects=ax.barh(Casos.index,Casos['NumCasos'])
    ax.set(xlim=(0, max(Casos['NumCasos'])+5))
    plt.title("En total existen {:,} en Bogotá para este mes".format(sum(Casos["NumCasos"])))
    autolabel(rects)
    #ax.set_yticklabels(ylabels)
    plt.ylabel('Día Diagnóstico')
    plt.xlabel('Número de casos día')
    plt.show()
    return

Wid=[('Marzo',5),('Abril',1),('Mayo',6),('Junio',4),('Julio',3),('Agosto',2)]
Wid2=interactive(filtromes, MesDiagnóstico=widgets.Dropdown(
    options=Wid,
    value=5,
    description='MesDx:',
    disabled=False,
))

#### Dashboard
##Misma funcion encabezado en los ejepmlos anteriores
def miprimerdashboard():
    display(HTML( '<h2>Casos distribuidos por sexo en Bogotá</h2>'+
                '<p>El siguiente gráfico muestra las distribuciones por sexo en Bogotá:</p>'))
    display(HTML('<h2>Proporción de casos en cada sexo</h2>'+
                '<p>Seleccione el sexo e identifique la cantidad de casos hay por ubicación:</p>'))
  
    display(Wid1)
    display(HTML('<h2>Distribución mensual de casos</h2>'+
                '<p>Ahora veamos la cantidad de casos diarios por mes:</p>'))
  
    display(Wid2)
    
    return