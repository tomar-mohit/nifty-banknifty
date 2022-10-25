import calendar
# from calendar import THURSDAY, calendar
from datetime import datetime, timedelta


class NBNDetails:
    '''Nifty BankNify Strategy Class'''
    today = datetime.today()
    next_weekly_expiry: datetime
    next_monthly_expiry: datetime

    def __init__(self):
        self.next_weekly_expiry = self.today + \
            timedelta((calendar.THURSDAY -self.today.weekday()) % 7)
        next_shift_date = (self.today.replace(day=1) + timedelta(days=32)).replace(day=1)
        # reduce 1 day in case 1st of next month is thursday
        next_shift_date = next_shift_date + timedelta(days=-1)
        while (next_shift_date.weekday() is not calendar.THURSDAY and next_shift_date > self.today):
            next_shift_date = next_shift_date + timedelta(days=-1)
            # print (next_shift_date)
        self.next_monthly_expiry = next_shift_date
        # if today is more than last thursday
        if next_shift_date <= self.today:
            next_shift_date = (self.today.replace(day=1) + timedelta(days=64)).replace(day=1)
            next_shift_date = next_shift_date + timedelta(days=-1)
            while (next_shift_date.weekday() is not calendar.THURSDAY and next_shift_date > self.today):
                next_shift_date = next_shift_date + timedelta(days=-1)
                # print (next_shift_date)
            self.next_monthly_expiry = next_shift_date



    def get_expiry(self):
        return {
            'week': self.next_weekly_expiry,
            'month': self.next_monthly_expiry
        }

    # ohlc from nifty class
    def get_pivot(self, ohlc):
        """Retuns the pivot of nifty

        Args:
            ohlc (objct): OHLC data

        Returns:
            object: different pivots
        """
        # ToDo: parallel
        classic = self.get_pivotdetails('classic', ohlc)
        woodie = self.get_pivotdetails('woodie', ohlc)
        camarilla = self.get_pivotdetails('camarilla', ohlc)
        demark = self.get_pivotdetails('demark', ohlc)
        fibonacci = self.get_pivotdetails('fibonacci', ohlc)
        return {
            'classic': classic,
            'woodie': woodie,
            'camarilla': camarilla,
            'demark': demark,
            'fibonacci': fibonacci,
        }

    def get_pivotdetails(self, type, ohlc):
        """
        It takes a type of pivot point calculation and a dictionary of open, high, low, and close values
        and returns a dictionary of support and resistance values
        
        :param type: classic, woodie, camarilla, demark, fibonacci
        :param ohlc: This is a dictionary of the open, high, low, and close values
        :return: A dictionary with the keys support1, support2, support3, resistance1, resistance2,
        resistance3.
        """
        open = ohlc['o']
        high = ohlc['h']
        low = ohlc['l']
        close = ohlc['c']
        pivot = support1 = support2 = support3 = resistance1 = resistance2 = resistance3 = -1
        if type == 'classic':
            pivot = (high + low + close)/3
            support1 = pivot * 2 - high
            support2 = pivot - (high - low)
            support3 = low - 2*(high - pivot)
            resistance1 = pivot * 2 - low
            resistance2 = pivot + (high - low)
            resistance3 = high + 2*(pivot - low)
            return {
                'support1': round(support1, 2),
                'support2': round(support2, 2),
                'support3': round(support3, 2),
                'resistance1': round(resistance1, 2),
                'resistance2': round(resistance2, 2),
                'resistance3': round(resistance3, 2)
            }
        if type == 'woodie':
            pivot = (high + low + (close * 2)) / 4
            resistance2 = pivot + (high - low)
            resistance1 = (2 * pivot) - low
            support1 = (2 * pivot) - high
            support2 = pivot - (high - low)
            return {
                'support1': round(support1, 2),
                'support2': round(support2, 2),
                'resistance1': round(resistance1, 2),
                'resistance2': round(resistance2, 2),
            }
        if type == 'camarilla':
            resistance3 = ((high - low) * 1.1) / 4 + close
            resistance2 = ((high - low) * 1.1) / 6 + close
            resistance1 = ((high - low) * 1.1) / 12 + close
            support1 = close - ((high - low) * 1.1) / 12
            support2 = close - ((high - low) * 1.1) / 6
            support3 = close - ((high - low) * 1.1) / 4
            return {
                'support1': round(support1, 2),
                'support2': round(support2, 2),
                'support3': round(support3, 2),
                'resistance1': round(resistance1, 2),
                'resistance2': round(resistance2, 2),
                'resistance3': round(resistance3, 2)
            }
        if type == 'demark':
            de_mid = 0
            if close < open:
                de_mid = high + (2 * low) + close
            if close > open:
                de_mid = (2 * high) + low + close
            if close == open:
                de_mid = high + low + (2 * close)
            support1 = de_mid/2 - high
            resistance1 = de_mid/2 - low
            return {
                'support1': round(support1, 2),
                'resistance1': round(resistance1, 2),
            }
        if type == 'fibonacci':
            pivot = (high + low + close)/3
            support1 = pivot - (0.382 * (high - low))
            support2 = pivot - (0.6182 * (high - low))
            support3 = pivot - (1 * (high - low))
            resistance1 = pivot + (0.382 * (high - low))
            resistance2 = pivot + (0.6182 * (high - low))
            resistance3 = pivot + (1 * (high - low))
            return {
                'support1': round(support1, 2),
                'support2': round(support2, 2),
                'support3': round(support3, 2),
                'resistance1': round(resistance1, 2),
                'resistance2': round(resistance2, 2),
                'resistance3': round(resistance3, 2)
            }
