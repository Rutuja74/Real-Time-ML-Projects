import pandas as pd
import yfinance as yf
from yahoofinancials import YahooFinancials
from autots import AutoTS
import warnings
warnings.filterwarnings('ignore')
import streamlit as st

st.title("Future Stock Price Prediction Model")
stk= st.text_input("Search your stock name")
print(stk)
def search_stock(a):
    try:
        a=a.upper()
        a=str(a)
        data=pd.read_excel(r'C:\Programming\Tickers_data.xlsx')
        TICKERS = pd.Series(data.Ticker.values.flatten())
        include_clique = TICKERS[TICKERS.str.startswith(a)]
        st.write('Kindly select the stock name from below mentioned list')
        st.dataframe(include_clique)
        
    except ValueError:
         st.write('I am glad you are here')
         
search_stock(stk)
        
user = st.text_input("Let's Predict the Future Prices")
print(user)
user=str(user)



def get_stock_name(user):
    #user=input('Enter the stock name').upper()
    try:
        df=yf.download(user)
        ticker = yf.Ticker(user)
        final_df = ticker.history(period="1y").reset_index()
        print('Please Wait we are searching the results')
        model_list = [
        'GLS',
        'UnobservedComponents',
        'SeasonalNaive',
        'DatepartRegression',
        'MetricMotif',
        'SeasonalityMotif',
        'ETS',
        'AverageValueNaive',
        'ARIMA'
        ]
        metric_weighting = {
        'smape_weighting': 5,
        'mae_weighting': 2,
        'rmse_weighting': 2,
        'made_weighting': 0.5,
        'mage_weighting': 1,
        'mle_weighting': 0,
        'imle_weighting': 0,
        'spl_weighting': 3,
        'containment_weighting': 0,
        'contour_weighting': 1,
        'runtime_weighting': 0.05,
        }
        model = AutoTS(
        forecast_length=10,
        frequency='D',
        prediction_interval=0.95,
        ensemble=None,
        models_mode='deep',
        model_list = model_list,# or ['ARIMA','ETS']
        max_generations=1,
        num_validations=3,
        no_negatives=True,
        n_jobs='auto',
        validation_method="backwards",
        metric_weighting=metric_weighting)
        model = model.fit(final_df, date_col='Date', value_col='Close', id_col=None)
        prediction = model.predict()
        forecast = prediction.forecast
        st.write(forecast)
        # accuracy of all tried model results
        model_results = model.results()
        print(model.results)
        #and aggregated from cross validation
        validation_results = model.results("validation")
        
    except ValueError:
        st.write("Please give a stock name for price prediction")
        


get_stock_name(user)
