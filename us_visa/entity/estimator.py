import sys
import os 
from pandas import DataFrame 
from sklearn.pipeline import Pipeline
from us_visa.exception import USvisaException
from us_visa.logger import logging 

class TargetValueMapping:
    def __init__(self):
        self.Certified = 1
        self.Denied = 0

    def _asdict(self):
        return self.__dict__
    # def reverse_mapping(self):
    #     mapping_response = self._asdict()
    #     return dict(zip(mapping_response.values(),mapping_response.keys()))
    

    
    
