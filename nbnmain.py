from datetime import datetime
from heapq import nsmallest
import json
import pathlib
import re
import sys
import os
from jugaad_data.nse import NSELive
import nbndetails


class NiftyBankNifty:
    '''Main Nifty BankNify Class'''

    __nbn_message = None
    __jsonout_path = None
    __nbndetails__ = nbndetails.NBNDetails()

    indent_setting = 2
    '''indent setting for json output file'''

    output_format = 'std'

    def __init__(self):
        path = self.__get_data_file_path__('assets/data.json')
        with open(path, 'r', encoding='utf8') as file:
            data = json.load(file)
            self.__nbn_message = data['messages']


    def main(self):
        """
        Main() is a function that takes in a user input and calls other functions based on the user
        input
        """
        user_choice = input('''select option:
            1. Get nifty status and last data
            2. Get all market status and data
            3. Option chain
            4. all indices
            5. derivative turnover
            6. livedata
            7. live fno data
            8. market turnover
            9. top 5 call and put
            ''')
        if user_choice == '1':
            self.current_status()
        elif user_choice == '2':
            self.main_market_data()
        elif user_choice == '3':
            self.opt_chain()
        elif user_choice == '4':
            self.all_indices()
        elif user_choice == '5':
            self.derivate_turnover()
        elif user_choice == '6':
            self.live_index()
        elif user_choice == '7':
            self.live_fno()
        elif user_choice == '8':
            self.market_turnover()
        elif user_choice == '9':
            print('not yet implemented. work in progress')
        else:
            print('select valid option')
        input('done')


    def current_status(self):
        """
        It takes the current market status from the NSE website and writes it to a json file
        """
        nse = NSELive()
        state = nse.market_status()['marketState']
        nifty = next((item for item in state if item['market'] == 'Capital Market'), None)
        self.get_jsonfile_path()
        self.output_data(nifty)
        return nifty

    def main_market_data(self):
        """
        It checks the market status and writes the output to a json file.
        """
        nse = NSELive()
        state = nse.market_status()['marketState']
        self.get_jsonfile_path()
        self.output_data(state)
        return state


    def opt_chain(self, limit=-1):
        """
        It takes the data from the NSE website, filters it and outputs the data in a JSON format
        :param limit: The number of strike prices to be displayed
        """
        nse = NSELive()
        state = nse.index_option_chain()
        self.get_jsonfile_path()
        data = None
        if limit == -1:
            # print(json.dumps(state, indent=indent_setting))
            data = state
            self.output_data(state)
        elif 1 <= limit <= 100:
            # get the value
            records = state["records"]
            underlying_value = records["underlyingValue"]
            all_expiry = records["expiryDates"]
            latest_expiry = all_expiry[0]
            latest_date = datetime.strptime(latest_expiry, '%d-%b-%Y')
            latest_month_expiry = latest_expiry
            month_expiry = [x for x in all_expiry if (datetime.strptime(x, '%d-%b-%Y').year == latest_date.year and datetime.strptime(x, '%d-%b-%Y').month == latest_date.month and datetime.strptime(x, '%d-%b-%Y').date != latest_date.date)]
            if (month_expiry is not None and len(month_expiry) != 0):
                latest_month_expiry = month_expiry[len(month_expiry) - 1]

            # find nearest (n - 1) list of expiry
            all_strikeprice = records["strikePrices"]
            all_nearby_strikes = nsmallest(2*limit, all_strikeprice, key=lambda x: abs(x - underlying_value))

            filtered = state["filtered"]["data"]
            nearby_data = [item for item in filtered if item["strikePrice"] in all_nearby_strikes]
            all_data = records["data"]
            filtered_month_data = [item for item in all_data if item["strikePrice"] in all_nearby_strikes and item["expiryDate"] == latest_month_expiry]
            filtered_all_data = nearby_data + filtered_month_data
            self.output_data(filtered_all_data)
            data = filtered_all_data
        else:
            print('invalid value for limit')
        return data


    def all_indices(self, index=None):
        """
        It takes the data from the API and writes it to a JSON file
        :param index: The index name
        """
        nse = NSELive()
        state = nse.all_indices()
        self.get_jsonfile_path()
        data = None
        if index != 'Nifty':
            self.output_data(state)
            data = state
        else:
            data = state["data"]
            nifty = next((item for item in data if item["index"] == "NIFTY 50"), None)
            if nifty is not None:
                self.output_data(nifty)
                data = nifty
            else:
                print('none')
        return data


    def derivate_turnover(self):
        """
        It takes the data from the NSE website and stores it in a json file
        """
        nse = NSELive()
        self.get_jsonfile_path()
        state = nse.eq_derivative_turnover()
        self.output_data(state)
        return state


    def live_index(self):
        """
        It takes the data from the live_index() function in the NSELive class and writes it to a json
        file
        """
        nse = NSELive()
        self.get_jsonfile_path()
        state = nse.live_index()
        self.output_data(state)
        return state


    def live_fno(self):
        """
        It takes the data from the nse website and stores it in a json file
        """
        nse = NSELive()
        state = nse.live_fno()
        self.get_jsonfile_path()
        self.output_data(state)
        return state


    def market_turnover(self):
        """
        It takes the data from the nse.market_turnover() function and writes it to a json file
        """
        nse = NSELive()
        state = nse.market_turnover()
        self.get_jsonfile_path()
        self.output_data(state)
        return state

    def get_ohlc(self):
        """retuns the OHLC of Nifty

        Returns:
            object: ohlc value
        """        
        # status = self.current_status()
        # if (status is not None):
        #     print (1)
        # Todo: Get from other API
        # ToDo: Regex escape in JSON from "Dr Reddy's Lab"
        idx = self.live_index()
        if idx is not None:
            # ToDo: check with Data without 0 why next of list expansion is not working
            nifty = idx['data'][0]
            # data = idx['data'][0]
            # if (data is not None):
            if nifty is not None:
                # nifty = [n for n in data if data['symbol'][0] == 'NIFTY 50']
                # nifty = next((item for item in data if data["symbol"] == "NIFTY 50"), None)
                # if (nifty is not None):
                # print (nifty)
                # print (nifty)
                ohlc = {
                    'o': nifty['open'],
                    'h': nifty['dayHigh'],
                    'l': nifty['dayLow'],
                    'c': nifty['lastPrice']
                }
                self.output_data(ohlc)
                return ohlc
            else:
                return None
        else:
            return None


    def big_main(self):
        """
        It takes a command line argument and calls a function based on the argument
        :return: The return value is a list of dictionaries.
        """
        local_args = sys.argv

        if len(local_args) < 2:
            print(self.__nbn_message['GenericStartMessage'])
            input()
            return

        first_arg = local_args[1]
        second_arg = None
        if len(local_args) >= 3:
            second_arg = local_args[2]

        if second_arg == '-json':
            self.output_format = 'json'

        if first_arg in ('h', '-h', '--h'):
            print(self.__nbn_message['usage'])
        elif first_arg == '--help':
            print(self.__nbn_message['detailedUsage'])
        elif first_arg == '-getNiftyOverview':
            self.current_status()
        elif first_arg == '-getMarketOverview':
            self.main_market_data()
        elif first_arg == '-optionChain':
            if (second_arg is None or second_arg == '-json'):
                self.opt_chain()
            elif second_arg.startswith("--limit="):  # and re.match("--limit=\d+") is not None):
                match = re.match("--limit=(\d+)", second_arg)
                if (match is not None and match.groups() is not None):
                    limit = match.groups()[0]
                    if len(local_args) >= 4:
                        if local_args[3] == '-json':
                            self.output_format = 'json'
                    self.opt_chain(limit=int(limit))
        elif first_arg == '-nifyDetails':
            self.all_indices('Nifty')
        elif first_arg == '-allIndices':
            self.all_indices()
        elif first_arg == '-derivativeTurnover':
            self.derivate_turnover()
        elif first_arg == '-liveData':
            self.live_index()
        elif first_arg == '-liveFnOData':
            self.live_fno()
        elif first_arg == '-marketTurnover':
            self.market_turnover()
        elif first_arg == '-topFnO':
            if (len(local_args) >= 3 and local_args[2] == '-json'):
                self.output_format = 'json'
            self.opt_chain(5)
        elif first_arg == '-supportAndResistence':
            if (len(local_args) >= 3 and local_args[2] == '-json'):
                self.output_format = 'json'
            self.get_pivot()
        else:
            print('invalid option')


    def get_jsonfile_path(self):
        """
        It returns the path of the json file to be created
        :return: The path to the json file.
        """
        method_name = sys._getframe(1).f_code.co_name
        cwd = os.getcwd()
        current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        path = os.path.join(cwd, 'output', method_name, current_time + '.json')
        self.__jsonout_path = path
        return path

    def output_data(self, message):
        """
        If the output_format is 'std', print the message. If the output_format is 'json', create a
        directory if it doesn't exist, and write the message to a file.
        :param message: The message to be outputted
        """
        if self.output_format == 'std':
            print(message)
        elif self.output_format == 'json':
            pathlib.Path(os.path.dirname(self.__jsonout_path)).mkdir(parents=True, exist_ok=True)
            with open(self.__jsonout_path, "w", encoding='utf8') as file1:
                # Writing data to a file
                file1.write(json.dumps(message, indent=self.indent_setting))

    def __get_data_file_path__(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def get_pivot(self):
        """Returns the pivot point

        Returns:
            object: pivots
        """        
        ohlc = self.get_ohlc()
        pivots = self.__nbndetails__.get_pivot(ohlc)
        self.output_data(pivots)
        return pivots
