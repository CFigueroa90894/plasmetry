# author: figueroa_90894@students.pupr.edu

[ #sweep_list
    [ #sweep 1
    [1, 2, 3, 2, 3], [1, 2, 3, 4, 5]
    ]
    , [], [] ]

[ #sweep_list
    [ #sweep 1
        (1, 2),
        (2, 3),
        (3, 4),
    ]
    , [], [] ]

import csv

class SweepParser:
    """Collection of utilities to parse sweeps from previous csv data."""
    
    # ----- PARSER METHODS ----- # 
    
    # PRIMARY PARSER
    @classmethod
    def parse_sweeps(cls, filepath:str)->list[list[list[int]]]:
        """The main functionality of the SweepParser. Accepts a file path to a CSV and
        returns a three-dimensional list of sweeps. Each sweep is a list, consisting of
        one current-sample list and one applied-voltage list. """
        raw_data = cls._load_csv(filepath)
        currents, voltages = cls._parse_raw_data(raw_data)
        return cls._slice_sweeps(currents, voltages)


    @classmethod
    def _load_csv(cls,
                 filepath:str=None,
                 newline_char:str='',
                 delimiter_char:str=',',
                 quote_char:str='|'):
        """Accepts a file path to a CSV and returns a list of its unparsed rows."""
        with open(filepath, newline=newline_char) as csvfile:
            dataReader = csv.reader(csvfile, delimiter=delimiter_char, quotechar=quote_char)
            raw_data = []
            for row in dataReader:
                raw_data.append(row)
            return raw_data

    @classmethod
    def _parse_raw_data(cls, raw_data) -> tuple[list[float]]:
        """Accepts a list of raw CSV rows. Assumes first and second columns
        correspond to current samples and applied biases, respectively.
        Returns two lists of parsed float values: current samples and applied biases."""
        current = []
        voltage = []
        for row in raw_data:
            try:
                current.append(float(row[0]))
                voltage.append(float(row[1]))
            except:
                pass
        return current, voltage

    # ----- SWEEP UTILS ----- #
    @classmethod
    def _find_sweep(cls, bias_list):
        """Accepts a list of applied voltages.
        Returns the length of the first sweep detected sweep."""
        if len(bias_list) == 0:
            raise ValueError("Bias list cannot be empty!")
        prev_bias = None    # store previous bias until drop is detected
        for count, bias in enumerate(bias_list):   # maintain a counter and iterate over biases
            if prev_bias is None:   # ignore first row
                pass
            # find the first drop in voltage
            elif prev_bias >= 0 and bias < 0:
                return count
            prev_bias = bias
        return len(bias_list)   # if only one sweep per list, return the entire length

    # Not tested
    @classmethod
    def _get_sweep_lengths(cls, current_list, voltage_list):
        """Accepts a list of current samples and a list of applied voltages.
        Returns a dictionary of validated sweep lengths.
        """

        # Initialize sweep lengths
        sweep_len = cls._find_sweep(voltage_list)
        current_len = len(current_list)
        voltage_len = len(voltage_list)
        
        # Pack dictionary
        lengths = {"sweep_len":sweep_len,
                   "current_len":current_len,
                   "voltage_len":voltage_len,}
        
        cls._validate_sweep_length(**lengths)
        return lengths

    # Not tested
    @classmethod
    def _get_sweep_counts(cls, sweep_len, current_len, voltage_len):
        """Accepts lengths of sweeps, current samples, and applied voltages.
        Returns a dictionary of validated sweep counts."""
        
        # Initialize sweep counts
        curr_sweep_count = current_len / sweep_len
        volt_sweep_count = voltage_len / sweep_len

        # Pack sweep counts
        sweep_counts = {"curr_sweep_count":curr_sweep_count,
                        "volt_sweep_count":volt_sweep_count}
        
        cls._validate_sweep_counts(**sweep_counts)
        return sweep_counts

    # Not tested
    @classmethod
    def _get_sweep_parameters(cls, current_list, voltage_list):
        """Accepts a list of current samples and a list of applied voltages.
        Returns a dictionary of sweep parameters."""
        
        lengths = cls._get_sweep_lengths(current_list=current_list,
                                         voltage_list=voltage_list)
        counts = cls._get_sweep_counts(**lengths)
        
        # Double-unpack each dictionary into a single merged dictionary.
        return {**lengths, **counts}

    # Not tested
    @classmethod
    def _slice_sweeps(cls, current_list, voltage_list):
        """Return a list of sweeps, where each sweep consists of
        one current list, and one voltage list."""

        # Initialize sweep lengths and counts
        sweep_param = cls._get_sweep_parameters(current_list=current_list,
                                                voltage_list=voltage_list)
        sweep_len = sweep_param["sweep_len"]            # number of samples per sweep
        sweep_count = sweep_param["curr_sweep_count"]   # number of sweeps

        sweep_list = []     # empty list to aggregate individual sweeps

        for sweep_index in range(sweep_count):
            # Calculate indexes
            start_index = sweep_index * sweep_len
            end_index = start_index + sweep_len + 1
            
            # Slice samples
            sweep_currents = current_list[start_index:end_index]
            sweep_voltages = voltage_list[start_index:end_index]

            # Append sweep
            sweep_list.append([sweep_currents, sweep_voltages])

        return sweep_list


        

        
        
    
    # ----- VALIDATION METHODS ----- #
    # Not tested
    @classmethod
    def _validate_sweep_length(cls, sweep_len, current_len, voltage_len):
        """Raise a ValueError if sweep lengths are invalid."""
        
        # Validate lengths
        if current_len != voltage_len:
            raise ValueError("Lengths of lists must be equal!")
        elif current_len % sweep_len != 0:
            raise ValueError("Number of current samples per sweep is not uniform!")
        elif voltage_len % sweep_len != 0:
            raise ValueError("Number of applied voltages per sweep is not uniform!")

    # Not tested
    @classmethod
    def _validate_sweep_counts(cls, curr_sweep_count, volt_sweep_count):
        """Raise a ValueError if sweep counts are invalid."""
        
        # Validate sweep counts
        if curr_sweep_count != volt_sweep_count:
            raise ValueError("Sweep counts are not equal!")
        elif type(curr_sweep_count) is not int:
            raise ValueError("Sweep count in current samples is not an integer!")
        elif type(volt_sweep_count) is not int:
            raise ValueError("Sweep count in applied voltages is not an integer!")
        

        

