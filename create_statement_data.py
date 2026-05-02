import math

class PerformanceCalculator:
  def __init__(self, a_performance, a_play):
    self.performance = a_performance
    self.play = a_play
    self._amount = self.amount

  @property
  def amount(self):
    raise ValueError('subclass responsability')

  @property
  def volume_credits(self):
    return max(self.performance['audience'] - 30, 0)

def create_performance_calculator(a_performance, a_play):
  if a_play['type'] == "tragedy":
    return TragedyCalculator(a_performance, a_play)
  elif a_play['type'] == "comedy":
    return ComedyCalculator(a_performance, a_play)

  else:
    raise ValueError(f'unknown type: {a_play["type"]}')

class TragedyCalculator(PerformanceCalculator):
  @property
  def amount(self):
    result = 40000
    if self.performance["audience"] > 30:
      result += 1000 * (self.performance["audience"] - 30)
    return result

class ComedyCalculator(PerformanceCalculator):
  @property
  def amount(self):
    result = 30000
    if self.performance["audience"] > 20:
      result += 1000 + 500 * (self.performance["audience"] - 20)
    result += 300 * self.performance["audience"]
    return result
  
  @property
  def volume_credits(self):
    return super().volume_credits + math.floor(self.performance['audience'] / 5)

def create_statement_data(invoice, plays):

  def play_for(a_performance):
    return plays[a_performance["playID"]]
  
  def amount_for(a_performance):
    return PerformanceCalculator(a_performance, play_for(a_performance)).amount

  def volume_credits_for(a_performance):
    return PerformanceCalculator(a_performance, play_for(a_performance)).volume_credits

  def total_amount(data):
    return sum(p["amount"] for p in data["performances"])
  
  def total_volume_credits(data):
    return sum(p["volume_credits"] for p in data["performances"])
  
  def enrich_performance(a_performance):
    calculator = create_performance_calculator(a_performance, play_for(a_performance))
    result = dict(a_performance)
    result['play'] = calculator.play
    result['amount'] = calculator.amount
    result['volume_credits'] = calculator.volume_credits
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