from web3 import Web3
import random
from datetime import datetime
import pandas as pd
from tqdm import trange

INFURA_API_KEY = "b6bf7d3508c941499b10025c0776eaf8"

address_list = [
    "0xd88032e588EEe73bC3e682be4EcB9B740dfb014a",
    "0x369c54759Cb1AE18a897ED2c6230Cf2043b92eF9"
]

RPC_LISTS = {
    "Ethereum": [
        f"https://mainnet.infura.io/v3/{INFURA_API_KEY}"
    ],
    "Linea": [
        f"https://linea-mainnet.infura.io/v3/{INFURA_API_KEY}"
    ],
    "Arbitrum": [
        f"https://arbitrum-mainnet.infura.io/v3/{INFURA_API_KEY}"
    ],
    "Optimism": [
        f"https://optimism-mainnet.infura.io/v3/{INFURA_API_KEY}"
    ],
    "Polygon": [
        f"https://polygon-mainnet.infura.io/v3/{INFURA_API_KEY}"
    ],
    "Avalanche": [
        f"https://avalanche-mainnet.infura.io/v3/{INFURA_API_KEY}"
    ],
    "Base": [
        # f"https://base-mainnet.infura.io/v3/{INFURA_API_KEY}"
        f"https://base.llamarpc.com",
        f"https://mainnet.base.org"
    ],
    "Blast": [
        f"https://rpc.blastblockchain.com"
    ],
    "Celo": [
        f"https://celo-mainnet.infura.io/v3/{INFURA_API_KEY}"
    ],
    "Palm": [
        f"https://palm-mainnet.infura.io/v3/{INFURA_API_KEY}"
    ],
    "Starknet": [
        f"https://starknet-mainnet.infura.io/v3/{INFURA_API_KEY}"
    ],
    "Mode": [
        f"https://1rpc.io/mode",
        f"https://mainnet.mode.network",
        f"https://mode.drpc.org"
    ],
    "BNB Smart Chain": [
        f"https://bsc-dataseed.bnbchain.org",
        f"https://bsc-dataseed1.defibit.io",
        f"https://bsc-dataseed1.ninicoin.io",
        f"https://bsc-dataseed3.defibit.io",
        f"https://bsc-dataseed4.defibit.io",
        f"https://bsc-dataseed2.ninicoin.io",
        f"https://bsc-dataseed3.ninicoin.io",
        f"https://bsc-dataseed4.ninicoin.io",
        f"https://bsc-dataseed1.bnbchain.org",
        f"https://bsc-dataseed2.bnbchain.org",
        f"https://bsc-dataseed3.bnbchain.org",
        f"https://bsc-dataseed4.bnbchain.org"
    ],
    "zkSync": [
        f"https://mainnet.era.zksync.io",
        f"https://zksync-era.blockpi.network/v1/rpc/public",
        f"https://1rpc.io/zksync2-era",
        f"https://endpoints.omniatech.io/v1/zksync-era/mainnet/public",
        f"https://zksync.drpc.org",
        f"https://zksync.meowrpc.com"
    ],
    "Zora": [
        f"https://rpc.zora.energy"
    ],
    "Dymension": [
        f"https://jsonrpc.dymension.nodestake.org",
        f"https://evm-archive.dymd.bitszn.com",
        f"https://dymension.liquify.com/json-rpc",
        f"https://dymension-evm.blockpi.network/v1/rpc/public",
        f"https://dymension-evm-rpc.publicnode.com"
    ]
}


class EvmBalance():
    def __init__(self) -> None:
        with open("erc20-abi.json") as abi_file:
            self.erc20_abi = "".join(abi_file.readlines())
        self.wallet_address = ""
        self.network_name = ""
        self.w3 = Web3()
        self.results = dict()

    def get_rpc(self, network: str):
        return random.choice(RPC_LISTS[network])

    def connect(self, network: str):
        self.network_name = network
        connected = False
        while not connected:
            self.w3.provider = Web3.HTTPProvider(self.get_rpc(network))
            connected = self.w3.provider.is_connected()

    def chg_address(self, new_address: str):
        self.wallet_address = self.w3.to_checksum_address(new_address)

    def get_native_token_balance(self):
        try:
            balance = self.w3.eth.get_balance(self.wallet_address)
            eth_balance = self.w3.from_wei(balance, 'ether')
            self.results[self.wallet_address][f"{self.network_name}-Native"] = float(balance)
            return float(eth_balance)
        except Exception as e:
            print(f"Something went wrong while fetching {self.network_name} data using {self.w3.provider}", e)
            self.connect(self.network_name)
            return self.get_native_token_balance()

    def get_erc20_token_balance(self, contract_address: str):
        try:
            contract_address = self.w3.to_checksum_address(contract_address)
            contract = self.w3.eth.contract(contract_address, abi=self.erc20_abi)
            token_symbol = contract.functions.symbol().call()
            decimal = contract.functions.decimals().call()
            balance = contract.functions.balanceOf(self.wallet_address).call()
            eth_balance = balance / (10 ** decimal)
            self.results[self.wallet_address][f"{self.network_name}-{token_symbol}"] = float(balance)
            return float(eth_balance)
        except Exception as e:
            print(f"Something went wrong while fetching {self.network_name} data using {self.w3.provider}", e)
            self.connect(self.network_name)
            return self.get_native_token_balance()

    # 从这里开始修改，添加你所需要的 Token 合约地址
    def get_balances(self):
        self.results[self.wallet_address] = dict()
        self.connect("Ethereum")
        self.get_native_token_balance()
        self.get_erc20_token_balance("0xdac17f958d2ee523a2206206994597c13d831ec7") # USDT
        self.get_erc20_token_balance("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48") # USDC
        self.get_erc20_token_balance("0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0") # MATIC
        self.get_erc20_token_balance("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2") # WETH

        self.connect("Linea")
        self.get_native_token_balance()

        self.connect("zkSync")
        self.get_native_token_balance()

        self.connect("Arbitrum")
        self.get_native_token_balance()

        self.connect("Optimism")
        self.get_native_token_balance()

        self.connect("Polygon")
        self.get_native_token_balance()

        self.connect("Avalanche")
        self.get_native_token_balance()

        self.connect("Base")
        self.get_native_token_balance()

        self.connect("Mode")
        self.get_native_token_balance()

        self.connect("BNB Smart Chain")
        self.get_native_token_balance()

        self.connect("Blast")
        self.get_native_token_balance()

        self.connect("Zora")
        self.get_native_token_balance()

        self.connect("Dymension")
        self.get_native_token_balance()

        # self.connect("Celo")
        # self.get_native_token_balance()

        # self.connect("Palm")
        # self.get_native_token_balance()


if __name__ == "__main__":
    balance_tracker = EvmBalance()
    for idx in trange(len(address_list)):
        address = address_list[idx]
        balance_tracker.chg_address(address)
        balance_tracker.get_balances()
    # 将字典转换为 DataFrame，并将索引重置为常规列
    df = pd.DataFrame.from_dict(
        balance_tracker.results, orient='index').reset_index()

    # 重命名重置后的索引列为 'Address'
    df.rename(columns={'index': 'Address'}, inplace=True)

    df.to_csv(f"account_balance-{datetime.now().strftime('%Y-%m-%d')}.csv")
