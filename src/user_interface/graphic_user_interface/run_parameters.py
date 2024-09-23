class RunParameters:
    def __init__(self):
        self.probe_parameters = {
                "slp": {
                "Floating Potential (Volts)": 0.5,
                "Plasma Potential (Volts)": 0.0,
                "Electron Saturation Current (Amperes)": 0.0,
                "Electron Temperature (eV)": 10.0,
                "Electron temperature (Joules)": 0,
                "Electron Density": 0.0,
                "Debye Length": 0.0,
                "Electrons in Debye Sphere": 200000
            },
                
            "dlp": {
                "Ion Saturation Current": 0.0,
                "Electron Temperature": 0.0,
                "Electron Density": 0.0,
                "Ion Temperature": 0.0,
                "Ion Density": 0.0,
                "Debye Length": 0.0
            },
            "tlc": {
                "Floating Potential": 0.0,
                "Plasma Potential": 0.0,
                "Electron Temperature": 0.0,
                "Electron Density": 0.0,
                "Ion Temperature": 0.0,
                "Ion Density": 0.0,
                "Debye Length": 0.0
            },
            "tlv": {
                "Floating Potential": 0.0,
                "Plasma Potential": 0.0,
                "Electron Saturation Current": 0.0,
                "Ion Saturation Current": 0.0,
                "Electron Temperature": 0.0
            },
            "iea": {
                "Floating Potential": 0.0,
                "Plasma Potential": 0.0,
                "Ion Saturation Current": 0.0,
                "Electron Temperature": 0.0,
                "Electron Density": 0.0,
                "Ion Temperature": 0.0,
                "Ion Density": 0.0,
                "Debye Length": 0.0
            },
            "hea": {
                "Floating Potential": 0.0,
                "Plasma Potential": 0.0,
                "Ion Saturation Current": 0.0,
                "Electron Temperature": 0.0,
                "Electron Density": 0.0,
                "Ion Temperature": 0.0
            }
        }

    def get_parameters_for_probe(self, probe_name):
        """
        Retrieve the parameters dictionary for the specified probe.

        :param probe_name: Name of the probe as a string.
        :return: Dictionary of parameters if probe exists, otherwise None.
        """
        return self.probe_parameters[probe_name]

    def print_probe_parameters(self, probe_name):
        """
        Print all parameters and their values for the specified probe.

        :param probe_name: Name of the probe as a string.
        """
        parameters = self.get_parameters_for_probe(probe_name)
        if parameters:
            print(f"Parameters for {probe_name}:")
            for param, value in parameters.items():
                print(f"{param}: {value}")
        else:
            print(f"No parameters found for probe: {probe_name}")


# Example usage:
if __name__ == "__main__":
    sys_control = RunParameters()
    
    # Example: Print parameters for Single Langmuir Probe (SLP)
    sys_control.print_probe_parameters("slp")
