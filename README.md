# EVM Balance Tracker

EVM Balance Tracker 是一个 Python 应用，用于从多个 Ethereum 兼容网络查询和记录指定地址的原生代币和 ERC-20 代币余额。

## 功能

- 支持多个网络，包括 Ethereum、Linea、Arbitrum 等。
- 查询原生代币余额。
- 查询常见的 ERC-20 代币余额，如 USDT、USDC、MATIC 和 WETH。
- 结果输出为 CSV 文件，包括时间戳。

## 必要条件

使用这个脚本之前，你需要安装以下依赖：

- Python 3.6+
- `web3.py`
- `pandas`
- `tqdm`

你可以使用以下命令安装这些依赖：

```bash
git clone https://github.com/hubei-xhjy/Blockchain-account-balance-retriever.git
cd Blockchain-account-balance-retriever
virtualenv .venv
source .venv/bin/activate
pip install web3 pandas tqdm
```

## 使用说明

1. **配置 API 密钥**：
   在 `INFURA_API_KEY` 变量中设置你的 Infura API 密钥。

2. **添加 ERC-20 ABI**：
   确保 `erc20-abi.json` 文件在同一目录下，并包含用于 ERC-20 代币交互的 ABI。

3. **设置地址列表**：
   在 `address_list` 中填入你要查询的地址。

4. **运行脚本**：
   使用以下命令运行脚本：

   ```bash
   python3 evm_balance_tracker.py
   ```

   结果将保存在当前目录的一个新的 CSV 文件中，文件名包括时间戳。

## 结果解释

CSV 文件中的每一行代表一个地址在不同网络上的代币余额。列名为网络和代币的组合，如 `Ethereum-Native` 或 `Linea-USDC`。

## 注意事项

- 确保所有查询的网络都在 `RPC_LISTS` 中正确配置了 RPC URL。
- 此脚本通过 Infura 进行网络连接，因此需要有效的 API 密钥和网络可用性。

## 贡献

如果你想改进这个项目或报告问题，请通过 GitHub Issue 或 Pull Request 提交。

## 许可证

[MIT License](LICENSE)
