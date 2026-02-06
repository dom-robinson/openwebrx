from pycsdr.modules import ExecModule
from pycsdr.types import Format


class DablinModule(ExecModule):
    def __init__(self):
        self.serviceId = 0
        super().__init__(
            Format.CHAR,
            Format.FLOAT,
            self._buildArgs()
        )

    def _buildArgs(self):
        # Use -w so dablin outputs WAV (with correct sample rate in header); ffmpeg then resamples to 48k
        return ["bash", "-c", "dablin -w -s {:#06x} | mbuffer -q -m 1M | ffmpeg -v error -i pipe:0 -f f32le -ar 48000 -ac 1 pipe:1".format(self.serviceId)]

    def setDabServiceId(self, serviceId: int) -> None:
        self.serviceId = serviceId
        self.setArgs(self._buildArgs())
        self.restart()
