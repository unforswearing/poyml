import argparse
import datetime
import os
import pandoc
from pathlib import Path
import sys
import yaml  

# install pyyaml via git
# pyyaml: https://github.com/yaml/pyyaml

# todo: using a poyml file to concatinate multiple input files
#       into a single output manuscript from the "body" key
#       see test/ for example
# todo: maybe make the extraction flags make more sense together?
#       -> replace all flags with an --extract flag that will accept
#          title, date, body, comments, submitted  as argumemnts.
#          eg. `poyml --extract title,body poem.yaml`
#          the code will need to change to accomodate this new setup
# todo: maybe add a flag to append submission info?
# ------------------------------------------------------------------/
# parsing args with argparse
parser = argparse.ArgumentParser(
  prog="poyml",
  description="serialize, read, and build literary poetry files from yaml.",
  epilog="eventually this will be on github"
)

parser.add_argument("yamlfile")

# ------------------------------------------------------------------/
# extraction commands
# these will eventually be replaced with a single --extract flag
# that accepts date, title, body, comments, and submitted as args
# parser.add_argument(
#  "-e", "--extract", action="store",
#  help="extract date, title, body, comments, submitted from poyml file"
# )
#
# the args below will go away when the above --extract command is added
parser.add_argument(
  "-d", "--date", action="store_true",
  help="print date created from poyml-formatted (yaml) file"
)
parser.add_argument(
  "-t", "--title", action="store_true",
  help="print poem title from poyml-formatted (yaml) file"
)
parser.add_argument(
  "-b", "--body", action="store_true",
  help="print the full poem body from poyml-formatted (yaml) file"
)
parser.add_argument(
  "-c", "--comments", action="store_true",
  help="print comments from poyml-formatted (yaml) file"
)
parser.add_argument(
  "-s", "--submitted", action="store_true",
  help="show sumbision info for this poem: { date, journal }"
)
# ------------------------------------------------------------------/
# when the extraction commands are changed the -x flag will change to -s
# serialize will require an output file via -o flag
parser.add_argument(
  "-x", "--serialize", action="store_true",
  help="create a poyml-formatted (yaml) file from an input poem file"
)
# when the extraction commands are changed  the -m flag will change to -b
# build will require an output file via -o flag
parser.add_argument(
  "-m", "--build", action="store_true",
  help="concatenate multiple input files with formatting options"
)
parser.add_argument(
  "-o", "--output", action="store",
  help="specify output name for --serialize and --build files"
)

args = parser.parse_args()

# ------------------------------------------------------------------/
# Creating custom tags for yaml

tagged_obj = {}
# usage
#  list_example: !set listname item1 item2 item3
def setitem(loader, node) -> dict:
  nodeseq = loader.construct_scalar(node)
  items = nodeseq.split(" ")
  listname = items[0]
  liststore = items[1:]
  tagged_obj[listname] = liststore
  return liststore

yaml.add_constructor("!set", setitem)

# usage
#  list_retrieve: !get listname 1
#  the value in the list_retrieve node will be item2
def getitem(loader, node):
  nodeseq = loader.construct_scalar(node)
  items = nodeseq.split(" ")
  listname = items[0]
  listidx = int(items[1])
  nodelist = tagged_obj[listname]
  return nodelist[listidx]
  
yaml.add_constructor("!get", getitem)

def settoday(loader, node):
  node = loader.construct_scalar(node)
  now = datetime.datetime.now()
  return now.strftime("%Y-%m-%d")

yaml.add_constructor("!today", settoday)

# ------------------------------------------------------------------/
# load file, create yaml object
def poyml_file(filepath):
  tmppoyml = open(filepath, "r")
  poymlcontent = tmppoyml.read()
  tmppoyml.close()
  return(poymlcontent)

loadedfile = poyml_file(args.yamlfile)
poymlobject = yaml.load(loadedfile, Loader=yaml.FullLoader)

# ------------------------------------------------------------------/
# serialize a file to yaml
def get_creation_date(filepath):
  created = os.stat(filepath).st_birthtime
  timestamp = datetime.datetime.fromtimestamp(created)
  return timestamp.strftime("%Y-%m-%d")

def get_file_name(filepath):
  return os.path.basename(filepath)

def get_poem_title(filepath):
  return Path(filepath).stem

def get_poem_body(filepath):
  with open(filepath, "r") as poem:
    poembody = [line for line in poem]
    
  poem.close()
  return "  ".join(poembody)

def serialize_poem(filepath, outputpath):
  def generate_yaml(pfp):
    return (
      f'title: {get_poem_title(pfp)}\n'
      f'date: !!timestamp {get_creation_date(pfp)}\n'
      f'body: |- \n'
      f'  {get_poem_body(pfp)}\n'
      f'comments: | \n'
      f'  creatd from file "{get_file_name(pfp)}"\n'
      f'submitted: []\n'
    )
    
  yaml_fmt = generate_yaml(filepath)
  
  output_file = open(outputpath, "w")
  output_file.write(yaml_fmt)
  output_file.close()

if args.serialize:
  serialize_poem(args.yamlfile, args.output)
  sys.exit()

# ------------------------------------------------------------------/
# UPDATE: This script will generate yaml for pandoc
#         The previous functions are in utils/yaml_extension.py

# the pandoc related functions needs to generate the following yaml example
# ---
# standalone: true
# css: "../pandoc/style.css"
# input-file: "--input argument"
# from: commonmark_x
# to: pdf
# pdf-engine: wkhtmltopdf
# title: "--title argument"
# include-after-body:
#   - "--file interstate.md"
#   - "--file push.md"
#   - "--file to_be_new.md"
#   - "--file wooded_land.md"
#   - "--file you_are_going_to_be_here.md"
# output-file: "--output argument"
# ---
#
def generate_pandoc_yaml(files):
  print("files")



# ------------------------------------------------------------------/
# extract serialized yaml

if args.title:
  print(poymlobject['title'])
  print("")

if args.date:
  print(poymlobject['date'])
  print("")

if args.body:
  print(poymlobject["body"])
  print("")

if args.comments:
  print("comments:")
  print(poymlobject["comments"])
  print("")

if args.submitted:
  print("submission info")
  print(f'poem \"{poymlobject["title"]}\"')
  print("---")
  for item in poymlobject["submitted"]:
    print(f'date: {dict(item)["date"]}')
    print(f'submitted to: {dict(item)["journal"]}')
    print("---")

  print("")
    

