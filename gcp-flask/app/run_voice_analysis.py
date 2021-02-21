mysp = __import__('voice_analysis_lib')
from parselmouth.praat import call, run_file

def run_voice_analysis(fileName):
    f_name = fileName.split('.')[0]
    c = r'audio'

    mysp.mysppaus(f_name, c)
    mysp.myspsr(f_name, c)
    mysp.myspsyl(f_name, c)
    mysp.myspgend(f_name, c)