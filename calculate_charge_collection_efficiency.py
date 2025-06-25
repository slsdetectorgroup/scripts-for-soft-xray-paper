import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import dblquad

def gauss2d(x,y,x0,y0,sigma,I):
	return I/(2*np.pi*np.power(sigma,2))*np.exp(-0.5*np.power(x-x0,2)/np.power(sigma,2)-0.5*np.power(y-y0,2)/np.power(sigma,2))
	
def integral_gauss2d(x0,y0,sigma,energy,pp):
	x,err = dblquad(gauss2d, 0, pp, 0, pp, args=(x0,y0,sigma,energy),epsabs=0.01)    
	return x

# dimension of the charge cloud at the pixel side, as sigma of a 2d gaussian
sigma_cloud = 7.16 # um

# pixel pitch
pp = 75 # um

Evgridx = np.arange(0,pp+.1,1)
Evgridy = np.arange(0,pp+.1,1)    
X, Y = np.meshgrid(Evgridx, Evgridy)
    
integral_gauss2d_v = np.vectorize(integral_gauss2d)
chcloud = integral_gauss2d_v(X,Y,sigma_cloud,1,pp)

fig2, sub2 = plt.subplots() # weighting field    
im = sub2.imshow(chcloud, extent=(0,pp,0,pp), vmin=0, vmax=1 ,cmap='inferno')
sub2.plot([0,pp,pp,0,0],[0,0,pp,pp,0],'-', color='black')
sub2.set(xlabel='x ($\\mu$m)',ylabel='y ($\\mu$m)')
sub2.tick_params(direction='in')
fig2.colorbar(im, label='Collected charge fraction')
fig2.show()

fout = open('charge_collection/charge_collection'+f'{sigma_cloud:0.2f}'+'um_pp'+f'{pp:0.0f}'+'um'+'.txt','w')
for el in chcloud: print(*el, file=fout)