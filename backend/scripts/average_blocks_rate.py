import time
from typing import List
from backend.blockchain.blockchain import Blockchain
from backend.config import SECONDS

blockchain = Blockchain()

times: List[float] = []

for i in range(1000):
    start_time: int = time.time_ns()
    blockchain.add_block(i)
    end_time: int = time.time_ns()

    time_to_mine: float = (end_time - start_time) / SECONDS
    times.append(time_to_mine)

    average_time: float = sum(times) / len(times)

    print(f"New block difficulty: {blockchain.chain[-1].difficulty}")
    print(f"Time to mine new block: {time_to_mine}")
    print(f"Average time to add blocks: {average_time}")
