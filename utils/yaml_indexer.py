import yaml

tagged_obj = {}
def setitem(loader, node):
  nodeseq = loader.construct_scalar(node)
  items = nodeseq.split(" ")
  listname = items[0]
  liststore = items[1:]
  tagged_obj[listname] = liststore
  return liststore
  
def getitem(loader, node):
  nodeseq = loader.construct_scalar(node)
  items = nodeseq.split(" ")
  listname = items[0]
  listidx = int(items[1])
  nodelist = tagged_obj[listname]
  return nodelist[listidx]

yaml.add_constructor("!set", setitem)
yaml.add_constructor("!get", getitem)

ystr = """
items: !set lst file.yaml test.yaml trees.yaml
test: !get lst 1
"""

print(yaml.load(ystr, Loader=yaml.FullLoader))
