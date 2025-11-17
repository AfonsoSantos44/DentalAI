from pydantic import BaseModel
from typing import List

'''
Dental Output Model

This model defines the structure for dental analysis output, becoming the oficial output contract between the AI and the backend.

Attributes:
- teeth_positions (List[float]): A list of floats representing the positions of teeth.
- diagnosis (List[str]): A list of strings containing the diagnosis for each tooth.
- procedures (List[str]): A list of strings detailing the recommended procedures.
- follow_up_days (int): An integer indicating the number of days until the next follow-up.
- notes (str): Additional notes or comments regarding the dental analysis.

'''

class DentalOutput(BaseModel):
    teeth: List[int]
    diagnosis: List[str]
    procedures: List[str]
    follow_up_days: int
    notes: str