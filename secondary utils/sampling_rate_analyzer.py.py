# author: figueroa_90894@students.pupr.edu

import sys
import os

# config
def get_file(file_path):
    file = open(file_path, 'r')
    return file

def get_args():
    args = sys.argv
    # if len(args) != 2:
    #     raise RuntimeError("File path must be specified! Only one file may be processed at a time!")
    # return args

def get_lines(log):
    return log.get_lines()

def find_analog_out(lines):
    out = []
    for line in lines:
        if "CountHW" in line and "Aout" in line:
            out.append(line)
    return out

def get_val(lines):
    out = []
    for line in lines:
        split = line.split(' ')
        for field in split:
            if "val" in field:
                out.append(split)
    return out

def parse_val(splits):
    div = 10000
    out = []
    for split in splits:
        for i in range(len(split)):
            if "val" in split[i]:
                val = split[i]
                fl = float(val.split(":")[-1])*div
                fl = int(fl)/div
                split[i] = fl
                out.append(split)
    out.pop(0)  # pop first zero
    out.pop()   # pop last dac zero
    out.pop()   # pop last amp zero
    return out

def parse_time(arr):
    for a in arr:
        tim = float(a[-1].split(':')[-1])
        a[-1] = tim
    return arr

def sweep_slice(parsed):
    sweeps = []
    var_arr = []
    prev = None
    for par in parsed:
        if prev is None:
            var_arr.append(par)
        elif prev > par:
            sweeps.append(var_arr)
            var_arr = [par]
        else:
            var_arr.append(par)
        prev = par
    sweeps.append(var_arr)
    return sweeps

def sweep_lens(sweeps):
    lengths = []
    for sweep in sweeps:
        lengths.append(len(sweep))
    return lengths

def validate_lens(lens):
    condition = True
    for l in lens:
        condition = lens[0] == l and condition
    return condition

def split_all(lines):
    out = []
    for line in lines:
        split = line.split(' ')
        out.append(split)
    return out

def trim_par(parsed):
    out = []
    for par in parsed:
        out.append(par[-3:-1])
    return out

def get_times(sweeps):
    out = []
    for sweep in sweeps:
        for sw in sweep:
            tim = sw
            out.append(tim)
    return out

def get_diff(tims):
    out = []
    for i in range(1, len(tims)):
        diff = tims[i][1] - tims[i-1][1]
        out.append(diff)
    return out

def average(arr):
    tot = 0
    for a in arr:
        tot += a
    return tot/len(arr)

def lprint(arr, prefix='', suffix=''):
    for a in arr:
        print(f"{prefix}{a}{suffix}")

def popper(inp):
    arr = inp[:]
    for i in range(len(arr)):
        x = arr.pop(0)[0]
        if x == 2:
            break

    for j in range(len(arr)):
        y = arr.pop()[0]
        if y == 2:
            break
    return arr

def sampling_interval(lines):
    for line in lines:
        if "SAMPLING INTERVAL" in line:
            return line

def convert_nano(arr):
    out = []
    for a in arr:
        out.append(a/1000000000)
    return out

def main():
    args = get_args()
    # file_path = args[1]
    # file = get_file(file_path)
    file = get_file(ABS_PATH)
    lines = file.readlines()
    # lprint(lines)
    
    interval = sampling_interval(lines)
    print(interval)

    a_out = find_analog_out(lines)
    # lprint(a_out)

    splits = split_all(a_out)
    parsed = parse_val(splits)
    # lprint(parsed)

    trimmed = trim_par(parsed)
    # lprint(trimmed)

    popped = popper(trimmed)
    # lprint(popped)

    tim_parsed = parse_time(popped)
    # tim_parsed = parse_time(trimmed)
    # lprint(tim_parsed)

    sweeps = sweep_slice(tim_parsed)
    # lprint(sweeps)

    lens = sweep_lens(sweeps)
    # lprint(lens)
    same = validate_lens(lens)
    assert same

    tims = get_times(sweeps)
    # lprint(tims)
    diffs = get_diff(tims)
    # lprint(diffs)

    seconds = convert_nano(diffs)

    print("DIFFERENCES")
    lprint(seconds, prefix='\t')
    
    avg = average(seconds)
    print("AVERAGE INTERVAL", avg)
    print("AVERAGE RATE    ", 1/avg)
    

F_NAME = "TEST_2024-09-19 20_56_57.742978_TIMED.txt"

DELIMETER = '/'
DIR_PATH = f'test_logs{DELIMETER}{F_NAME}'
ABS_PATH = os.path.abspath(DIR_PATH)

print(ABS_PATH)

if __name__ == "__main__":
    main()