# ---- TESTS ---- # 
class SweepParserTests:
    
    sp = SweepParser    # create class shorthand

    @classmethod
    def lprint(cls, arr):
        for item in arr:
            print(item)

    @classmethod
    def test_load(cls):
        print("test_load()\n")
        new_path = 'src\\diagnostics\\calculations\\testing\\Feliz_A1 MirorSLP120200813T105858.csv'
        felix = cls.sp._load_csv(filepath=new_path,
                        newline_char='',
                        delimiter_char=',',
                        quote_char='|')
        cls.lprint(felix)

    @classmethod
    def test_parse_data(cls):
        print("test_parse_data()\n")
        new_path = 'src\\diagnostics\\calculations\\testing\\Feliz_A1 MirorSLP120200813T105858.csv'
        felix = cls.sp._load_csv(filepath=new_path,
                        newline_char='',
                        delimiter_char=',',
                        quote_char='|')
        data = cls.sp._parse_raw_data(felix)
        print("CURRENTS")
        cls.lprint(data[0])
        print("\n\nVOLTAGES")
        cls.lprint(data[1])

    @classmethod
    def test_find_sweep(cls):
        print("test_find_sweep()\n")
        sweep_3 = [-3, -2, -1, 0, 1, 2, -3, -2, -1, 0, 1, 2, -3, -2, -1, 0, 1, 2]
        sweep_2 = [-3, -2, -1, 0, 1, 2, -3, -2, -1, 0, 1, 2]
        sweep_1 = [-3, -2, -1, 0, 1, 2]
        sweep_0 = []

        sweeps = [sweep_1, sweep_2, sweep_3]
        for count, sweep in enumerate(sweeps):
            expected = 6
            received = cls.sp._find_sweep(sweep)
            print(f"Sweep_{count+1}\nExpected: {expected}\nRecieved: {received}\n\n")
            assert expected == received

        try:
            print("Sweep_0")
            print("Expected: ValueError")
            cls.sp._find_sweep(sweep_0)
            print("Recieved: No error was raised!")
        except ValueError:
            print(f"Recieved: Correct error was raised.")

    @classmethod       
    def run_tests(cls):
        # test_load()
        # test_parse_data()
        cls.test_find_sweep()

if __name__ == "__main__":
     SweepParserTests.run_tests()