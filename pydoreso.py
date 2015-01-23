# Copyright 2014 Doreso
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""A Doreso API client library.

For full API documentation, visit https://developer.doreso.com/.

Typical usage:

    doreso = Doreso('my api key')
    d = doreso.song_identify_file('./test.mp3')
    print json.dumps(d, indent=4)

In addition to standard getters and setters, we provide a few convenience
methods for document editing. For example, you can use `add_to_first_list`
to append items (in Markdown) to the first bulleted or checklist in a
given document, which is useful for automating a task list.
"""

import requests
import subprocess
import json

class Doreso(object):
    def __init__(self, api_key, base_url=None, ffmpeg_path=None):
        self.api_key = api_key
        self.base_url = base_url or 'http://developer.doreso.com/api/v1/'
        self.ffmpeg = ffmpeg_path or 'ffmpeg'

    def song_identify_file(self, filepath, start=0, duration=10):
        """Identify a audio file.

        This method will post 10 seconds wav buffer for recognition by default.
        Your can change start point or duration for practical use.
        """
        wav = self.gen_wavbuffer_from_filebuffer(open(filepath, 'rb').read(), start=start, duration=duration)
        r = requests.post(self._url('song/identify'), data=wav, headers={'Content-Type': 'application/octet-stream'})
        return r.json()
        
    def gen_wavbuffer_from_filebuffer(self, file_buffer, start=0, duration=10):
        proc = subprocess.Popen([self.ffmpeg, '-i', '-', '-ac', '1', '-ar', '8000', '-f', 'wav', '-'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=open('/dev/null'))
        wav_buffer = proc.communicate(input=file_buffer)[0]
        if len(wav_buffer) < (start*128*1024)/8:
            return wav_buffer
        return wav_buffer[(start*128*1024)/8:((start+duration)*128*1024)/8]

    def _url(self, path):
        return '%s/%s?api_key=%s' % (self.base_url, path, self.api_key) 


