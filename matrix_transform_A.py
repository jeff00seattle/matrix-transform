#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import sys
import getopt
import logging
import random
import string
import json
import copy

class JaggedMatrixGenerator(object):
    """Generate a Jagged Matrix and fill it with random characters as defined by available string sequences.
    """

    SEQUENCE = ["ascii_letters", "ascii_lowercase", "ascii_uppercase",
           "digits", "hexdigits", "octdigits", "printable", "punctuation",
           "whitespace"]

    @classmethod
    def _sequence(cls, sequence):
        assert sequence in cls.SEQUENCE
        if "ascii_letters" == sequence:
            return string.ascii_letters
        if "ascii_lowercase" == sequence:
            return string.ascii_lowercase
        if "ascii_uppercase" == sequence:
            return string.ascii_uppercase
        if "digits" == sequence:
            return string.digits
        if "hexdigits" == sequence:
            return string.hexdigits
        if "octdigits" == sequence:
            return string.octdigits
        if "printable" == sequence:
            return string.printable
        if "punctuation" == sequence:
            return string.punctuation
        if "whitespace" == sequence:
            return string.whitespace

    @property
    def matrix(self):
        return self.__matrix
    @matrix.setter
    def matrix(self, value):
        self.__matrix = value

    #
    # Initialize
    #
    def __init__(self, kw={}):
        """Initialize
        """
        cls = self.__class__

        self.matrix = None

        self.row_length_min = kw.get("row-length-min", 4)
        self.row_length_max = kw.get("row-length-max", 8)
        assert(self.row_length_max >= self.row_length_min)

        self.rows_count_min = kw.get("rows-count-min", 4)
        self.rows_count_max = kw.get("rows-count-max", 8)
        assert(self.rows_count_max >= self.rows_count_min)

        self.sequence = cls._sequence(kw.get("sequence", "ascii_uppercase"))

    def __str__(self):
        """Pretty print plain rows with seat reservations
        """
        assert self.matrix

        s = [[str(e) for e in row] for row in self.matrix]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = "\t".join("{{:{}}}".format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        return "\n" + "\n".join(table)

    def generate(self):
        self.matrix = [[random.choice(self.sequence)
                        for _ in range(random.randint(self.row_length_min, self.row_length_max))]
                            for _ in range(random.randint(self.rows_count_min, self.rows_count_max))]

        return self.matrix

    @staticmethod
    def serialize(matrix):
        assert matrix
        return json.dumps(matrix)

    @staticmethod
    def deserialize(matrix_serialize):
        assert matrix_serialize
        return json.loads(matrix_serialize)


class MatrixTransformA(object):
    """Transform rows and columns based upon matching target character.
    """

    @property
    def verbose(self):
        return self.__verbose
    @verbose.setter
    def verbose(self, value):
        self.__verbose = value

    @property
    def case_sensitive(self):
        return self.__case_sensitive
    @case_sensitive.setter
    def case_sensitive(self, value):
        self.__case_sensitive = value

    @property
    def matrix(self):
        return self.__matrix
    @matrix.setter
    def matrix(self, value):
        self.__matrix = value

    @property
    def matrix_transformed(self):
        return self.__matrix_transformed
    @matrix_transformed.setter
    def matrix_transformed(self, value):
        self.__matrix_transformed = value

    @property
    def target(self):
        return self.__target
    @target.setter
    def target(self, value):
        self.__target = value

    @property
    def logger(self):
        return self.__logger
    @logger.setter
    def logger(self, value):
        self.__logger = value

    def _logger_config(self):
        """Logger config"""
        self.logger = logging.getLogger("MatrixTransformation")

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.logger.setLevel(logging.INFO)
        if self.verbose:
            self.logger.setLevel(logging.DEBUG)

    #
    # Initialize
    #
    def __init__(self, kw):
        """Initialize
        """
        self.verbose = kw.get("verbose", False)
        matrix_serialized = kw.get("matrix", None)
        self.matrix = JaggedMatrixGenerator.deserialize(matrix_serialized) if matrix_serialized else None
        self.target = kw.get("target", None)
        self.case_insensitive = kw.get("case-insensitive", False)

        self._logger_config()

    def match_target(self, value):
        return str(self.target).lower() == str(value).lower() if self.case_insensitive else self.target == value

    def transform(self):
        numrows_max = len(self.matrix)  # Number rows in matrix
        numcols_max = len(self.matrix[0])  # Number columns in first row of matrix

        rows = [False for i in range(numrows_max)]
        columns = [False for i in range(numcols_max)]

        for i_row, v_row in enumerate(self.matrix):
            # print("row: {}: {}".format(i_row, v_row))
            for i_column, v_column in enumerate(v_row):
                # print("column: {}: {}".format(i_column, v_column))

                numcols = len(v_row)
                # print(f"{numcols_max}:{numcols}:{i_column}")
                if numcols_max < numcols:
                    extend_numcols = numcols - numcols_max
                    numcols_max = numcols
                    extend_columns = [False for i in range(extend_numcols)]
                    columns.extend(extend_columns)
                    # print("extending: ", columns)

                if self.match_target(v_column):
                    rows[i_row] = True
                    columns[i_column] = True

        self.logger.info("rows:    {0}: {1}".format(numrows_max, rows))
        self.logger.info("columns: {0}: {1}".format(numcols_max, columns))

        self.matrix_transformed = copy.copy(self.matrix)
        # print(self.present_transformed)

        for i_row, v_row in enumerate(self.matrix_transformed):
            for i_column, v_column in enumerate(v_row):
                # self.logger.info(
                #     "{}: {}: {}".format(i_row, len(rows), rows)
                # )
                assert i_row >= 0
                assert i_row < len(rows)
                # self.logger.info(
                #     "{}: {}: {}".format(i_column, len(columns), columns)
                # )
                assert i_column >= 0
                assert i_column < len(columns)
                if rows[i_row] or columns[i_column]:
                    self.matrix_transformed[i_row][i_column] = self.target

    @property
    def present_original(self):
        matrix_str = "\n"
        for i_row, v_row in enumerate(self.matrix):
            matrix_str += "{} : {}\n".format(i_row, v_row)
        self.logger.info("Original JaggedMatrixGenerator:\n{0}\n".format(matrix_str))

    @property
    def present_transformed(self):
        matrix_str = "\n"
        for i_row, v_row in enumerate(self.matrix_transformed):
            matrix_str += "{} : {}\n".format(i_row, v_row)
        self.logger.info("Transformed JaggedMatrixGenerator:\n{0}\n".format(matrix_str))

def main():
    matrix = ""
    target = ""
    sequence = "ascii_uppercase"
    case_insensitive = False
    usage = ("""Usage: {0} 
        [-v | --verbose] 
        [-h | --help] 
        --matrix string
        --target string
        --case-insensitive
        --sequence {1}
    --matrix: Strigified 2-D Jagged Array, If not provided then random is generated.
    --target: Target matrix transformation with specific character [Required]
    --case-insensitive: Be case-insensitive when targeting specific character, Default: {2}
    --sequence: If random matrix is generated this uses this sequence, Default: '{3}'
    """).format(sys.argv[0], JaggedMatrixGenerator.SEQUENCE, case_insensitive, sequence)

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hv",
            ["help", "verbose", "matrix=", "target=", "case-insensitive", "sequence="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        print(usage)
        sys.exit(1)

    kw = {}

    for opt, val in opts:
        if opt in ("-v", "--verbose"):
            kw["verbose"] = True
        elif opt in ("-h", "--help"):
            print(usage)
            sys.exit(0)
        elif opt in ("--matrix"):
            kw["matrix"] = str(val)
        elif opt in ("--target"):
            kw["target"] = str(val)
        elif opt in ("--case-insensitive"):
            kw["case-insensitive"] = True
        elif opt in ("--sequence"):
            kw["sequence"] = str(val)

    if "target" not in kw:
        print("%s: Provide --target" % sys.argv[0])
        print(usage)
        sys.exit(2)

    if "case-insensitive" not in kw:
        kw["case-insensitive"] = case_insensitive

    if "sequence" not in kw:
        kw["sequence"] = sequence

    if "matrix" not in kw:
        matrix = JaggedMatrixGenerator(kw)
        matrix.generate()
        kw["matrix"] = JaggedMatrixGenerator.serialize(matrix.matrix)

    assert "matrix" in kw
    assert "target" in kw
    assert "case-insensitive" in kw

    plane_reservations = MatrixTransformA(kw)
    plane_reservations.present_original
    plane_reservations.transform()
    plane_reservations.present_transformed


if __name__ == "__main__":
    main()