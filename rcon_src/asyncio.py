"""Asynchronous RCON."""

from asyncio import open_connection
from typing import IO

from rcon.exceptions import RequestIdMismatch, WrongPassword
from rcon.proto import Packet, Type


__all__ = ['rcon']


async def communicate(reader: IO, writer: IO, packet: Packet) -> Packet:
    """Asynchronous requests."""

    writer.write(bytes(packet))
    await writer.drain()
    return await Packet.aread(reader)


async def rcon(command: str, *arguments: str, host: str, port: int,
               passwd: str, encoding: str = 'utf-8') -> str:
    """Runs a command asynchronously."""

    reader, writer = await open_connection(host, port)
    login = Packet.make_login(passwd, encoding=encoding)
    response = await communicate(reader, writer, login)

    # Wait for SERVERDATA_AUTH_RESPONSE according to:
    # https://developer.valvesoftware.com/wiki/Source_RCON_Protocol
    while response.type != Type.SERVERDATA_AUTH_RESPONSE:
        response = await Packet.aread(reader)

    if response.id == -1:
        raise WrongPassword()

    request = Packet.make_command(command, *arguments, encoding=encoding)
    response = await communicate(reader, writer, request)

    if response.id != request.id:
        raise RequestIdMismatch(request.id, response.id)

    return response.payload.decode(encoding)
