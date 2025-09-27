import os
from tool import SegmentFile, FunctionFile, Analyzer
from pytest import approx

DATA_DIR = os.path.join(os.path.dirname(__file__), "testfiles")

def test_overlap_segments():
    file1 = SegmentFile(os.path.join(DATA_DIR, "testfile_a.s"))
    file2 = SegmentFile(os.path.join(DATA_DIR, "testfile_b.s"))
    analyzer = Analyzer(file1, file2)

    result = analyzer.run()

    assert result == 45983

def test_pearson_correlation():
    file1 = FunctionFile(os.path.join(DATA_DIR, "testfile_a.f"))
    file2 = FunctionFile(os.path.join(DATA_DIR, "testfile_b.f"))
    analyzer = Analyzer(file1, file2)

    result = analyzer.run()
    
    assert result == approx(-0.0155507, rel=1e-5)

def test_mean():
    file1 = FunctionFile(os.path.join(DATA_DIR, "testfile_b.f"))
    file2 = SegmentFile(os.path.join(DATA_DIR, "testfile_a.s"))
    analyzer = Analyzer(file1, file2)

    result = analyzer.run()
    
    assert result == approx( 3.6632504, rel=1e-5)