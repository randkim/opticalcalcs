import numpy as np

def rayleigh_range(wavelength, beam_waist):
    z_0 = np.pi*beam_waist**2/wavelength
    
    return z_0

def lens_bw_collimated(wavelength, beamwaist, focal_length):
    #Calculates beam waist after a single lens for a collimated input beam
    new_beamwaist = wavelength/(np.pi*beamwaist) * focal_length
    return new_beamwaist


def lens_bw(focal_length, beamwaist, dist_from_beamwaist):
    z_0 = np.pi*beamwaist**2/wavelength
    
    r = z_0/(dist_from_beamwaist - focal_length)
    M_r = np.abs(focal_length/(dist_from_beamwaist - focal_length))
    M = M_r/np.sqrt(1+r**2)
    
    new_beamwaist = M*beamwaist
    new_beamwaist_location = M**2 * (dist_from_beamwaist - focal_length) + focal_length
    
    return new_beamwaist, new_beamwaist_location


def two_lens_bw_collimated(wavelength, beamwaist, focal_length, focal_length2, dist_from_beamwaist):
    
    new_beamwaist = lens_bw_collimated(wavelength, beamwaist, focal_length)
    
    new_new_beamwaist, new_new_beamwaist_location = lens_bw(focal_length2, new_beamwaist, dist_from_beamwaist)
    
    z_0_new = rayleigh_range(wavelength, new_new_beamwaist)
    
    return new_new_beamwaist, new_new_beamwaist_location, z_0_new
    

def beam_divergence(wavelength, beamwaist, z):
    #Calculates beam waist after distance z of propogation through free space
    z_0 = np.pi*beamwaist**2/wavelength
    new_beamwaist = beamwaist*np.sqrt(1+(z/z_0)**2)
    return new_beamwaist


def aom_solve_z_collimated(wavelength, beamwaist, focal_length, desired_beamwaist):
    #Calculates the distance from focus of lens such that the desired beam waist is incident on the AOM
    
    #First, assume collimated input and calculate new beam waist after the lens
    new_beamwaist = lens_bw_collimated(wavelength, beamwaist, focal_length)
    
    #Inverse of beam divergence, calculate for z, the distance from the focus
    z_0 = np.pi*new_beamwaist**2/wavelength
    z = z_0 * np.sqrt((desired_beamwaist/new_beamwaist)**2-1)
    return new_beamwaist, z


def diffraction_limit(wavelength, focal_length, beamwaist):
    limit = 1.22*focal_length*wavelength/(2*beamwaist)
    return limit


wavelength = 355*10**(-9)
beamwaist = 510*10**(-6)
focal_length = 100*10**(-3)


new_beamwaist, z_wanted = aom_solve_z_collimated(wavelength, beamwaist, focal_length, 100*10**(-6))
print(np.format_float_positional(z_wanted*10**(3), precision=3), 'mm')
print(np.format_float_positional(new_beamwaist*10**(6), precision=3), 'um')

limit = diffraction_limit(wavelength, focal_length, beamwaist)
print(np.format_float_positional(limit*10**(6), precision=3), 'um')

beamwaist2, beamwaist2_loc, z_0_2 = two_lens_bw_collimated(wavelength, beamwaist, 150*10**(-3), 150*10**(-3), 15.5*10**(-2))
print(beamwaist2, beamwaist2_loc, z_0_2)
