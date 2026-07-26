"""
LBH Educational Protocol
HormigasAIS Edu Lab
Versión 1.0
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class LBHMessage:
    source: str
    target: str
    opcode: str
    payload: dict
    timestamp: str


class ColonyBus:

    def __init__(self):
        self.messages = []

    def emit(self, source, target, opcode, payload):

        msg = LBHMessage(
            source=source,
            target=target,
            opcode=opcode,
            payload=payload,
            timestamp=datetime.utcnow().isoformat()
        )

        self.messages.append(msg)

        return msg

    def audit(self):

        return [
            {
                "source": m.source,
                "target": m.target,
                "opcode": m.opcode,
                "payload": m.payload,
                "timestamp": m.timestamp
            }
            for m in self.messages
        ]


def demo():

    bus = ColonyBus()

    bus.emit(
        "CENTINELA",
        "TRAMPA",
        "MOSQUITO_DETECTED",
        {
            "confidence": 0.98,
            "sensor": "IR"
        }
    )

    print(bus.audit())


if __name__ == "__main__":
    demo()

