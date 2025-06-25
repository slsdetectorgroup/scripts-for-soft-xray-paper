import numpy as np
import re
import json

# this function opens the files containing raw data
# generally raw data from an Eiger Quad (512x512 ~ 250k pixels)
# are divided into 2 files, a "master" file with the same name is also created
# the master has either .raw or .json extension
# the functions takes as input the latter
# 
# the function returns a numpy.array of the shape:
# (frames, 512,512)
# in which the different frames correspond to a value of the counter threshold in a threshold scan
# the master file contains the parameters of the scan, e.g., the range, step, exposure time, dynamic range etc...

def file_read(fname):
	dtype = 'uint32'
	header = 28 
	if fname.endswith('.json'):
		scan_par = json.load(open(fname))
		if scan_par['Dynamic Range'] == '32': 
			dtype = 'uint32'
			header = 28
		if scan_par['Dynamic Range'] == '16': 
			dtype = 'uint16'
			header = 56
		rawfile0 = fname.replace('.json','.raw').replace('_master','_d0_f0')
		rawfile1 = fname.replace('.json','.raw').replace('_master','_d1_f0')

	if fname.endswith('.raw'):
		scan_par = open(fname,'r').read()
		if re.search('Dynamic Range              : (.*)', scan_par).group(1) == '32': 
			dtype = 'uint32'
			header = 28
		if re.search('Dynamic Range              : (.*)', scan_par).group(1) == '16': 
			dtype = 'uint16'
			header = 56
		rawfile0 = fname.replace('_master','_d0_f0')
		rawfile1 = fname.replace('_master','_d1_f0')
	print(scan_par)

	data0 = np.fromfile(rawfile0, dtype=dtype, count=-1)
	frames0 = int(np.shape(data0)[0]/(256*512+header))
	data1 = np.fromfile(rawfile1, dtype=dtype, count=-1)
	frames1 = int(np.shape(data1)[0]/(256*512+header))
	if frames1!=frames0:
		print('Problem with files')
		return 0
	data0 = np.reshape(data0, (frames0,-1))[:,header:]
	data1 = np.reshape(data1, (frames1,-1))[:,header:]
	data0 = np.reshape(data0, (frames0,256,512))
	data1 = np.reshape(data1, (frames1,256,512))
	return np.concatenate((data1[:,::-1,:],data0), axis=1)

