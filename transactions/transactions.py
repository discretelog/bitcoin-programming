from helper import (
        hash256,
        little_endian_to_int,
        int_to_little_endian,
        parse_varint,
    )

class Tx:

    def __init__(self, version, tx_in, tx_out, locktime, testnet=True):
        self.version = version
        self.tx_in = tx_in
        self.tx_out = tx_out
        self.locktime = locktime
        self.testnet = testnet

    def id(self):
        self.hash().hex()

    def hash(self):
        return hash256(self.serialize())[::-1]

    def __repr__(self):
        tx_ins = ''
        for tx in self.tx_in:
            tx_ins += tx.__repr__() + '\n'
        tx_outs = ''
        for tx in self.tx_out:
            tx_outs += tx.__repr__() + '\n'
        return 'id:{}\nversion:{}\ntx_ins:{}\ntx_outs:{}\nlocktime:{}'.format(
                self.id,
                self.version,
                tx_ins,
                tx_outs,
                self.locktime)

    def parse(cls, s, testnet=False):
        version = little_endian_to_int(s.read(4))
        num_inputs = parse_varint(s)
        inputs = []
        for _ in range(num_inputs):
            inputs.append(TxIn.parse(s))
        return cls(version, inputs, None, None, testnet=testnet)


class TxIn:

    def __init__(self, prev_tx, prev_index, script_sig=None,
                 sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence

    def __repr__(self):
        return '{} : {} '.format(
                self.prev_tx.hex(),
                self.prev_index)