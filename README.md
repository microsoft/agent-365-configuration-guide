# Microsoft Agent 365 — Security Configuration Guide

*A visual, step-by-step guide to configuring security and governance for agents built with Microsoft Agent 365 and Copilot Studio.*

*Copilot Studio(New experience)에서 만든 에이전트의 보안 및 거버넌스 구성을 스크린샷과 함께 안내하는 웹 가이드입니다.*

**🌐 View the guide / 가이드 보기: [https://microsoft.github.io/agent-365-configuration-guide/](https://microsoft.github.io/agent-365-configuration-guide/)**

---

## Overview / 개요

This guide walks through the end-to-end security lifecycle of an agent — from creation in
Copilot Studio to identity governance, risk detection, runtime protection, and traffic
monitoring — using **Microsoft Entra**, **Microsoft Purview**, and **Microsoft Defender**.

에이전트 생성부터 ID 거버넌스, 리스크 탐지, 런타임 보호, 트래픽 모니터링까지 보안
라이프사이클 전반을 Entra · Purview · Defender 기능을 중심으로 순서대로 정리했습니다.

| # | Chapter | 챕터 |
|---|---------|------|
| 0 | Create an agent | 에이전트 생성 |
| 1 | Approve and deploy organization-wide | 에이전트 승인 및 전사 배포 |
| 2 | Review the agent inventory | 에이전트 인벤토리 확인 |
| 3 | Block an agent | 에이전트 차단 |
| 4 | Basic access control for agents | 에이전트에 대한 기본 접근제어 |
| 5 | Detect agent risk | 에이전트 리스크 탐지 |
| 6 | Risk-based access control for agents | 에이전트 리스크 기반 접근제어 |
| 7 | Agent runtime protection | 에이전트 런타임 보호 |
| 8 | Monitor agent traffic | 에이전트 트래픽 모니터링 |

> [!NOTE]
> This guide is provided for reference and reflects the product experience at the time of
> authoring. Product UI and capabilities evolve — always confirm against the official
> documentation at [Microsoft Learn](https://learn.microsoft.com).
>
> 본 가이드는 참고용이며 작성 시점의 제품 화면을 기준으로 합니다. 제품 UI와 기능은
> 변경될 수 있으므로 항상 [Microsoft Learn](https://learn.microsoft.com) 공식 문서를 함께
> 확인하시기 바랍니다.

## Deployment / 배포

Pushing to the `main` branch triggers a GitHub Actions workflow
(`.github/workflows/deploy.yml`) that publishes `index.html` and `img/` to GitHub Pages.

`main` 브랜치에 push하면 GitHub Actions(`.github/workflows/deploy.yml`)가 `index.html`과
`img/`를 GitHub Pages로 배포합니다.

## Rebuilding the source / 소스 재생성

- `extract.py` — extract slide structure from the source PPTX into `deck.json`
- `crop.py` — crop the content area (excluding title/description) from slide PNGs
- `build2.py` — generate `index.html`

The source PPTX and `slides/` (original slide PNGs) are **not** included in this repository.

원본 PPTX와 `slides/`(원본 슬라이드 PNG)는 저장소에 포함되지 않습니다.

## Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit [https://cla.opensource.microsoft.com](https://cla.opensource.microsoft.com).

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the
instructions provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
