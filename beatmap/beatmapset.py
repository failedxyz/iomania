import os

import beatmap


class BeatmapSet(object):
    @classmethod
    def load(cls, folder):
        files = os.listdir(folder)

        beatmapset = BeatmapSet()
        for file in files:
            if file.endswith(".osu"):
                map = beatmap.Beatmap.load_file(os.path.join(folder, file))
                beatmapset.beatmaps.append(map)

        beatmapset.beatmaps.sort(key=lambda beatmap: repr(beatmap))
        return beatmapset

    def __init__(self):
        self.beatmaps = []
