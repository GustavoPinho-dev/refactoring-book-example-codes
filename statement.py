import math
import json
from create_statement_data import create_statement_data

with open('plays.json', 'r') as file:
  plays = json.load(file)

with open('invoices.json', 'r') as file:
  invoice = json.load(file)

def statement(invoice, plays):
  return render_plain_text(create_statement_data(invoice, plays))

def format(a_number):
  return f"${a_number/100:0,.2f}"

def render_plain_text(data):
  
  result = f'Statement for {data["customer"]}\n'

  for perf in data['performances']:
    result += f' {perf["play"]["name"]}: {format(perf['amount'])} ({perf["audience"]} seats)\n'

  result += f'Amount owed is {format(data['total_amount'])}\n'
  result += f'You earned {data['total_volume_credits']} credits\n'
  return result
