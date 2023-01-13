
# Description

This library uses `ffmpeg` to extract a/the audio track from a video file.  The audio can also be separated by chapter, if the chapters are annotated in the video.

# Installation

TODO

The `ffmpeg` and `ffprobe` commands must be available on your system (and `PATH`).

# Usage

```python
from video2audio import AVFile

f = AVFile('/path/to/some/movie.mkv')

# Extract the entire audio track as a single mp3:
f.extract_audio('/path/to/some/audio_only.mp3', chapter=None)

# Extract the second, entire audio track as a single mp3:
f.extract_audio('/path/to/some/audio_only_second_stream.mp3', chapter=None, stream=1)

# Extract each chapter to a separate mp3 file:
f.extract_all_chapters_audio('/path/to/chapter/outputs/')

# Extract each chapter to a separate mp3 file, manually naming them:
f.extract_all_chapters_audio(
    '/path/to/chapter/outputs/',
    output_filenames=['ch1_title.mp3', 'ch2_title.mp3', 'ch3_title.mp3']
)

# Extract only chapter number 12 (or 13, using 1-indexing):
chapter_list = f.get_chapters()
f.extract_audio('single_chapter.mp3', chapter=chapter_list[12])
```

## CLI

TODO: document it, if we add a CLI command.

# TODO

* Add tests
* Check for injection / missing escapes
