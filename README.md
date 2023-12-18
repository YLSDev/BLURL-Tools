# BLURL-Tools
A super simple tool made in Python that allows you to compress or de-compress `.blurl` files.

## Usage

1. Place the `blurl.py` script and the JSON/BLURL file you want to compress/decompress in the same directory.
2. Open a command prompt or terminal in the directory.
3. Run the script using Python:

   To de-compress a `.blurl` file:
   ```python
   python blurl.py -d yourfile.blurl
   ```
   To compress a `.json` file:
   ```python
   python blurl.py -c yourfile.json
   ```