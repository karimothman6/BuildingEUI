import streamlit as st
import joblib
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

model=joblib.load("C:/Users/othma/Karim/DS/Projects/Python/Building/forest_model.sav")

st.title("Application")

side,main=st.columns([3,1])
with side:
    st.header("Basic Input")
    buildinglist=['College', 'HighriseApartment', 'Hospital', 'Laboratory','LargeOffice', 'MediumOffice', 'MidriseApartment', 'Outpatient']
    building=st.selectbox('Building Type',buildinglist)
    zonelist=['1A', '2A', '2B', '3A', '3B', '3C', '4A', '4B', '4C', '5A', '5B','6A', '6B', '7A']
    zone=st.selectbox('Climate Zone',zonelist)
    
    st.header("Massing")
    tarea=st.slider("Total Area",3700,94000)
    pdepth=st.slider("Plate Depth",10,50)
    plength=st.slider("Plate Length",40,125)
    fheight=st.slider("Floor Height",3,6)
   
    st.header("Facade")
    wwr=st.slider("WWR (Window to Wall Ratio)",25,90)
    solar=st.selectbox('Solar Design',('Bad','Typical','Good'))
    envelope=st.selectbox('Envelope Quality',('Baseline', 'HighPerformance','UltraPerformance'))
    lpd=st.selectbox('LPD (Lightinig Power Density)',('Base', 'Better','Best'))

    st.header("HVAC")
    hvac=st.selectbox('HVAC Setting',('Baseline', 'Good', 'Great', 'Ultra'))
    setpoint=st.selectbox('Setpoint Setting',('Baseline', 'Expanded'))
    heatcoil=st.selectbox('Heating Coil',('Water', 'Electric','DX(Single Speed)'))
    coolcoil=st.selectbox('Cooling Coil',('Electric','DX(Single Speed)','DX(Double Speed)'))


with main:
    
    model_df=pd.DataFrame(columns=['TotalArea', 'PlateDepth', 'PlateLength', 'FloorHeight', 'WWR',
       'BuildingType_College', 'BuildingType_HighriseApartment','BuildingType_Hospital', 'BuildingType_Laboratory',
       'BuildingType_LargeOffice', 'BuildingType_MediumOffice','BuildingType_MidriseApartment', 'BuildingType_Outpatient',
       'ClimateZone_1A', 'ClimateZone_2A', 'ClimateZone_2B', 'ClimateZone_3A','ClimateZone_3B', 'ClimateZone_3C', 'ClimateZone_4A', 'ClimateZone_4B',
       'ClimateZone_4C', 'ClimateZone_5A', 'ClimateZone_5B', 'ClimateZone_6A','ClimateZone_6B', 'ClimateZone_7A',
       'SolarDesign','EnvelopeQuality_Setting', 'HVAC_Setting', 'Setpoint_Setting','HeatingCoil', 'CoolingCoil', 'LPD_Adjustment_Setting'],index=[0]) 
    
    model_df=model_df.fillna(0)
    
    build='BuildingType_'+building
    model_df[build]=1
    
    climate='ClimateZone_'+zone
    model_df[climate]=1

    model_df['TotalArea']=tarea
    model_df['PlateLength']=plength
    model_df['PlateDepth']=pdepth
    model_df['FloorHeight']=fheight

    model_df['WWR']=wwr
    
    design={'Bad':0,'Typical':2,'Good':1}
    model_df['SolarDesign']=design[solar]
    
    quality={'Baseline':0, 'HighPerformance':1,'UltraPerformance':2}
    model_df['EnvelopeQuality_Setting']=quality[envelope]
    
    hsetting={'Baseline':0, 'Good':1, 'Great':2, 'Ultra':3}
    model_df['HVAC_Setting']=hsetting[hvac]

    ssetting={'Baseline':0, 'Expanded':1}
    model_df['Setpoint_Setting']=ssetting[setpoint]
    
    hcoiltypes={'Water':2, 'Electric':1,'DX(Single Speed)':0}
    model_df["HeatingCoil"]=hcoiltypes[heatcoil]
    
    ccoiltypes={'Electric':0,'DX(Single Speed)':1,'DX(Double Speed)':2}
    model_df["CoolingCoil"]=ccoiltypes[coolcoil]
    
    lpdadjust={"Base":0,"Better":2, "Best":1 }
    model_df['LPD_Adjustment_Setting']=lpdadjust[lpd]
    
    st.title("EUI(kWh/m2): ")
    EUI=model.predict(model_df)
    st.write(float(EUI))