import re

balMatcher = re.compile("Pulsa (\d+)")
balance = balMatcher.findall("Pulsa 5000 s/d 14Nov14. Bonus Nelpon 100menit SEPUASNYA!")
print balance
