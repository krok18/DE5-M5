import unittest 
import pandas as pd
from app_refactored import enrich_dateDuration  # Make sure this function returns a DataFrame

class TestEnrichment(unittest.TestCase):

    def setUp(self):
        # creating a test dataframe
        self.test_df = pd.DataFrame({
            'start_date' : ['01/01/2025', '02/01/2024', '03/01/2024'],
            'end_date' : ['01/02/2025', '02/02/2024', '03/02/2024']
        })

        # covert the column to datetime
        self.test_df['start_date'] = pd.to_datetime(self.test_df['start_date'], format = '%d/%m/%Y')
        self.test_df['end_date'] = pd.to_datetime(self.test_df['end_date'], format = '%d/%m/%Y')

        # apply the enrichment function
        self.enriched_df = enrich_dateDuration(df=self.test_df, colA="start_date", colB="end_date")

    def test_duration_as_int(self):
         self.assertTrue(pd.api.types.is_integer_dtype(self.enriched_df['date_delta']), "The delta column is not an integer")

    def test_duration_above_zero(self):
         self.assertTrue((self.enriched_df['date_delta']>0).all(), "Some durations are less than 0")

if __name__ == '__main__':
        unittest.main()