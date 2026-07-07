// AUR Faucet 前端：连接钱包 → 读余额/冷却 → 领取
// 部署后把合约地址填到这里：
const CONTRACT_ADDRESS = "0x0000000000000000000000000000000000000000";

const ABI = [
  "function balanceOf(address) view returns (uint256)",
  "function claim()",
  "function timeUntilClaim(address) view returns (uint256)",
  "event Claim(address indexed to, uint256 value)"
];

let provider, signer, contract, account;

const $ = (id) => document.getElementById(id);
const setStatus = (msg) => ($("status").textContent = msg || "");

function fmtDuration(sec) {
  sec = Number(sec);
  if (sec <= 0) return "现在可领";
  const h = Math.floor(sec / 3600);
  const m = Math.floor((sec % 3600) / 60);
  return `${h}h ${m}m 后`;
}

async function connect() {
  if (!window.ethereum) {
    setStatus("未检测到钱包，请安装 MetaMask。");
    return;
  }
  provider = new ethers.BrowserProvider(window.ethereum);
  await provider.send("eth_requestAccounts", []);
  signer = await provider.getSigner();
  account = await signer.getAddress();
  contract = new ethers.Contract(CONTRACT_ADDRESS, ABI, signer);

  $("connect").style.display = "none";
  $("panel").style.display = "block";
  $("addr").textContent = account.slice(0, 6) + "…" + account.slice(-4);
  const net = await provider.getNetwork();
  $("net").textContent = net.name + " (" + net.chainId + ")";
  await refresh();
}

async function refresh() {
  if (CONTRACT_ADDRESS.startsWith("0x0000")) {
    setStatus("请先在 app.js 中填入已部署的合约地址。");
    return;
  }
  try {
    const [bal, cool] = await Promise.all([
      contract.balanceOf(account),
      contract.timeUntilClaim(account)
    ]);
    $("bal").textContent = ethers.formatUnits(bal, 18) + " AUR";
    $("cool").textContent = fmtDuration(cool);
    $("claim").disabled = Number(cool) > 0;
  } catch (e) {
    setStatus("读取失败：请确认已切换到合约所在网络。");
  }
}

async function claim() {
  try {
    setStatus("发送交易中…");
    const tx = await contract.claim();
    setStatus("等待上链：" + tx.hash.slice(0, 10) + "…");
    await tx.wait();
    setStatus("领取成功！");
    await refresh();
  } catch (e) {
    setStatus("领取失败：" + (e.shortMessage || e.message || "交易被拒绝"));
  }
}

$("connect").addEventListener("click", connect);
$("claim").addEventListener("click", claim);
