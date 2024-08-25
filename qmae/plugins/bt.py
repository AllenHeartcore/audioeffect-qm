from qmae.audio import Audio


class QMAEPluginBT:

    def __init__(self, data: dict):

        self.bass = data["bass"]
        self.treble = data["treble"]

    def applyto(self, audio: Audio):

        raise NotImplementedError
