import pandas as pd  # Importamos la librería pandas para el manejo de datos
import numpy as np  # Importamos la librería numpy para operaciones numéricas
import matplotlib.pyplot as plt  # Importamos la librería matplotlib para graficar
import scipy.optimize as optimize  # Importamos la función de optimización de scipy
import yfinance as yf  # Importamos la librería yfinance para obtener datos de Yahoo Finance
from datetime import datetime  # Importamos la función datetime para manejar fechas

# Definimos los activos en los que estamos interesados
Assets = ['AMZN', 'AAPL', 'BABA', 'MSFT']

# Obtenemos la fecha actual
Today = datetime.today().strftime('%Y-%m-%d')

# Creamos un DataFrame vacío para almacenar los datos de los activos
Data = pd.DataFrame()

# Descargamos los datos de cierre ajustado de los activos desde 2018-01-01 hasta la fecha actual
for x in Assets:
    Data[x] = yf.download(x, 'Date', start="2018-01-01", end=Today)['Adj Close']

# Calculamos los rendimientos logarítmicos de los datos
Log_returns = np.log(1 + Data.pct_change())

# Inicializamos listas vacías para almacenar rendimientos y volatilidades
Returns = []
Volatility = []

# Generamos 5000 carteras aleatorias y calculamos sus rendimientos y volatilidades
for _ in range(5000):
    Num_assets = len(Assets)
    Weights = np.random.random(Num_assets)
    Weights = np.round(Weights, 1)
    Weights /= np.sum(Weights)
    Returns.append(np.sum(Weights * Log_returns.mean()) * 252)
    Volatility.append(np.sqrt(np.dot(Weights.T, np.dot(Log_returns.cov(), Weights))))

# Convertimos las listas a arrays numpy
Returns = np.array(Returns)
Volatility = np.array(Volatility)

# Definimos una función para calcular estadísticas de carteras
def portfolio_stats(Weights, Log_returns):
    Returns = np.sum(Weights * Log_returns.mean()) * 252
    Volatility = np.sqrt(np.dot(Weights.T, np.dot(Log_returns.cov(), Weights)))  
    Sharpe = Returns / Volatility
    max_sr_returns = Returns
    max_sr_volatility = Volatility
    return {'return': Returns, 'volatility': Volatility, 'sharpe': Sharpe, 'max_sr_returns': max_sr_returns, 'max_sr_volatility': max_sr_volatility}

# Definimos una función para minimizar el Ratio de Sharpe
def minimize_sharpe(Weights, Log_returns):
    return -portfolio_stats(Weights, Log_returns)['sharpe']

# Inicializamos los pesos iniciales y los límites para la optimización
initializer = [1. / len(Assets)] * len(Assets)
bounds = tuple((0, 1) for _ in range(len(Assets)))

# Optimizamos los pesos para maximizar el Ratio de Sharpe
Optimal_sharpe = optimize.minimize(minimize_sharpe, initializer, method='SLSQP', args=(Log_returns,), bounds=bounds)
Optimal_sharpe_weights = Optimal_sharpe.x.round(3)

# Calculamos las estadísticas óptimas de la cartera
Optimal_stats = portfolio_stats(Optimal_sharpe_weights, Log_returns)

# Imprimimos los resultados
print("Pesos óptimos de la cartera: ", list(zip(Assets, list(Optimal_sharpe_weights*100))))
print("Retorno óptimo de la cartera: ", np.round(Optimal_stats['return']*100,3))
print("Volatilidad óptima de la cartera: ", np.round(Optimal_stats['volatility']*100,3))
print("Sharpe óptimo de la cartera: ", np.round(Optimal_stats['sharpe']*100,3))

# Graficamos la frontera de eficiencia
plt.figure(figsize=(12, 6))
plt.scatter(Volatility, Returns, c=Returns / Volatility, marker='o')
plt.scatter(Optimal_stats['max_sr_volatility'], Optimal_stats['max_sr_returns'], c='red', s=20)
plt.title('Frontera de Eficiencia')
plt.xlabel('Volatilidad')
plt.ylabel('Retorno')
plt.colorbar(label='Ratio de Sharpe')
plt.show()
