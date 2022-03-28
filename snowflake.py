import sys

file_name = sys.argv[1]
print(f"{file_name} has been changed")
qyery = ""
with open(file_name, 'r') as f:
  query = f.readlines()
  
print(query)
print("working")
print("working2")
