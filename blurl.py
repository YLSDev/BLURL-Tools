import zlib
import os
import argparse
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Define the magic number as a constant
MAGIC_NUMBER = b'blul'

def constructFileName(originalName: str, targetExtension: str, identifier: str = 'YLSDev') -> str:
    """
    Constructs a new filename based on the original name, a target extension, and an optional identifier.
    """
    baseName, _ = os.path.splitext(originalName)
    return f"{baseName}.{identifier}{targetExtension}"

def confirmOverwrite(fileName: str) -> bool:
    """
    Ask the user to confirm if they want to overwrite an existing file.
    """
    return input(f"The file '{fileName}' already exists. Overwrite? (y/n): ").lower() == 'y'

def compressFile(fileName: str, chunkSize=1024*1024):
    """
    Compresses a file with zlib using 1MB chunk sizes.
    """
    try:
        compressedFileName = constructFileName(fileName, '.blurl')
        if os.path.exists(compressedFileName) and not confirmOverwrite(compressedFileName):
            return 1

        with open(fileName, "rb") as inFile, open(compressedFileName, 'wb') as outFile:
            outFile.write(MAGIC_NUMBER)
            outFile.write(os.path.getsize(fileName).to_bytes(4, byteorder='big', signed=False))
            compressor = zlib.compressobj()
            while True:
                chunk = inFile.read(chunkSize)
                if not chunk:
                    break
                compressed = compressor.compress(chunk)
                if compressed:
                    outFile.write(compressed)
            outFile.write(compressor.flush())
        logging.info(f"Successfully compressed to {compressedFileName}")
    except FileNotFoundError:
        logging.error("File not found.")
        return 1
    except OSError as e:
        logging.error(f"OS error: {e}")
        return 1
    return 0

def decompressFile(fileName: str, chunkSize=1024*1024):
    """
    Decompresses a .blurl file with zlib using 1MB chunk sizes.
    """
    try:
        with open(fileName, "rb") as inFile:
            magic = inFile.read(4)
            if magic != MAGIC_NUMBER:
                raise ValueError("Invalid file format")
            original_size = int.from_bytes(inFile.read(4), byteorder='big')
            decompressor = zlib.decompressobj()
            decompressedFileName = constructFileName(fileName, '.json')
            if os.path.exists(decompressedFileName) and not confirmOverwrite(decompressedFileName):
                return 1

            with open(decompressedFileName, "wb") as outFile:
                while True:
                    chunk = inFile.read(chunkSize)
                    if not chunk:
                        break
                    decompressed = decompressor.decompress(chunk)
                    if decompressed:
                        outFile.write(decompressed)
                outFile.write(decompressor.flush())
        logging.info(f"Successfully decompressed to {decompressedFileName}")
    except FileNotFoundError:
        logging.error("File not found.")
        return 1
    except ValueError as e:
        logging.error(f"Value error: {e}")
        return 1
    except OSError as e:
        logging.error(f"OS error: {e}")
        return 1
    return 0

def getFileExtension(fileName: str) -> str:
    """
    Extracts the file extension from a given filename.
    """
    _, ext = os.path.splitext(fileName)
    return ext

def isValidFile(fileName: str, expectedExtension: str) -> bool:
    """
    Validates if the file extension matches the expected extension.
    """
    return getFileExtension(fileName) == expectedExtension

def main():
    parser = argparse.ArgumentParser(description='File Compression and Decompression Tool using zlib.')
    parser.add_argument('filename', help='Name of the file to compress or decompress.')
    parser.add_argument('-c', '--compress', action='store_true', help='Compress the specified file.')
    parser.add_argument('-d', '--decompress', action='store_true', help='Decompress the specified file.')

    args = parser.parse_args()

    if args.compress:
        if not isValidFile(args.filename, '.json'):
            logging.error("Compression only supports .json files.")
            return 1
        return compressFile(args.filename)
    elif args.decompress:
        if not isValidFile(args.filename, '.blurl'):
            logging.error("Decompression only supports .blurl files.")
            return 1
        return decompressFile(args.filename)
    else:
        logging.error("No action specified. Use -c to compress or -d to decompress.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
