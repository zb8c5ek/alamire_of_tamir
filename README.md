# TAMIR: A TOOLBOX FOR RECOGNITION AND TRANSCRIPTION OF MUSIC MANUSCRIPTS IN MENSURAL NOTATION
The codes for Alamire's manuscipt transcription: alamire_of_tamir
------------------------------------------------------------------
<a href="http://www.youtube.com/watch?feature=player_embedded&v=7TdqeqmfMVE
" target="_blank"><img src="http://img.youtube.com/vi/7TdqeqmfMVE/0.jpg" 
alt="Demo video of transcription" width="640" height="480" border="10" /></a>

We hope you enjoyed the video. And yes, the background soundtrack is generated by our toolbox, not a recording ;)

The demo .annotation file is added. One could find it under .../site-packages/path/alamire_of_tamir/data_alamire/demo.annotation .
The library was released online, and packaged on pypi. Therefore one can easily install it using pip:

```bash
pip install alamire_of_tamir
```
The dependencies are automatically installed as well.
## How to find our demo file together with the installation?
Along with the installation, the demo files are also downloaded. They are inside the library path with the name ".../site-packages/path/alamire_of_tamir/data_alamire/". In Python, this path could be tracked as:
```python
import alamire_of_tamir
import os
demo_file_path = os.path.dirname(alamire_of_tamir.__file__) + '/data_alamire/demo.annotation'
```
Together with the .annotation file, an original image is inside "data_alamire" as well. Interested users could track to the image and visualize. It is gorgeous ;)

# Quick Start Hand-on Commands: Simple Version
The above command installs our toolbox and its dependencies into the user's default python site-packages. Then s/he can start the transcription in a Python terminal as:

```python
import alamire_of_tamir  
f_i = "path/to/your/input/file.annotation"  
f_o = "path/to/your/output/file.xml"  
alamire_of_tamir.transcribe_script(f_i,f_o) 
```

Here f_i and f_o represent the input annotation file and output xml file, respectively. The output result file is in MusicXML format, which is displayable and editable using third-party software, e.g. MuseScore, Finale etc. 
# Codes Break Down Version: For Curious Users

Users can use our toolbox with a one-line command  as described in previously. Yet, it is far from perfect and it is therefore beneficial to enable users to easily make modifications. Below one finds the code spelled out in terms of its parts, which can be swapped with novel tools.

```python
import alamire_of_tamir
#   Specify the input annotation file  
filename = 'path/to/your/input/file.annotation'  
#   Declare an object of AnnotationPage class  
ann = alamire_of_tamir.read_write_init.AnnotationPage()  
#   Load the information in annotation file.
ann.read_annotation_file(filename)  
#   Transcription happens here. Ligature transcription is also called by this function. You might would like to trace back to its class, then blend in here.  
s = ann.process_modern()  
#   The output s is a music21 stream object. Details at: http://web.mit.edu/music21/ 
#   We suggest to install lilypond to visualize directly from code, http://www.lilypond.org
s.show()  
#   To export the result into MusicXML, use:  
outfile = 'path/to/your/output/file.xml'  
s.write('xml',outfile)
#   To generate the MIDI performance, do this:
outmidifile = 'path/to/your/output/midifile.mid'
s.write('midi', outmidifile)
```

# Contact Information
Xuanli Chen

PhD student at PSI-VISICS, KU Leuven

Supervisor: Prof. Luc Van Gool

Research Domain: Computer Vision, Machine Learning


Address:

Kasteelpark Arenberg 10 - bus 2441

B-3001 Heverlee

Belgium

Group website: http://www.esat.kuleuven.be/psi/visics

LinkedIn: https://be.linkedin.com/in/xuanlichen
