import os
import settings
import pandas as pd

def add_long_transcripts():
    '''
    Adds transcripts for 3 talks whose transcripts exceeded csv single cell capacity
    '''
    df = pd.read_excel(os.path.join(settings.PROCESSED_DIR, "all.xsl"))