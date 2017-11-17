import json

result = [{'name': "foo"},{'name': "bar"}]


def addElement( name):
  path = name.split('.')
  element = path.pop(0)
  position = {}
  for i, item in enumerate(result):
    if item['name'] == name:
      position = result[i]
  if len(position) == 0:
    result.append({'name': name})
    position = result[-1]
    


#def writeJson():
  #TODO: write json to file

def addProperty( name, key, value):
  for index, element  in enumerate(result):
    print ('TODO')
  

#def solveConflict( key, value):
  #TODO: add logic called by addValue if the value already exists.
  # Print old / new values with index and wait for
  # index to choose input from user before continuing execution