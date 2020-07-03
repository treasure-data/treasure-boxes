import os
import sys
os.system(f"{sys.executable} -m pip install -U pytd==1.3.0 xlrd")


def import_table(database, table):
    import pandas as pd
    import pytd

    # http://archive.ics.uci.edu/ml/datasets/Online+Retail#
    url = "http://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"

    df = pd.read_excel(url, dtype={
        "InvoiceNo": str,
        "InvoiceDate": str,
        "CustomerID": float,
        "Country": str,
        "StockCode": str,
        "Description": str,
        "UnitPrice": float,
        "Quantity": int
    })
    df = df.loc[pd.notnull(df.CustomerID)]
    df.CustomerID = df.CustomerID.astype(int)

    client = pytd.Client(apikey=os.environ.get('TD_API_KEY'),
                         endpoint=os.environ.get('TD_API_SERVER'),
                         database=database)
    client.load_table_from_dataframe(df, table, if_exists="overwrite")


if __name__ == "__main__":
    import_table("takuti", "transactions")
