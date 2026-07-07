// Hardhat 测试：ERC-20 基本行为 + 水龙头冷却
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("AureliaToken", function () {
  let token, owner, alice;

  beforeEach(async function () {
    [owner, alice] = await ethers.getSigners();
    const Token = await ethers.getContractFactory("AureliaToken");
    token = await Token.deploy(ethers.parseUnits("1000000", 18));
  });

  it("mints initial supply to deployer", async function () {
    expect(await token.balanceOf(owner.address)).to.equal(ethers.parseUnits("1000000", 18));
  });

  it("transfers tokens", async function () {
    await token.transfer(alice.address, ethers.parseUnits("50", 18));
    expect(await token.balanceOf(alice.address)).to.equal(ethers.parseUnits("50", 18));
  });

  it("claims from faucet", async function () {
    await token.connect(alice).claim();
    expect(await token.balanceOf(alice.address)).to.equal(ethers.parseUnits("100", 18));
  });

  it("enforces cooldown", async function () {
    await token.connect(alice).claim();
    await expect(token.connect(alice).claim()).to.be.revertedWith("cooldown: try again later");
  });

  it("reports time until next claim", async function () {
    await token.connect(alice).claim();
    expect(await token.timeUntilClaim(alice.address)).to.be.greaterThan(0);
  });
});
