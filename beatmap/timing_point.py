class TimingPoint(object):
    @classmethod
    def parse(cls, line):
        point = TimingPoint()
        parts = line.split(",")

        point.bpm = None

        point.offset = int(parts[0])
        point.velocity = 1
        point.beat_length = float(parts[1])
        point.timing_signature = int(parts[2])
        point.sample_set_id = int(parts[3])
        point.custom_sample_index = int(parts[4])
        point.sample_volume = int(parts[5])
        point.timing_change = int(parts[6]) == 1
        point.kiai_time_active = int(parts[7]) == 1

        if point.beat_length > 0:
            point.bpm = round(60000.0 / point.beat_length)
            point.base_offset = point.offset
        else:
            point.velocity = abs(100.0 / point.beat_length)

        return point

    def __repr__(self):
        return "TimingPoint(%s)" % (self.offset)
