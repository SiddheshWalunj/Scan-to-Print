from dataclasses import dataclass

@dataclass
class PrintSettings:
    color: bool
    duplex: bool
    copies: int
    pages: int
