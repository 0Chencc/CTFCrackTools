<div align="center">

[English](README_en.md) | 简体中文

# CTFCrackTools X

**新一代节点化 CTF 工具箱**

*从 V4 到 X —— 不只是版本号的升级*

![CTFCrackTools X](img/theme.jpg)

[![Release](https://img.shields.io/github/v/release/0Chencc/CTFCrackTools?style=flat-square)](https://github.com/0Chencc/CTFCrackTools/releases)
[![License](https://img.shields.io/github/license/0Chencc/CTFCrackTools?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue?style=flat-square)]()

[下载](#下载) | [功能特性](#功能特性) | [作者留](#作者留)

</div>

---

## 品牌升级

**CTFCrackTools X** 是 CTFCrackTools 的全新一代版本。"X" 代表着：

- **eXtreme** — 极致的性能与体验
- **eXtensible** — 可扩展的节点化架构
- **neXt** — 面向未来的技术栈

| | CTFCrackTools V4 | CTFCrackTools X |
|---|---|---|
| 界面 | 传统表单 | **节点化工作流** |
| 性能 | Java 运行时 | **原生性能** |
| 体积 | ~50MB+ | **<15MB** |
| 跨平台 | 需要 JRE | **原生支持** |

---

## 功能特性

### 节点化工作流

告别传统的线性操作，通过可视化节点自由组合编解码流程。

1. **下载并安装** 适合你系统的版本
2. **启动应用**，你会看到一个空白画布
3. **右键添加节点**：Input → 编码节点 → Output
4. **连接节点**，输入文本，点击执行

![Workflow](img/workflow.gif)

### 43+ 内置算法

覆盖 CTF 常见的编解码、加密、哈希需求：

<details>
<summary><b>编码 (15)</b></summary>

- Base64 / Base32 / Base58 / Base85
- Hex / URL / ASCII / Binary
- Morse / UUEncode / ROT47
- Unicode / HTML Entity
- JWT Decode / Brainfuck

</details>

<details>
<summary><b>古典密码 (11)</b></summary>

- Caesar / ROT13 / Atbash
- Vigenère / Beaufort
- Playfair / Polybius
- Affine / Rail Fence
- Bacon / XOR

</details>

<details>
<summary><b>现代加密 (5)</b></summary>

- AES-128-CBC
- DES / 3DES
- Blowfish
- RC4

</details>

<details>
<summary><b>哈希 & KDF (6)</b></summary>

- MD5 / SHA1 / SHA256 / SHA512
- HMAC-SHA256
- PBKDF2

</details>

<details>
<summary><b>文本处理 (7)</b></summary>

- Uppercase / Lowercase
- Reverse / Trim
- Capitalize / SwapCase
- Length

</details>

### 跨平台支持

原生支持 Windows、macOS、Linux，无需安装运行时。

---

## 下载

前往 [Releases](https://github.com/0Chencc/CTFCrackTools/releases) 下载适合你系统的版本：

| 平台 | 文件名 |
|------|------|
| Windows x64 | `ctfcracktools-x-windows-x64.exe` |
| macOS ARM64 | `ctfcracktools-x-macos-arm64` |
| Linux x64 | `ctfcracktools-x-linux-x64` |

> **注意**: macOS/Linux 用户下载后需要添加执行权限：`chmod +x ctfcracktools-x-*`

---

## 作者留

很长的一段时间里，我收到过许多关于本工具的反馈，但是因为很长一段时间没有接触CTF这个圈子所以一直搁置，这个项目也因为年轻时不懂事错误地迭代了四个大版本。

因为很多朋友反馈本工具的问题并非通过github，而是通过我私人的联系方式，这也导致我常常忘记。

我印象中本工具最初是在2016发布的，同时我多次清理commit记录，因为年轻时不懂事并不知道如何规范地push代码，为了规范化和代码的整洁只能不停地覆盖git记录。

现在已经熟练掌握git地操作了，但是也已经过去了十年，我想起了十年前使用eclipse编程的那个过年夜，如果时间可以停留在当年该有多美好。

近期的一段时间，我一直在参与或者主导一些我兴趣使然的项目，当我检索以前写过的项目里，我注意到这款我16岁时编写的工具，我也想起当时挑灯夜战做CTF题目的初心。确实本工具在开源的圈子并不算非常优秀的工具，它仅仅只是一个新手入门的工具。

之所以让这段话留在文末是希望抛开煽情本身让大家更专注于工具功能本身，我很清楚这款工具在十年后的今天并非“优秀”的工具，所以我希望在日后能够不停地更新让这款工具重新被大家使用。在重构本项目前，我特地翻看了几年前自己的留言，以及在搜索引擎上搜索了本工具的相关内容，我看到一些博主在今天仍然在推荐我的工具，以及在一些write up提到我这款工具，这让我非常开心。谢谢大家这么多年的支持。

为了让本工具能在当前的环境下依然能发挥一点余热，我花费了一点时间使用全新的架构对本项目进行重构。希望你能喜欢。

在提交代码的这一天是2025年12月25号，是圣诞节，祝大家圣诞节愉快。
<div align="center">

**CTFCrackTools X** — *Perhaps it will be better than better*

Made with Rust + React by [0Chencc](https://github.com/0Chencc)

</div>
