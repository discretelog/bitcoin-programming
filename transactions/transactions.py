from helper import hash256

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