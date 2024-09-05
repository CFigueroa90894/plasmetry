import unittest
from BaseCase import BaseCase

class GlobalTestCases(BaseCase):    
    
    parameters = {}
    probe_equations = []
    
          
    @classmethod
    def set_probe_type(cls, equations, parameters):
        GlobalTestCases.probe_equations = equations
        GlobalTestCases.parameters = parameters
        
    def test_1_filter_current(self):
        
        """Test the filter_current function for all implementations"""
        
        # For loop thoough each equation, to identify the one used in this test case
        for equation in GlobalTestCases.probe_equations:
            if 'filter_current' == equation.__name__:
                
                # Running equation with parameters attribute as argument
                equation(GlobalTestCases.parameters)
                
                # Verifying that the expected parameter key was generated
                self.assertIn('Filtered current', GlobalTestCases.parameters)
                
                # Verifying that the new list is not empty
                self.assertGreater(len(GlobalTestCases.parameters['Filtered current']), 0, "Filtered current list cannot be empty.")
                break
        

    def test_2_get_floating_and_plasma_potential(self):
        
        """Test the get_floating_and_plasma_potential function used for SLP calculations"""
        
        # For loop thoough each equation, to identify the one used in this test case
        for equation in GlobalTestCases.probe_equations:
            if 'get_floating_and_plasma_potential' == equation.__name__:
                
                # Running equation with parameters attribute as argument
                equation(GlobalTestCases.parameters)
                
                # Verifying that the expected parameter keys were generated
                self.assertIn('Floating potential', GlobalTestCases.parameters)
                self.assertIn('Floating potential index', GlobalTestCases.parameters)
                self.assertIn('Plasma potential', GlobalTestCases.parameters)
                self.assertIn('Plasma potential index', GlobalTestCases.parameters)
                
                # Verifying that the plasma potential is a non-negative value
                self.assertGreaterEqual(GlobalTestCases.parameters['Plasma potential'], 0, "Plasma potential should be non-negative")
                
                # Verifying that the floating potential index is within the expected range
                self.assertTrue(0 <= GlobalTestCases.parameters['Floating potential index'] \
                                <  GlobalTestCases.parameters['Plasma potential index'] \
                                , "Floating potential index should be less than plasma \
                                   potential index and greater than 0")
                
                # Verifying that the Plasma potential index is not greater than expected
                self.assertTrue(GlobalTestCases.parameters['Plasma potential index'] < len(GlobalTestCases.parameters['Bias']),  "Plasma potential index is too large.")
                break
            
    def test_3_get_electron_saturation_current(self):
        
        """Test the get_electron_saturation_current function"""

        # For loop thoough each equation, to identify the one used in this test case
        for equation in GlobalTestCases.probe_equations:
            if 'get_electron_saturation_current' == equation.__name__:
                
                # Running equation with parameters attribute as argument
                equation(GlobalTestCases.parameters)
                
                # Verifying that the expected parameter key was generated
                self.assertIn('Electron saturation current', GlobalTestCases.parameters)
                
                # Veriifying the electron saturation current is in the expected position within the filtered current list
                self.assertEqual(GlobalTestCases.parameters['Electron saturation current'], GlobalTestCases.parameters['Filtered current'][GlobalTestCases.parameters['Plasma potential index']])
                
                # Verifying that the electron saturation current is a positive value.
                self.assertGreater(GlobalTestCases.parameters['Electron saturation current'], 0, "Electron saturation current should be positive.")
                break
                
    def test_4_get_ion_saturation_current(self):
        
        """Test the get_electron_saturation_current function"""
        
        # For loop thoough each equation, to identify the one used in this test case
        for equation in GlobalTestCases.probe_equations:
            if 'get_ion_saturation_current' == equation.__name__:
            
                # Running equation with parameters attribute as argument
                equation(GlobalTestCases.parameters)
                
                # Verifying that the expected parameter key was generated
                self.assertIn('Ion saturation current', GlobalTestCases.parameters)
                
                # Verifying that the ion saturation current is a negative value
                self.assertLess(GlobalTestCases.parameters['Ion saturation current'],0, "Ion saturation current should be negative.")
                
    def test_5_get_electron_temperature(self):
        
        """Test the get_electron_temperature function"""
        
        # For loop thoough each equation, to identify the one used in this test case
        for equation in GlobalTestCases.probe_equations:
            if 'get_electron_temperature' == equation.__name__:
                
                # Running equation with parameters attribute as argument
                equation(GlobalTestCases.parameters)
                
                # Verifying that the expected parameter keys were generated
                self.assertIn('Electron temperature (eV)', GlobalTestCases.parameters)
                self.assertIn('Electron temperature (Joules)', GlobalTestCases.parameters)
                
                # Verifying that the calculated temperatures are positive values
                self.assertGreater(GlobalTestCases.parameters['Electron temperature (eV)'], 0, "Electron temperature (eV) should be positive")
                self.assertGreater(GlobalTestCases.parameters['Electron temperature (Joules)'], 0, "Electron temperature (Joules) should be a positive value.")
                break
       
    def test_6_get_particle_density(self):
        
        """Test the get_particle_density global function"""
        for equation in GlobalTestCases.probe_equations:
            if 'get_particle_density' == equation.__name__:
                
                # Running equation with parameters attribute as argument
                equation(GlobalTestCases.parameters)
                # Verifying if SLP or EA density was generated
                if 'Electron saturation current' in GlobalTestCases.parameters:
                    # Verifying that the expected parameter key was generated
                    self.assertIn('Electron density', GlobalTestCases.parameters)
                    
                    # Verifying that the calculated density is a positive values
                    self.assertGreater(GlobalTestCases.parameters['Electron density'], 0, "Electron density should be a positive value.")
            
                else:
                    print(GlobalTestCases.parameters['Particle density'])
                    # Verifying that the expected parameter key was generated
                    self.assertIn('Particle density', GlobalTestCases.parameters)
                    
                    # Verifying that the calculated density is a positive values
                    self.assertGreater(GlobalTestCases.parameters['Particle density'], 0, "Particle density should be a positive value.")
                    
                    
       
    def test_7_get_debye_length(self):
        print()
        
        
    def test_8_get_number_of_electrons(self):
        print()
        
if __name__ == '__main__':
    unittest.main(verbosity=2)