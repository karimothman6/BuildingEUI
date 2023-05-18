import streamlit as st
import joblib
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from PIL import Image

#Load Model
model=joblib.load("forest_model.sav")

# Define the color scheme
primary_color = "#0078FF"
secondary_color = "#F0F6FC"

# Set the page title and icon
st.set_page_config(page_title="Buildings EUI", page_icon=":rocket:")

# Add a heading and divider for the first section
st.sidebar.title("Basic Input")

# Add two dropdown menus for the first section
buildinglist=['College', 'HighriseApartment', 'Hospital', 'Laboratory','LargeOffice', 'MediumOffice', 'MidriseApartment', 'Outpatient']
building=st.sidebar.selectbox('Building Type',buildinglist)
zonelist=['1A', '2A', '2B', '3A', '3B', '3C', '4A', '4B', '4C', '5A', '5B','6A', '6B', '7A']
zone=st.sidebar.selectbox('Climate Zone',zonelist)

# Add a heading and divider for the second section
st.sidebar.markdown("---")
st.sidebar.title("Massing")

# Add four sliders for the second section
tarea=st.sidebar.number_input("Total Area",3700,94000)
pdepth=st.sidebar.slider("Plate Depth",10,50)
plength=st.sidebar.slider("Plate Length",40,125)
fheight=st.sidebar.slider("Floor Height",3.0,6.0)

# Add a heading and divider for the third section
st.sidebar.markdown("---")
st.sidebar.title("Facade")

# Add one slider and three dropdown menus for the third section
wwr=st.sidebar.slider("WWR (Window to Wall Ratio)",25,90)
solar=st.sidebar.selectbox('Solar Design',('Bad','Typical','Good'),help="Bad: N-S Orientation.All glazing on E/W \n \n Typical: E-W Orientation.Glazing evenly distributed \n \n Good: E-W Orientation. All glazing on N/W")
envelope=st.sidebar.selectbox('Envelope Quality',('Baseline', 'HighPerformance','UltraPerformance'))
lpd=st.sidebar.selectbox('LPD (Lightinig Power Density)',('Base', 'Better','Best'),help="Base: Baseline LPD from DOE Reference Building \n \n Better: 30% reduction from baseline \n \n Best: 60% reduction from baseline")
	
# Add a heading and divider for the fourth section
st.sidebar.markdown("---")
st.sidebar.title("HVAC")

# Add four dropdown menus for the fourth section
hvac=st.sidebar.selectbox('HVAC Setting',('Baseline', 'Good', 'Great', 'Ultra'),help="Baseline: Baseline HVAC from DOE Reference Building \n \n Good: 20% increase in COP from baseline \n \n Great: 35% increase in COP from baseline \n \n Ultra: 50% increase in COP from baseline")
setpoint=st.sidebar.selectbox('Setpoint Setting',('Baseline', 'Expanded'),help="Baseline: Default settings for program and system \n \n Expanded: Cooling +1.67 °C, Heating -1.67 °C")
heatcoil=st.sidebar.selectbox('Heating Coil',('Water', 'Electric','DX(Single Speed)'))
coolcoil=st.sidebar.selectbox('Cooling Coil',('Electric','DX(Single Speed)','DX(Double Speed)'))

# Add a heading for the fifth section
st.sidebar.markdown("---")
st.title("EUI & Cost:")

# Add a card to display the result
result_card = st.empty()
# Define a function to update the result card

def update_result():
    # Calculate delta
    prev_EUI = st.session_state.get("prev_EUI", 0)
    delta = EUI - prev_EUI


    # Display metric
    st.metric("EUI (kWh/m2):", "{:.4f}".format(float(EUI)), "{:.4f}".format(float(delta)))
    st.metric("Cost of Energy per year (18¢ per kWh):","{:,} $".format(int(EUI*.18*tarea)),"{:,} $".format(int(delta*.18*tarea)))
    
    # Update previous input value
    st.session_state.prev_EUI = EUI


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

EUI=model.predict(model_df)

update_result()

st.title("Climate Zones")
img = Image.open("IECCmap_Revised.jpg")
st.image(img)

# Add some custom CSS to improve the styling
st.markdown(
    f"""
    <style>
    .sidebar .sidebar-content {{
        background-color: {secondary_color};
        box-shadow: none;
    }}

    .sidebar .sidebar-content .block-container {{
        padding: 1rem;
    }}

    .sidebar .sidebar-content .stButton {{
        margin-top: 1rem;
    }}

    .main .block-container {{
        padding: 2rem;
    }}

    .main .stButton {{
        margin-top: 2rem;
    }}

    .stSlider .stSlider-min {{
        color: {primary_color};
    }}

    .stSlider .stSlider-max {{
        color: {primary_color};
    }}

    .stSlider .stSlider-value {{
        color: {primary_color};
    }}

    .stDropdown {{
        color: {primary_color};
        background-color: {secondary_color};
    }}

    .stMarkdown {{
        color: {primary_color};
    }}

    .stCard {{
        background-color: {secondary_color};
        border: none;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }}

    .stCardHeader {{
        border-bottom: none;
        padding: 1rem;
    }}

    .stCardBody {{
        padding: 1rem;
    }}

    .stCardFooter {{
        border-top: none;
        padding: 1rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


    
