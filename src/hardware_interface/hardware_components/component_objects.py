"""G3 - Plasma Devs
Layer 1 - Hardware Interface - Component Objects
    Defines classes for probe subcomponents, including basic sensors and amplifiers.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    VoltageSensor
    BaseAmp
    HighVoltAmp
    VoltageSweeper
    RelaySet
"""

# built-in imports
import sys
import os

from typing import Tuple

# ----- PATH HAMMER v3.0 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:
    """Resolve absolute imports by recursing into subdirs and appending them to python path."""
    # os delimeters
    win_delimeter, rpi_delimeter = "\\", "/"

    # locate project root
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    print(f"Path Hammer: {src_abs}")

    # select path delimeter
    if win_delimeter in src_abs: delimeter = win_delimeter
    elif rpi_delimeter in src_abs: delimeter = rpi_delimeter
    else: raise RuntimeError("Path Hammer could not determine path delimeter!")

    # validate correct top folder
    assert src_abs.split(delimeter)[-1*len(root_target):] == root_target
    
    # get subdirs, exclude unwanted
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split(delimeter)[-1] not in exclude]
    for dir in dirs: sys.path.append(dir)    # add all subdirectories to python path

if __name__ == "__main__":  # execute path hammer if this script is run directly
    path_hammer(2, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #


# local imports
from channel_objects import AnalogIn, AnalogOut, DigitalOut
from range_map import high_to_low


# ----- INPUT SUBCOMPONENTS ----- #
class VoltageSensor:
    """Implements a voltage sensor based on a differential amplifier.
    
    Attributes:
        # _input: AnalogIn - associated input channel
        # _gain: float - gain of associated diff amp

    Methods:
        + __init__() - initialize the sensor object
        + read(): float - return voltage measured by analog input
        # _division_read(): float - returns voltage divided by gain
        # _no_division_read(): float - returns the voltage, without dividing by gain
    """
    def __init__(self, gain:float, analog_in: AnalogIn):
        """Constructor for VoltageSensor, saves the given channel and gain.
        
        Arguments:
            gain: float - gain value of associated diff amp; used to divide voltage measures
            analog_in: AnalogIn - input channel from the diff amp
        """

        # Validate analog_in
        if not isinstance(analog_in, AnalogIn):
            err_msg = f"analog_in must be instance of AnalogIn!"
            err_msg += f" Given {type(analog_in)}"
            raise TypeError(err_msg)
        else:
            self._input = analog_in

        # Validate gain
        if gain == 0:
            raise ValueError("Gain cannot be zero!")

        # Select appropriate read function
        if gain == 1: # input does not require dividing by gain
            self.read = self._no_division_read
        else:         # inpuy requires division by gain
            self._gain = gain
            self.read = self._division_read

    # Overridden by constructor
    def read(self) -> float:
        """Returns the voltage measured by the associated differential amplifier."""
        raise NotImplementedError("VoltageSensor did not correctly override its read() method!")

    def _division_read(self) -> float:
        """Returns the voltage, corrected for gain."""
        return self._input.read() / self._gain

    def _no_division_read(self) -> float:
        """Returns voltage as is, without correcting for gain."""
        return self._input.read()

 
# ----- OUTPUT SUBCOMPONENTS ----- #
class BaseAmp:
    """Parent class for amplifier subclasses.
    
    Attributes:
        # _output: AnalogOut - the associated output channel
        # _dac_min: float - the minimum value expected by the amp's input
        # _dac_max: float - the maximum value expected by the amp's input
        # _amp_min: float - the minimum value produced at the amp's output
        # _amp_max: float - the maximum value produced at the amp's output

    Methods:
        + __init__() - initialize the object
    """
    def __init__(self, dac_range:dict, amp_range: dict, analog_out: AnalogOut):
        """Constructor for BaseAmp and its subclasses.
        
        Arguments:
            dac_range: dict - min and max of the DAC's output
            amp_range: dict - min and max of the amp's output
            analog_out: AnalogOut - output channel to the amplifier
        """
        
        # Validate analog_out
        if not isinstance(analog_out, AnalogOut):
            err_msg = f"analog_out must be instance of AnalogOut!"
            err_msg += f" Given {type(analog_out)}"
            raise TypeError(err_msg)
        else:
            self._output = analog_out
        
        # Save mapping ranges
        self._dac_min = dac_range['min']
        self._dac_max = dac_range['max']
        self._amp_min = amp_range['min']
        self._amp_max = amp_range['max']


class HighVoltAmp(BaseAmp):
    """Subclass of BaseAmp, associated with a high voltage amplifier.
    
    Attributes:
        ^# _output: AnalogOut - the associated output channel
        ^# _dac_min: float - the min volt expected by the amp's input
        ^# _dac_max: float - the max volt expected by the amp's input
        ^# _amp_min: float - the min volt produced at the amp's output
        ^# _amp_max: float - the max volt produced at the amp's output

    Methods:
        ^+ __init__() - constructor inherited from parent
        + write(float) - produce the desired voltage at the HV-amp's output
        + zero() - reset the amp's output to zero volts
    """

    def __init__(self, *args, **kwargs):
        """Constructor for HighVoltAmp class, inherited from BaseAmp
        
        Arguments:
            dac_range: dict - min and max of the DAC's output
            amp_range: dict - min and max of the amp's output
            analog_out: AnalogOut - output channel to the amplifier
        """
        super().__init__(*args, **kwargs)   # invoke parent constructor

    def write(self, voltage: float):
        """Sets the associated high voltage amplifier's output to the given value."""
        low_volt = self._translate(voltage)     # translate desired HV-out to required LV-in
        self._output.write(low_volt)            # output required LV to associated output channel

    def _translate(self, desired_high_voltage):
        """Obtain the required low voltage input to produce the desired high voltage output using
        the amp's and dac's min and max values."""
        # Translate using utils method and given ranges
        low_volt = high_to_low(
            high_val=desired_high_voltage,
            low_min=self._dac_min,
            low_max=self._dac_max,
            high_min=self._amp_min,
            high_max=self._amp_max
        )
        return low_volt
    
    def zero(self):
        zero_val = self._translate(0)   # low-volt stimulus to drive the amp's output to zero volts
        self._output.write(zero_val)


class VoltageSweeper(HighVoltAmp):
    """Subclass of HighVoltAmp, associated with a high voltage amplifier to perform voltage sweeps.
    
    The VoltageSweeper pre-computes the values of its voltage steps in order to save performance
    during diagnostics, avoiding calls to translate desired high voltage to required low voltage.

    Attributes:
        ^# _output: AnalogOut - the associated output channel, inherited from parent
        ^# _dac_min: float - the minimum value expected by the amp's input, inherited from parent
        ^# _dac_max: float - the maximum value expected by the amp's input, inherited from parent
        ^# _amp_min: float - the minimum value produced at the amp's output, inherited from parent
        ^# _amp_max: float - the maximum value produced at the amp's output, inherited from parent
        # _num_samples: int - steps voltage steps per sweep
        # _min_volt: float - the minimum voltage applied by the sweeper amp
        # _max_volt: float - the maximum voltage applied by the sweeper amp
        # _premap: Tuple[float] - premapped low voltage values to stimulate the sweeper amp's input 
    
    Methods:
        + __init__() - sweeper constructor
        ^+ zero() - reset the amp's output to zero volts
        + write(int) - produces the premapped high-voltage at the given index at the amp's output
        # _map_volts() - returns tuple of premapped low-voltage values
    """
    def __init__(self, num_samples:int, sweep_min:float, sweep_max, *args, **kwargs):
        """Constructor for VoltageSweeper class, saves own args and calls parent constructor.
        
        Arguments:
            dac_range: dict - min and max of the DAC's output
            amp_range: dict - min and max of the amp's output
            analog_out: AnalogOut - output channel to the amplifier
            num_samples: int - number of voltage steps to be performed by a single sweep
            sweep_min: float - the minimum voltage produced the start of a sweep
            sweep_max: float - the maximum voltage produced the end of a sweep
        """
        super().__init__(*args, **kwargs) # invoke parent constructor
        
        # Save arguments
        self._num_samples = num_samples
        self._min_volt = sweep_min
        self._max_volt = sweep_max

        # Pre-map desired high-volt steps to required low-volt steps
        self._premap = self._map_volts()

    def write(self, index: int) -> float:
        """Outputs the required low-voltage through the associated DAC channel, and returns
        the desired high-voltage that it will produce at the amp's output.
        
        Arguments:
            index: int - index to the corresponding, premapped voltage-value pair 
        """
        step = self._premap[index]  # access premapped value pairs
        self._output.write(step[0])    # drive the amp's input through the associated channel
        return step[1]                # return the applied high voltage for calculations

    def _map_volts(self) -> Tuple[float, float]:
        """Return a tuple of low-voltage and high-voltage value pairs.
        
        In each pair, index:0 corresponds to the required low-voltage, and index:1 to the desired
        high-voltage. To produce the desired high-voltage at the amp's output, its input must be
        driven with the required low-voltage.
        """
        # access protected attributes, makes reading the function easier
        high_max = self._max_volt
        high_min = self._min_volt
        num_samples = self._num_samples

        sweep_width = high_max - high_min   # width of sweep in volts; calculates increment
        num_increments = num_samples - 1    # number of increments per sweep
        hv_increment = sweep_width / num_increments     # desired high volt increment per step
        
        # list LV-HV step value pairs
        steps = []  # calculated value of each desired HV step and required LV step
        
        # generate each high voltage step and corresponding low voltage step
        for index in range(self._num_samples):
            high_volt_step = index*hv_increment + high_min  # calculate HV value of step
            low_volt_step = self._translate(high_volt_step) # translate into LV value of step
            steps.append((low_volt_step, high_volt_step))   # append steps to list

        # cast list to tuple and return
        return tuple(steps)


class RelaySet:
    """Defines a collection of relays as a set of digital output channels.
    
    Attributes:
        # relays: Tuple[DigitalOut] - collection of output channels for various relays

    Methods:
        + __init__() - initialize the object
        + set() - enable all relays in the collection
        + clear() - disable all relays in the collection
        # _validate_args(tuple) - verify all elements in args are valid
    """
    def __init__(self, digital_outputs: Tuple[DigitalOut]):
        """Initialize the RelaySet object with given tuple of digital output channels."""
        self._validate_args(digital_outputs)    # raise error if any element is not DigitalOut
        self._relays = digital_outputs          # save tuple to attribute

    def set(self):
        """Enable all relays in the set."""
        for relay in self._relays:
            relay.set()

    def clear(self):
        """Disable all relays in the set."""
        for relay in self._relays:
            relay.clear()

    def _validate_args(self, digital_outputs):
        """Iterate over args and raise an error if an item other than DigitalOut is found."""
        for item in digital_outputs:
            if not isinstance(item, DigitalOut):
                err_msg = f"RelaySet arguments only accept DigitalOut objects!"
                err_msg += f" Given {type(item)}"
                raise ValueError(err_msg)
