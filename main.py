from __future__ import annotations
import argparse
import os
import uuid
import json
from typing import TypedDict, cast

class JFile(TypedDict):
    name: str
    newName: str
    isDir: bool
    children: list[JFile]

def encode(source_dir: str, meta_file_path: str) -> None:
    json_obj = folder_to_json(source_dir, 0)
    with open(meta_file_path, "w") as meta_file:
        meta_file.write(json.dumps(json_obj, indent=4))

def folder_to_json(path, idx_num) -> JFile:
    # Initialize the result dictionary with folder 
    # name, type, and an empty list for children 

    result = JFile(
        name=os.path.basename(path),
        newName=str(uuid.uuid4()),
        # newName=str(idx_num),
        isDir=True,
        children=[]
    )
  
    # Check if the path is a directory 
    if not os.path.isdir(path): 
        return result 
  
    # Iterate over the entries in the directory 
    for idx, entry in enumerate(os.listdir(path)): 
       # Create the full path for the current entry 
        entry_path = os.path.join(path, entry) 
  
        # If the entry is a directory, recursively call the function 
        if os.path.isdir(entry_path):
            child_jfile = folder_to_json(entry_path, idx)
            result['children'].append(child_jfile)
            new_name = child_jfile['newName']
        # If the entry is a file, create a dictionary with name and type 
        else: 
            new_name = str(uuid.uuid4())
            # new_name = str(idx)
            result["children"].append(JFile(
                name=entry,
                newName=new_name,
                isDir=False,
                children=[]
            ))
        os.rename(os.path.join(path, entry), os.path.join(path, new_name))

    return result 


def decode(source_dir: str, meta_file_path: str) -> None:
    with open(meta_file_path, "r") as meta_file:
        meta_obj = cast(JFile, json.loads(meta_file.read()))
    json_to_folder(meta_obj, source_dir)

def json_to_folder(jfile: JFile, dir_path: str) -> None:
    if jfile['isDir'] == False:
        return

    for child in jfile['children']:
        child_file = os.path.join(dir_path, child['newName'])
        if child['isDir'] == True:
            json_to_folder(child, child_file)
        os.rename(child_file, os.path.join(dir_path, child['name']))



def create_arg_parsers() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="file-name-obfuscator",
        description="App to obfuscate file names in a directory recursively."
    )

    mode_parser = parser.add_subparsers(dest="mode", required=True, help='sub-command help')

    encode_args = mode_parser.add_parser('encode', help='Encode file names of a directory tree.')
    encode_args.add_argument('dir', type=str, help='Source folder')
    encode_args.add_argument('meta_file', type=str, help='Meta file name')

    decode_args = mode_parser.add_parser('decode', help='Decode file names.')
    decode_args.add_argument('dir', type=str, help='Source folder')
    decode_args.add_argument('meta_file', type=str, help='Meta file name')

    return parser

if __name__ == "__main__":
    print("Hello World!")
    parser = create_arg_parsers()

    parsed_args = parser.parse_args()
    print("Args", parsed_args)
    if parsed_args.mode == "encode":
        encode(parsed_args.dir, parsed_args.meta_file)
    elif parsed_args.mode == "decode":
        decode(parsed_args.dir, parsed_args.meta_file)
    
