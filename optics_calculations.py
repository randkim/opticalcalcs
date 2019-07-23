import numpy as np

#To perform simple, zero or one-lens calculations
class one_lens_optics_calculations:
    
    def __init__(self, wavelength):
        #Initialises to the wavelength of the laser. This assumes that the same laser wavelength is used.
        self.wavelength = wavelength
        
    def rayleigh_range(self, beamwaist):
        #Calculates the Rayleigh range for a given beamwaist
        z_0 = np.pi*(beamwaist**2)/self.wavelength
        return z_0
    
    def diffraction_limit(self, beamwaist, focal_length):
        #Calculates the diffraction limited beamwaist for a given lens of focal_length
        #The beam CANNOT be focused to a beamwaist below this limit, regardless of the actual focusing power of the lens
        limit = 1.22*focal_length*self.wavelength/(2*beamwaist)
        return limit
        
    def beam_divergence(self, beamwaist, z):
        #Calculates the beam width after distance z from the minimum beamwidth
        z_0 = np.pi*(beamwaist**2)/self.wavelength
        new_beamwaist = beamwaist*np.sqrt(1+(z/z_0)**2)
        return new_beamwaist
    
    def inverse_beam_divergence(self, beamwaist, desired_beamwaist):
        #Calculates the position z for which a certain desired_beamwaist is reached
        z_0 = np.pi*(beamwaist**2)/self.wavelength
        z = z_0 * np.sqrt((desired_beamwaist/beamwaist)**2-1)
        return z
        
    def lens_beamwaist_collimated(self, beamwaist, focal_length):
        #Calculates beamwaist after a lens of focal_length, assuming collimated input beam
        #Beamwaist is at the focus of the lens
        new_beamwaist = self.wavelength/(np.pi*beamwaist) * focal_length
        return new_beamwaist
    
    def lens_beamwaist(self, beamwaist, focal_length, dist_from_beamwaist):
        #Calculates beamwaist and beamwaist location after a lens of focal_length
        
        #Some intermediate calculations
        z_0 = np.pi*(beamwaist**2)/self.wavelength
        r = z_0/(dist_from_beamwaist - focal_length)
        m_r = np.abs(focal_length/(dist_from_beamwaist - focal_length))
        m = m_r/np.sqrt(1 + r**2)
        
        new_beamwaist = m*beamwaist
        new_beamwaist_loc = m**2 * (dist_from_beamwaist - focal_length) + focal_length
        return new_beamwaist, new_beamwaist_loc
    
    def lens_inverse_beam_divergence_collimated(self, beamwaist, focal_length, desired_beamwaist, dist_from_beamwaist):
        #Calculates for position z after a lens to achieve desired_beamwaist, for collimated input beam
        #Used mainly for AOM positioning
        
        #First calculate the beamwaist after the lens
        new_beamwaist = self.wavelength/(np.pi*beamwaist) * focal_length
        
        #The beamwaist diverges from here. So we employ the inverse beam divergence calculations:
        z_0 = np.pi*(beamwaist**2)/self.wavelength
        z = z_0 * np.sqrt((desired_beamwaist/new_beamwaist)**2 - 1)
        return z, new_beamwaist
            
        
    def lens_inverse_beam_divergence(self, beamwaist, focal_length, desired_beamwaist, dist_from_beamwaist):
        #Calculates for position z after a lens to achieve desired_beamwaist
        #Used mainly for AOM positioning
        
        #First calculate beamwaist and location of beamwaist after lens
        z_0 = np.pi*(beamwaist**2)/self.wavelength
        r = z_0/(dist_from_beamwaist - focal_length)
        m_r = np.abs(focal_length/(dist_from_beamwaist - focal_length))
        m = m_r/np.sqrt(1 + r**2)
        
        new_beamwaist = m*beamwaist
        new_beamwaist_loc = m**2 * (dist_from_beamwaist - focal_length) + focal_length
    
        #Then perform the inverse beam divergence calculations
        z_0_new = np.pi*(new_beamwaist**2)/self.wavelength
        z = z_0_new * np.sqrt((desired_beamwaist/new_beamwaist)**2 - 1)
        return z, new_beamwaist, new_beamwaist_loc



#Used for multiple-lens calculations.
class multiple_lens_optics_calculations(one_lens_optics_calculations):
    
    def __init__(self, wavelength):
        one_lens_optics_calculations.__init__(self, wavelength)

        
    def two_lens_beamwaist_collimated(self, beamwaist, focal_length, focal_length2, lens23_seperation):
        #First calculate the beamwaist after the first lens
        new_beamwaist = one_lens_optics_calculations.lens_beamwaist_collimated(self, beamwaist, focal_length)
        
        #Calculate beamwaist and beamwaist location after the second lens
        #Assume here that the minimum beamwaist of the first lens is positioned at the focus of the first lens itself
        new_new_beamwaist, new_new_beamwaist_location = one_lens_optics_calculations.lens_beamwaist(self, new_beamwaist, focal_length2, lens23_seperation - focal_length)
        
        return new_new_beamwaist, new_new_beamwaist_location
            
    def two_lens_beamwaist(self, beamwaist, focal_length, focal_length2, dist_beamwidth_firstlens, lens23_seperation):
        #First calculate the beamwaist after the first lens
        new_beamwaist, new_beamwaist_loc = one_lens_optics_calculations.lens_beamwaist(self, beamwaist, focal_length, dist_beamwidth_firstlens)
        
        #Calculate beamwaist and beamwaist location after the second lens
        new_new_beamwaist, new_new_beamwaist_location = one_lens_optics_calculations.lens_beamwaist(self, new_beamwaist, focal_length2, lens23_seperation - new_beamwaist_loc)
        
        return new_new_beamwaist, new_new_beamwaist_location
