import typing

class SupportsRead(typing.Protocol):
    def read(self, size: int =-1) -> bytes:
        ...
