import pandas as pd
from color_difference import ciede2000_color_difference as deltaE

def nameit(rgb):

    dataset = pd.read_csv('colors.csv')

    diffs = []
    for row in dataset.iterrows():
        name = row[1][1]
        rgb2 = tuple(row[1][3:6])
        diffs.append([name, rgb, rgb2, deltaE(rgb, rgb2)])
    
    diffs = pd.DataFrame(diffs, columns=['name', 'source_rgb', 'comp_rgb', 'deltaE'])
    diffs = diffs.sort_values('deltaE')
    return diffs.iloc[0, 0]

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

        
if __name__ == "__main__":
    import sys
    hex = str(sys.argv[1])
    rgb = hex_to_rgb(hex)
    print(nameit(rgb))