from qmae.audio import Audio


class QMAEPluginSE:

    def __init__(self, data: dict):

        self.ambience = data["ambience"]
        self.presence = data["presence"]
        self.sshaper = data["sshaper"]
        self.stereoizer = data["stereoizer"]

    def applyto(self, audio: Audio):

        raise NotImplementedError
