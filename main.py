import json
from statement import statement

with open('plays.json', 'r') as file:
  plays = json.load(file)

with open('invoices.json', 'r') as file:
  invoices = json.load(file)

result = statement(invoices[0], plays)
print(result)