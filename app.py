from flask import Flask, redirect, render_template, url_for, request
import requests
import simplejson as json
import numpy as np 
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components 

app = Flask(__name__)

app.vars={}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')
    
@app.route('/graph', methods=['POST'])
def graph():
    app.vars['symbol'] = request.form['symbol']
    symbol = app.vars['symbol']
    API_key='no_7haifmMMUdYQPyt_Q'
    api_url='http://www.quandl.com/api/v3/datasets/WIKI/%s.json?api_key=%s'%(symbol, API_key)

    session=requests.Session()
    session.mount('http://',requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api_url)
    if raw_data.status_code != 200 : 
        print 'Fail in getting data'

    df = pd.DataFrame(data=np.array(raw_data.json()['dataset']['data']), columns=raw_data.json()['dataset']['column_names'])

    dfdate = pd.to_datetime(df['Date'])

    p = figure(title='Stock prices for %s' % symbol ,x_axis_label='Date', x_axis_type='datetime')

    if request.form.get('Close'):
        colname='Close'
    elif request.form.get('Adj. Close'):
        colname='Adj. Close'
    elif request.form.get('Open'):
        colname='Open'
    elif request.form.get('Adj. Open'):
        colname='Adj. Open'
    else:  
        return redirect('/error')

    p.line(x=dfdate.values, y=df[colname].values, line_width=2, line_color="purple", legend=colname)
    #show(p)

    script, div = components(p)
    return render_template('graph.html', script=script, div=div)

@app.route('/error')
def error():
    return render_template('error.html', stock=app.vars['symbol'])


if __name__ == '__main__':
    app.run(port=33507)



