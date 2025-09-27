# Genome Analyzer

Small Python program for the GDI/ELIXIR task of Oslo University.

It supports the following file types
- type segment (ends with *.s), tap seperated intervals
- type function (ends with *.f), float value for each genome position

## Usage

```bash
python main.py file1 file2
```

## Manual

There are three possible combinations you could pass to the program.
- segment + segment -> calculates the overlap length
- function + function -> calculates the pearson correlation
- segment + function (or other way around) -> mean of all positions inside segments

## Example

```bash
python tool.py testfiles/testfile_a.s testfiles/testfile_a.s
python tool.py testfiles/testfile_b.f testfiles/testfile_a.s
python tool.py testfiles/testfile_b.f testfiles/testfile_a.f
```

## Tests

Requries pytest, either install it or configure your env.

Install:
```bash
pip install pytest
```

Ausführen:
```bash
pytest
```