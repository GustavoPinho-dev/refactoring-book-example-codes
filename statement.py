import math
import json


with open('plays.json', 'r') as file:
  plays = json.load(file)

with open('invoices.json', 'r') as file:
  invoice = json.load(file)

def statement(invoice, plays):
  def play_for(a_performance):
    return plays[a_performance["playID"]]

  def enrich_performance(a_performance):
    result = dict(a_performance)
    result['play'] = play_for(result)
    return result

  statement_data = {}
  statement_data['customer'] = invoice['customer']
  statement_data["performances"] = [
    enrich_performance(performance)
    for performance in invoice["performances"]
  ]
  return render_plain_text(statement_data, plays)

def render_plain_text(data, plays):
  
  def total_amount():
    result = 0
    for perf in data['performances']:
      result += amount_for(perf)
    return result

  def total_volume_credits():
    result = 0
    for perf in data['performances']:
      result += volume_credits_for(perf)
    
    return result

  def format(a_number):
      return f"${a_number/100:0,.2f}"

  def volume_credits_for(a_performance):
    result = 0
    result += max(a_performance['audience'] - 30, 0)
    if "comedy" == a_performance["play"]["type"]:
      result += math.floor(a_performance['audience'] / 5)

    return result

  def amount_for(a_performance):
    result = 0
    if a_performance["play"]["type"] == "tragedy":
      result = 40000
      if a_performance['audience'] > 30:
        result += 1000 * (a_performance['audience'] - 30)
    elif a_performance["play"]["type"] == "comedy":
      result = 30000
      if a_performance['audience'] > 20:
        result += 10000 + 500 * (a_performance['audience'] - 20)

      result += 300 * a_performance['audience']

    else:
      raise ValueError(f'unknown type: {a_performance["play"]["type"]}')
    
    return result

  
  result = f'Statement for {data["customer"]}\n'

  for perf in data['performances']:
    result += f' {perf["play"]["name"]}: {format(amount_for(perf)/100)} ({perf["audience"]} seats)\n'

  result += f'Amount owed is {format(total_amount())}\n'
  result += f'You earned {total_volume_credits()} credits\n'
  return result
