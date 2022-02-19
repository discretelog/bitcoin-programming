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
        num_outputs = parse_varint(s)
        outputs = []
        for _ in range(num_outputs):
            outputs.append(TxIn.parse(s))
        locktime = little_endian_to_int(s.read(4))
        return cls(version, inputs, outputs, locktime, testnet=testnet)

    def serialize(self):
        result = int_to_little_endian(self.version, 4)
        result += encode_varint(len(self.tx_ins))
        for tx_in in self.tx_ins:
            result += tx_in.serialize()
        result += encode_varint(len(self.tx_outs))
        for tx_out in self.tx_outs:
            result += tx_out.serialize()
        result += int_to_little_endian(self.locktime, 4)
        return result

    def fee(self, testnet=False):
        input_sum, output_sum = 0, 0
        for tx_in in self.tx_ins:
            input_sum += tx_in.get_amount(testnet=testnet)
        for tx_out in self.tx_outs:
            output_sum += tx_out.amount
        return input_sum - output_sum

    def sig_hash(self, input_index):
        s = int_to_little_endian(self.version, 4)
        s += encode_varint(len(self.tx_ins))
        for i, tx_in in enumerate(self.tx_ins):
            if i == input_index:
                s += TxIn(
                    prev_tx=tx_in.prev_tx,
                    prev_index=tx_in.prev_index,
                    script_sig=tx_in.script_pubkey(self.testnet),
                    sequence=tx_in.sequence,
                ).serialize()
            else:
                s += TxIn(
                    prev_tx=tx_in.prev_tx,
                    prev_index=tx_in.prev_index,
                    sequence=tx_in.sequence,
                ).serialize()
        s += encode_varint(len(self.tx_outs))
        for tx_out in self.tx_outs:
            s += tx_out.serialize()
        s += int_to_little_endian(self.locktime, 4)
        s += int_to_little_endian(SIGHASH_ALL, 4)
        h256 = hash256(s)
        return int.from_bytes(h256, 'big')

    def verify_input(self, input_index):
        tx_in = self.tx_ins[input_index]
        script_pubkey = tx_in.script_pubkey(testnet=self.testnet)
        z = self.sig_hash(input_index)
        combined = tx_in.script_sig + script_pubkey
        return combined.evaluate(z)

    def verify(self):
        '''Verify this transaction'''
        if self.fee() < 0:  1
            return False
        for i in range(len(self.tx_ins)):
            if not self.verify_input(i):  2
                return False
        return True

     def sign_input(self, input_index, private_key):
        z = self.sig_hash(input_index)
        der = private_key.sign(z).der()
        sig = der + SIGHASH_ALL.to_bytes(1, 'big')
        sec = private_key.point.sec()
        self.tx_ins[input_index].script_sig = Script([sig, sec])
        return self.verify_input(input_index)


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

    def serialze(self):
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += int_to_little_endian(self.sequence, 4)
        return result

    def fetch_tx(self, testnet=False):
        return TxFetcher.fetch(self.prev_tx.hex(), testnet=testnet)

    def get_amount(self, testnet=False):
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].amount


class TxOut:

    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def __repr__(self):
        return '{} : {}'.format(self.amount, self.script_pubkey)

    def script_pubkey(self, testnet=False):
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].script_pubkey

    @classmethod
    def parse(cls, s):
        amount = little_endian_to_int(s.read(8))
        script_pubkey = Script.parse(s)
        return cls(amount, script_pubkey)

    def serialize(self):
        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize()
        return result

class Fetcher:

    cache = {}

    @classmethod
    def get_url(cls, test_net=False):
        if testnet:
            return 'http://testnet.programmingbitcoin.com'
        else:
            return 'http://mainnet.programmingbitcoin.com'

    def fetch(cls, tx_id, testnet=False, fresh=False):
        if fresh or (tx_id not in cache):
            url = '{}/tx/{}.hex'.format(cls.get_url(testnet), tx_id)
            response = requests.get(url)
            try:
                raw = bytes.fromhex(response.text.strip())
            except ValueError:
                raise ValueError('unexpected response: {}'.format(response.text))
            if raw[4] == 0:
                raw = raw[:4] + raw[6:]
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
                tx.locktime = little_endian_to_int(raw[-4:])
            else:
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
            if tx.id() != tx_id:  1
                raise ValueError('not the same id: {} vs {}'.format(tx.id(),
                                  tx_id))
            cls.cache[tx_id] = tx
        cls.cache[tx_id].testnet = testnet
        return cls.cache[tx_id]
