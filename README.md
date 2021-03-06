# Redshift Playblast

Tools to easily create Playblasts from Maya, but instead of OpenGL render them with Redshift for proper DOF, Motion Blur, lighting etc.
Demo video: https://vimeo.com/252221253
# Features
- a command line script to create the playblast
- a Deadline Plugin to create the playblast on the Render Farm
- a Maya Tool with settings to create the playblast

# Requirements
- ffmpeg is required to stitch the single rendered frames together
- mock is required to run the tests, Qt.py for GUI/Signals

# Installation
### Maya
- install Python Dependencies:
You have tow options:
1. using pip
```sh
pip install -r requirements.txt --target <some_folder_in_PYTHONPATH_for_Maya>
```
2. Download Qt.py manually and place it in some_folder_in_PYTHONPATH_for_Maya, mock is only required to run tests:
https://github.com/mottosso/Qt.py
- install ffmpeg, download here: https://www.ffmpeg.org/download.html
- adjust the hook get_ffmpeg_folder() in redshift_playblast/hooks/hooks.py to the path of your ffmpeg folder
- copy the folder "redshift_playblast" to some folder in PYTHONPATH for Maya

### Deadline
- the folder "RedshiftPlayblast" is the Deadline Plugin. Inside your Deadline Repository, copy the folder to <DEADLINE_REPOSITOY>/custom/plugins
- configure the path to redshift_playblast/playblast.py file in the plugin settings in your Deadline Repository

# Usage
Run inside Maya 
```python
from redshift_playblast.view import redshift_playblast_view
redshift_playblast_view.run_maya()
```
# Limitations / knows issues
- only tested under Windows
- only Deadline 10 is supported as a Render Manager
- only Deadline is supported as a Render Manager
- Deadline currently only supports a single render task, so only one machine will be rendering
- the script renders single images and stitches them together to a Quicktime using ffmpeg. These single images are rendered as .png files instead of .exr,
because ffmpeg has problems with exrs from Redshift

