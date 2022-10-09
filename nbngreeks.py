import math
import sys
from cmath import inf
import numpy
from scipy.stats import norm


class NBNGreeks:
    '''Main class to calculate greeks of nifty/banknifty'''

    def d_to_use(self, spot: float, strike: float, time: float, roi: float, sigma: float):
        """returns the d1 to be used in calculation of greeks

        Args:
            spot (float): Spot Price
            strike (float): Target/Strike Price
            time (float): Time to expire in years
            roi (float): rate of interest
            sigma (float): implied volatility

        Returns:
            float: returns the d1
        """
        div = 0
        d1 = (math.log(spot/strike) + ((roi-div) + math.pow(sigma, 2)/2)*time)/(sigma*math.sqrt(time))
        return d1

    def d2_to_use(self, spot: float, strike: float, time: float, roi: float, sigma: float):
        """returns the d2 to be used in calculation of greeks

        Args:
            spot (float): Spot Price
            strike (float): Target/Strike Price
            time (float): Time to expire in years
            roi (float): rate of interest
            sigma (float): implied volatility

        Returns:
            float: returns the d1
        """
        div = 0
        d2 = (math.log(spot/strike) + ((roi-div) - math.pow(sigma, 2)/2)*time)/(sigma*math.sqrt(time))
        return d2

    def call_delta(self, spot: float, strike: float, time: float, roi: float, sigma: float):
        """returns the delta of call

        Args:
            spot (float): Spot Price
            strike (float): Target/Strike Price
            time (float): Time to expire in years
            roi (float): rate of interest
            sigma (float): implied volatility

        Returns:
            float: call delta
        """
        div = 0
        p = (math.log(spot/strike) + ((roi-div) + math.pow(sigma, 2)/2)*time)/(sigma*math.sqrt(time))
        delta = norm.cdf(p)
        return round(delta, 2)

    def put_delta(self, spot: float, strike: float, time: float, roi: float, sigma: float):
        """returns the delta of put

        Args:
            spot (float): Spot Price
            strike (float): Target/Strike Price
            time (float): Time to expire in years
            roi (float): rate of interest
            sigma (float): implied volatility

        Returns:
            float: call delta
        """
        p = self.call_delta(spot, strike, time, roi, sigma)
        delta = p - 1
        return round(delta, 2)

    def call_theta(self, spot: float, strike: float, time: float, roi: float, sigma: float):
        """Return the theta of a call option

        Args:
            spot (float): Spot Price
            strike (float): Target/Strike Price
            time (float): Time to expire in years
            roi (float): rate of interest
            sigma (float): implied volatility

        Returns:
            float: theta of the call
        """
        theta = (-1 * ((spot * ((1 / math.sqrt(2 * math.pi)) * math.exp(((-1) * (sys.float_info.max
                 if numpy.float_power(self.d_to_use(spot, strike, time, roi, sigma), 2) == inf
            else numpy.float_power(self.d_to_use(spot, strike, time, roi, sigma), 2))) / 2)) * sigma * math.exp(-1 * time * 0)) / (2 * math.sqrt(time))) + 0 * spot * self.call_delta(spot, strike, time, roi, sigma) - roi * strike * math.exp(-1 * roi * time) * norm.cdf(self.d2_to_use(spot, strike, time, roi, sigma))) / 365
        return round(theta, 2)

    def put_theta(self, spot: float, strike: float, time: float, roi: float, sigma: float):
        """Return the theta of a put option

        Args:
            spot (float): Spot Price
            strike (float): Target/Strike Price
            time (float): Time to expire in years
            roi (float): rate of interest
            sigma (float): implied volatility

        Returns:
            float: theta of the put
        """
        theta = ((-1 *
                 (spot *
                  ((1 / math.sqrt(2 * math.pi)) * math.exp((-1 * (sys.float_info.max if numpy.float_power(self.d_to_use(spot, strike, time, roi, sigma), 2) == inf else numpy.float_power(self.d_to_use(spot, strike, time, roi, sigma), 2))) / 2)) *
                  sigma *
                  math.exp(-1 * time * 0))) /
                 (2 * math.sqrt(time)) -
                 0 * spot * norm.cdf(-1 * self.d_to_use(spot, strike, time, roi, sigma)) * math.exp(-1 * time * 0) +
                 roi * strike * math.exp(-1 * roi * time) * norm.cdf(-1 * self.d2_to_use(spot, strike, time, roi, sigma))) / 365
        return round(theta, 2)

    def call_put_gamma(self, spot: float, strike: float, time: float, roi: float, sigma: float):
        """Return the gamma for call or put as they are same

        Args:
            spot (float): Spot Price
            strike (float): Target/Strike Price
            time (float): Time to expire in years
            roi (float): rate of interest
            sigma (float): implied volatility

        Returns:
            float: gamma of the call/put
        """
        gamma = (
                (1 / math.sqrt(2 * math.pi)) *
                math.exp((-1 * (sys.float_info.max if numpy.float_power(self.d_to_use(spot, strike, time, roi, sigma), 2) == inf else numpy.float_power(self.d_to_use(spot, strike, time, roi, sigma), 2))) / 2) *
                math.exp(-1 * time * 0)
            ) / (spot * sigma * math.sqrt(time))
        return round(gamma, 2)

    def call_put_vega(self, spot: float, strike: float, time: float, roi: float, sigma: float):
        """Return the vega for call or put as they are same

        Args:
            spot (float): Spot Price
            strike (float): Target/Strike Price
            time (float): Time to expire in years
            roi (float): rate of interest
            sigma (float): implied volatility

        Returns:
            float: vega of the call/put
        """
        vega = ((1 / math.sqrt(2 * math.pi)) *
                math.exp((-1) * (sys.float_info.max if numpy.float_power(self.d_to_use(spot, strike, time, roi, sigma), 2) == inf else numpy.float_power(self.d_to_use(spot, strike, time, roi, sigma), 2))/2) *
                math.exp(-1 * time * 0) *
                spot *
                math.sqrt(time)) / 100
        return round(vega, 2)

    def call_rho(self, spot: float, strike: float, time: float, roi: float, sigma: float):
        """Return the rho for call

        Args:
            spot (float): Spot Price
            strike (float): Target/Strike Price
            time (float): Time to expire in years
            roi (float): rate of interest
            sigma (float): implied volatility

        Returns:
            float: rho of the call
        """
        rho = (strike * time * math.exp(-1 * roi * time) * norm.cdf(self.d2_to_use(spot, strike, time, roi, sigma)) * math.exp(-1 * 0 * time)) / 100
        return round(rho, 2)

    def put_rho(self, spot: float, strike: float, time: float, roi: float, sigma: float):
        """Return the rho for put

        Args:
            spot (float): Spot Price
            strike (float): Target/Strike Price
            time (float): Time to expire in years
            roi (float): rate of interest
            sigma (float): implied volatility

        Returns:
            float: rho of the put
        """
        rho = (-1 *
               strike *
               time *
               math.exp(-1 * roi * time) *
               norm.cdf(-1 * self.d2_to_use(spot, strike, time, roi, sigma)) *
               math.exp(-1 * 0 * time)) / 100
        return round(rho, 2)
