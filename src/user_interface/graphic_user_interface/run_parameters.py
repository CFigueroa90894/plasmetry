""" G3 - Plasma Devs
Layer 4 - User Interface - Run Parameters
    <...>

author: <-------------------------
author: <-------------------------

status: DONE

Classes:
    RunParameters

"""

class RunParameters:
    """<.......>
    
    Attributes:
        + probe_parameters
    
    Methods:
        + __init__()
        + get_parameters_for_probe()
        + print_probe_parameters()

    """
    def __init__(self):
        self.probe_parameters = {
                "slp": [
                "Floating Potential (Volts)",
                "Plasma Potential (Volts)",
                "Electron Saturation Current (Amperes)",
                "Electron Temperature (eV)",
                "Electron temperature (Joules)",
                "Electron Density (m<sup>-3</sup>)",
                "Debye Length (Meters)",
                "Number of electrons"
            ],
                
            "dlp": [
                "Ion Saturation Current (Amperes)",
                "Electron Temperature (eV)",
                "Electron temperature (Joules)",
                "Electron Density (m<sup>-3</sup>)",
                "Debye Length  (Meters)",
                "Number of electrons"
            ],
            "tlc": [
                'Ion saturation current (Amperes)',
                "Electron Temperature (eV)",
                "Electron Temperature (Joules)",
                "Electron Density (m<sup>-3</sup>)",
            ],
            "tlv": [
                "Electron Temperature (eV)",
                "Electron Temperature (Joules)",
                "Electron Density (m<sup>-3</sup>)",
            ],
            "iea": [
            "Particle saturation current (Amperes)",
            "Particle temperature (eV)",
            "Particle temperature (Joules)",
            "Particle density (m<sup>-3</sup>)"

            ],
            "hea": [
            "Particle saturation current (Amperes)",
            "Particle temperature (eV)",
            "Particle temperature (Joules)",
            "Particle density (m<sup>-3</sup>)"

        ]
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
