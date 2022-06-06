import datetime as dt
import hashlib as _hashlib
import json as _json


class Blockchain:
    def __init__(self):
        self.chain = list()
        initial_block = self._create_block(
            data="genesis block", proof=1, previous_hash="0", index=1
        )
        self.chain.append(initial_block)

    def _mine_block(self, data: str) -> dict:
        previous_block = self.chain[-1]
        previous_proof = previous_block["proof"]
        index = len(self.chain) + 1
        proof = self._proof_of_work(previous_proof=previous_proof, index=index, data=data)
        previous_hash = self._hash(block=previous_block)
        block = self._create_block(data=data, proof=proof, previous_hash=previous_hash, index=index)
        self.chain.append(block)
        return block

    def _create_block(self, data: str, proof: int, previous_hash: str, index: int) -> dict:
        block = {
            "index": index,
            "timestamp": str(dt.datetime.now()),
            "data": data,
            "proof": proof,
            "previous_hash": previous_hash,
        }
        return block


    def _proof_of_work(self, previous_proof: str, index: int, data: str) -> int:
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = _hashlib.sha256((str(new_proof ** 2 - previous_proof ** 2 + index) + data).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def _hash(self, block: dict) -> str:
        return _hashlib.sha256(_json.dumps(block, sort_keys=True).encode()).hexdigest()

    def is_chain_valid(self) -> bool:
        previous_block = self.chain[0]
        block_index = 1
        while block_index < len(self.chain):
            block = self.chain[block_index]
            if block["previous_hash"] != self._hash(previous_block):
                return False
            previous_proof = previous_block["proof"]
            index, data, proof = block["index"], block["data"], block["proof"]
            hash_operation = _hashlib.sha256((str(proof ** 2 - previous_proof ** 2 + index) + data).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True