from flask import Flask, render_template, request, redirect
import pandas as pd
import numpy as np
import requests 
import simplejson
import datetime
import dateutil
import io
from bokeh.charts import Line
from bokeh.embed import components
#from bokeh.models import SingleIntervalTicker, LinearAxis

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/index', methods=['POST'])
def doSomething():
  if request.form['symbol']:
	if request.method == 'POST':
		print 'Got POST request that looks like ' + request.form['symbol']
		#api_addr = 'https://www.quandl.com/data/WIKI/'
		api_addr = 'https://www.quandl.com/api/v3/datasets/WIKI/'
		file_key = request.form['symbol'] + '.csv'
		my_api_key = 'W8o1M8Y_wPyXnjs-HQPq'
		end_date = datetime.date.today()
		numMonths = -1
		if request.form['timeframe'] == 'three': numMonths = -3
		elif request.form['timeframe'] == 'twelve': numMonths = -12
		start_date = end_date + dateutil.relativedelta.relativedelta(months=numMonths)
		payload = {'api_key':my_api_key, 'start_date':start_date, 'end_date':end_date, 'column_index':'4'}
		try:
			r = requests.get(api_addr + file_key, params=payload)
			closes_df = pd.read_csv(io.StringIO(r.content.decode('utf-8'))).sort_index(by='Date')
			plot = Line(closes_df, x='Date', y='Close', title='Close v. Date for ' + request.form['symbol'], 
			plot_width=1000)#, x_axis_type=None)
# Try to figure out how to change the ticker size on the x axis someday when my internet works. 
			if numMonths==1:
				tick_size_big=1
				tick_size_small=0
				dnt = 31
			elif numMonths==3:
				tick_size_big=12
				tick_size_small=7
				dnt = 12
			elif numMonths==12:
				tick_size_big=12
				tick_size_small=4
				dnt = 12
			#plot.models.ticker.desired_num_ticks = dnt
			#ticker = SingleIntervalTicker(interval=tick_size_big, num_minor_ticks=tick_size_small)
			#xaxis = LinearAxis(ticker=ticker)
			#plot.add_layout(xaxis, 'below')

			script, div = components(plot)
			return result(request.form['symbol'], script, div)
		except: 
			return incorrect_code()
	else:
		return 'request method was a GET apparently' 

@app.route('/err')
def incorrect_code():
	return render_template('err.html')


@app.route('/result/<tickerSymbol>')
def result(tickerSymbol, bokeh_script, bokeh_div):
  return render_template('result.html', symbol=tickerSymbol, b_s_=bokeh_script, b_d_=bokeh_div)

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=33507)