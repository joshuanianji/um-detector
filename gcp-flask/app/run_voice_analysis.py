mysp = __import__('voice_analysis_lib')
from parselmouth.praat import call, run_file

def run_voice_analysis(fileName):
    f_name = fileName.split('.')[0]
    c = r'audio'

    try:
        data = mysp.mysptotal(f_name, c)
        posteriori_score = mysp.mysppron(f_name, c)
        gender = mysp.myspgend(f_name, c)

        data["pronounciation_score"] = posteriori_score
        data["gender"] = gender

        return data
    except Exception as e: 
        raise e