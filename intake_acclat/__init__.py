import intake

from intake.container import register_container

from .source.AccLat import AccLatSource
from .containers.acclat import  RemoteAccLat

intake.register_driver('remote_acclat', RemoteAccLat)
register_container('acclat', RemoteAccLat)