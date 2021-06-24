# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 01:18:05 2021

@author: DELL
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 20:21:46 2021

@author: Efernandez
"""
import streamlit as st   ### para reportear 
import pandas as pd      ### para leer base de datos 
import numpy as np       #### para operaciones numericas
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64

st.set_page_config(page_title= "Presidencial 2021", layout="wide")

 #VOTOS_P1  es PERU LIBRE     
 #VOTOS_P1  es FUERZA POPULAR
 
st.title('ELECCIÓN PRESIDENCIAL 2021 - Segunda vuelta')
st.markdown("""
             ** Data source:** [Oficina Nacional de Procesos Electorales (ONPE)-Datos Abiertos](https://www.datosabiertos.gob.pe/dataset/resultados-por-mesa-de-las-elecciones-presidenciales-2021-segunda-vuelta-oficina-nacional-de")   
             ** Fecha de Descarga :** 2021-06-22 
             """)
        
st.sidebar.header("Filtros")   
st.sidebar.header("") 

  
    ###### importamos información de los excel #################################################################################
@st.cache(suppress_st_warning=True)
def get_data():
        ruta ='BASE.xlsx'    
        base = pd.read_excel(ruta,sheet_name= "BASE", header = 0,engine ='openpyxl' )
        #mask = (base["DESCRIP_ESTADO_ACTA"].isin(["CONTABILIZADA","COMPUTADA RESUELTA"]))
        #base= base[mask].fillna(0)
        base= base.fillna(0)
        
        base["PART"] = np.round(base["N_CVAS"]/base["N_ELEC_HABIL"],3) 
        #base["VOTO_SHARE_FP"] = np.round(base["VOTOS_P2"]/( base["VOTOS_P2"] +base["VOTOS_P1"]),3)  # ratio de participación por mes
       # base["VOTO_SHARE_PL"] = np.round(base["VOTOS_P1"]/( base["VOTOS_P2"] +base["VOTOS_P1"]),3)
       # base["VOTO_SHARE_DIFF"] = abs(base["VOTO_SHARE_PL"]-base["VOTO_SHARE_FP"])
         
        COL ={"VOTOS_P1":"PERU LIBRE", "VOTOS_P2":"FUERZA POPULAR",
              "V1_VOTOS_P1":"Partido Nacionalista Peruano", "V1_VOTOS_P2": "Frente Amplio",
              "V1_VOTOS_P3":"Partido Morado","V1_VOTOS_P4": "Peru Patria Segura",
              "V1_VOTOS_P5": "Victoria Nacional","V1_VOTOS_P6": "Accion Popular",
              "V1_VOTOS_P7": "Avanza Pais", "V1_VOTOS_P8": "Podemos Peru",
              "V1_VOTOS_P9": "Juntos Por El Peru","V1_VOTOS_P10": "Partido Popular Cristiano",
              "V1_VOTOS_P11": "FUERZA POPULAR*","V1_VOTOS_P12": "Union Por El Peru",
              "V1_VOTOS_P13": "Renovacion Popular","V1_VOTOS_P14": "RUNA",
              "V1_VOTOS_P15": "Somos Perú","V1_VOTOS_P16": "PERÚ LIBRE*",
              "V1_VOTOS_P17": "Democracia Directa","V1_VOTOS_P18": "Alianza Para El Progreso"
              }
        
        base = base.rename(columns=COL)
         
        return base
    
base = get_data()    
       
  
dep = list(base["DEPARTAMENTO"].unique())  
select_dep = st.sidebar.selectbox("Departamento / Continente", dep,9)

mask=(base["DEPARTAMENTO"]== select_dep)
prov= list(base[mask]["PROVINCIA"].unique())   
select_prov = st.sidebar.selectbox("Provincia / País", prov,3)

mask=(mask)&(base["PROVINCIA"]== select_prov)
dist= list(base[mask]["DISTRITO"].unique())   
select_dist = st.sidebar.selectbox("Distrito / Ciudad", dist,2)


mask=(mask)&(base["DISTRITO"]== select_dist)
col= list(base[mask]["NOMB_LOCAL"].unique())   
select_col = st.sidebar.selectbox("Colegio / Local de Votación", col,0)

mask =(mask)&(base["NOMB_LOCAL"]==select_col)

#baseto = base[mask].set_index('MESA_DE_VOTACION',)
baseto = base[mask].reset_index(drop= True)
st.dataframe(baseto)


def filedownload(data):
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    ref = f'<a href="data:file/csv;base64,{b64}" download="eep2021.csv">Download CSV File</a>'
    return ref

st.markdown(filedownload(baseto), unsafe_allow_html=True)


LIS =["NOMB_LOCAL","PERU LIBRE","FUERZA POPULAR","N_CVAS","N_ELEC_HABIL","VOTOS_VB","VOTOS_VN",
      "Partido Nacionalista Peruano"  ,"Frente Amplio"   ,    "Partido Morado"   ,"Peru Patria Segura" ,
      "Victoria Nacional"       , "Accion Popular"  , "Avanza Pais"  , "Podemos Peru" ,
      "Juntos Por El Peru", "Partido Popular Cristiano" ,  "FUERZA POPULAR*"     , "Union Por El Peru",
      "Renovacion Popular" , "RUNA",  "Somos Perú"    , "PERÚ LIBRE*" ,
      "Democracia Directa", "Alianza Para El Progreso"  ,
      "V1_N_CVAS","V1_N_ELEC_HABIL","V1_VOTOS_VB","V1_VOTOS_VN"]
  
baseres= baseto[LIS].groupby(["NOMB_LOCAL"]).sum()
baseres = baseres.T.reset_index()
baseres = baseres.set_axis(['PARTIDOS', 'VOTOS'], axis=1, inplace=False)


base2v= baseres.loc[:5]
base2v["% VOTOS"] = base2v["VOTOS"]/sum(base2v.loc[:1]["VOTOS"])

base1v= baseres.loc[6:].reset_index(drop=True)
base1v["% VOTOS"] = base1v["VOTOS"]/sum(base1v.loc[:17]["VOTOS"])
#baseres1["% VOTOS "]=  baseres.loc[0:4]


base21v= base2v.loc[:1]
base12v= base1v.loc[:17]

#st.dataframe(base21v)
#st.dataframe(base12v)

fig = px.bar(base21v, x='PARTIDOS', y='% VOTOS',
             hover_data=['PARTIDOS', 'VOTOS'], 
             #labels={'pop':'population of Canada'},
             color='PARTIDOS',
             color_discrete_map={
                "PERU LIBRE": "red",
                "FUERZA POPULAR": "orange"},
             width = 420, height=430,
             title ="Resultados Segunda Vuelta"
             )
fig.update_layout(showlegend=False,
                  xaxis={'categoryorder':'total descending'},
                  title_x=0.5)                 
st.plotly_chart(fig, use_container_width=False)



fig2 = px.bar(base12v, x='PARTIDOS', y='% VOTOS',
             hover_data=['PARTIDOS', 'VOTOS'], 
             color="PARTIDOS",
             color_discrete_map={
                 "Partido Nacionalista Peruano" : "maroon",
                 "Frente Amplio"  :"darkseagreen"  ,
                 "Partido Morado"  :"blueviolet"  ,
                 "Peru Patria Segura" : "dodgerblue",
                 "Victoria Nacional"  :"khaki" , 
                 "Accion Popular"  :"lightcoral" ,
                 "Avanza Pais" : "darkblue" ,
                 "Podemos Peru" :"darkgoldenrod",
                 "Juntos Por El Peru": "green",
                 "Partido Popular Cristiano" :"forestgreen", 
                 "FUERZA POPULAR*"  : "orange"   ,
                 "Union Por El Peru" :  "goldenrod", 
                 "Renovacion Popular" : "deepskyblue",
                 "RUNA" : "darkgray",
                 "Somos Perú"  : "lightpink"  , 
                 "PERÚ LIBRE*" :"red" ,
                 "Democracia Directa" :"gainsboro"  , 
                 "Alianza Para El Progreso":"darkblue" },
             width = 800, height=475,
             title ="Resultados Primera Vuelta"
             )

fig2.update_layout(#showlegend=False,
                  xaxis={'categoryorder':'total descending'},
                 title_x=0.5)
st.plotly_chart(fig2, use_container_width=True)


option_1 = st.checkbox('initial velocity (u)')
option_2 = st.checkbox('final velocity (v)')
option_3 = st.checkbox('acceleration (a)')
option_4 = st.checkbox('time (t)')
