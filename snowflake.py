import sys

file_name = sys.argv[1]
branch = sys.argv[2]
file_type = file_name.split('.')[1]
if file_type.lower() in ['yml', 'py']:
  sys.exit(0)
else:
  print(f"{file_name} has been changed")
  query = ""
  with open(file_name, 'r') as f:
    query = f.readlines()
    query = ''.join(query).replace('\n','')
  print(query)
 