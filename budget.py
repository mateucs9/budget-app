class Category:
  def __init__(self, category):
    self.category = category
    self.ledger = []
    self.balance = 0.0

  def __repr__(self):
    header = self.category.center(30, '*')
    body = ''
    for item in self.ledger:
      line_description = "{:<23}".format(item['description'])
      line_amount = "{:>7.2f}".format(item['amount'])
      body += "\n{}{}".format(line_description[:23], line_amount[:7])
    total = "\nTotal: {:.2f}".format(self.get_balance())
    return header + body + total

  def get_balance(self):
    balance = sum([x['amount'] for x in self.ledger])
    return balance

  def deposit(self, amount, description=''):
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, description=''):
    if self.get_balance() <= amount:
      return False
    else:
      self.ledger.append({"amount": -amount, "description": description})
      return True

  def check_funds(self, amount):
    if self.get_balance() >= amount:
      return True
    else:
      return False

  def transfer(self, amount, other_category):
    if self.check_funds(amount):
      self.withdraw(amount, description = "Transfer to {}".format(other_category.category))
      other_category.deposit(amount, "Transfer from {}".format(self.category))
      return True
    else:
      return False


def create_spend_chart(categories):
  spent_log = []
  for category in categories:
    amounts = [x['amount'] for x in category.ledger if x['amount'] < 0]
    spent_log.append({category.category: abs(sum(amounts))})
  
  category_names = [x.category for x in categories]
  spent_amounts = [list(x.values())[0] for x in spent_log]
  total_amount = sum(spent_amounts)
  percentages = [round(x/total_amount, 2)*100 for x in spent_amounts]

  chart = 'Percentage spent by category\n'
  for value in reversed(range(0, 101, 10)):
    chart += "{:>3}| ".format(str(value))
    for percent in percentages:
      if percent >= value:
        chart += "o  "
      else:
        chart += " " * 3
    chart += '\n'
  
  break_line = "    "+"-"*(len(categories)*3+1)+"\n"
  footer = ''
  for num in range(len(max(category_names, key=len))):
    footer += ' '*5
    for category in category_names:
      if num < len(category):
        footer += '{}  '.format(category[num])
      else:
        footer += ' ' * 3
    footer += '\n'
  return chart + break_line + footer[:-1]