import os
import settings
import pandas as pd

def read_data():
    df = pd.read_excel(os.path.join(settings.PROCESSED_DIR, "all_with_liwc_segmented.xls"), encoding="ISO-8859-1")
    return df







if __name__ == "__main__":
    df = read_data()
