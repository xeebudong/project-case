# erc20-faucet

一个自包含的 **ERC-20 代币 + 领取水龙头（faucet）** 合约，配套 **ethers.js 前端领取页**。
合约无外部依赖，逻辑清晰；前端连接 MetaMask 后可查余额、看冷却、一键领取。

## 合约 · AureliaToken (AUR)

- 标准 ERC-20：`transfer` / `approve` / `transferFrom` / 事件
- 水龙头：`claim()` 每地址每 24h 领 100 AUR，`timeUntilClaim()` 返回剩余冷却
- 安全点：转账零地址校验、余额/授权校验、`unchecked` 仅用于不可能溢出处

## 测试（Hardhat）

```bash
npm install
npx hardhat test
```

覆盖：初始铸造、转账、领取、冷却拦截、冷却剩余时间。

## 部署到测试网

```bash
export SEPOLIA_RPC=...   export PRIVATE_KEY=...
npm run deploy:sepolia
# 把输出的合约地址填入 web/app.js 的 CONTRACT_ADDRESS
```

## 前端

`web/index.html` + `web/app.js`（ethers v6，CDN 引入）。本地起个静态服务器即可：

```bash
cd web && python -m http.server 5600   # 需浏览器装 MetaMask 并切到部署网络
```

## 结构

```
contracts/AureliaToken.sol   代币 + 水龙头合约
scripts/deploy.js            部署脚本
test/token.test.js           合约测试
web/index.html, web/app.js   领取页前端
hardhat.config.js
```
