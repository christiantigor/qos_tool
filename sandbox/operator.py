import re

pattern = r'Rp.([0-9_]*).'
rspn = "pulsa anda Rp.192837."
text = re.findall(pattern,rspn)
print text[0]
