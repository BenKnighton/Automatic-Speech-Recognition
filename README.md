# Automatic-Speech-Recognition
Automatic speech recognition (ASR) using Vosk models, and some clever coding. 

In this code, I have made some updates to the typical microphone Vosk code, so that the result, which has the preface final; now instead states "got" which is received as a better answer (better than the partial) much faster than waiting for the final. If the final and the last got are not the same, then the final is used. If the code starts running from the got, and the final is the same as the got, then there is no need to re-start the entire code, it has already been running from the last received correct "got”. The “got” is gotten when 2-3 of the partials match exactly, which makes things much faster.

download the vosk-model-en-us-0.22 (1.8 GB) https://alphacephei.com/vosk/models and put the folder in your directory. 

### Run test_microphone f.py to start the code.
