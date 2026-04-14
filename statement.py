import math
import json


with open('plays.json', 'r') as file:
  plays = json.load(file)

def play_for(a_performance):
  return plays[a_performance["playID"]]

def amount_for(a_performance, play):
  result = 0
  if play['type'] == "tragedy":
    result = 40000
    if a_performance['audience'] > 30:
      result += 1000 * (a_performance['audience'] - 30)
  elif play['type'] == "comedy":
    result = 30000
    if a_performance['audience'] > 20:
      result += 10000 + 500 * (a_performance['audience'] - 20)

    result += 300 * a_performance['audience']

  else:
    raise ValueError(f'unknown type: {play["type"]}')
  
  return result

def statement(invoice, plays):
  total_amount = 0
  volume_credits = 0
  result = f'Statement for {invoice["customer"]}\n'

  def format_as_dollars(amount):
    return f"${amount:0,.2f}"

  for perf in invoice['performances']:
    play = play_for(perf)
    this_amount = amount_for(perf, play)

    # add volume credits
    volume_credits += max(perf['audience'] - 30, 0)
    # add extra credit for every ten comedy attendees
    if "comedy" == play["type"]:
        volume_credits += math.floor(perf['audience'] / 5)
    # print line for this order
    result += f' {play["name"]}: {format_as_dollars(this_amount/100)} ({perf["audience"]} seats)\n'
    total_amount += this_amount

  result += f'Amount owed is {format_as_dollars(total_amount/100)}\n'
  result += f'You earned {volume_credits} credits\n'
  return result

