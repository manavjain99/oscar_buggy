from goprocam import GoProCamera
from goprocam import constants
gopro = GoProCamera.GoPro()
gopro.streamSettings(resolution = "R480p")
gopro.stream("udp://127.0.0.1:10000?overrun_nonfatal=1&fifo_size=557753", quality = "low")