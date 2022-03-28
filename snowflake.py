import sys

file_name = sys.argv[1]
file_type = file_name.split('.')[1]
if file_type.lower() == 'yml':
  sys.exit(0)
else:
  print(f"{file_name} has been changed")
  qyery = ""
  with open(file_name, 'r') as f:
    query = f.readlines()
    
  print(query)
  print("working")
  print("working")
