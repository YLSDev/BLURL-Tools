import zlib
import json 


def compressFile(fileName: str):
    fileNameWithoutExtenstion = fileName.split('.json')[0]
    with open(fileName, "rb") as file:
        content = file.read()
    compressed = zlib.compress(content)
    with open(f'{fileNameWithoutExtenstion}.YLSDev.blurl', 'wb') as file:
        file.write(b'blul')
        file.write(len(content).to_bytes(4, byteorder='big', signed=False))
        file.write(compressed)
    with open(f"{fileNameWithoutExtenstion}.YLSDev.blurl", "rb") as file:
        print(f"Successfully compressed the JSON supplied into {fileNameWithoutExtenstion}.YLSDev.blurl")

def decompressFile(fileName: str):
    fileNameWithoutExtenstion = fileName.split('.blurl')[0]
    with open(fileName, "rb") as file:
        content = file.read()
    try:
        decompressed = zlib.decompress(content[8:])
        meta = json.loads(decompressed)
    except:
        raise Exception('Invalid BLURL Passed')
    sorted = json.dumps(meta, sort_keys=False, indent=4)
    with open(f"{fileNameWithoutExtenstion}.YLSDev.json", "w") as file:
        file.write(f'{sorted}')
    with open(f"{fileNameWithoutExtenstion}.YLSDev.json", "rb") as file:
        print(f"Successfully decompressed the BLURL supplied into {fileNameWithoutExtenstion}.YLSDev.json")
        
print("""Basic Instructions:
Place the JSON you want to compress or the BLURL you want to decompress in the same directory
Then input the name of it under and make sure to include the extension aka .blurl or .json\n""")

fileName = input('Input the name of the file here: ')

if fileName.endswith('.json'):
    compressFile(fileName=fileName)
elif fileName.endswith(".blurl"):
    decompressFile(fileName=fileName)
else:
    print('Unsupported File Format, are you sure you included the extension?')   