#!/usr/bin/python

"""
Custom Statistical Analysis Library.

This module defines the Data class and functions for computing advanced 
statistical metrics on numerical series, including biweight mean, 
MAD, NMAD, robust standard deviation, and sigma clipping.

@package AIDA
@module iotstats
"""

import numpy as np
import numpy.ma as ma
import math
from scipy.stats import skew, kurtosis, mode
import warnings
warnings.simplefilter("ignore", category=RuntimeWarning)

class Data(object):
    """Provide methods for comprehensive statistical analysis on numerical data.

    Parameters
    ----------
    myinput : array_like
        Input sequence or array of numerical data values.

    Attributes
    ----------
    data : numpy.ndarray
        Float64 1D array of input data values.
    rdigits : int
        Rounding precision for statistical result metrics.
    """
    
    def __init__(self, myinput):
        #convert to numpy
        self.data = np.array(myinput, dtype=np.float64)
        #round digits        
        self.rdigits = 6

    def dqc_biweight(self, iterMax=25, epsilon=1.0e-20):
        """Calculate the mean of the dataset using bisquare weighting iterations.  

        Based on the biweight_mean routine from the AstroIDL User's Library [1]_.
        
        Parameters
        ----------
        iterMax : int, optional
            Maximum number of approximation iterations (default is 25).
        epsilon : float, optional
            Minimum standard deviation threshold to stop iteration (default is 1.0e-20).

        Returns
        -------
        float
            Calculated biweight mean value.
   
        References
        ---------
            ..[1] http://idlastro.gsfc.nasa.gov/
        """
        itermax = int(iterMax)
        epsilon = float(epsilon)
        X = self.data
      
        y = np.ravel(X)
        y = y[~np.isnan(y)]
        n = len(y)
        diff = 1.0e30
        #define minimum sigma to stop iteration
        if n>1 :
            closeEnough = 0.03 * np.sqrt(0.5 / (n - 1))
        else:
            closeEnough = diff
            
        y0 = np.nanmedian(y)
        deviation = y - y0
        d = Data(deviation)
        #starting standard deviation
        sigma = d.dqc_robust_stdev(epsilon)

        nIter = 0
        weightsOut = 0    
        if sigma < epsilon:
            diff = 0
        #repeat until difference between previous and current std is less than closeEnough            
        while diff > closeEnough:
            nIter = nIter + 1
            #stop loop if maximum number of iterations is reached
            if nIter > itermax:
                break
            #calculate weights
            uu = ((y - y0) / (6.0 * sigma))**2.0
            uu = np.where(uu > 1.0, 1.0, uu)
            weightsOut = (1.0 - uu)**2.0
            
            weights = weightsOut/weightsOut.sum()
            y0 = (weights * y).sum()
            #calculate value deviations
            deviation = y - y0
            d = Data(deviation)
            prevSigma = sigma
            #calculate current sigma of deviations
            sigma = d.dqc_robust_stdev(epsilon, Zero=True)
            #re-calculate difference
            if sigma > epsilon:
                diff = np.abs(prevSigma - sigma) / prevSigma
            else:
                diff = 0.0

        return round(y0, self.rdigits)

    def dqc_kurtosis(self, axis = None, bias = True, nan_policy = 'omit'):
        """Compute the kurtosis of the dataset, ignoring NaN values.

        Parameters
        ----------
        axis : int or None, optional
            Axis along which kurtosis is calculated (default is None).
        bias : bool, optional
            If False, corrects calculation for statistical bias (default is True).
        nan_policy : {'propagate', 'raise', 'omit'}, optional
            Policy for handling NaNs in input data (default is 'omit').

        Returns
        -------
        float
            Calculated kurtosis value.
        """
        return round(kurtosis(self.data, axis, bias, nan_policy), self.rdigits)

    def dqc_mad(self, axis=None):
        """Compute the Median Absolute Deviation (MAD) of the dataset.

        Parameters
        ----------
        axis : int or None, optional
            Axis along which MAD is computed (default is None).

        Returns
        -------
        float
            Calculated median absolute deviation value.
        """
        # MAD calculation
        med = np.nanmedian(self.data, axis=axis, keepdims=True)
        x = np.nanmedian(np.absolute(self.data - med), axis=axis)

        return round(x, self.rdigits)

    def dqc_max(self):
        """Return the maximum value of the array, ignoring NaNs.

        Returns
        -------
        float
            Maximum data value.
        """
        # Max calculation
        return np.nanmax(self.data)
        
    def dqc_mean(self):
        """Compute the arithmetic mean of the array, ignoring NaNs.

        Returns
        -------
        float
            Arithmetic mean value.
        """
        # Mean calculation
        return round(np.nanmean(self.data),self.rdigits)

    def dqc_median(self):
        """Compute the median value of the array, ignoring NaNs.

        Returns
        -------
        float
            Median data value. 

        Notes
        -------
            Given a vector V of length N, the median of V is the middle value of a sorted copy of V, V_sorted - i e., 
            V_sorted[(N-1)/2],
            when N is odd, and the average of the two middle values of V_sorted when N is even.

        """

        # Median calculation
        return round(np.nanmedian(self.data),self.rdigits)
     
    def dqc_min(self):
        """Return the minimum value of the array, ignoring NaNs.

        Returns
        -------
        float
            Minimum data value.
        """
        
        # Min calculation
        return np.nanmin(self.data)

    def dqc_mode(self, precision=None):
        """Compute the standard mode of an array, ignoring any NaNs. If precision is set, data will be
        arranged into bins of width = 2*precision and the median of values in each bin will be considered for calculation. 

        Parameters
        --------
        precision : float or None, optional
            Binning precision width for mode evaluation (default is None). If precision is set, data will be arranged into bins of 
            width = 2*precision and the median of values in each bin will be considered for calculation.

        Returns
        -------
        result : str
            HTML formatted string detailing mode value and count. 
        """
        if precision == 0:
            precision = None
    
        if precision is not None:
            precision = float(precision)
            # Binning input data
            binwidth=2*precision
            # interval extremes
            start = self.dqc_min()-precision
            stop = self.dqc_max()+precision
            # number of bins
            numbin = int((stop-start)/binwidth+1)
            # evenly spaced bins
            binz = np.linspace(start, stop, numbin)
            # indices of bins to which each value in input array belongs.
            datamode = np.digitize(self.data,binz)
            # calculation of mode of bins
            x = mode(datamode)
            binref=x[0][0]
            # mode of values
            m = binz[binref-1]+precision
            # occurrences of mode value
            c = x[1][0]
        else:
            # Mode calculation
            x = mode(self.data)
            # mode of value
            m = x[0][0]
            # occurrences of mode value
            c = x[1][0]

        result = "Mode : "+str(m) +"<br/>Counts : " +str(c)
        return result

    def dqc_nmad(self, axis=None):
        """Compute Normalized Median Absolute Deviation (NMAD) of the dataset.

        Parameters
        ----------
        axis : int or None, optional
            Axis along which NMAD is computed (default is None).

        Returns
        -------
        float
            Normalized median absolute deviation value.
        """
        # NMAD calculation
        mad = self.dqc_mad(axis=axis)
        scale = 0.6745
        x = mad / scale

        return round(x, self.rdigits)

    def dqc_percentile(self, quantile=None, interpolation="linear"):
        """Compute the q-th percentile of the data, ignoring NaN values.

        Parameters
        ----------
        quantile : float
            Percentile value in the range [0, 100].
        interpolation : str, optional
            Interpolation method to use when the desired quantile lies between two data points i < j.
            Available values are "linear", "lower", "higher", "nearest" and "midpoint" (default is "linear"):
                linear: i + (j - i) * fraction, where fraction is the fractional part of the index 
                    surrounded by i and j;
                lower: i;
                higher: j;
                nearest: i or j, whichever is nearest;
                midpoint: (i + j) / 2.

        Returns
        -------
        float
            Calculated percentile value.
        """
        # Percentile calculation
        x = np.nanpercentile(self.data, quantile, interpolation=interpolation)
        return round(x, self.rdigits)

    def dqc_rms(self):
        """Compute the Root Mean Square (RMS) of the dataset.

        Returns
        -------
        float
            Calculated RMS value.
        """

        # RMS calculation
        return round(np.sqrt(np.nanmean(self.data**2)), self.rdigits)

    def dqc_robust_stdev(self, epsilon=None, Zero=False):#, dtype=None):
        """Calculate robust estimator of standard deviation based on AstroIDL robust_sigma.  
        
        Based on the robust_sigma function from the AstroIDL User's Library [1]_.
        
        Parameters
        ----------
        epsilon : float or None
            Minimum threshold for MAD computation.
        Zero : bool, optional
            If True, calculates dispersion relative to 0.0 (default is False).

        Returns
        -------
        float
            Robust standard deviation value, or -1.0 on failure.

        References
        ---------
            ..[1] http://idlastro.gsfc.nasa.gov/
        """

        data = self.data.ravel()
        data = data[~np.isnan(data)]
           
        if Zero:
            data0 = 0.0
        else:
            data0 = np.nanmedian(data)
        #calculate NMAD
        maxAbsDev = np.nanmedian(np.abs(data-data0)) / 0.6745
        if maxAbsDev < epsilon:
            maxAbsDev = np.nanmean(np.abs(data-data0)) / 0.8000
        #if maxAbsDev < epsilon, then return sigma = 0
        if maxAbsDev < epsilon:
            sigma = 0.0
            return sigma
            
        u = (data-data0) / 6.0 / maxAbsDev
        u2 = u**2.0
        good = np.where( u2 <= 1.0 )
        good = good[0]
        #if too few good values, return -1
        if len(good) < 3:
            sigma = -1.0
            return sigma
            
        numerator = ((data[good]-data0)**2.0 * (1.0-u2[good])**4.0).sum()
        nElements = (data.ravel()).shape[0]
        denominator = ((1.0-u2[good])*(1.0-5.0*u2[good])).sum()
        #calculate robust sigma
        sigma = nElements*numerator / (denominator*(denominator-1.0))
        if sigma > 0:
            sigma = math.sqrt(sigma)
        else:
            sigma = 0.0
            
        return sigma

    def dqc_sigma_clip(self, sigma=3.0, function="median"):
        """Perform iterative sigma-clipping on an array. The data will be iterated over, each time rejecting points 
        that are discrepant by more than a specified number of standard deviations from a center value. 
        If the data contains invalid values (NaNs or infs), they are automatically masked before performing 
        the sigma-clipping.
        
        This method is a modified version of astropy.stats.sigma_clip.

        Parameters
        ----------
        sigma : float, optional
            Standard deviation threshold limit for clipping (default is 3.0).
        function : {'biweight', 'median', 'mean'}, optional
            Central statistic used for clipping baseline (default is 'median').

        Returns
        -------
        result : str
            Formatted HTML string listing unclipped and outlier values.
        """
        data = self.data

        # define centering function
        if function == "mean":
            cenfunc = self.dqc_mean
        elif function== "median":
            cenfunc = self.dqc_median
        elif function== "biweight":
            cenfunc = self.dqc_biweight

        # Mask NaN values
        if np.any(~np.isfinite(data)):
            data = np.ma.masked_invalid(data)

        clipped = np.ma.array(data)

        # repeat clipping until the last iteration clips nothing
        i = -1
        lastrej = clipped.count() + 1

        while clipped.count() != lastrej:
            i += 1
            lastrej = clipped.count()
            if type(clipped.mask) is np.ndarray:
                clipped_val = clipped[clipped.mask == False]
            else:
                clipped_val = clipped
            #select central function            
            dqc = Data(clipped_val)
            if function== "biweight":
                deviation = clipped - dqc.dqc_biweight()[0]
            elif function=="mean":
                deviation = clipped - dqc.dqc_mean()
            elif function=="median":
                deviation = clipped - dqc.dqc_median()
                
            # to compute the standard deviation about the center, np.std is used  
            std = np.std(clipped)
            clipped.mask |= np.ma.masked_less(deviation, -std * sigma).mask
            clipped.mask |= np.ma.masked_greater(deviation, std * sigma).mask

        # prevent clipped.mask = False (scalar) if no values are clipped
        if clipped.mask.shape == ():
            clipped.mask = False   # .mask shape will now match .data shape
            
        outliers = np.ma.masked_array(data, np.logical_not(clipped.mask))
        #convert output to list and then to string
        clipped = np.ma.filled(clipped.astype(float), fill_value=np.nan)        
        final_clipped = []
        for el in clipped:
            if not np.isnan(el):
                final_clipped.append(round(el, self.rdigits))        
        c=str(final_clipped)
        outliers = np.ma.filled(outliers.astype(float), fill_value=np.nan)
        final_outl = []
        for el in outliers:
            if not np.isnan(el):
                final_outl.append(round(el, self.rdigits))
        outl = str(final_outl)
        out = "Unclipped : "+c+"<br/>Outliers : "+outl
        
        return out
 
    def dqc_skewness(self, axis = None, bias = True, nan_policy = 'omit'):
        """Compute skewness of dataset values, ignoring NaNs.

        Parameters
        ----------
        axis : int or None, optional
            Axis along which skewness is calculated (default is None).
        bias : bool, optional
            If False, corrects calculation for statistical bias (default is True).
        nan_policy : {'propagate', 'raise', 'omit'}, optional
            Policy for handling NaNs in input data (default is 'omit').

        Returns
        -------
        float
            Calculated skewness value.
        """
        
        return round(skew(self.data, axis, bias, nan_policy), self.rdigits)
 
    def dqc_stdev(self, df=0):
        """Compute standard deviation of dataset values, ignoring NaNs.

        Parameters
        ----------
        df : int, optional
            Delta degrees of freedom divisor correction (default is 0).

        Returns
        -------
        float
            Standard deviation value.
        """

        # Standard deviation calculation
        return round(np.nanstd(self.data, ddof=df), self.rdigits)
        
    def dqc_variance(self):
        """Compute variance of dataset values, ignoring NaNs.

        Returns
        -------
        float
            Calculated variance value.
        """

        # Variance calculation
        return round(np.nanvar(self.data), self.rdigits)
    

def calculateGlobal(datain):
    """Calculate default global statistical metrics on input dataset.

    Parameters
    ----------
    datain : array_like
        Input sequence or array of values.

    Returns
    -------
    results : dict
        Dictionary mapping metric names to calculated statistical values.
    """
    #input data
    data = Data(datain)
    #stats (name) to calculate    
    global_stats = ["Mean", "Median", "Max", "Min", "Standard Dev", "RMS", "Variance", "Kurtosis", "Skewness", "MAD", "NMAD"]
    #stats (slug) to calculate    
    global_res = [data.dqc_mean(),data.dqc_median(), data.dqc_max(), data.dqc_min(), data.dqc_stdev(), data.dqc_rms(), data.dqc_variance(), data.dqc_kurtosis(), data.dqc_skewness(), data.dqc_mad(), data.dqc_nmad()]
    results = {}
    #calculate results    
    for i in range(len(global_stats)):
        results.update({global_stats[i]: global_res[i]})
    return results
    