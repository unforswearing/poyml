import yaml
import datetime

def settoday(loader, node):
  node = loader.construct_scalar(node)
  now = datetime.datetime.now()
  return now.strftime("%Y-%m-%d %H:%M:%S")

yaml.add_constructor("!today", settoday)

ystr = """
items: !today
"""

yload = yaml.load(ystr, Loader=yaml.FullLoader)

print (yload)
