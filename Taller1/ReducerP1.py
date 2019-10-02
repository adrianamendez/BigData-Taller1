import sys


top = 9
finalResult = sys.stdin.groupby(['sitio', 'speed', 'hora', 'diasem']).ciudad.value_counts().nlargest(top)
print(finalResult)
