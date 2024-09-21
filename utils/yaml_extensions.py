registered_files = {}
def registerfiles(loader, node):
  nodestr = loader.construct_scalar(node)
  nodelst = nodestr.split(" ")
  filelist = nodelst[1:]

  for item in filelist:
    rf = yaml.load(item, Loader=yaml.FullLoader)
    registered_files[rf[title]] = { 
      title: rf[title], body: rf[body] 
    }

  return filelist
  
# yaml.add_constructor("!register", registerfiles)

def usefile(loader, node):
  # parse node to extract file name
  nodestr = loader.construct_scalar(node)
  nodelst = nodestr.split(" ")
  filename = nodelst[0]
  # search registered_files{} for file name
  # if found, replace node contents with title and body as block literal
  if hasattr(registered_files[filename]):
    registeredfile = registered_files[filename]
    title, body = registeredfile
    output_obj[title, "\n\n", body, "\n\n\n"]
    return (
      f'|\n  {registeredfile.title}\n\n'
      f'  {registerdfile.body}\n\n\n'
    )

# yaml.add_constructor("!use", usefile)
