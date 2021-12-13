#!/usr/bin/python3


import pandas as pd
from pandas.core.accessor import PandasDelegate

import plotly.graph_objs as go
from plotly.offline import plot
from plotly.subplots import make_subplots


class chart():
  """docstring for chartcreator"""
  def __init__(self):

    pass

  @staticmethod
  def plotData(df, symbol:str, timeframe:str, parameters, TLSR:list):
    print("PLOT FUNCTION")
    fig = make_subplots(rows=2, cols=1, specs=[[{"secondary_y": True}],[{"secondary_y": True}]])


    color = dict(
      blue   = 'rgba(0, 0, 255, 1)',
      red    = 'rgba(255, 0, 0, 1)',
      green  = 'rgba(0, 128, 0, 1)',
      black  = 'rgba(0, 0, 0, 1)',
      aqua   = 'rgba(0, 255, 255, 1)',
      yellow = 'rgba(255, 255, 0, 1)'
      )

    colordf = pd.DataFrame(columns=['color'])

    ctr = 0
    marker_symbolList = []
    for i in range(len(TLSR)-1):

      if TLSR[i][1] == 'long':
        colordf.loc[i,'color'] = 'rgba(0, 128, 0, 1)'
        marker_symbolList.append('triangle-up')

      elif TLSR[i][1] == 'short':
        colordf.loc[i,'color'] = 'rgba(255, 0, 0, 1)'
        marker_symbolList.append('triangle-down')

      else:
        colordf.loc[i,'color'] = 'rgba(255, 255, 255, 1)'
        marker_symbolList.append('asterisk')

      print("TLSR[i][1] "+str( TLSR[i][1])+"\tcolordf: "+str(colordf.loc[i,'color']))



    colorList = colordf['color'].values.tolist()
    print(colorList)
    #print(colordf)
    #print(type(colordf))

    
    # plot candlestick chart
    
    fig.add_trace(
      go.Candlestick(
      x = df['date'],
      open = df['open'],
      close = df['close'],
      high = df['high'],
      low = df['low'],
      name = "Candlesticks"), row=1, col=1
    )

    x = []
    y = []
    for i in range(0, len(df['close'])):
      x.append(df['date'][i])
      y.append(df['10_ema'][i])

    fig.add_trace(
      go.Scatter(
        x = x,
        y = y,
        name = "EMA10",
        line=dict(color='blue', width=1),
        #mode = 'lines',
        ), 
      row=1, col=1
    )

    x = []
    y = []
    for i in range(0, len(df['close'])):
      x.append(df['date'][i])
      y.append(df['55_ema'][i])

    fig.add_trace(
      go.Scatter(
        x = x,
        y = y,
        name = "EMA55",
        line=dict(color='red', width=1),
        #mode = 'lines',
        ), 
      row=1, col=1
    )

    x = []
    y = []
    for item in TLSR:
      x.append(item[0])
      if item[1] == 'long':
        y.append(item[2])
      elif item[1] == 'sort':
        y.append(item[3])
      else:
        y.append(item[2])
    fig.add_trace(
      go.Scatter(
      x = x,
        y = y,
        name = "LONG",
        mode = "markers", 
        marker_symbol=marker_symbolList,
        marker_color=colorList,
        marker_size = 10
        ), 
      row=1, col=1
    )


    x = []
    y = []
    for i in range(0, len(df['close'])):
      x.append(df['date'][i])
      y.append(df['ADX'][i])

    fig.add_trace(
      go.Scatter(
      x = x,
        y = y,
        name = "ADX",
        mode = "markers", 
        marker_symbol="triangle-down",
        marker_color='black'
        #marker_size = 10
        ), 
      row=2, col=1
    )
    x = []
    y = []
    for i in range(0, len(df['close'])):
      x.append(df['date'][i])
      y.append(23)

    fig.add_trace(
      go.Scatter(
      x = x,
        y = y,
        name = "ADX",
        #mode = "markers", 
        #marker_symbol="triangle-down",
        marker_color='black'
        #marker_size = 10
        ), 
      row=2, col=1
    )



    x = []
    y = []
    for i in range(0, len(df['close'])):
      x.append(df['date'][i])
      y.append(df['SMIH'][i])

    fig.add_trace(
      go.Scatter(
      x = x,
        y = y,
        name = "SMIH",
        marker_color='red',
        fill='tozeroy'), 
      row=2, col=1, secondary_y=True,
    )

    """
    candle = go.Candlestick(
      x = df['time'],
      open = df['open'],
      close = df['close'],
      high = df['high'],
      low = df['low'],
      name = "Candlesticks")
    data = [candle]
   
    for item in parameters:
      if df.__contains__(item['col_name']):
        indicator = go.Scatter(
                x = df['time'],
                y = df[item['col_name']],
             name = item['name'],
             line = dict(color = (color[item['color']])))
        data.append(indicator)

    strategy = go.Scatter(
      x = [item[0] for item in TLSR],
        y = [item[2]  for item in TLSR],
        name = "TLS",
        mode = "markers", 
        marker_symbol="triangle-down",
        marker_color=colorList
        #marker_size = 10
    )
    data.append(strategy)
    """
    

    plot_title = symbol+"_"+timeframe
    #layout =
    go.Layout(
      title=plot_title,
      xaxis = {
        "title" : symbol+"_"+timeframe,
        "rangeslider" : {"visible": False},
        "type" : "date"
      },
      yaxis = {
        "fixedrange" : False,
      })
    #exit()
    #fig = go.Figure(data = data, layout = layout)
    fig.update_layout(title_text=symbol+"_"+timeframe, xaxis_rangeslider_visible=False)
    plot(fig, filename='../'+plot_title+'.html')

  @staticmethod
  def plotEachTrade(df, symbol:str, timeframe:str, param:dict = None):
    fig = go.Figure()
    # plot candlestick chart 
    fig.add_trace(
      go.Candlestick(
      x = df['date'],
      open = df['open'],
      close = df['close'],
      high = df['high'],
      low = df['low'],
      name = "Candlesticks")#, row=1, col=1
      )

    x = []
    y = []
    marker_symbol = []
    colorList = []
    for i in range(0, len(df['close'])):
      if df['trade'][i] == 'openLong':
        x.append(df['date'][i])
        y.append(df['close'][i])
        marker_symbol.append('triangle-up')
        colorList.append('green')
      elif df['trade'][i] == 'closeLong':
        x.append(df['date'][i])
        y.append(df['close'][i])
        marker_symbol.append('circle')
        colorList.append('green')
      elif df['trade'][i] == 'closeLongBySL':
        x.append(df['date'][i])
        y.append(df['low'][i])
        marker_symbol.append('x')
        colorList.append('green')
      if df['trade'][i] == 'openShort':
        x.append(df['date'][i])
        y.append(df['close'][i])
        marker_symbol.append('triangle-down')
        colorList.append('purple')
      elif df['trade'][i] == 'closeShort':
        x.append(df['date'][i])
        y.append(df['close'][i])
        marker_symbol.append('circle')
        colorList.append('red')
      elif df['trade'][i] == 'closeShortBySL':
        x.append(df['date'][i])
        y.append(df['high'][i])
        marker_symbol.append('x')
        colorList.append('red')

    filename = './BTResults/PlotBackTestDetail_'+symbol+'_'+str(timeframe)+'.resume'
      
    with open(filename, 'w') as f:
      for i in range(0, len(x)):
        f.write(str(x[i])+' '+str(y[i])+'\n')

    fig.add_trace(
      go.Scatter(
        x = x,
        y = y,
        name = "TRADES",
        mode = "markers", 
        marker_symbol = marker_symbol,
        marker_color = colorList,
        marker_size = 15
        ), #row=1, col=1
    )


    fig.add_trace(
      go.Scatter(
        x = list(df['date']) ,
        y = list(df['sslUp']) ,
        name = "SSLGreen",
        line = dict(color = 'green')
        ), #row=1, col=1
    )

    fig.add_trace(
      go.Scatter(
        x = list(df['date']) ,
        y = list(df['sslDown']) ,
        name = "SSLRed",
        line = dict(color = 'red')
        ), #row=1, col=1
    )

    fig.add_trace(
      go.Scatter(
        x = list(df['date']) ,
        y = list(df['200_ema']) ,
        name = "EMA200",
        line = dict(color = 'black')
        ), #row=1, col=1
    )





    plot_title = symbol+"_"+timeframe
    #layout =
    go.Layout(
      title=plot_title,
      xaxis = {
        "title" : symbol+"_"+timeframe,
        "rangeslider" : {"visible": False},
        "type" : "date"
      },
      yaxis = {
        "fixedrange" : False,
      })
    #exit()
    #fig = go.Figure(data = data, layout = layout)
    fig.update_layout(title_text=symbol+"_"+timeframe, xaxis_rangeslider_visible=False)
    
    plot(fig, filename='../'+plot_title+'.html')