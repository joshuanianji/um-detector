# um-detector

A filler word detector based on this [Public Speaking Feedback tool](https://github.com/wellesleynlp/elizabethhau_emilyahn-finalproject) using [Pocketsphinx](https://pypi.org/project/pocketsphinx/)

## Voice-Analysis stuff

### Setup and Python environment

We only need to set up pocketsphinx for the actual voice analysis; there are optional dependencies if you want to record audio using the `utils.py`.

1. Make sure you have [`pyenv`](https://opensource.com/article/20/4/pyenv) installed and working.
2. Install python `3.5.10` by `pyenv install 3.5.10` (this might take a while).
3. Navigate to the directory and run `pyenv local 3.5.10` so you're using the right version ONLY in the directory (you don't want to clog up your global python stuff).
4. Start the venv via `python -m venv venv`.
5. Run `source venv/bin/activate` in the terminal to make sure you're running the python environment. You should have a (venv) before your terminal lines. Make sure you are running the correct python environment with `which python`, which should show the directory to the virtual env. `deactivate` will stop the virtualenv.
6. To set up pocketsphinx, follow [this comment](https://github.com/bambocher/pocketsphinx-python/issues/28#issuecomment-334493324).
7. Change the directory constants in [speech_to_text.py](voice-analyzer/speech_to_text.py), specifically `MODELDIR` since the others are not in use.
8. Test everything out by running `python speech_to_text.py uh_1min_1.wav`.


If you want to use `utils.py`, run `pip install PyAudio`, but you'll have to make sure you have [PortAudio](http://files.portaudio.com/download.html) installed as well; I just used `brew` since I'm on a mac. Also note that VSCode [does not record audio correctly without some weird setup](https://github.com/MicrosoftDocs/live-share/issues/3254), so you might have to use your computer's native terminal application.

