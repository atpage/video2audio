import os
import subprocess
import shlex
from shutil import which
from warnings import warn

# import ffmpeg  # can't seem to get chapter data with this


class AVFile:
    def __init__(self, filename=None):
        if type(filename) != str:
            raise TypeError('filename must be a string.')
        self.filename = filename

    def get_chapters(self):
        """Get a list of chapters.  Each chapter is a dict with a title, start
        time, and end time.  Titles will be automatically generated as
        'Chapter 1', 'Chapter 2', etc. if they aren't available in the
        metadata.
        """
        check_file(self.filename)
        ffprobe_path = get_bin_path('ffprobe')
        command = "ffprobe -loglevel error -i %s -print_format json -show_chapters" % (
            shlex.quote(self.filename)
        )
        try:
            output = subprocess.check_output(
                command,
                shell=True,
                # stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError:
            warn(
                "Couldn't process %s.  Will assume it has no chapters." % self.filename
            )
            return []
        results = []
        for chapnum, c in enumerate(json.loads(output)['chapters']):
            if 'title' not in c['tags']:
                title = 'Chapter ' + str(chapnum + 1)
            else:
                title = c['tags']['title']
            results.append(
                {
                    'title': title,
                    'start_time': c['start_time'],
                    'end_time': c['end_time'],
                }
            )
        return results

    def extract_audio(self, output_filename, chapter=None):
        raise NotImplementedError
        # if method == 'first_audio_track':
        #     command = "ffmpeg -v error -i %s -map 0:a:0 -f null -" % (
        #         shlex.quote(self.filename)
        #     )
        # elif method == 'full':
        #     command = "ffmpeg -v error -i %s -f null -" % (shlex.quote(self.filename))


def check_file(filename):
    if filename is None:
        raise ValueError('No filename was given.')
    if not os.path.isfile(filename):
        raise FileNotFoundError("Couldn't find %s" % filename)


def get_bin_path(binfile):
    """binfile is a command like 'ls' or 'ffmpeg'.  The full path to the
    actual binary is returned."""
    bin_path = which(binfile)
    if bin_path is None:
        raise RuntimeError("Couldn't find the %s binary." % binfile)
    return bin_path
