import math

class PerformanceCalculator:
  def __init__(self, a_performance, a_play):
    self.performance = a_performance
    self.play = a_play
    self._amount = self.amount

  @property
  def amount(self):
    result = 0
    if self.play["type"] == "tragedy":
      result = 40000
      if self.performance['audience'] > 30:
        result += 1000 * (self.performance['audience'] - 30)
    elif self.play["type"] == "comedy":
      result = 30000
      if self.performance['audience'] > 20:
        result += 10000 + 500 * (self.performance['audience'] - 20)

      result += 300 * self.performance['audience']

    else:
      raise ValueError(f'unknown type: {self.play["type"]}')
    
    return result

def create_statement_data(invoice, plays):

  def play_for(a_performance):
    return plays[a_performance["playID"]]
  
  def amount_for(a_performance):
    return PerformanceCalculator(a_performance, play_for(a_performance)).amount

  def volume_credits_for(a_performance):
    result = 0
    result += max(a_performance['audience'] - 30, 0)
    if "comedy" == a_performance["play"]["type"]:
      result += math.floor(a_performance['audience'] / 5)

    return result

  def total_amount(data):
    return sum(p["amount"] for p in data["performances"])
  
  def total_volume_credits(data):
    return sum(p["volume_credits"] for p in data["performances"])
  
  def enrich_performance(a_performance):
    calculator = PerformanceCalculator(a_performance, play_for(a_performance))
    result = dict(a_performance)
    result['play'] = calculator.play
    result['amount'] = calculator.amount
    result['volume_credits'] = volume_credits_for(result)
    return result

  result = {}
  result['customer'] = invoice['customer']
  result["performances"] = [
    enrich_performance(performance)
    for performance in invoice["performances"]
  ]
  result['total_amount'] = total_amount(result)
  result['total_volume_credits'] = total_volume_credits(result)
  return result