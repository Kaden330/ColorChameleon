import requests
import pandas as pd

def load_new():
    with requests.get('https://www.colorhexa.com/color-names') as page:

        stats = pd.read_html(page.text)[0]
    
    return stats

def save_new(fpath):
    with requests.get('https://www.colorhexa.com/color-names') as page:

        stats = pd.read_html(page.text)[0].to_csv(fpath)

if __name__ == '__main__':
    save_new('colors.csv')