class SystemControlMockup:
    def __init__(self):
        self.probe_parameters = {
            "Single Langmuir Probe (SLP)": {
                "Floating Potential": 0.0,
                "Plasma Potential": 0.0,
                "Electron Saturation Current": 0.0,
                "Ion Saturation Current": 0.0,
                "Electron Temperature": 0.0,
                "Electron Density": 0.0,
                "Ion Temperature": 0.0,
                "Ion Density": 0.0,
                "Debye Length": 0.0,
                "Charged Particles in the Debye Sphere": 0.0,
            },
            "Double Langmuir Probe (DLP)": {
                "Ion Saturation Current": 0.0,
                "Electron Temperature": 0.0,
                "Electron Density": 0.0,
                "Ion Temperature": 0.0,
                "Ion Density": 0.0,
                "Debye Length": 0.0,
            },
            "Triple Langmuir Probe (TLP)": {
                "TLP-C": {
                    "Floating Potential": 0.0,
                    "Plasma Potential": 0.0,
                    "Electron Temperature": 0.0,
                    "Electron Density": 0.0,
                    "Ion Temperature": 0.0,
                    "Ion Density": 0.0,
                    "Debye Length": 0.0,
                },
                "TLP-V": {
                    "Floating Potential": 0.0,
                    "Plasma Potential": 0.0,
                    "Electron Saturation Current": 0.0,
                    "Ion Saturation Current": 0.0,
                    "Electron Temperature": 0.0,
                },
            },
            "Ion Energy Analyzer (IEA)": {
                "Floating Potential": 0.0,
                "Plasma Potential": 0.0,
                "Ion Saturation Current": 0.0,
                "Electron Temperature": 0.0,
                "Electron Density": 0.0,
                "Ion Temperature": 0.0,
                "Ion Density": 0.0,
                "Debye Length": 0.0,
            },
            "Hyperbolic Energy Analyzer (HEA)": {
                "Floating Potential": 0.0,
                "Plasma Potential": 0.0,
                "Ion Saturation Current": 0.0,
                "Electron Temperature": 0.0,
                "Electron Density": 0.0,
                "Ion Temperature": 0.0,
            }
        }

    def get_parameters_for_probe(self, probe_name):
        """
        Retrieve the parameters dictionary for the specified probe.

        :param probe_name: Name of the probe as a string.
        :return: Dictionary of parameters if probe exists, otherwise None.
        """
        return self.probe_parameters.get(probe_name, None)

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
    sys_control = SystemControlMockup()
    
    # Example: Print parameters for Single Langmuir Probe (SLP)
    sys_control.print_probe_parameters("Single Langmuir Probe (SLP)")
