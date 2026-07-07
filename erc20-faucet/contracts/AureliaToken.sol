// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title AureliaToken
/// @notice 自包含的极简 ERC-20 代币，内置水龙头（faucet）：每地址每 24 小时可领取一次。
/// @dev 无外部依赖，便于审阅与教学；生产环境建议改用 OpenZeppelin。
contract AureliaToken {
    string public constant name = "Aurelia Token";
    string public constant symbol = "AUR";
    uint8 public constant decimals = 18;

    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    // faucet 参数
    uint256 public constant FAUCET_AMOUNT = 100 * 1e18; // 每次领取 100 AUR
    uint256 public constant FAUCET_COOLDOWN = 1 days;
    mapping(address => uint256) public lastClaim;

    address public owner;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Claim(address indexed to, uint256 value);

    constructor(uint256 initialSupply) {
        owner = msg.sender;
        _mint(msg.sender, initialSupply);
    }

    // ---------- ERC-20 ----------
    function transfer(address to, uint256 value) external returns (bool) {
        _transfer(msg.sender, to, value);
        return true;
    }

    function approve(address spender, uint256 value) external returns (bool) {
        allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    function transferFrom(address from, address to, uint256 value) external returns (bool) {
        uint256 allowed = allowance[from][msg.sender];
        require(allowed >= value, "allowance exceeded");
        if (allowed != type(uint256).max) {
            allowance[from][msg.sender] = allowed - value;
        }
        _transfer(from, to, value);
        return true;
    }

    // ---------- Faucet ----------
    /// @notice 领取测试代币；每地址每 FAUCET_COOLDOWN 一次。
    function claim() external {
        require(
            block.timestamp - lastClaim[msg.sender] >= FAUCET_COOLDOWN,
            "cooldown: try again later"
        );
        lastClaim[msg.sender] = block.timestamp;
        _mint(msg.sender, FAUCET_AMOUNT);
        emit Claim(msg.sender, FAUCET_AMOUNT);
    }

    /// @notice 距离下次可领取还需多少秒（0 表示现在可领）。
    function timeUntilClaim(address user) external view returns (uint256) {
        uint256 elapsed = block.timestamp - lastClaim[user];
        return elapsed >= FAUCET_COOLDOWN ? 0 : FAUCET_COOLDOWN - elapsed;
    }

    // ---------- internal ----------
    function _transfer(address from, address to, uint256 value) internal {
        require(to != address(0), "transfer to zero");
        uint256 bal = balanceOf[from];
        require(bal >= value, "balance too low");
        unchecked {
            balanceOf[from] = bal - value;
            balanceOf[to] += value;
        }
        emit Transfer(from, to, value);
    }

    function _mint(address to, uint256 value) internal {
        totalSupply += value;
        unchecked {
            balanceOf[to] += value;
        }
        emit Transfer(address(0), to, value);
    }
}
