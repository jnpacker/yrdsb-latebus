import pandas as pd
import html5lib
f_states= pd.read_html('./latebus.html')

table = f_states[0]
print(f_states)
for (idx, row) in table.iterrows():
    print (row['School'])
