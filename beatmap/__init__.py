import re

import beatmapset
from hit_object import HitObject
from timing_point import TimingPoint

re_split_lines = re.compile(r"\r?\n")
re_section = re.compile(r"^\[([a-zA-Z0-9]+)\]$")
re_osu_format = re.compile(r"osu\ file\ format (v[0-9]+)")
re_key_pair = re.compile(r"^([a-zA-Z0-9]+)[ ]*:[ ]*(.+)$")
re_combo_color = re.compile(r"combo(\d+)")

STAR_SCALING_FACTOR = 0.018
INDIVIDUAL_DECAY_BASE = 0.125
OVERALL_DECAY_BASE = 0.3
DECAY_WEIGHT = 0.9
STRAIN_STEP = 400


class Beatmap(object):
    @classmethod
    def load_file(cls, file):
        beatmap = Beatmap()

        data = open(file, "r").read()
        lines = re_split_lines.split(data)
        section = ""
        sections = {
            "timing_points": [],
            "hit_objects": [],
            "events": []
        }
        beatmap.combo_colors = []

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            match = re_section.match(line)
            if match:
                section = match.group(1).lower()
                continue
            if section == "timingpoints":
                sections["timing_points"].append(line)
            elif section == "hitobjects":
                sections["hit_objects"].append(line)
            elif section == "events":
                sections["events"].append(line)
            else:
                if not section:
                    match = re_osu_format.match(line)
                    if match:
                        beatmap.file_format = match.group(1)
                        continue
                else:
                    match = re_key_pair.match(line)
                    if match:
                        if re_combo_color.match(match.group(1)):
                            # something
                            continue
                        if match.group(1).lower() == "tags":
                            beatmap.tags = match.group(2).split(" ")
                        elif match.group(1).lower() in ["stackleniency", "distancespacing", "beatdivisor", "gridsize",
                                                        "previewtime", "mode",
                                                        "hpdrainrate", "circlesize", "approachrate",
                                                        "overalldifficulty", "slidermultiplier",
                                                        "slidertickrate"]:
                            setattr(beatmap, match.group(1).lower(), float(match.group(2)))
                        else:
                            setattr(beatmap, match.group(1).lower(), match.group(2))

        beatmap.timing_points = []
        beatmap.bpm_max = float("inf")
        beatmap.bpm_min = 0
        prev = None
        for i, line in enumerate(sections["timing_points"]):
            point = TimingPoint.parse(line)
            if point.bpm:
                beatmap.bpm_max = max(beatmap.bpm_max, point.bpm)
                beatmap.bpm_min = min(beatmap.bpm_min, point.bpm)
                point.base_offset = point.offset
            elif prev:
                point.beat_length = prev.beat_length
                point.bpm = prev.bpm
                point.base_offset = prev.base_offset
            prev = point
            beatmap.timing_points.append(point)
        beatmap.timing_points.sort(key=lambda point: point.offset)

        beatmap.hit_objects = []
        for i, line in enumerate(sections["hit_objects"]):
            obj = HitObject.parse(line)
            obj.beatmap = beatmap
            beatmap.hit_objects.append(obj)
        beatmap.hit_objects.sort(key=lambda obj: obj.start_time)

        beatmap.columns = int(beatmap.circlesize)

        return beatmap

    def __repr__(self):
        return "%s - %s [%s]" % (self.artist, self.title, self.version)

    def unicode(self):
        return "%s - %s [%s]" % (self.artistunicode, self.titleunicode, self.version)
