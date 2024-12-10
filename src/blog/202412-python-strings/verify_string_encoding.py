"""Using CPython is assumed.

Dirty numerical verification that my understanding on PEP393 and the CPython code is
correct.

"""

import ctypes
import random
import sys
import unicodedata


class Pep393VerifyEncoding:
    """Numerically verify encoding used in PEP 393.

    Warning
    --------
    This is a one-time-test only. The code is not organised well!

    """

    def __init__(self, numb_tests=100_000):
        self.numb_tests = numb_tests
        self.max_code_poit = 1114112

        self.data = {
            cp: unicodedata.category(chr(cp)) for cp in range(self.max_code_poit)
        }
        self.categories = set(self.data.values())
        self.categories_to_include = self.categories - {"Cs"}

    def verify(self):
        self.verify_case1()
        self.verify_case2()
        self.verify_case3()
        self.verify_case4()
        self.verify_surrogate_points_fail_utf32()
        self.verify_nonsurrogate_points_ok_utf32()

    def verify_surrogate_points_fail_utf32(self):
        """

        Cs code points can happily be encoded using utf-32 but there is a problem
        because, given a code point CP (i.e., CP is an integer), we use chr(CP) and
        the output of chr(.) cannot be trusted because there are no characters
        associated with a Cs point.

        """
        k = 0
        surogate_code_points = self.get_surogate_code_points()
        for cp in surogate_code_points:
            try:
                self.verify_one_code_point(cp, "utf-32")
            except:
                k += 1
        assert k == len(surogate_code_points)

    def verify_nonsurrogate_points_ok_utf32(self):
        for cp in self.get_nonsurogate_code_points():
            self.verify_one_code_point(cp, "utf-32")

    def verify_one_code_point(self, code_point, encoding="utf-32"):
        character = chr(code_point)
        return character.encode(encoding)

    def get_surogate_code_points(self):
        return [k for k, v in self.data.items() if v == "Cs"]

    def get_nonsurogate_code_points(self):
        return [k for k, v in self.data.items() if v != "Cs"]

    def verify_case1(self):
        range1 = self.filter_code_points(0, 2**7 - 1)
        range2 = self.filter_code_points(0, 2**7 - 1)

        for _ in range(self.numb_tests):
            i1 = random.sample(range1, 1)[0]
            i2 = random.sample(range2, 1)[0]
            s = chr(i1) + chr(i2)

            e1 = self.memory_dump(s)[40:-1].hex()
            # utf-8 consides with ascii in case 1
            e2 = s.encode("ascii").hex()
            e3 = s.encode("utf-8").hex()
            assert e1 == e2
            assert e1 == e3

    def verify_case2(self):
        range1 = self.filter_code_points(0, 2**8 - 1)
        range2 = self.filter_code_points(2**7, 2**8 - 1)

        for _ in range(self.numb_tests):
            i1 = random.sample(range1, 1)[0]
            i2 = random.sample(range2, 1)[0]
            s = chr(i1) + chr(i2)

            e1 = self.memory_dump(s)[56:-1].hex()
            e2 = s.encode("latin-1").hex()
            e3 = s.encode("utf-16-le").hex()
            e3 = e3[:2] + e3[-4:-2]
            assert e1 == e2
            assert e1 == e3

    def verify_case3(self):
        range1 = self.filter_code_points(256, 2**16 - 1)
        range2 = self.filter_code_points(0, 2**16 - 1)

        for _ in range(self.numb_tests):
            i1 = random.sample(range1, 1)[0]
            i2 = random.sample(range2, 1)[0]
            s = chr(i1) + chr(i2)

            e1 = self.memory_dump(s)[56:-2].hex()
            e2 = s.encode("utf-16-le").hex()
            assert e1 == e2

    def verify_case4(self):
        range1 = self.filter_code_points(2**16 - 1, self.max_code_poit)
        range2 = self.filter_code_points(0, self.max_code_poit)

        for _ in range(self.numb_tests):
            i1 = random.sample(range1, 1)[0]
            i2 = random.sample(range2, 1)[0]
            s = chr(i1) + chr(i2)

            e1 = self.memory_dump(s)[56:-4].hex()
            e2 = s.encode("utf-32-le").hex()
            assert e1 == e2

    @staticmethod
    def memory_dump(s):
        address_of_s = id(s)  # assuming CPython
        buffer_s = (ctypes.c_char * sys.getsizeof(s)).from_address(address_of_s)
        return bytes(buffer_s)

    def filter_code_points(self, lb=0, ub=None):
        """Filter code points.

        https://www.compart.com/en/unicode/category
        """
        if ub is None:
            ub = self.max_code_poit

        selected_code_points = []
        for cp, category in self.data.items():
            if category in self.categories_to_include:
                if cp <= ub and cp >= lb:
                    selected_code_points.append(cp)

        return selected_code_points


def cast_back(x):
    return ctypes.cast(id(x), ctypes.py_object).value
    return ctypes.cast(id(x), ctypes.py_object).value


def main():
    v = Pep393VerifyEncoding()
    v.verify()


if __name__ == "__main__":
    main()
