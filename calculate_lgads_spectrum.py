import numpy as np
import matplotlib.pyplot as plt
import multiprocessing

# parameters of the LGADs variation
W1 = {'e_gain': 1,
	  'h_gain': 0.253,
	  'h_gain_err': 0.003,
	  'th_impl': 112,  # nm
	  'depth_gl': 670,  # nm
	  'depth_gl_err': 12,  # nm
	  'noise': 23.61, # e-
	  'noise_err': 0.48, # e-
	  'charge_cloud': 7.16, # um
	  'charge_cloud_err': 0.15  
	  }

W9 = {'e_gain': 1,
	  'h_gain': 0.377,
	  'h_gain_err': 0.003,
	  'th_impl': 107,  # nm
	  'depth_gl': 299,  # nm 
	  'depth_gl_err': 5,  # nm

    # vrpre 3500
  	  'noise': 22.57, # e-
	  'noise_err': 0.40, # e- 
	  
    # vrpre 3700
  	#   'noise': 24.81, # e-
	#   'noise_err': 1.57, # e- 
	  'charge_cloud': 5.05, # um
	  'charge_cloud_err': 0.16 #um 
	  }

def get_simulated_data(txt_fname):
	data = np.loadtxt(txt_fname)
	return data[:,0], data[:,1], data[:,2]

def lgad_multiplication_noiseless(x, e, w):
	if x < 0: return 0
	if x >= 0 and x<= w['th_impl']: return e*w['h_gain']
	if x > w['th_impl'] and x < w['depth_gl']: 
		m = e*(w['e_gain']-w['h_gain'])/(w['depth_gl']-w['th_impl'])
		q = e*w['h_gain']-m*w['th_impl']
		return x*m + q
	if x>= w['depth_gl']: return e*w['e_gain']

# chose which variation
variation = W9

# charge collection efficiency file
# choose the charge cloud dimensions
chcloud = np.loadtxt('charge_collection/charge_collection7.16um_pp75um.txt').flatten()
print('Charge-cloud bins:', len(chcloud))

# simulated photon absorption events
# choose energy
eventID, posZ, edep = get_simulated_data('simulated_absorption/LGADs_absorption_700eV.txt')

# apply the multiplication factor
th_passivation = np.min(posZ)
mult_events = np.array([lgad_multiplication_noiseless(z-th_passivation, e*1000, variation) for z,e in zip(posZ,edep)])
print('Simulated events:', len(mult_events))

charge_shared_events = np.array([])

# apply the charge collection efficiency and noise
for i_en, en in enumerate(mult_events):
	
    # extract a few random impinging positions per photon-event
	rand = np.random.randint(0, len(chcloud), 10)
	charge_shared_events = np.append(charge_shared_events, np.random.normal(en*chcloud[rand], variation['noise']*3.6))
	if i_en%100==0:
		print(f'{i_en}/{len(mult_events)} ({i_en/len(mult_events)*100:0.2f}%)', end="\r")

print('Total simulated events:', len(charge_shared_events))
fig1, sub1 = plt.subplots() 
sub1.set(title='Single-pixel LGADs spectrum', xlabel='Energy (eV)', ylabel='Counts')
sub1.hist(charge_shared_events, bins=1000, histtype='step')

fig1.show()