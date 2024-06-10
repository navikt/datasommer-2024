import pandas as pd

def get_data():
    df = pd.read_csv('../../datasommer/arbeidssokere-yrke.csv', sep= ';')
    df = df.replace('*', pd.NA)
    df = df.convert_dtypes()
    df.yrke_grovgruppe = df.yrke_grovgruppe.astype('category')
    df.antall_arbeidssokere = pd.to_numeric(df['antall_arbeidssokere'])
    return df
