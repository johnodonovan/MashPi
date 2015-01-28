import plotly.plotly as py
# (*) Useful Python/Plotly tools
import plotly.tools as tls   
 
# (*) Graph objects to piece together plots
from plotly.graph_objs import *
 
import numpy as np  # (*) numpy for math functions and arrays
#import readadc
import os
import glob
import time
from plotly.graph_objs import *
#import readadc # helper functions to read ADC from the Raspberry Pi



#sign in.  could be done with a credentials file too

username = 'johnodonovan'
api_key = 'lqmjc5tvy1'
stream_token1 = 'wtiitelka1'
stream_token2 = 'odygjrmtdy';
stream_token3 = 'dltfgsfgti';

py.sign_in(username, api_key)




#load system drivers
os.system('modprobe w1-gpio')

os.system('modprobe w1-therm')

temp_sensor1 = '/sys/bus/w1/devices/28-0000065cc2d0/w1_slave'
temp_sensor2 = '/sys/bus/w1/devices/28-0000065cd208/w1_slave'



#default Mash temperature 152. @todo Read this in (in F) with -t param.
target_temp = 152


def temp_raw():

    f1 = open(temp_sensor1, 'r')
    f2 = open(temp_sensor2, 'r')
    lines1 = f1.readlines()
    lines2 = f2.readlines()

    f1.close()
    f2.close()

    Lines = [lines1, lines2]

    return Lines


def read_temp1():
    Lines = temp_raw()
    lines = Lines[0]
    while lines[0].strip()[-3:] != 'YES':

        time.sleep(0.2)

        lines = temp_raw()
    temp_output = lines[1].find('t=')

    if temp_output != -1:

        temp_string = lines[1].strip()[temp_output+2:]

        temp_c = float(temp_string) / 1000.0

        temp_f = temp_c * 9.0 / 5.0 + 32.0

        #return temp_c, temp_f
        return temp_f





def read_temp2():
    Lines = temp_raw()
    lines = Lines[1]
    while lines[0].strip()[-3:] != 'YES':

        time.sleep(0.2)

        lines = temp_raw()


    temp_output = lines[1].find('t=')

    if temp_output != -1:

        temp_string = lines[1].strip()[temp_output+2:]

        temp_c = float(temp_string) / 1000.0

        temp_f = temp_c * 9.0 / 5.0 + 32.0

        #return temp_c, temp_f
        return temp_f

# Get stream id from stream id list 
#stream_id = stream_ids[0]

# Make instance of stream id object 
stream = Stream(
    token=stream_token1,  # (!) link stream id to 'token' key
    maxpoints=80000      # (!) keep a max of 80 pts on screen
)

# Make instance of stream id object 
stream2 = Stream(
    token=stream_token2,  # (!) link stream id to 'token' key
    maxpoints=80000      # (!) keep a max of 80 pts on screen
)

stream3 = Stream(
    token=stream_token3,  # (!) link stream id to 'token' key
    maxpoints=80000      # (!) keep a max of 80 pts on screen
)
# Initialize trace of streaming plot by embedding the unique stream_id
trace1 = Scatter(
    x=[],
    y=[],
    mode='histogram',
    stream=dict(stream), 
    name='Hot Liquor Tank'        # (!) embed stream id, 1 per trace
)

trace2 = Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    stream=dict(stream2), 
    name='Mash Tun'        # (!) embed stream id, 1 per trace
)

trace3 = Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    stream=dict(stream3),         # (!) embed stream id, 1 per trace
    name='Target Temp'
)

data = Data([trace1,trace2,trace3])

# Add title and other details to layout object

layout = Layout(
    showlegend=True,
    title='HLT, Mash and Target Temperatures :: ShamrockBrew',
    xaxis=XAxis(
        title='Time (Pacific Standard Time)',
        titlefont=Font(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=YAxis(
        title='Temperature in Degrees Fahrenheit',
        titlefont=Font(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)

# Make a figure object
fig = Figure(data=data, layout=layout)

# (@) Send fig to Plotly, initialize streaming plot, open new tab
unique_url = py.plot(fig, filename='BrewControl')

print unique_url


# (@) Make instance of the Stream link object, 
#     with same stream id as Stream id object
s = py.Stream(stream_token1)
s2 = py.Stream(stream_token2)
s3 = py.Stream(stream_token3)
# (@) Open the stream
s.open()
s2.open()
s3.open()
# (*) Import module keep track and format current time
import datetime
from datetime import timedelta  #for computing your timezone
import time   
 
i = 0    # a counter
k = 5    # some shape parameter
N = 200  # number of points to be plotted

# Delay start of stream by 5 sec (time to switch tabs)
time.sleep(5) 



while i<N:
    i += 1   # add to counter
    
    # Compute offset for Pacific Time (PST)
    d1 = datetime.datetime.now()
    d = timedelta(hours = 16)
    d2 = d1+d
    x=d2.strftime('%Y-%m-%d %H:%M:%S.%f')

    
    
    
    # (-) Both x and y are numbers (i.e. not lists nor arrays)
    
    # (@) write to Plotly stream!
    s.write(dict(x=x,y=read_temp1()))  
    s2.write(dict(x=x,y=read_temp2()))
    s3.write(dict(x=x,y=target_temp))
    #
    #(!) Write numbers to stream to append current data on plot,
    #     write lists to overwrite existing data on plot (more in 7.2).
            
    time.sleep(0.08)  # (!) plot a point every 80 ms, for smoother plotting
    
# (@) Close the stream when done plotting
s.close() 
s2.close()
s3.close()


        



