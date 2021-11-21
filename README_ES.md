##Sobre la función backtesting

  `
    backtesting(self, symbol:str, 
                  timeframe:str, 
                       smaL:int = 8, 
                        btd:bool = False, 
                    restart:bool = False, 
                      limit:int = 1000, 
                      param:dict = {})
  `


  El diccionario `resume` contiene todo lo relacionado con la estadística tanto general como particular del backtest. Estos datos van a ser ordenados y exportados para conformar el resumen o detalle estadístico cuando se hace un estudio de varias variables como: indicadores, pares, temporalidades, etc. 

  ```
    resume = {'symbol'         : '',
              'timeframe'      : '',
              'backTestPeriod' : '',
              'totalProfit'    : 0,

              'longN'         : 0,
              'longProfit'    : 0,
              'longMaxP'      : 0,
              'longMinP'      : 0,
              'longCloseBySL' : 0,

              'shortN'         : 0,
              'shortProfit'    : 0,
              'shortMaxP'      : 0,
              'shortMinP'      : 0,
              'shortCloseBySL' : 0}
  ```

  El dicionario dataTrade contiene datos que no van a ser exportados directamente, pero se utilizan para el el manejo interno de cada trade.

  ```
  dataTrade = {'initialBalance': 100.0,
                   'finalBalance'  : 100.0,
                   'entryPrice'    : 00.0,
                   'dateEntry'     : '',
                   'closePrice'    : 00.0,
                   'dateClose'     : '',
                   'totalTrades'   : 0,
                   'signalE':'',
                   'signalC':'',}
  ```
