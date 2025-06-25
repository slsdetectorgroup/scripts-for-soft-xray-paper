import numpy as np
from lmfit import Model,Parameters,Minimizer, report_fit
from scipy import special

# the returns are 15 parameters:
# pedestal, pedslope, flex, noise, amplitude, chargesharing, sign,
# errors (pedestal, pedslope, flex, noise, amplitude, chargesharing, sign)
# chi_squared/N0

# NOTE: the initial parameters and limits might need to be optimized

# to use serial (channel by channel)
#	fl0 is flex starting parameter
#
#	gmodel = Model(fsc.scurve)
#	params = gmodel.make_params()
#
#	for i_x in np.arange(0,512):
#		for i_y in np.arange(0,512):
#			f_r = fsc.fit_scurve_func(vthreshold[i_min:i_max], 
#				data[i_min:i_max,i_y,i_x], mask[i_y,i_x], -1, fl0, chi_thresh)
#
   
def scurve(x,pedestal, pedslope, flex, noise, amplitude, chargesharing, sign=1):
	return 0.5*amplitude*(1+special.erf(sign*(flex-x)/(noise*1.414213562))) \
		*(1+chargesharing*(flex-x))+pedestal-pedslope*x*sign

gmodel = Model(scurve)

cs0 = -0.0006		

def init_params_LGADs(flex0, ampl0, noise0, sign, ped=0, pedsl=0):
	gmodel.set_param_hint('pedestal',value=ped, min=0, max=max(ampl0/4,1))
	gmodel.set_param_hint('pedslope',value=pedsl)

	# if you need to fix ped/pedslope
	#    gmodel.set_param_hint('pedestal',value=0, vary=False ) 
	#    gmodel.set_param_hint('pedslope',value=0, vary=False )

	gmodel.set_param_hint('flex',value=flex0, min=0, max=2100)
	gmodel.set_param_hint('noise',value=noise0, min=5, max=500)
	gmodel.set_param_hint('amplitude',value=ampl0,min=0, max=1.8*ampl0+1)

	if sign==-1:
		gmodel.set_param_hint('chargesharing',value=cs0,min=-0.1,max=-0.0001)
	if sign==1:
		gmodel.set_param_hint('chargesharing',value=-cs0,min=0.0001,max=0.1)

	gmodel.set_param_hint('sign',value=sign, vary=False)
	params = gmodel.make_params()
	return params

def fit_scurve_LGADs_f(thresholds, data, params):
	result = gmodel.fit(data, params, x=thresholds)
	return result	
	    
def fit_scurve_func(thr, data, mask, sign, fl0, ns0=50, chi_thresh=1e6, N0=0):
	if mask == 0: return np.zeros(15, dtype = float)
	result = fit_scurve_LGADs_f(thr, data, init_params_LGADs(fl0, np.max(data)*1.25, ns0, sign))
	if result.success==False or result.params['amplitude'].value==0 : return np.zeros(15, dtype=float)
	norm_chi = result.redchi/result.params['amplitude'].value
	if norm_chi > chi_thresh: return np.zeros(15, dtype=float)

	return [result.params[p].value for p in result.params.keys()] \
				+[result.params[p].stderr for p in result.params.keys()] \
				+ [norm_chi]