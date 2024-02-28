#!/usr/bin/python

import numpy as np
import numpy.ma as ma
import math
from scipy.stats import skew, kurtosis, mode
import warnings
warnings.simplefilter("ignore", category=RuntimeWarning)

class Data(object):
	"""Class to use for statistical analysis of input

	Attributes
	---------
		data: ndarray
			Numpy array containing data

	"""
	
	def __init__(self, myinput):
		#convert to numpy
		self.data = np.array(myinput, dtype=np.float64)
		#round digits        
		self.rdigits = 6

	def dqc_biweight(self, iterMax=25, epsilon=1.0e-20):
		"""Calculate the mean of a data set using bisquare weighting. It works on 1D or 2D input arrays.  

		Based on the biweight_mean routine from the AstroIDL User's Library [1]_.
		
		Parameters
		--------
			iterMax: int, optional
				Maximum number of iterations to approximate the standard deviation of the distribution (default is 25).
			epsilon: float, optional
				Minimum value of the standard deviation to continue iterations (default is 1.0e-20).
		
		Returns
		-------
			y0: float or ndarray
				New array containing the biweight mean values. The value is a float if axis is None. 
			
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
		"""Compute the skewness of an array, ignoring any NaNs.

        Parameters
        --------
			axis : int or None, optional
				Axis along which kurtosis is calculated. If None, compute over the whole array a. Default is None.
			bias : bool, optional
				If False, then the calculations are corrected for statistical bias.
			nan_policy : {‘propagate’, ‘raise’, ‘omit’}, optional
				Defines how to handle when input contains nan. ‘propagate’ returns nan, ‘raise’ throws an error, ‘omit’ performs the calculations ignoring nan values. 
				Default is ‘omit’.

        Returns
        -------
			kurtosis : ndarray
				The kurtosis of values along an axis, returning 0 where all values are equal.

		"""
		return round(kurtosis(self.data, axis, bias, nan_policy), self.rdigits)

	def dqc_mad(self, axis=None):
		"""Compute the Median Absolute Deviation (MAD) of an array along the specified axis. 

		Parameters
		--------
			axis: int, optional
				Axis along which the MAD is computed, according with Numpy definition (default is 'None').

		Returns
		-------
			float or ndarray
				New array containing the MAD values. The value is a float if axis is None.
		"""
		# MAD calculation
		med = np.nanmedian(self.data, axis=axis, keepdims=True)
		x = np.nanmedian(np.absolute(self.data - med), axis=axis)

		return round(x, self.rdigits)

	def dqc_max(self):
		"""Return the maximum of an array ignoring any NaNs. 

        Returns
        -------
            float
                Maximum value of the array

		"""
		# Max calculation
		return np.nanmax(self.data)
        
	def dqc_mean(self):
		"""Compute the standard mean of an array, ignoring any NaNs. 

        Returns
        -------
            float 
				Mean value of the array.

		"""
		# Mean calculation
		return round(np.nanmean(self.data),self.rdigits)

	def dqc_median(self):
		"""Compute the median of an array, ignoring any NaNs. 

        Returns
        -------
            float
                Median value of the array. 

        Notes
        -------
            Given a vector V of length N, the median of V is the middle value of a sorted copy of V, V_sorted - i e., 
            V_sorted[(N-1)/2],
            when N is odd, and the average of the two middle values of V_sorted when N is even.

		"""

		# Median calculation
		return round(np.nanmedian(self.data),self.rdigits)
     
	def dqc_min(self):
		"""Return the minimum of an array, ignoring any NaNs. 

        Returns
        -------
            float
                Minimum value of the array
				
		"""
        
		# Min calculation
		return np.nanmin(self.data)

	def dqc_mode(self, precision=None):
		"""Compute the standard mode of an array, ignoring any NaNs. If precision is set, data will be
		arranged into bins of width = 2*precision and the median of values in each bin will be considered for calculation. 

		Parameters
		--------
			precision: float, optional
				precision for mode evaluation. If precision is set, data will be arranged into bins of width = 2*precision and 
				the median of values in each bin will be considered for calculation.

		Returns
		-------
			result: str
			   String containing the mode values and their counts. 
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
		"""Compute the Normalized Median Absolute Deviation (NMAD) of an array along the specified axis. 

		Parameters
		--------
			axis: int, optional
				Axis along which the NMAD is computed, according with Numpy definition (default is 'None').

		Returns
		-------
			float or ndarray
				New array containing the NMAD values. The value is a float if axis is None. 

		"""
		# NMAD calculation
		mad = self.dqc_mad(axis=axis)
		scale = 0.6745
		x = mad / scale

		return round(x, self.rdigits)

	def dqc_percentile(self, quantile=None, interpolation="linear"):
		"""Compute the qth percentile of the data along the specified axis, while ignoring NaN values.

		Parameters
		----------
			quantile : float in range of [0,100]
				Percentile to compute, which must be between 0 and 100 inclusive.
			interpolation : string, optional
				Interpolation method to use when the desired quantile lies between two data points i < j.
				Available values are "linear", "lower", "higher", "nearest" and "midpoint" (default is "linear"):

					linear: i + (j - i) * fraction, where fraction is the fractional part of the index 
						surrounded by i and j;
					lower: i;
					higher: j;
					nearest: i or j, whichever is nearest;
					midpoint: (i + j) / 2.

		Returns
		---------
			float or ndarray
				New array containing the percentile values. The value is a float if axis is None.

		"""
		# Percentile calculation
		x = np.nanpercentile(self.data, quantile, interpolation=interpolation)
		return round(x, self.rdigits)

	def dqc_rms(self):
		"""Compute the Root Mean Square (RMS) of an array. 

        Returns
        -------
            float
                RMS value of the array

		"""

		# RMS calculation
		return round(np.sqrt(np.nanmean(self.data**2)), self.rdigits)

	def dqc_robust_stdev(self, epsilon=None, Zero=False):#, dtype=None):
		"""Robust estimator of the standard deviation of a data set.  
		
		Based on the robust_sigma function from the AstroIDL User's Library [1]_.
		
		Parameters
		--------
			epsilon: float
				Minimum value allowed for the MAD to compute the robust standard deviation.
			Zero: bool, optional
				if True, the dispersion is calculated w.r.t. 0.0 rather 
				than the central value of the array (default is False).
		
		Returns
		-------
			float
				Robust standard deviation value. In case of failure, returns value of -1.0.

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
		
		This method is a modified version of astropy.stats.sigma_clip, fitted for Euclid DQCT requirements

		Parameters
		-----------
			sigma : float, optional
				The number of standard deviations to use for both the lower and upper clipping limit. Defaults is 3.
			function : 'biweight', 'median' or 'mean', optional
				The statistic used to compute the center value for the clipping. The default is 'median'

		Returns
		--------
            result: str
			   String containing the list of points rejected or not by the algorithm, into separated lists.
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
		"""Compute the skewness of an array, ignoring any NaNs.

        Parameters
        --------
			axis : int or None, optional
				Axis along which skewness is calculated. If None, compute over the whole array a. Default is None.
			bias : bool, optional
				If False, then the calculations are corrected for statistical bias.
			nan_policy : {‘propagate’, ‘raise’, ‘omit’}, optional
				Defines how to handle when input contains nan. ‘propagate’ returns nan, ‘raise’ throws an error, ‘omit’ performs the calculations ignoring nan values. 
				Default is ‘omit’.

        Returns
        -------
			skewness : ndarray
				The skewness of values along an axis, returning 0 where all values are equal.

		"""
		
		return round(skew(self.data, axis, bias, nan_policy), self.rdigits)
 
	def dqc_stdev(self, df=0):
		"""Compute the standard deviation of an array, ignoring any NaNs.

        Parameters
        --------
            df: int, optional
                Means Degrees of Freedom. The divisor used in calculations is N-df, where N is the number of elements.
                (default is 0)

        Returns
        -------
            float 
                Standard deviation of the array

		"""

		# Standard deviation calculation
		return round(np.nanstd(self.data, ddof=df), self.rdigits)
        
	def dqc_variance(self):
		"""Compute the variance of an array, ignoring any NaNs.

        Returns
        -------
            float 
                Variance value of the array 

		"""

		# Variance calculation
		return round(np.nanvar(self.data), self.rdigits)
    

def calculateGlobal(datain):
	"""Calculate statistical estimators indicated in global_stats.
    
	Parameters
	-----------
	datain : list or ndarray,
    	list of data to use
    
	Returns
    -------
		results : dict 
			results of statistical analysis in the form {<stats name> : value} 
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
	