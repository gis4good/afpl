# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 10:50:37 2022

@author: THIS-LAPPY
"""


from flask import Flask,jsonify,render_template,redirect, url_for, session
from flask_cors import CORS, cross_origin
import geopy.distance
#import chart as chart
from flask import request
from collections.abc import Mapping
import requests,json,numpy as np,pandas as pd,io
from twilio.twiml.messaging_response import MessagingResponse
from sqlalchemy import create_engine,text
from io import StringIO
from google.auth import compute_engine
#from matplotlib import pylab
#from matplotlib.animation import FuncAnimation
#from pylab import rcParams
import os
#service_account ='apindvi@ndvi12345.iam.gserviceaccount.com'
#credentials = ee.ServiceAccountCredentials(service_account, 'templates/private_key.json')
#ee.Initialize(credentials)
#os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

#from keras.models import load_model
#from tensorflow.keras.utils import load_img

from IPython.display import Image

import pandas as pd
import matplotlib
engine = create_engine('postgresql://root:oJmXhoHDzuGG3IZHnbnrEnRQR7QqLR5Q@dpg-cl6p55oicrhc73csvf10-a.oregon-postgres.render.com/afpldb')
conn = engine.connect()
app=Flask(__name__)
app.secret_key = 'rabbit12345' 
CORS(app)
@app.route('/home/')
def world():
    x='hello home'
    return x
    
#@app.route('/')
#def index():
#return "<h1>Welcome to our server !!</h1>"


@app.route('/dist/',methods=['GET'])
def distance():
    try:
        x1 = request.args.get('x1')
        x2 = request.args.get('x2')
        y1 = request.args.get('y1')
        y2 = request.args.get('y2')
        coords_1 = (x1,y1)
        coords_2 = (x2,y2)
        dist=geopy.distance.geodesic(coords_1, coords_2).km
        dist={'Distance (Km)':round(dist,2)}
    
        return dist
    except Exception as e:
        err={'Error':str(e)}
        return err

@app.route('/temp/',methods=['GET'])
def wt():
    try:
        x1=request.args.get('x1')
        y1 = request.args.get('y1')
        crop=str(request.args.get('crop'))
        
        if x1=='None' or y1 == 'None' or crop == 'None':
             err={'Error':'Enter correcr arguments','Status':'False'}
             return err    
        
        
        if crop.lower()=='wheat':
           wf=requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={float(y1)}&longitude={float(x1)}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m,precipitation')
           content = json.loads(wf.content)
           wf = pd.DataFrame.from_dict(content)
           wheattmax=35
           
           if np.mean(wf['hourly'][6])>wheattmax:
                msg={'Weather Status':"""Temperatures would be 3-5 degrees Celsius above normal
                                         over your cropping area for the next five days. 
                                         Maximum temperatures are already at 35-37 degrees.""",
                     'Effects':       """This higher day temperature might lead to adverse effect on wheat 
                                         as wheat crop is approaching reproductive growth period, which is sensitive to temperature. 
                                         High temperature during flowering and maturing period leads to loss in yield. 
                                         There could be similar impact on other standing crops and horticulture.""",
                     'Mitigation':    """Adapting to heat stress through agronomic management practices like timely sowing, 
                                         zero tillage, supplemental irrigation and fertilizer at grain filling stage and 
                                         selection of suitable cultivars according to the agro-climatic conditions are some of 
                                         the options which can help alleviation of terminal heat stress in wheat.""",     
                     'Status':True                    
                                        
                    }
                # msg=pd.DataFrame.from_dict(msg)
                response= jsonify(msg) 
                response.set_data(json.dumps(msg, ensure_ascii=False, separators=(',', ':')))
                return response

           else:
               msg={'Weather Status':"All seems to be looking good.Happy Farming",
                    'Mean Temperature':round(np.mean(wf['hourly'][6]),2),
                    'Mean Precipitation':round(np.mean(wf['hourly'][9]),2),
                    'Status':'True'
                   
                   }
               return jsonify(msg)
           
        elif crop.lower()=='rice':
            wf=requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={float(y1)}&longitude={float(x1)}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m,precipitation')
            content = json.loads(wf.content)
            wf = pd.DataFrame.from_dict(content)
            ricemax=44
            
            if np.mean(wf['hourly'][6])>ricemax:
                 msg=[{'Weather Status':"""Temperatures would be 3-5 degrees Celsius above normal
                                          over your cropping area for the next five days. 
                                          Maximum temperatures are already at 42-45 degrees.""",
                      'Effects':       """Reduced yield: High temperatures can cause decreased pollen production and poor grain filling, resulting in reduced yields.

                                          Increased susceptibility to pests and diseases: Rice plants that are exposed to high temperatures are more susceptible to pests and diseases, which can further reduce yields.

                                          Reduced nutrient uptake: High temperatures can impair the uptake of essential nutrients, such as nitrogen and phosphorus, leading to reduced growth and yield.

                                          Reduced water use efficiency: Rice plants exposed to high temperatures tend to use more water, leading to reduced water use efficiency.""",
                      'Mitigation':    """Planting heat-tolerant rice varieties: Researchers have developed rice varieties that are more heat tolerant, which can help reduce the negative effects of high temperatures on crop yields.

                                          Shading and cooling: Providing shade to rice crops, either through the use of shading nets or intercropping with shade-giving crops, can help reduce the amount of heat stress experienced by the rice plants. Additionally, cooling techniques such as sprinkling water on the crop or using evaporative cooling can help mitigate the negative effects of high temperatures.

                                          Improving soil fertility: Maintaining healthy soil fertility can help improve the heat tolerance of rice crops, as healthy soil can help plants better withstand stress.

                                          Changing planting schedules: Planting rice earlier or later in the season can help avoid periods of high temperature stress, reducing the negative effects on the crop.""",     
                      'Status':True                    
                                         
                     }]
                 msg=pd.DataFrame.from_dict(msg)
                 return jsonify(msg.to_dict('records')) 
            else:
                msg={'Weather Status':"All seems to be looking good.Happy Farming",
                     'Mean Temperature':round(np.mean(wf['hourly'][6]),2),
                     'Mean Precipitation':round(np.mean(wf['hourly'][9]),2),
                     'Status':True
                    
                    }
                return jsonify(msg)
           
            
           
            
           
            
        else:
            
               msg={"Message":'Request crop not found,we have added in our database and soon it will be added'
                   
                   }
        
               return msg

    except Exception as e:
           err={'Error':str(e),'Status':False}
           return err
@app.route('/msg',methods=['POST'])   
def reply():
    incoming_msg = request.form.get('Body').lower()
    response = MessagingResponse()
    message=response.message()
    responded = False
    words = incoming_msg.split('@')
    if "hello" in incoming_msg:
        reply = "THis is a Farmer Support System :-Here are the avalaible information"
        message.body(reply)
        responded = True        
    return str(response)    
@app.route('/map/<file>',methods=['GET'])    
def leaf(file):
    if file=='tl':
        return render_template('tl.html')
    if file=='od':
        return render_template('od.html') 
    if file=='balipatna':
        return render_template('balipatna.html')  
    if file=='kurmalguda':
        return render_template('kurmalguda.html') 
    if file=='rangareddy':
        return render_template('rangareddy.html')    
    if file=='maheshwaram':
        return render_template('maheshwaram.html')
    if file=='chevella':
        return render_template('chevella.html')    
    if file=='ibrahim':
        return render_template('ibrahim.html')     
    if file=='narayankhed':
        return render_template('narayanked.html')
    if file=='zaheerabad':
            return render_template('zaheerabad.html')
    if file=='sadashivpet':
            return render_template('sadashivpet.html')
    if file=='pashamylaram':
            return render_template('pashamylaram.html')
    if file=='narsapur':
            return render_template('narsapur.html')      
    if file=='Kulkacharla':
        return render_template('Kulkacharla.html')
    if file=='tandur':
            return render_template('tandur.html')
    if file=='vikarabad':
            return render_template('vikarabad.html')
    if file=='narisinghi':
        return render_template('narisinghi.html')
    if file=='shankarampet':
        return render_template('shankarampet.html') 
    if file=='form':
        return render_template('form.html')     
    if file=='kyc':
        return render_template('kyc.html')     
@app.route('/ai/',methods=['GET'])
def ai():
    try:
        
        x1 = request.args.get('x1')
        y1 = request.args.get('y1')
        Point_1 = ee.FeatureCollection(
                [ee.Feature(
                    ee.Geometry.Point([  float(x1),float(y1)]),
                    {
                      "system:index": "0"
                    })]);



        startDateviz = ee.Date.fromYMD(2021,1,1);
        endDateviz = ee.Date.fromYMD(2023,12,20);
        collectionviz = ee.ImageCollection("COPERNICUS/S2").filterDate(startDateviz,endDateviz).filterBounds(Point_1).filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than', 30);





        startDate = ee.Date.fromYMD(2018,1,1);
        endDate = ee.Date.fromYMD(2023,12,31);

        S2_nocloud = ee.ImageCollection("COPERNICUS/S2_SR").filterDate(startDate,endDate).filterBounds(Point_1).filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than',10)

        # S2_NDVI_nocloud = S2_nocloud.map(lambda image: image.normalizedDifference(['B8', 'B4']).rename('NDVI').copyProperties(image, ['system:time_start']))
        S2_EVI_nocloud = S2_nocloud.map(lambda image: image.expression(
                '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
                    'NIR': image.select('B8').divide(10000),
                    'RED': image.select('B4').divide(10000),
                    'BLUE': image.select('B2').divide(10000)
                }).rename('EVI').copyProperties(image, ['system:time_start']))


        point_evi = chart.Image.series(**{'imageCollection': S2_EVI_nocloud,
                                           'region': Point_1,
                                           'reducer': ee.Reducer.mean(),
                                           'bands' : 'EVI',
                                           'scale': 20,
                                           'xProperty': 'system:time_start'})



        point_evi.renderWidget(width='50%')
        p2_dataframe = point_evi.dataframe
        resampled_data = p2_dataframe.resample("30D").mean().dropna()
        evi_values=resampled_data['EVI']
        resampled_data['vv']=resampled_data.index
        time_values=list(resampled_data['vv'])

        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 12
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        import matplotlib.pyplot as plt
        plt.style.use('fivethirtyeight')
        rcParams['figure.figsize'] = 18, 8




        plt.style.use('fivethirtyeight')
        rcParams['figure.figsize'] = 18, 8

        p2_dataframe.plot(figsize=(15, 6),ylim=(0,1))
        plt.savefig(f"./static/images/{float(x1)+float(y1)}.jpg")
        
        model = load_model('model_saved.h5')
          
        image = load_img(f"./static/images/{float(x1)+float(y1)}.jpg" ,target_size=(224, 224))
        img = np.array(image)
        img = img / 255.0
        img = img.reshape(1,224,224,3)
        label = model.predict(img)
        
        def update(frame):
            ax.clear()
            ax.plot(time_values[:frame+1], evi_values[:frame+1], marker='o')
            ax.set_title('EVI Values Over Time')
            ax.set_xlabel('Time')
            ax.set_ylabel('EVI')
            ax.set_xlim(min(time_values), max(time_values))  # Set limits for x-axis
            ax.set_ylim(0, 1)  # Set limits for y-axis
            
        fig, ax = plt.subplots()

        ax.xaxis_date()

        ani = FuncAnimation(fig, update, frames=int(len(time_values)), interval=1)
        plt.show()

        animation_filename =f"./static/images/{float(x1)+float(y1)}.gif"
        ani.save(animation_filename, writer='pillow')
        
        
        if label[0][0]<0.85:
            type='Non Crop'
            
        else:
           type='Crop Land' 
           
           
         # Replace with your image URL
        description ='Vegetation Report='+type
        image_url=f'images/{float(x1)+float(y1)}.gif'
        return render_template('img.html', image_url=image_url, description=description)    
       
    except Exception as e:
        err={'Error':str(e)}
        return err

@app.route('/fdata/',methods=['POST'])
def fdata():
        bid = request.form.get('bid')
        zone = request.form.get('zone')
        phone = request.form.get('phone')
        date = request.form.get('date')
        vila = request.form.get('vila')
        lid = request.form.get('lid')
        lat = request.form.get('latitude')
        long = request.form.get('longitude')
        cn = request.form.get('cn')
        pin = request.form.get('pincode')
        yq=request.form.get('yesNoQuestion')
        ar = request.form.get('number1')
        mr = request.form.get('number2')
        cd = request.form.get('question')



        selfie_base64 = request.form.get('selfie')
        
        
        response_data = {
           'name': bid,
           'zone': zone,
           'phone': phone,
           'lat':lat,
           'long':long,
           'village':vila,
           'client_name':cn,
           'pincode':pin,
           'met_with_client':yq,
           'collection_done':cd,
           'amount_received':ar,
           'mr_number':mr,
           'ptp_date':date,
           'lid':lid,
           'selfie':selfie_base64,
                   }
        
        rr=pd.DataFrame.from_records([response_data])
        rr.to_sql('df',con=conn,if_exists='append',index=False)
        return response_data 

@app.route('/sugg/',methods=['GET'])
def get_suggestions():
    input_value = request.args.get('input', '')
    input_value=input_value.title()
    db=request.args.get('db')
    # Handle empty input gracefully
    if not input_value:
        return jsonify([])

    # Execute a query to get suggestions
    query = text(f'SELECT "{db}" FROM public.{db} WHERE "{db}" LIKE :input_value LIMIT 5')
    with conn.connect() as connection:
        result = connection.execute(query, input_value=f'{input_value}%')
        suggestions = [row[0] for row in result.fetchall()]

    # Return suggestions as JSON
    return jsonify(suggestions)
        
@app.route('/')
def index():
    # Check if the user is logged in before rendering the HTML template
    if 'username' in session:
        return render_template('form.html')
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username,password)
        # Check credentials against the database
        if check_credentials(username, password):
            session['username'] = username
            # Redirect to the main page after successful login
            return redirect(url_for('index'))
        else:
            # Render the login page again with an error message
            return render_template('login.html', error='Invalid credentials')

    # Render the login page for GET requests
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session to log the user out
    session.clear()
    # Redirect to the login page after logout
    return redirect(url_for('login'))
@app.route('/fdatakyc/',methods=['POST'])
def fdatakyc():
        bid = request.form.get('bid')
        zone = request.form.get('zone')
        staff = request.form.get('staff')
        mid = request.form.get('mid')
        lid = request.form.get('lid')
        mname = request.form.get('mname')
        lat = request.form.get('latitude')
        long = request.form.get('longitude')
        sname = request.form.get('sname')
        kyc = request.form.get('kyc')
        kycid=request.form.get('kycid')
        yq=request.form.get('yesNoQuestion')
        selfie_base64 = request.form.get('selfie')
        selfie_base641 = request.form.get('selfie1')
        selfie_base642 = request.form.get('selfie2')
        selfie_base643 = request.form.get('selfie3')
        selfie_base644 = request.form.get('selfie4')

        
        
        response_data = {
           'branch': bid,
           'zone': zone,
           'emp_id': staff,
           'client_id':mid,
           'lat':lat,
           'long':long,
           'ln_id':lid,
           'client_name':mname,
           'spouce_name':sname,
           'kyc_id':kycid,
           'secondary_id_type':yq,
           'kyc_photo_back':selfie_base64,
           'spouse_photo':selfie_base641,
           'kyc_photo_front':selfie_base642,
           'secondary_photo_front':selfie_base643,
           'secondary_photo_back':selfie_base644,
                   }
        
        rr=pd.DataFrame.from_records([response_data])
        rr.to_sql('kyc',con=conn,if_exists='append',index=False)
        return response_data 

def check_credentials(username, password):
    us=pd.read_sql(f"""select * from public.pass where "Emp ID"='{username}' and "password"='{password}'""" ,conn)
    if len(us)==1:
        return username == us['Emp ID'][0] and password == us['password'][0]
    else:
        return False
       

if __name__ == '__main__':
    app.run() 
