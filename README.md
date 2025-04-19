<h1 align="center">QuantumBid</h1>
<p align="center">An automated agent for running Orderbook strategies in your terminal</p>

---

<details>
<summary><strong>Table&nbsp;of&nbsp;Contents</strong></summary>

- [Experimental Technology Disclaimer](#experimental-technology-disclaimer)
- [Quickstart](#quickstart)
- [Why Codex?](#whycodex)
- [Security Model \& Permissions](#securitymodelpermissions)
  - [Platform sandboxing details](#platform-sandboxing-details)
- [System Requirements](#systemrequirements)
- [CLI Reference](#clireference)
- [Memory \& Project Docs](#memoryprojectdocs)
- [Non‑interactive / CI mode](#noninteractivecimode)
- [Recipes](#recipes)
- [Installation](#installation)
- [Configuration](#configuration)
- [FAQ](#faq)
- [Funding Opportunity](#funding-opportunity)
- [Contributing](#contributing)
  - [Development workflow](#development-workflow)
    - [Nix Flake Development](#nix-flake-development)
  - [Writing high‑impact code changes](#writing-highimpact-code-changes)
  - [Opening a pull request](#opening-a-pull-request)
  - [Review process](#review-process)
  - [Community values](#community-values)
  - [Getting help](#getting-help)
  - [Contributor License Agreement (CLA)](#contributor-license-agreement-cla)
    - [Quick fixes](#quick-fixes)
  - [Releasing `codex`](#releasing-codex)
- [Security \& Responsible AI](#securityresponsibleai)
- [License](#license)
- [Zero Data Retention (ZDR) Organization Limitation](#zero-data-retention-zdr-organization-limitation)

</details>

---

## Experimental Technology Disclaimer

QuantumBid is an experimental project under active development. It is not yet stable, may contain bugs, incomplete features, or undergo breaking changes. We’re building it in the open with the community and welcome:

- Bug reports
- Feature requests
- Pull requests
- Good vibes

Help us improve by filing issues or submitting PRs (see the section below for how to contribute)!

## Quickstart

Install globally:

```shell
Download repo locally and run the QuantumBid.py file in your local terminal.
```

Next, set your 5paisa API credentials

```shell
change the auth credentials within the credentials.py file in the auth folder
```

> **Note:** This command sets the key only for your current terminal session. To make it permanent, add your client ID and TOTP to the credentials.py file for persistence
>
> **Tip:** You can also place your API key into a `.env` file at the root of your project:
>
> ```env
> 5PAISA_API_KEY=your-api-key-here
> ```
>
> The CLI will automatically load variables from auth folder

Run interactively:

```shell
python quantumbid.py
```

That’s it – QuantumBid will download Orderbook data from 5paisa, run it inside a sandbox, install any
missing dependencies, and show you the live result. If required priveledges are given then the BOT will trade on
your behalf using your 5paisa brokerage account

---

## Why QuantumBid?

QuantumBid is built for developers who already **live in the terminal** and want
HFT strategies for thier local setups **plus** the power to actually run code, manipulate
files, and iterate – all under version control. In short, it’s _market‑making
agent_ that understands and executes your trades.

- **Zero setup** — bring your 5paisa API key and it just works!
- **Full auto-approval, while safe + secure** by running network-disabled and directory-sandboxed
- **Multimodal** — generates orderbook charts in terminal itself to give view on Bid Ask volume ✨

And it's **fully open-source** so you can see and contribute to how it develops!

---

## Security Model & Permissions

QuantumBid lets you decide _how much autonomy_ the agent receives and auto-approval policy via the
`--auth-module` in the credentials.py file in the auth folder

| Mode                      | What the agent may do without asking                                                               | Still requires approval                                                                         |
| ------------------------- | -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Suggest** <br>(default) | • Download order book data                                                                         | • **All** file writes/patches <br>• **Any** arbitrary shell commands (aside from reading files) |
| **Auto Edit**             | • Read **and** apply‑strategies for trade                                                          | • **All** shell commands                                                                        |
| **Full Auto**             | • Read/write files <br>• Execute shell commands (network disabled, writes limited to your workdir) | –                                                                                               |

In **Full Auto** every command is run **network‑disabled** and confined to the
current working directory (plus temporary files) for defense‑in‑depth. Codex
will also show a warning/confirmation if you start in **auto‑edit** or
**full‑auto** while the directory is _not_ tracked by Git, so you always have a
safety net.

Coming soon: you’ll be able to whitelist specific commands to auto‑execute with
the network enabled, once we’re confident in additional safeguards.

### Platform sandboxing details

The hardening mechanism QuantumBid uses depends on your OS:

- **macOS 12+** – commands are wrapped with **Apple Seatbelt** (`sandbox-exec`).

  - Everything is placed in a read‑only jail except for a small set of
    writable roots (`$PWD`, `$TMPDIR`, `~/.codex`, etc.).
  - Outbound network is _fully blocked_ by default – even if a child process
    tries to `curl` somewhere it will fail.

- **Linux** – there is no sandboxing by default.
  We recommend using Docker for sandboxing, where Codex launches itself inside a **minimal
  container image** and mounts your repo _read/write_ at the same path. A
  custom `iptables`/`ipset` firewall script denies all egress except the
  API. This gives you deterministic, reproducible runs without needing
  root on the host. 

---

## System Requirements

| Requirement                 | Details                                                         |
| --------------------------- | --------------------------------------------------------------- |
| Operating systems           | macOS 12+, Ubuntu 20.04+/Debian 10+, or Windows 11 **via WSL2** |
| Node.js                     | **22 or newer** (LTS recommended)                               |
| Git (optional, recommended) | 2.23+ for built‑in PR helpers                                   |
| RAM                         | 4‑GB minimum (8‑GB recommended)                                 |

> Never run `sudo pip install QuantumBid`; Download repo locally instead.

---

## Tracing / Verbose Logging

Refer to the excel log generated inside the data folder. The excel log tracks all trades the BOT executes when running

```shell
Excel data/execution_log.csv
```

---

## Zero Data Retention (ZDR) Organization Limitation

> **Note:** QuantumBid does **not** currently support OpenHFT organizations policy on localized trade execution

If you are using this repo for your firm and your organization has no localized trade execution then this agent may fail.

---

## Contributing

This project is under active development and the code will likely change pretty significantly. We'll update this message once that's complete!

More broadly we welcome contributions – whether you are opening your very first pull request or you’re a seasoned maintainer. At the same time we care about reliability and long‑term maintainability, so the bar for merging code is intentionally **high**. The guidelines below spell out what “high‑quality” means in practice and should make the whole process transparent and friendly.

### Development workflow

- Create a _topic branch_ from `main` – e.g. `feat/interactive-prompt`.
- Keep your changes focused. Multiple unrelated fixes should be opened as separate PRs.
- Use `pnpm test:watch` during development for super‑fast feedback.
- We use **Vitest** for unit tests, **ESLint** + **Prettier** for style, and **TypeScript** for type‑checking.
- Before pushing, run the full test/type/lint suite:

### Git Hooks with Husky

This project uses [Husky](https://typicode.github.io/husky/) to enforce code quality checks:

- **Pre-commit hook**: Automatically runs lint-staged to format and lint files before committing
- **Pre-push hook**: Runs tests and type checking before pushing to the remote

These hooks help maintain code quality and prevent pushing code with failing tests. For more details, see [HUSKY.md](./codex-cli/HUSKY.md).

### Writing high‑impact code changes

1. **Start with an issue.** Open a new one or comment on an existing discussion so we can agree on the solution before code is written.
2. **Add or update tests.** Every new feature or bug‑fix should come with test coverage that fails before your change and passes afterwards. 100 % coverage is not required, but aim for meaningful assertions.
3. **Document behaviour.** If your change affects user‑facing behaviour, update the README, inline help (`codex --help`), or relevant example projects.
4. **Keep commits atomic.** Each commit should compile and the tests should pass. This makes reviews and potential rollbacks easier.

### Opening a pull request

- Fill in the PR template (or include similar information) – **What? Why? How?**
- Run **all** checks locally. CI failures that could have been caught locally slow down the process.
- Make sure your branch is up‑to‑date with `main` and that you have resolved merge conflicts.
- Mark the PR as **Ready for review** only when you believe it is in a merge‑able state.

### Review process

1. One maintainer will be assigned as a primary reviewer.
2. We may ask for changes – please do not take this personally. We value the work, we just also value consistency and long‑term maintainability.
3. When there is consensus that the PR meets the bar, a maintainer will squash‑and‑merge.

### Community values

- **Be kind and inclusive.** Treat others with respect; we follow the [Contributor Covenant](https://www.contributor-covenant.org/).
- **Assume good intent.** Written communication is hard – err on the side of generosity.
- **Teach & learn.** If you spot something confusing, open an issue or PR with improvements.

### Getting help

If you run into problems setting up the project, would like feedback on an idea, or just want to say _hi_ – please open a Discussion or jump into the relevant issue. We are happy to help.

Together we can make Codex CLI an incredible tool. **Happy hacking!** :rocket:

### Contributor License Agreement (CLA)

All contributors **must** accept the CLA. The process is lightweight:

1. Open your pull request.
2. Paste the following comment (or reply `recheck` if you’ve signed before):

   ```text
   I have read the CLA Document and I hereby sign the CLA
   ```

3. The CLA‑Assistant bot records your signature in the repo and marks the status check as passed.

No special Git commands, email attachments, or commit footers required.

## License

This repository is licensed under the [Apache-2.0 License](LICENSE).
