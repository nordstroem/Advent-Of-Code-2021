import util
from dataclasses import dataclass, field
import operator
from functools import reduce

code = bin(int(util.read_file("inputs/day16.txt").strip(), 16))[2:]
padding = min(4-len(code) % 4, len(code) % 4)
code = util.split("0"*padding + code)


@dataclass
class Packet:
    version: int
    type_id: int
    value: int = None
    sub_packets: list = field(default_factory=list)


def consume(bits, num_bits):
    consumed_bits = bits[:num_bits]
    for i in range(num_bits):
        bits.pop(0)
    return consumed_bits


def to_int(bits):
    return int("".join(bits), 2)


def parse_literal(code):
    literal = []
    while True:
        bit_id = to_int(consume(code, 1))
        literal += consume(code, 4)
        if bit_id == 0:
            break
    return to_int(literal)


def parse_packet(code):
    version = to_int(consume(code, 3))
    type_id = to_int(consume(code, 3))
    packet = Packet(version, type_id)
    if type_id == 4:
        packet.value = parse_literal(code)
    else:
        operator_id = to_int(consume(code, 1))
        if operator_id == 0:
            sub_packets_bits = to_int(consume(code, 15))
            consumed_bits = 0
            code_length = len(code)
            while consumed_bits < sub_packets_bits:
                packet.sub_packets.append(parse_packet(code))
                consumed_bits += code_length - len(code)
                code_length = len(code)
        if operator_id == 1:
            num_sub_packets = to_int(consume(code, 11))
            for i in range(num_sub_packets):
                packet.sub_packets.append(parse_packet(code))
    return packet


def total_version_number(packet):
    total = packet.version
    for sub_packet in packet.sub_packets:
        total += total_version_number(sub_packet)
    return total


def part1():
    print(total_version_number(parse_packet(code)))


def compute(packet):
    if packet.value:
        return packet.value
    elif packet.type_id == 0:
        return sum(compute(p) for p in packet.sub_packets)
    elif packet.type_id == 1:
        return reduce(operator.mul, [compute(p) for p in packet.sub_packets], 1)
    elif packet.type_id == 2:
        return min(compute(p) for p in packet.sub_packets)
    elif packet.type_id == 3:
        return max(compute(p) for p in packet.sub_packets)
    elif packet.type_id == 5:
        p0, p1 = packet.sub_packets
        return 1 if compute(p0) > compute(p1) else 0
    elif packet.type_id == 6:
        p0, p1 = packet.sub_packets
        return 1 if compute(p0) < compute(p1) else 0
    elif packet.type_id == 7:
        p0, p1 = packet.sub_packets
        return 1 if compute(p0) == compute(p1) else 0


def part2():
    print(compute(parse_packet(code)))
