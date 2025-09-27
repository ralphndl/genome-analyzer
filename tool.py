#!/usr/bin/env python3
import sys
import math

# file handling

class BaseFile:
    def __init__(self, path):
        self.path = path

class SegmentFile(BaseFile):
    def __init__(self, path):
        super().__init__(path)
        self.segments = self._read_segments()

    def _read_segments(self):
        segs = []
        with open(self.path) as inputFile:
            for line in inputFile:
                if not line.strip():
                    continue
                start, end = line.strip().split("\t") # cleanup line and split by tab
                segs.append((int(start), int(end)))
        return segs

class FunctionFile(BaseFile):
    def values(self): # avoid to load the full data set, therefore go for generator
        with open(self.path) as inputFile:
            for line in inputFile:
                yield float(line.strip()) # just cleanup the line

# analyzer

class Analyzer:
    def __init__(self, file1, file2):
        self.inputFile1 = file1
        self.inputFile2 = file2

    def run(self):
        if isinstance(self.inputFile1, SegmentFile) and isinstance(self.inputFile2, SegmentFile): # detected two segment files, do the overlap calculation
            return self._overlap_segments()
        elif isinstance(self.inputFile1, FunctionFile) and isinstance(self.inputFile2, FunctionFile): # detected two function files, do the calculate person
            return self._pearson()
        elif isinstance(self.inputFile1, SegmentFile) and isinstance(self.inputFile2, FunctionFile): # detected segment and function file -> calculate mean
            return self._mean_over_segments(self.inputFile1, self.inputFile2)
        elif isinstance(self.inputFile1, FunctionFile) and isinstance(self.inputFile2, SegmentFile): # detected function and segment file -> calculate mean
            return self._mean_over_segments(self.inputFile2, self.inputFile1)
        else:
            raise ValueError("file types not supported")

    def _overlap_segments(self): # returns the count of overlapping segments
        a, b = self.inputFile1.segments, self.inputFile2.segments
        i, j = 0, 0
        total = 0
        while i < len(a) and j < len(b):
            s1, e1 = a[i]
            s2, e2 = b[j]
            start = max(s1, s2)
            end = min(e1, e2)
            if start < end:
                total += end - start
            if e1 < e2:
                i += 1
            else:
                j += 1
        return total

    def _pearson(self): # compute the pearson correlation between two files
        n = 0
        sumx = sumy = sumxx = sumyy = sumxy = 0.0
        for x, y in zip(self.inputFile1.values(), self.inputFile2.values()): # just do the math
            n += 1
            sumx += x
            sumy += y
            sumxx += x*x
            sumyy += y*y
            sumxy += x*y
        num = n*sumxy - sumx*sumy
        den = math.sqrt((n*sumxx - sumx*sumx) * (n*sumyy - sumy*sumy))
        if den == 0:
            return 0.0
        return num / den

    def _mean_over_segments(self, segmentFile, functionFile): # returns the mean from all positions inside a segment or 0
        segs = segmentFile.segments
        k = 0
        total = 0.0
        count = 0
        for pos, val in enumerate(functionFile.values()):
            while k < len(segs) and pos >= segs[k][1]:
                k += 1
            if k >= len(segs):
                break
            if segs[k][0] <= pos < segs[k][1]:
                total += val
                count += 1
        return total / count if count > 0 else 0.0

# app

def load_file(path):
    if path.endswith(".s"):
        return SegmentFile(path)
    elif path.endswith(".f"):
        return FunctionFile(path)
    else:
        raise ValueError("file type unkown")

def main():
    if len(sys.argv) != 3:
        print("help for usage: python tool.py file1 file2")
        sys.exit(1)

    inputFile1 = load_file(sys.argv[1])
    inputFile2 = load_file(sys.argv[2])

    analyzer = Analyzer(inputFile1, inputFile2)
    result = analyzer.run()

    # workaround for if its integer or float, little bit ugly
    if isinstance(result, int):
        print(result)
    else:
        print(f"{result:.7f}")

if __name__ == "__main__":
    main()