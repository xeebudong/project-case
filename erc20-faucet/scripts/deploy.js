// 部署脚本：npx hardhat run scripts/deploy.js --network sepolia
const { ethers } = require("hardhat");

async function main() {
  const initial = ethers.parseUnits("1000000", 18);
  const Token = await ethers.getContractFactory("AureliaToken");
  const token = await Token.deploy(initial);
  await token.waitForDeployment();
  console.log("AureliaToken deployed to:", await token.getAddress());
  console.log("→ 把该地址填入 web/app.js 的 CONTRACT_ADDRESS");
}

main().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
