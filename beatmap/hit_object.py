from util.vector import Vector


class HitObject(object):
    @classmethod
    def parse(cls, line):
        parts = line.split(",")
        properties = {}
        properties["sound_type"] = int(parts[4])
        properties["object_type"] = int(parts[3])

        properties["original_line"] = line
        properties["start_time"] = properties["end_time"] = int(parts[2])
        properties["sound_types"] = []
        properties["new_combo"] = (properties["object_type"] & 4) == 4
        properties["position"] = Vector(int(parts[0]), int(parts[1]))

        if properties["object_type"] & 1:
            return SingleObject(properties)
        else:
            return HoldObject(properties)

    def __init__(self, properties):
        for key in properties:
            setattr(self, key, properties[key])


class SingleObject(HitObject):
    def __init__(self, properties):
        super(SingleObject, self).__init__(properties)


class HoldObject(HitObject):
    def __init__(self, properties):
        super(HoldObject, self).__init__(properties)
