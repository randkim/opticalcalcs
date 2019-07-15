import numpy as np
import scipy.special
import scipy.optimize
import pandas as pd
import matplotlib.pyplot as plt

wavelength = 355*10**(-9)

def erfunc(x, width, p):
    #Knife-Edge Method 
    #Finds width that best fits the observed data
    return p*(1-scipy.special.erf(np.sqrt(2)*x/width))

def beam_waist_func(z, w_0):
    #Finds w_0, the minimum beam waist
    return np.sqrt(w_0**2 + (z**2)*(wavelength/np.pi)**2)

def data_fixer(data):
    #Measurements are done in mm and some arbirarily voltage range
    #For the above-specified error function, the voltage range must be changed to 0~2V, and centered about the position 
    #where half the maximum voltage is measured
    #This function performs the unit change mm->m, semi-normalisation and positional shift
    
    #To semi-normalise (Error function has y-range 0~2 so need to double after normalisation)
    #data[:,1] = data[:,1]*2/max(data[:,1])
    
    #Convert mm (reading) to m
    data[:,0] = data[:,0]*0.001

    #First, shift everything left to 0
    data[:,0] = data[:,0] - min(data[:,0])
    
    #The half-intensity point is now brought to 0
    half_intensity = (max(data[:,1]) - min(data[:,1]))/2

    
    for i in range(len(data[:,1])):
        if data[i,1] - half_intensity < 0.1:
            half_intensity_point = i
    
    data[:,0] = data[:,0] - data[half_intensity_point,0]
    
    return data

def plotter(data, errfunc, params, power, z, i):
    #Note: Change this to class object later, and cut down the number of inputs
    plt.subplot(211)
    plt.plot(data[i][:,0], data[i][:,1], '-o')
    plt.plot(data[i][:,0], errfunc[i])
    plt.xlabel('Position centered about half-intensity')
    plt.ylabel('Intensity')
    plt.title('Graph of intensity against position')
    plt.show()
    
    print("The beam waist at z=", round(z[i], 3), "is:", round(params[i]*1000, 5), "mm")
    #print("The associated maximum power is: ", power[i])
    
    
    
#Data Read
z_0 = pd.read_csv("z_0_data.xlsx")
z_0 = z_0.values;
z_0 = data_fixer(z_0)

# =============================================================================
# z_0_2 = pd.read_csv("z_0_data2.xlsx")
# z_0_2 = z_0_2.values
# z_0_2 = data_fixer(z_0_2)
# =============================================================================

z_25 = pd.read_csv("z_25_data.xlsx")
z_25 = z_25.values
z_25 = data_fixer(z_25)

z_50 = pd.read_csv("z_50_data.xlsx")
z_50 = z_50.values
z_50 = data_fixer(z_50)

z_75 = pd.read_csv("z_75_data.xlsx")
z_75 = z_75.values
z_75 = data_fixer(z_75)

# =============================================================================
# z_100 = pd.read_csv("z_100_data.xlsx")
# z_100 = z_100.values
# z_100 = data_fixer(z_100)
# =============================================================================


intensity_data = [z_0, z_25, z_50, z_75]


#Actual optimisation
beam_waist = [];
p_max = []
extras= [];
y_erf = [];
z = [0.04, 0.04+25*10**-3, 0.04+50*10**-3, 0.04+75*10**-3]

for i in range(len(intensity_data)):
    hi, bye = scipy.optimize.curve_fit(erfunc, intensity_data[i][:,0], intensity_data[i][:,1], sigma = 0.005 + intensity_data[i][:,2], p0 = [0.0001, 5], maxfev = 10000)
    
    p_max.append(hi[1])
    
    beam_waist.append(hi[0])
    
    extras.append(bye)
    
    y_erf.append(erfunc(intensity_data[i][:,0], beam_waist[i], p_max[i]))
    
    plotter(intensity_data, y_erf, beam_waist, p_max, z, i)


beam_waist_min_avg = []
    
for k in range(len(beam_waist)):
    beam_waist_min_avg.append(np.sqrt(beam_waist[k]**2 - (z[k]*wavelength/np.pi)**2))
    mean = np.mean(beam_waist_min_avg)

print("Minimum beam waist by averaging:", mean*1000, "mm")
    
beam_waist_min_fit, extras2 = scipy.optimize.curve_fit(beam_waist_func, z, beam_waist)    

print("Minimum beam waist by fitting:", round(beam_waist_min_fit[0]*1000 ,5), "mm")

divergence = wavelength/(np.pi*beam_waist_min_avg[0])

print("So the divergence of the beam is:", round(2*divergence*100000,5), "urad")


z_plot = []

for k in range(0,100):
    z_plot.append(0.03 + k*5*10**-3)
    
nuwedi = []

for k in range(len(z_plot)):
    nuwedi.append(beam_waist_func(z_plot[k], mean))

plt.subplot(212)
plt.plot(z_plot, nuwedi)
plt.scatter(z, beam_waist)
plt.xlabel('Position')
plt.ylabel('Beam Waist')
plt.title('Calculated vs. recorded beam waist')
