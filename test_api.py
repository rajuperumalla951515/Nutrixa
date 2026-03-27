import os
import sys

sys.path.append(os.getcwd())
try:
    from config import *
    from gemini_service import get_gemini_response

    print("Attempting to call Gemini API...")
    response = get_gemini_response('test')
    print("API Response:", response)
except Exception as e:
    print("Caught Exception:", type(e).__name__)
    print("Error Details:", str(e))
