import pandas as pd
import requests
import os
import io
import time
from datetime import datetime

from fmp_python.common.constants import BASE_URL, INDEX_PREFIX
from fmp_python.common.requestbuilder import RequestBuilder
from fmp_python.common.fmpdecorator import FMPDecorator
from fmp_python.common.fmpvalidator import FMPValidator
from fmp_python.common.fmpexception import FMPException

   
"""
Base class that implements api calls 
"""

class FMP(object):

    def __init__(self, api_key=None, output_format='json', write_to_file=False):
        self.api_key = api_key or os.getenv('FMP_API_KEY')
        self.output_format = output_format
        self.write_to_file = write_to_file
        self.current_day = datetime.today().strftime('%Y-%m-%d')

    @FMPDecorator.write_to_file
    @FMPDecorator.format_data
    def get_quote_short(self, symbol):
        rb = RequestBuilder(self.api_key)
        rb.set_category('quote-short')
        rb.add_sub_category(symbol)
        quote = self.__do_request__(rb.compile_request())
        return quote
    
    @FMPDecorator.write_to_file
    @FMPDecorator.format_data
    def get_quote(self,symbol):
        rb = RequestBuilder(self.api_key)
        rb.set_category('quote')
        rb.add_sub_category(symbol)
        quote = self.__do_request__(rb.compile_request())
        return quote

    def get_index_quote(self,symbol):
        return FMP.get_quote(self,str(INDEX_PREFIX)+symbol)
    
    @FMPDecorator.write_to_file
    @FMPDecorator.format_data
    def get_historical_chart(self, interval, symbol):
        if FMPValidator.is_valid_interval(interval):
            rb = RequestBuilder(self.api_key)
            rb.set_category('historical-chart')
            rb.add_sub_category(interval)
            rb.add_sub_category(symbol)
            hc = self.__do_request__(rb.compile_request())
            return hc
        else:
            raise FMPException('Interval value is not valid',FMP.get_historical_chart.__name__)

    def get_historical_chart_index(self,interval,symbol):
        return FMP.get_historical_chart(self, interval, str(INDEX_PREFIX)+symbol)

    @FMPDecorator.write_to_file
    @FMPDecorator.format_historical_data
    def get_historical_price(self,symbol):
        rb = RequestBuilder(self.api_key)
        rb.set_category('historical-price-full')
        rb.add_sub_category(symbol)
        hp = self.__do_request__(rb.compile_request())
        return hp

    @FMPDecorator.write_to_file
    @FMPDecorator.format_data
    def get_key_metrics(self, symbol: str, period: str=None, limit: int=None):
        rb = RequestBuilder(self.api_key)
        rb.set_category('key-metrics')
        rb.add_sub_category(symbol)
        if (period):
            rb.add_query_param({'period': period})
        if (limit):
            rb.add_query_param({'limit': limit})
        hp = self.__do_request__(rb.compile_request())
        return hp

    @FMPDecorator.write_to_file
    @FMPDecorator.format_data
    def get_financial_growth(self, symbol: str, period: str=None, limit: int=None):
        rb = RequestBuilder(self.api_key)
        rb.set_category('financial-growth')
        rb.add_sub_category(symbol)
        if (period):
            rb.add_query_param({'period': period})
        if (limit):
            rb.add_query_param({'limit': limit})
        hp = self.__do_request__(rb.compile_request())
        return hp

    @FMPDecorator.write_to_file
    @FMPDecorator.format_data
    def get_enterprise_values(self, symbol: str, period: str=None, limit: int=None):
        rb = RequestBuilder(self.api_key)
        rb.set_category('enterprise-values')
        rb.add_sub_category(symbol)
        if (period):
            rb.add_query_param({'period': period})
        if (limit):
            rb.add_query_param({'limit': limit})
        hp = self.__do_request__(rb.compile_request())
        return hp

    @FMPDecorator.write_to_file
    @FMPDecorator.format_data
    def get_rating(self, symbol: str, period: str=None, limit: int=None):
        rb = RequestBuilder(self.api_key)
        rb.set_category('rating')
        rb.add_sub_category(symbol)
        if (limit):
            rb.add_query_param({'limit': limit})
        hp = self.__do_request__(rb.compile_request())
        return hp

    @FMPDecorator.write_to_file
    @FMPDecorator.format_data
    def get_historical_rating(self, symbol: str, period: str=None, limit: int=None):
        rb = RequestBuilder(self.api_key)
        rb.set_category('historical-rating')
        rb.add_sub_category(symbol)
        if (limit):
            rb.add_query_param({'limit': limit})
        hp = self.__do_request__(rb.compile_request())
        return hp

    @FMPDecorator.write_to_file
    @FMPDecorator.format_data
    def get_financial_statement_symbol_lists(self):
        rb = RequestBuilder(self.api_key)
        rb.set_category('financial-statement-symbol-lists')
        hp = self.__do_request__(rb.compile_request())
        return hp

    @FMPDecorator.write_to_file
    @FMPDecorator.format_data
    def get_sp500_constituent(self):
        rb = RequestBuilder(self.api_key)
        rb.set_category('sp500_constituent')
        hp = self.__do_request__(rb.compile_request())
        return hp

    @FMPDecorator.write_to_file
    @FMPDecorator.format_data
    def get_income_statement(self, symbol: str, period: str=None, limit: int=None):
        rb = RequestBuilder(self.api_key)
        rb.set_category('income-statement')
        rb.add_sub_category(symbol)
        if (period):
            rb.add_query_param({'period': period})
        if (limit):
            rb.add_query_param({'limit': limit})
        hp = self.__do_request__(rb.compile_request())
        return hp

    @FMPDecorator.write_to_file
    @FMPDecorator.format_data
    def get_historical_earning_calendar(self, symbol: str, limit: int=None):
        rb = RequestBuilder(self.api_key)
        rb.set_category('historical/earning_calendar')
        rb.add_sub_category(symbol)
        if (limit):
            rb.add_query_param({'limit': limit})
        hp = self.__do_request__(rb.compile_request())
        return hp

    @FMPDecorator.write_to_file
    @FMPDecorator.format_data
    def get_earning_call_transcript(self, symbol: str, quarter: str=None, year: str=None):
        rb = RequestBuilder(self.api_key, api_version=4)
        rb.set_category('earning_call_transcript')
        rb.add_query_param({'symbol': symbol})
        if (quarter):
            rb.add_query_param({'quarter': quarter})
        if (year):
            rb.add_query_param({'year': year})
        hp = self.__do_request__(rb.compile_request())
        return hp

    @FMPDecorator.write_to_file
    @FMPDecorator.format_historical_data
    def get_historical_price_full(self, symbol: str, from_date: str=None, to_date: str=None):
        rb = RequestBuilder(self.api_key)
        rb.set_category('historical-price-full')
        rb.add_sub_category(symbol)
        if (from_date):
            rb.add_query_param({'from': from_date})
        if (to_date):
            rb.add_query_param({'to': to_date})
        hp = self.__do_request__(rb.compile_request())
        return hp

    @FMPDecorator.write_to_file
    @FMPDecorator.format_data
    def get_analyst_estimates(self, symbol: str, period: str=None, limit: int=None):
        rb = RequestBuilder(self.api_key)
        rb.set_category('analyst-estimates')
        rb.add_sub_category(symbol)
        if (period):
            rb.add_query_param({'period': period})
        if (limit):
            rb.add_query_param({'limit': limit})
        hp = self.__do_request__(rb.compile_request())
        return hp

    @FMPDecorator.write_to_file
    def get_analyst_estimates_for_next_earnings_call(self, symbol: str):
        original_output_format = self.output_format
        self.output_format = 'pandas'
        analyst_estimate = pd.DataFrame()
        analyst_estimates = self.get_analyst_estimates(symbol, period='quarter', limit=15)
        if (analyst_estimates.shape[0] > 1):
            analyst_estimates['date'] = pd.to_datetime(analyst_estimates['date'])
            analyst_estimates = analyst_estimates[analyst_estimates['date'] >= pd.to_datetime(datetime.now().date())]
            analyst_estimates.sort_values(['date'], ascending=True, inplace=True)
            analyst_estimate = analyst_estimates.head(1)
        self.output_format = original_output_format
        if (original_output_format == 'json'):
            return analyst_estimate.to_json()
        elif (original_output_format == 'pandas'):
            return analyst_estimate

    def __do_request__(self, url, retry: bool=True):
        response = requests.get(url)
        if not (response.ok) or not (response.json):
            if (retry):
                time.sleep(30)
                response = self.__do_request__(url, retry=False)
            else:
                raise FMPException(f'url: {url} returned {response.status_code}', FMP.__do_request__.__name__)
        return response 
