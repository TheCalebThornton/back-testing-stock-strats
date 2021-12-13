from fastquant import get_crypto_data, backtest
import pandas as pd
from prophet import Prophet
from matplotlib import pyplot as plt

def stan_init(m):
    """Retrieve parameters from a trained model.

    Retrieve parameters from a trained model in the format
    used to initialize a new Stan model.

    Parameters
    ----------
    m: A trained model of the Prophet class.

    Returns
    -------
    A Dictionary containing retrieved parameters of m.

    """
    res = {}
    for pname in ['k', 'm', 'sigma_obs']:
        res[pname] = m.params[pname][0][0]
    for pname in ['delta', 'beta']:
        res[pname] = m.params[pname][0]
    return res

def train_and_predict_next_day (trainSet, currentModel):
    ts = trainSet.reset_index()[["dt", "close"]]
    ts.columns = ['ds', 'y']
    m = None
    try:
        # Try to warm-load with existing model
        m = Prophet(daily_seasonality=True, yearly_seasonality=True).fit(ts, init=stan_init(currentModel))
    except:
        m = Prophet(daily_seasonality=True, yearly_seasonality=True).fit(ts)
    # this is asking prophet to predict 1(period) Day(frequency) into the future
    forecast = m.make_future_dataframe(periods=1, freq='D', include_history=False)
    return m.predict(forecast)

# Facebook's Prophet AI predictor
def prophet (dataSet, initCash=10000, plot=False, verbose=False, graph=False):
    # re-train everyday and predict next day
    dailyTrainSet = dataSet.copy().reset_index()
    daily_yhats = []
    dailyPredModel = None
    for index, row in dailyTrainSet.iterrows():
        # need to have at least 2 entries of data
        if (index > 1):
            trainSet = dailyTrainSet.iloc[:index]
            dailyPredModel = train_and_predict_next_day(trainSet, dailyPredModel)
            daily_yhats.append(dailyPredModel.yhat)
        else:
            daily_yhats.append(row.close)
    # yhat_series = pd.Series(daily_yhats).pct_change().multiply(100)
    yhat_series = pd.Series(daily_yhats)
    dailyTrainSet["custom"] = yhat_series.tolist()
    print(f'yhat_series {dailyPredModel}')
    print(f'yhat_series {yhat_series}')
    print(f'dailyTrainSet {dailyTrainSet}')
    # Convert predictions to expected 1 day return

    # Upper and lower values here describe the forecasted percentage gain or loss
    # given .25 / -.1, the algo will buy when projected gain is >= .25 and sell when <= -.1
    # TODO oddly, complaning that there is no custom column....
    # return backtest("custom",
    #                 dailyTrainSet.dropna(),
    #                 init_cash=initCash,
    #                 upper_limit=[.25, .75, .5, 2],
    #                 lower_limit=[-.1, -.2, -.5, 2],
    #                 plot=plot,
    #                 verbose=verbose)

# Generate prediction and output the result
def get_predictions (dataSet, include_hist=True):
    # Fit model on closing prices
    ts = dataSet.reset_index()[["dt", "close"]]
    ts.columns = ['ds', 'y']
    print(f'TIME SERIES: {ts}')
    m = Prophet(daily_seasonality=False, weekly_seasonality=True, yearly_seasonality=True).fit(ts)
    # this is asking prophet to predict 1(period) Day(frequency) into the future
    future = m.make_future_dataframe(periods=1, freq='D')
    print(f'FUTURE: {future}')
    pred = m.predict(future)
    out = pred[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()


    print(f'CLOSE PRICE PREDICITIONS:')
    print(f'{out}')

    return out

# Output signal for tomorrow's open.
def give_me_next_signal (dataSet, optimal_upper, optimal_lower):
    pred = get_predictions(dataSet)
    # TODO there is absolutely a cleaner way to do this
    expected_1day_return = pred.set_index("ds").yhat.pct_change().shift(-1).multiply(100)
    next_day_return = expected_1day_return[-2]

    if (next_day_return >= optimal_upper):
        print(f'BUY')
    elif (next_day_return <= optimal_lower):
        print(f'SELL')
    else:
        print('HOLD position')
    print(f'Predicted Change: {next_day_return}')


    print(f'full set: {expected_1day_return}')
