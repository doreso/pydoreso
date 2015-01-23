Doreso API Python Client
=====

The official [Doreso API](https://developer.doreso.com/) Python client library.

```python
doreso = Doreso('my api key')
d = doreso.song_identify_file('./test.mp3')
print json.dumps(d, indent=4)
```


Requirement:

* `ffmpeg`: [https://www.ffmpeg.org/](https://www.ffmpeg.org/)
* `requests`: [http://docs.python-requests.org/en/latest/](http://docs.python-requests.org/en/latest/)

