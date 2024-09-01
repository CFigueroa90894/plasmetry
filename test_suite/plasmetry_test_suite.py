# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings

# built-in imports
import sys
import os

from unittest import defaultTestLoader, TestSuite, TextTestRunner

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
# modified to side step into src folder
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 1             # how many parent folders to reach /plasmetry/src

    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..') # absolute path to plasmetry/src
    src_abs += "\\src"   # custom: side step into src 
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__'] # get subdirs, exclude __pycache__
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: subdirectories appended to python path\n\n\n")
# ----- END PATH HAMMER ----- #


class PlasmetryTestSuite:
    """<...>"""
    def __init__(self,
                 modules,
                 loader=defaultTestLoader,
                 pattern='unittest*.py',
                 start_dir=None,
                 verbosity=2
                 ):
        """<...>"""
        print(f"PLASMETRY TEST SUITE INITIALIZED")
        self.module_names = modules
        self.loader = loader
        self.pattern = pattern
        self.directory = start_dir
        self.tests = TestSuite()
        # Verbosity:
        #   0 : print the bare minimum
        #   1 : print what test modules are being loaded
        #   2 : additionally, print individual result for each test
        #   3 : additionally, print loaded test cases and tests
        #   4 : additionally, print testrunner output
        self.verbosity = verbosity
        self.result = None

        if self.directory is None:
            self.directory = os.path.abspath(os.path.dirname(__file__)+'/../src') # absolute path to plasmetry/src

    def __collect_all_tests(self):
        print("LOADING TEST MODULES")
        for mod_name in self.module_names:
            self.__collect_test(mod_name)
        print("")

    def __collect_test(self, mod_name):
        code = self.__get_module(mod_name)
        msg = code['msg']
        load = code['load']
        module = code['module']
        if self.verbosity >= 1:
            print(f"\t{msg}")
        if load:
            new_tests = self.loader.loadTestsFromModule(module)
            if self.verbosity >= 3:
                self.__print_tests_in_testSuite(new_tests)
            self.tests.addTests(new_tests)

    def __print_tests_in_testSuite(self, test:TestSuite, level=0, char="\t"):
            pre = (level+1)*char
            if level == 1 and len(test._tests) > 0:
                testCase_name = self.__get_testCase_name(test._tests[0])
                print(f"{pre}Test Case: {testCase_name}")

            if type(test) is TestSuite:
                for testCase in test._tests:
                    self.__print_tests_in_testSuite(testCase, level + 1)
            else:
                test_name = self.__get_test_name(test)
                print(f"{pre}Test : {test_name}")

    def __get_test_name(self, test):
        return f"{str(test).split(" ")[0]}"

    def __get_testCase_name(self, test):
        return str(test.__class__).split("'")[-2]

    def __get_module(self, mod_name):
        msg = "!!!ERROR IN TEST SUITE!!!"
        load = False
        module = None
        try:
            module = __import__(mod_name)
            status = module.test_ready
            if status is False:
                msg = f"ERROR: LOAD ABORTED BY MODULE"
            elif status == "WIP":
                msg = f"WARNING: WIP"
                load = True
            elif status is True:
                msg = f"READY"
                load = True
            else:
                msg = f"ERROR: UNKNOWN TEST CODE"
        except ModuleNotFoundError:
            msg = f"ERROR: MODULE NOT FOUND"
        finally:
            return {"msg":f"{msg}: {mod_name}", "load":load, "module": module}

    def __get_errors(self, results):
        err = {}
        for error in results.errors: # tuple(obj, reason)
            err_case = self.__get_testCase_name(error[0])
            err_name = self.__get_test_name(error[0])
            err_reason = error[1].split('\n')[-2]
            err[err_name] = {"case": err_case, "reason": err_reason}
        return err
    
    def __get_skip(self, results):
        skip = {}
        for skipped in results.skipped: # tuple(obj, reason)
            skip_case = self.__get_testCase_name(skipped[0])
            skip_name = self.__get_test_name(skipped[0])
            skip_reason = skipped[1]
            skip[skip_name] = {"case": skip_case, "reason": skip_reason}
        return skip
    
    def __get_fail(self, results):
        fail = {}
        for failure in results.failures: # tuple(obj, reason)
            fail_case = self.__get_testCase_name(failure[0])
            fail_name = self.__get_test_name(failure[0])
            fail_reason = failure[1].split('\n')[-2]
            fail[fail_name] = {"case": fail_case, "reason": fail_reason}
        return fail
    
    def __get_unexpected_success(self, results):
        succ = {}
        for success in results.unexpectedSuccesses: # obj
            succ_case = self.__get_testCase_name(success)
            succ_name = self.__get_test_name(success)
            succ[succ_name] = {"case": succ_case, "reason": "UNEXPECTED SUCCESS"}
        return succ
                
    def __get_tests_ran(self, results) -> list[str]:
        ran  = []
        for test in results.collectedDurations:  # tuple(str, time) 
            ran.append(test[0].split(" ")[0])
        return ran

    def __process_results(self, results):
        out = []
        tests = self.__get_tests_ran(results)
        skipped = self.__get_skip(results)
        failure = self.__get_fail(results)
        errors = self.__get_errors(results)
        unexpected = self.__get_unexpected_success(results)

        out = []
        for test in tests:
            entry = None
            if test in failure:
                entry = self.__format_output("FAIL", test, failure)
            elif test in errors:
                entry = self.__format_output("ERROR", test, errors)
            elif test in unexpected:
                entry = self.__format_output("FAIL", test, unexpected)
            else:
                entry = self.__format_output("ok", test)
            out.append(entry)
        for skip in skipped:
            out.append(self.__format_output("skip", skip, skipped))
        return out

    def __format_output(self, prefix, test_name, meta_data=None):
        out = f"{prefix}  ...  {test_name}"
        if meta_data is not None:
            meta = meta_data[test_name]
            test_case = meta["case"]
            reason = meta["reason"]
            out += f"  in  {test_case}"
            if reason is not None:
                out += f"  ...  {reason}"
        return out

    def __run(self):
        runner = TextTestRunner(verbosity=self.verbosity-2)
        raw_results = runner.run(self.tests)
        results = self.__process_results(raw_results)
        if self.verbosity >= 2:
            print("")
            self.__lprint(results)
        print("\nTESTS COMPLETE\n")
        return results

    def __lprint(self, lines, char=""):
        for line in lines:
            print(f"{char}{line}")

    def execute(self):
        self.__collect_all_tests()
        return self.__run()


def main():
    # Module names to test here
    test_mods = [
        "unittest_probe_factory",
        "unittest_slp_dlp",
        "unittest_hea_iea",
        "unittest_tlc_tlv",
        "unittest_probe_operation"
    ]
    suite = PlasmetryTestSuite(modules=test_mods)
    suite.execute()

if __name__ == "__main__":
    main()