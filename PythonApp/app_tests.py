import unittest
import pandas as pd

from app_refactored import enrich_dateDuration# add functions that are needed to test

# at a minimum test the following
## check that the duration column between checkout and return is an integer
## check that the same column is above 0
## do any other function 

class TestOperations(unittest.TestCase):
        
    def setUp(self):
        self.data=enrich_dateDuration(df=pd.DataFrame
            (
             data=[('01/01/2025', '04/01/2025'), 
                   ('01/04/2025', '04/04/2025')], 
             columns=['Book checkout', 'Book Returned']
             ), 
             colA='Book Returned',
             colB='Book checkout'
             )

    def test_durationint(self):
         self.assertTrue(self.data.enrich_dateDuration().df['date_delta'],int,"Data type is not int")     

if __name__ == '__main__':
        unittest.main()




