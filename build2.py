# -*- coding: utf-8 -*-
import json, os, html, re

BASE = os.path.dirname(os.path.abspath(__file__))
deck = json.load(open(os.path.join(BASE, "deck.json"), encoding="utf-8"))

def table_of(slide_no):
    for sh in deck[slide_no-1]["shapes"]:
        if sh["kind"] == "table":
            return sh["table"]
    return None

CH = [
 dict(id="ch0", num="0", orig="0", name="에이전트 생성", intro=3, range=(4,17),
      lead="Copilot Studio(New experience)에서 실습용 에이전트를 만들고, 지침·지식·도구를 구성한 뒤 Teams / Microsoft 365 Copilot 채널로 게시하고 관리자 승인까지 제출하는 단계입니다. 이후 1~8장의 모든 관리·보안 시나리오는 여기서 만든 에이전트를 대상으로 진행합니다."),
 dict(id="ch1", num="1", orig="1", name="에이전트 승인 및 전사 배포", intro=18, range=(19,25),
      lead="제작자가 제출한 에이전트를 AI 관리자가 검토·승인하고, 조직 카탈로그(Microsoft Store)에 게시해 전사에 배포하는 단계입니다. 승인 심사에서는 제작자·업무 목적·지식·도구·요청 권한을 함께 확인합니다."),
 dict(id="ch2", num="2", orig="2", name="에이전트 인벤토리 확인", intro=26, range=(27,30),
      lead="테넌트에 존재하는 에이전트를 레지스트리에서 조회하고, 각 에이전트의 소유자·지식·도구·권한·채널 구성과 실제 사용량을 확인하는 단계입니다. 등록되어 있다는 것과 실제로 쓰이고 있다는 것은 다르므로 두 가지를 분리해서 봅니다."),
 dict(id="ch3", num="3", orig="3", name="에이전트 차단", intro=31, range=(32,37),
      lead="문제가 있는 에이전트를 즉시 사용 불가 상태로 만들고, 사용자 화면에서 실제로 차단됐는지 확인한 뒤 복구하는 단계입니다. 차단은 삭제나 Agent ID 인증 중지와는 구분되는 조치입니다."),
 dict(id="ch4", num="4", orig="4", name="에이전트에 대한 기본 접근제어", intro=38, range=(39,47), custom=True,
      lead="사용자가 <b>사외(신뢰할 수 없는 네트워크)</b>에서 <b>Copilot Studio 에이전트</b>를 사용하지 못하도록 Entra 조건부 액세스 정책을 만들고, 실제 차단과 로그인 로그의 평가 결과를 확인하는 단계입니다. 접근 제어 대상이 클라우드 리소스가 아니라 에이전트 자체가 됩니다."),
 dict(id="ch5", num="5", orig="5", name="에이전트 리스크 탐지", intro=48, range=(49,64),
      lead="Purview 내부 위험 관리(IRM)에서 에이전트 정책을 만들어 위험 신호를 수집하고, 에이전트 경고를 확인하는 단계입니다. 감사 로그 수집이 켜져 있어야 지표·경고가 생성됩니다."),
 dict(id="ch6", num="6", orig="4", name="에이전트 리스크 기반 접근제어", intro=38, range=(39,47),
      lead="에이전트가 접근하는 클라우드 앱·커넥터 리소스를 대상으로 조건부 액세스 정책을 적용하고, 위치·네트워크 등 리스크 신호에 따라 허용/차단을 제어한 뒤 로그인 로그로 평가 결과를 검증하는 단계입니다. 앞의 기본 접근제어가 에이전트 자체를 대상으로 했다면, 여기서는 에이전트가 호출하는 리소스(클라우드 앱)를 대상으로 접근을 통제합니다."),
 dict(id="ch7", num="7", orig="6", name="에이전트 런타임 보호", intro=65, range=(66,80),
      lead="Defender AI 보안과 Power Platform 위협 탐지를 연결해, Copilot Studio 에이전트의 도구 호출·프롬프트를 실시간으로 검사하고 차단하는 단계입니다. 커넥터 설정 → 인증용 앱 생성 → 환경 연결 → 보호 정책 순으로 진행합니다."),
 dict(id="ch8", num="8", orig="7", name="에이전트 트래픽 모니터링", intro=81, range=(82,86),
      lead="Global Secure Access for Agents(preview)를 환경 단위로 켜고, Entra의 Gen AI 인사이트 로그에서 에이전트가 주고받은 실제 트래픽(요청·응답)을 조회하는 단계입니다."),
 dict(id="ch9", num="9", orig="8", name="에이전트 실행 텔레메트리", intro=None, range=None, custom=True, hidden=True,
      lead="Defender·Entra의 보안·트래픽 이벤트와 별개로, <b>에이전트 내부 실행</b>(노드 실행·도구 호출 인자/결과·LLM span)을 <b>Application Insights</b>로 수집하는 관측(observability) 단계입니다. Power Platform 관리 센터의 환경 단위 데이터 내보내기로 Copilot Studio 텔레메트리를 App Insights에 연결하고, Foundry 기반 에이전트는 Tracing으로 연결합니다."),
]

# 보류(업데이트 대기) 챕터는 빌드에서 제외해 사이드바·본문·네비게이션에서 숨긴다.
HIDDEN_IDS = {c["id"] for c in CH if c.get("hidden")}
CH = [c for c in CH if not c.get("hidden")]

DESC = {
 4:"New Copilot Studio 우측 상단의 환경 선택기에서 실습에 사용할 Power Platform 환경을 먼저 고정합니다. <b>Power Platform 환경</b>은 앱·에이전트·데이터(Dataverse)를 담는 격리된 컨테이너로, 환경마다 접근 권한·보안·DLP 정책이 따로 적용됩니다. 여기서 선택한 환경이 7장(런타임 보호)·8장(트래픽 모니터링)의 <b>환경 단위 설정 대상</b>과 동일해야 하므로, 처음부터 실습 환경을 정해두는 것이 중요합니다. 해당 환경에 대한 제작자(Maker) 이상의 역할이 필요합니다.<br><br><b>⚠️ Notice —</b> 본 Agent 365 관련 데모는 기본 환경(Default Environment)에서도 따라 하실 수는 있으나, <b>실 운영 환경에서는 반드시 테스트를 위한 별도의 환경을 구성하시어 진행</b>하셔야 합니다. 환경 개념·생성 방법은 <a class='xref-ext' href='https://learn.microsoft.com/ko-kr/power-platform/admin/environments-overview' target='_blank' rel='noopener'>Power Platform 환경 개요(공식 문서)</a>를 참고하세요.",
 5:"Agents 화면에서 <b>New agent</b>를 선택해 템플릿이 아닌 빈 에이전트로 시작합니다. 빈 에이전트로 시작해야 지침·지식·도구를 하나씩 통제하면서 붙일 수 있고, 이후 승인 심사에서 무엇이 왜 붙었는지 설명하기 쉽습니다. 이 가이드에서는 <code>Agent365-Guide-Demo</code>라는 이름을 사용합니다.",
 6:"① 에이전트 이름, ② 지침(Instructions), ③ 모델·행동 설정 순으로 입력합니다. New experience에서는 모델과 오케스트레이션 설정 위치가 기존 UI와 달라 <code>Settings &gt; AI &amp; behavior</code>에서 확인해야 하며, 기존의 '생성형 AI' 토글과는 구분됩니다. 지침은 1장의 관리자 승인 심사에서 <b>업무 목적을 판단하는 근거</b>가 되므로 구체적으로 작성합니다.",
 7:"<code>Build &gt; Add knowledge</code>에서 SharePoint·OneDrive·Dataverse 등 지식 원본을 연결합니다. 여기서 붙인 지식은 1장의 관리자 승인 화면과 2장의 인벤토리 <b>데이터 &amp; 도구</b> 탭에 그대로 노출되므로, 민감한 사이트를 연결할 때는 사전 검토가 필요합니다.",
 8:"<code>Build &gt; Add tool &gt; Model Context Protocol (MCP)</code> 카탈로그에서 필요한 도구를 연결합니다. MCP 도구는 런타임에 실제로 호출되는 지점이므로, 5장(리스크 탐지)·7장(런타임 보호)·8장(트래픽 모니터링)에서 <b>탐지·보호·로깅의 실제 대상</b>이 됩니다.",
 9:"Preview(테스트) 패널에서 한국어 프롬프트로 실행해 지식 인용과 도구 호출이 정상인지 확인합니다. 단, 테스트 패널에서 발생한 활동은 2장에서 보는 <b>활성 사용자·세션 통계에는 집계되지 않습니다</b>. 실제 사용량 확인은 게시된 채널에서 실행한 결과로 판단해야 합니다.",
 10:"구성이 끝나면 게시 다이얼로그에서 채널 추가를 시작합니다. 게시는 '에이전트를 저장하는 것'이 아니라 <b>사용자에게 노출될 경로를 여는 것</b>이라는 점을 구분합니다.",
 11:"채널 선택기에서 <b>Teams 및 Microsoft 365 Copilot</b>을 선택합니다. 이 채널이 연결되어 있어야 이후 1장의 조직 카탈로그 배포, 3장의 차단 결과를 사용자 화면에서 확인할 수 있습니다.",
 12:"① 사용할 채널을 확인하고 ② 표시(가용성) 범위를 선택합니다. 이 단계에서 선택한 범위가 관리자 승인 요청 여부를 결정합니다.",
 13:"Teams + Microsoft 365 채널 게시가 완료된 상태입니다. <b>게시 완료가 곧 조직 카탈로그 승인·전사 배포 완료를 뜻하지는 않습니다</b>. 조직 전체 노출은 다음 단계의 관리자 승인을 거쳐야 합니다.",
 14:"① 채널의 가용성 옵션을 열고 ② <b>내 조직의 모든 사람에게 표시</b>를 선택합니다. 이 선택이 AI 관리자에게 전달되는 승인 요청을 생성합니다.",
 15:"제출 전 검토 화면에서 제작자, 설명, 연결된 지식·도구, 요청 권한 요약을 확인합니다. 여기 표시되는 내용이 관리자 검토 화면에 그대로 전달되므로, 설명이 비어 있으면 승인이 지연될 수 있습니다.",
 16:"조직 공개 여부를 묻는 확인 대화상자에서 <b>예</b>를 선택하면 승인 요청이 제출됩니다.",
 17:"제출 후에는 <b>승인 대기</b> 상태로 표시됩니다. 새로 고침으로 요청 상태를 확인하며, 이 시점부터는 제작자가 아니라 AI 관리자의 작업(1장)으로 넘어갑니다.",

 19:"AI 관리자 계정으로 <code>Microsoft 365 관리 센터 &gt; 에이전트 &gt; 모든 에이전트 &gt; 요청</code>으로 이동해 ① 요청 목록에서 ② 대상 요청을 엽니다. 이 메뉴가 보이지 않으면 Entra에서 <b>AI 관리자</b> 역할이 할당되었는지 먼저 확인합니다.",
 20:"요청 상세에서 ① <b>Microsoft Store에 게시</b> 버튼을 선택해 게시 마법사를 시작합니다. 이 화면에서 제작자·업무 목적·지식·도구·요청 권한을 검토하고, 부적절하면 제출을 거부할 수 있습니다.<br><br><b>보안·AX 담당자 전사 게시 전 체크리스트</b> (상세 화면의 각 탭에서 확인)<br>• <b>세부 정보</b> — 제작자·소유자·업무 목적·게시 채널을 확인하고, <b>제작자·소유자가 식별·검증 가능한가</b><br>• <b>데이터 &amp; 도구</b> — 연결된 지식 원본과 MCP 도구 목록을 확인하고, <b>목적·지침 대비 적정한 MCP 도구만 연결되어 있는가</b>(불필요한 광범위 도구 없음), <b>지식 원본이 민감 사이트·과도한 범위를 포함하지 않는가</b><br>• <b>사용 권한</b> — 에이전트가 요청하는 API/커넥터 권한이 <b>업무 목적에 비해 과도하지 않은가</b>(최소 권한)<br>부적절한 경우 승인을 보류하고 제작자에게 수정 요청 후 재제출받습니다.",
 21:"① 설치 가능 대상과 ② 사전 설치 대상을 지정한 뒤 ③ 다음으로 진행합니다. <b>설치 가능</b>은 사용자가 원할 때 직접 추가하는 방식이고, <b>사전 설치</b>는 대상 사용자에게 자동으로 배포되는 방식이므로 영향 범위가 다릅니다.",
 22:"배포 시 적용될 앱 정책 템플릿을 확인합니다. 조직에 이미 적용 중인 앱 설정 정책이 있는 경우 여기서 함께 확인됩니다.",
 23:"권한 검토 화면입니다. 이 사례에서는 <b>필요한 권한 없음</b>으로 표시됐지만, 이는 에이전트의 모든 MCP 도구가 무권한으로 실행된다는 뜻이 <b>아닙니다</b>. 도구별 인증·동의는 별도로 적용되며, 실제 데이터 접근은 도구 수준에서 다시 통제됩니다.<br><br><b>Note —</b> <b>Copilot Studio 에이전트</b>는 <b>생성 시점에 API 권한(위임/애플리케이션 권한)을 직접 부여하지 않으며</b>, 실제 권한은 각 도구·커넥터를 사용할 때 <b>런타임에 사용자 동의·연결 단위로 부여</b>됩니다. 따라서 이 화면에 요청 권한이 비어 있는 것은 정상입니다. 반면 <b>Copilot Studio 이외의 플랫폼·방법으로 생성된 에이전트</b>는 요청 권한이 함께 넘어올 수 있으므로, 그런 경우 이 <b>권한 검토 화면에서 요청 권한의 적정성을 확인</b>하면 됩니다.",
 24:"최종 검토 화면에서 대상·권한·정책을 한 번 더 확인한 뒤 게시합니다.",
 25:"관리자 처리가 완료된 상태입니다. 배포 직후에는 Teams / Microsoft 365 Copilot 사용자 화면에 반영되기까지 시간이 걸릴 수 있으므로, 사용자 실행 확인은 잠시 후 다시 시도합니다.",

 27:"① <code>에이전트 &gt; 모든 에이전트 &gt; 레지스트리</code>로 이동해 ② <b>Platform = Copilot Studio</b>로 필터링합니다. 레지스트리는 테넌트에 등록된 에이전트의 단일 목록이며, <b>등록되어 있다는 사실이 실제로 사용 중이라는 뜻은 아닙니다</b>.",
 28:"에이전트 상세의 <b>세부 정보</b>에서 소유자, 게시 채널, 상태, 그리고 해당 에이전트의 <b>Entra Agent ID</b>를 확인합니다. 이 Agent ID는 4장에서 조건부 액세스 대상으로 지정하고 로그인 로그와 대조할 때 사용하는 핵심 식별자입니다. 지식·도구(Data &amp; tools) 구성은 여기서 조회만 하고, 변경은 Copilot Studio에서 수행합니다.",
 29:"① 조회 기간을 지정하고 ② 활성 사용자·세션 지표를 확인합니다. 관리 센터의 활성 지표는 <b>게시된 채널에서 발생한 실사용</b>을 기준으로 집계됩니다.",
 30:"Copilot Studio의 <b>모니터</b>에서 세션·사용자 추이를 확인합니다. ① 조회 기간, ② 활성 사용자 보기를 확인하되 <b>기본 시간대가 UTC</b>인 점과 <b>테스트 패널 활동이 제외</b>되는 점을 감안해 해석합니다.",

 32:"차단 전 에이전트 상세 화면입니다. 차단 이전 상태(채널, 설치 대상, 상태 값)를 먼저 기록해 두면 이후 복구가 정상적으로 됐는지 비교할 수 있습니다.",
 33:"① <b>에이전트 차단</b>을 선택하고 ② 저장합니다. 차단은 에이전트를 삭제하거나 Agent ID의 인증 자체를 중지하는 것과는 다른 조치로, 구성은 유지한 채 <b>사용만 즉시 막는</b> 방식입니다.",
 34:"저장 후 관리 센터에서 상태가 차단으로 바뀐 것을 확인합니다.",
 35:"관리자 화면뿐 아니라 <b>일반 사용자 화면(Teams / Microsoft 365 Copilot)</b>에서 실제로 실행이 막히는지 확인합니다. 기존 진입점, 신규 설치, 새 대화 각각에 대해 확인하고 채널별 결과를 기록해 두는 것이 좋습니다.",
 36:"복구를 위해 다시 에이전트 상세로 이동합니다.",
 37:"① <b>에이전트 차단 해제</b>를 선택하고 ② 저장합니다. 해제 후에는 설치·가용성 범위가 차단 전과 동일한지, 사용자 실행이 정상으로 돌아왔는지 함께 재확인합니다.",

 39:"<code>Entra 관리 센터 &gt; 보호 &gt; 조건부 액세스 &gt; 정책</code>에서 ① 새 정책을 만들고 ② 이름을 지정합니다. 이 작업에는 <b>조건부 액세스 관리자</b> 역할이 필요합니다.",
 40:"할당 단계에서 정책 적용 대상을 지정합니다(①~④). 에이전트는 사람 사용자와 달리 <b>Agent ID</b>로 지정하며, 사용자 대상 정책과 섞이지 않도록 대상 범위를 명확히 분리합니다.",
 41:"① 대상 리소스에서 ② 에이전트가 실제로 호출하는 커넥터·리소스를 지정합니다. 에이전트만 지정하고 실제 접근 리소스를 빠뜨리면 <b>커넥터 호출이 정책 평가에서 누락</b>될 수 있습니다.",
 42:"조건(네트워크·디바이스·위치 등)을 구성합니다(①~⑤). 에이전트는 사용자 디바이스가 없는 워크로드 형태로 동작하므로, 디바이스 기반 조건을 그대로 적용하면 의도치 않은 차단이 발생할 수 있습니다.",
 43:"액세스 제어에서 허용/차단과 요구 제어를 지정합니다(①~③).",
 44:"① 정책 사용 상태를 지정하고 ② 생성합니다. 운영 적용 전에는 <b>보고서 전용(Report-only)</b>으로 먼저 영향도를 확인하는 것을 권장하며, 보고서 전용은 <b>실제로 차단하지 않습니다</b>.",
 45:"정책 평가를 검증하기 위해 ① 대상 에이전트를 확인하고 ② Teams에서 에이전트와 커넥터를 실제로 실행해 트래픽을 발생시킵니다.",
 46:"<code>Entra &gt; 모니터링 및 상태 &gt; 로그인 로그</code>에서 ①~③ 순으로 조회합니다. 사용자 로그인이 아닌 <b>서비스 주체 / 에이전트 로그인</b> 영역을 확인해야 에이전트 트래픽이 보입니다.",
 47:"로그인 상세에서 ① Agent ID·리소스·시각과 ② 조건부 액세스 평가 결과를 대조합니다. 정책이 실제로 적용됐는지는 이 <b>조건부 액세스 탭의 결과 값</b>으로 판단합니다.",

 49:"<code>Purview &gt; 감사 &gt; 감사 수집 상태</code>에서 감사 로그 수집이 켜져 있는지 먼저 확인합니다. <b>감사 로그가 꺼져 있으면 IRM 정책을 만들어도 분석할 활동 이벤트 자체가 없어 지표·경고가 생성되지 않습니다.</b>",
 50:"<code>내부 위험 관리 &gt; 정책</code>에서 ①~④ 순으로 에이전트 정책 생성을 시작합니다. 이 작업에는 <b>내부자 위험 관리 분석가</b> 또는 <b>조사자</b> 역할이 필요합니다.",
 51:"정책 템플릿을 선택합니다. 에이전트 전용 템플릿을 선택하면 에이전트 활동 지표가 기본 세트로 구성됩니다.",
 52:"① 정책 이름, ② 설명, ③ 다음 순으로 입력합니다. 이름에 적용 범위를 드러내면 이후 경고 분류에 도움이 됩니다.",
 53:"정책을 적용할 에이전트 범위를 지정합니다. 현재 UI에서는 ① <b>모든 에이전트</b>가 선택되어 있고 ② 특정 에이전트 선택은 비활성화되어 있습니다. 따라서 정책 이름에 Demo가 들어 있어도 <b>단일 에이전트 범위가 아니라 테넌트 전체 범위</b>로 적용된다는 점에 유의합니다.",
 54:"우선순위로 다룰 콘텐츠(민감도 레이블·사이트·파일 유형 등)를 선택합니다(①②).<br><br><b>Note —</b> <b>우선순위 콘텐츠 지정 여부는 위험 점수 산정에 직접 영향</b>을 줍니다. 우선순위로 지정한 콘텐츠(예: 민감도 레이블이 높은 문서, 특정 SharePoint 사이트)에 에이전트가 접근·조작하면 <b>더 높은 위험 가중치</b>가 부여되어 경고 심각도가 올라가고 더 쉽게 트리거됩니다. 지정하지 않으면 모든 콘텐츠가 동일 가중치로 평가되어 <b>중요 자산에 대한 위험 활동이 상대적으로 묻힐 수</b> 있습니다. 따라서 조직의 핵심 자산을 우선순위로 지정해 탐지 민감도를 집중시키는 것이 좋습니다.",
 55:"앞서 선택한 콘텐츠 각각에 대해 세부 항목을 추가로 지정합니다(①~④). 우선순위 콘텐츠는 위험 점수 가중치에 직접 영향을 줍니다.",
 56:"알림(경고)을 생성할 범위를 지정합니다(①②).",
 57:"경고를 유발할 이벤트 트리거를 선택합니다(①②). 에이전트의 어떤 행위를 위험 신호의 시작점으로 볼 것인지 정하는 단계입니다.",
 58:"트리거 임계값을 지정합니다(①~③). <b>초기에는 경고가 실제로 생성되는지 확인하기 위해 임계값을 최대한 낮게 잡고</b>, 오탐 추이를 보면서 사내 환경에 맞게 점차 올리는 방식을 권장합니다.",
 59:"표시기(Indicator) 단계에서 선택한 총 표시기 수(4/4)와 에이전트 지표 분류를 확인합니다. 화면에 선택되어 있다고 해서 <b>해당 이벤트가 실제로 수집·탐지되고 있다는 보장은 아니며</b>, 실제 동작 여부는 경고와 활동 증거로 별도 확인해야 합니다.",
 60:"탐지 옵션의 <b>위험 점수 부스터</b>에는 에이전트 활동이 그날 평균 활동을 상회하는 경우 등의 조건이 표시됩니다. 앞서 설정한 <b>트리거 임계값·지표 임계값과는 별개</b>이므로 구분해서 검토합니다.",
 61:"최종 검토 후 정책을 생성합니다.",
 62:"정책 생성이 완료된 상태입니다. <b>정책 생성 후 실제 경고가 표시되기까지 최대 24시간이 걸릴 수 있습니다.</b>",
 63:"<code>내부 위험 관리 &gt; 에이전트 &gt; 경고</code>에서 ① 시간·상태·심각도 필터, ② 항목 수, ③ 결과를 확인합니다. 이 실습 시점에서는 <b>사용 가능한 경고가 0건</b>이었고 경보 상세·활동 탐색기·증거는 열 수 없었습니다. 이 경우 임계값과 감사 수집 상태, 에이전트 실사용량을 먼저 점검하는 것이 순서입니다.",
 64:"경고가 생성된 경우의 확인 경로입니다(①~③). <b>심각도</b>를 기준으로 에이전트 활동과 관련해 <b>어떤 리스크가 탐지되었는지</b>를 확인합니다.",

 66:"<code>Defender &gt; 설정 &gt; AI 보안 &gt; 시작</code>에서 ①~③ 순으로 이동한 뒤 <b>Microsoft 365 커넥터</b>를 구성합니다. 이 커넥터가 Agent 365·Microsoft 365 활동과 Entra 관리 이벤트를 수집하는 입구 역할을 합니다. <b>애플리케이션 관리자 / 보안 관리자</b> 역할이 필요합니다.",
 67:"수집할 구성 요소를 선택합니다(①②). Agent 365와 Microsoft 365가 모두 연결 대상인지 확인합니다.",
 68:"커넥터 연결이 완료된 상태입니다.",
 69:"<b>Copilot Studio 실시간 보호</b> 항목으로 이동해 ①② 순으로 통합을 엽니다. 이 화면에 표시되는 <b>Power Platform 통합용 엔드포인트 URL은 반드시 복사해 둡니다</b>. <a class=\"xref\" data-target=\"s72\">4단계(PowerPlatform 보안 설정)</a>에서 그대로 입력해야 합니다.",
 70:"관리자 권한으로 Windows PowerShell을 열고, 스크립트가 있는 디렉터리에서 <code>Create-CopilotWebhookApp.ps1</code>을 실행합니다. ① <b>TenantId</b>는 Entra 개요의 테넌트 ID, ② <b>Endpoint</b>는 <a class=\"xref\" data-target=\"s69\">2단계(Copilot Studio 연결)</a>에서 복사한 URL을 넣고, <code>DisplayName</code>과 <code>FICName</code>은 조직 고유 값으로 지정합니다. 이 스크립트는 Defender가 Power Platform을 호출할 때 사용할 앱 등록과 <b>페더레이션 자격 증명(FIC)</b>을 함께 만듭니다.",
 71:"스크립트 실행 결과로 생성된 앱 등록을 Entra에서 확인합니다(①~③). 여기 표시된 <b>앱(클라이언트) ID도 복사해 둡니다</b> — <a class=\"xref\" data-target=\"s72\">4단계(PowerPlatform 보안 설정)</a>의 연결 설정에 입력합니다.",
 72:"<code>Power Platform 관리 센터 &gt; 보안 &gt; 위협 탐지 &gt; 추가 위협 탐지</code>로 이동합니다(①~③). <b>Power Platform 관리자</b> 역할이 필요합니다.",
 73:"① 실습 환경(Agent-Demo)을 선택하고 ② 설정을 엽니다. <b>보호 연결은 환경 단위</b>이므로 다른 환경이나 기본 환경을 선택하지 않도록 주의합니다.",
 74:"연결 설정에서 ①~⑤ 순으로 값을 입력합니다. <b>앱 ID는 <a class=\"xref\" data-target=\"s70\">3단계(인증용 앱 구성)</a>에서 생성한 값</b>, <b>엔드포인트는 <a class=\"xref\" data-target=\"s69\">2단계(Copilot Studio 연결)</a>에서 복사한 URL</b>을 사용합니다. 검사 실패(오류) 시 동작을 <b>Allow</b>로 둘지 <b>Block</b>으로 둘지 선택한 뒤 저장합니다. Block은 보호 수준이 높지만 탐지 서비스 장애 시 에이전트 실행이 함께 막힐 수 있습니다.",
 75:"6-1 ~ 6-4 설정이 모두 연결된 상태입니다. 여기까지가 <b>탐지 파이프라인 구성</b>이고, 실제 차단 동작은 다음 단계의 보호 정책에서 결정됩니다.",
 76:"<code>Defender &gt; 설정 &gt; AI 보안 &gt; 정책 및 규칙</code>에서 ①② 순으로 커스텀 실시간 보호 정책을 만듭니다. <b>기본(Default) 정책은 Audit</b>이므로 차단이 필요하면 별도 커스텀 정책을 만들어야 합니다.",
 77:"정책 이름과 적용 범위를 지정합니다(①②).",
 78:"탐지 대상과 조치(Block/Audit)를 지정합니다(①~③).",
 79:"정책 검토 후 생성합니다. 실시간 보호의 감사·차단 이벤트는 <b>동작(behavior)</b>으로 <code>BehaviorInfo</code> 테이블에 기록되며, <b>Prompt Shields for Foundry</b>와 <b>Copilot Agent Builder</b>의 차단 이벤트도 동작으로 기록됩니다. 다만 <b>Copilot Studio로 빌드된 에이전트의 차단 이벤트는 아직 지원되지 않습니다</b>(<a class='xref-ext' href='https://learn.microsoft.com/ko-kr/defender-xdr/security-for-ai/ai-agent-real-time-protection#how-real-time-protection-works' target='_blank' rel='noopener'>공식 문서 · 실시간 보호 작동 방식</a>).",
 80:"<b>프롬프트 증거 수집</b> 설정입니다. 켜면 경고 조사 시 실제 프롬프트 내용을 근거로 볼 수 있지만, 프롬프트 본문이 저장되므로 민감정보 취급 정책과 함께 검토해야 합니다.",

 82:"<code>Power Platform 관리 센터 &gt; 보안 &gt; ID 및 액세스 &gt; 에이전트에 대한 전역 보안 액세스</code>로 이동합니다(①~③). <b>전역 보안 액세스 관리자</b> 역할이 필요합니다.",
 83:"① 실습 환경을 선택하고 ② 설정을 엽니다. GSA 적용도 <b>환경 단위</b>이므로 같은 환경의 다른 에이전트에도 함께 영향이 갑니다.",
 84:"① <b>Enable</b>을 On으로 바꾸고 ② 저장합니다. 이 시점부터 해당 환경 에이전트의 아웃바운드 트래픽이 Global Secure Access를 경유합니다.",
 85:"<code>Entra &gt; 전역 보안 액세스 &gt; 모니터링</code>에서 활성화 상태를 확인합니다(①②).",
 86:"<b>Gen AI 인사이트 로그</b>에서 에이전트가 실제로 주고받은 트래픽을 조회합니다. <b>Event ID·Transaction ID로 상관 분석</b>하면 하나의 실행에 대한 요청·응답을 이어서 볼 수 있으며, MCP <code>tools/call</code>의 요청 본문과 응답까지 확인할 수 있습니다. 로그 반영에는 지연이 있을 수 있습니다.",
}

# Real, copyable code blocks that replace a code screenshot on a slide.
CODE = {
 70: ('PowerShell',
r'''.\Create-CopilotWebhookApp.ps1 `
  -TenantId "11111111-2222-3333-4444-555555555555" `
  -Endpoint "https://provider.example.com/threat_detection/copilot" `
  -DisplayName "Copilot Security Integration - Production" `
  -FICName "ProductionFIC"'''),
}

# Override the displayed figure title for specific slides (unify section name before dash).
TITLE_OVERRIDE = {
 60: "에이전트 정책 생성 — 위험 점수 부스터",
}

# Extra example figures appended after a slide's note (raw HTML).
EXTRA = {
 20: """
      <figure class="fig">
        <div class="fig-title"><span class="fig-num" style="background:var(--surface-2);color:var(--text-soft);">예시</span>데이터 &amp; 도구 탭 — 지식·도구 확인 화면</div>
        <a href="img/admin-tab-datatools.png" target="_blank" rel="noopener"><img loading="lazy" src="img/admin-tab-datatools.png" alt="관리자 승인 상세 - 데이터 및 도구 탭 예시"></a>
        <figcaption class="fig-cap">각 탭을 열면 이렇게 항목별 상세가 표시됩니다. 예: <b>데이터 &amp; 도구</b> 탭에서는 <b>기능</b>(읽을 수 있음·그래프 커넥터), <b>지식</b>(참조 자료), <b>도구</b>(연결된 MCP 서버 목록·설명)를 확인해 목적 대비 적정성을 검토합니다.</figcaption>
      </figure>""",
 64: """
      <figure class="fig" id="s64-2">
        <div class="fig-title"><span class="fig-num">3-2</span>에이전트 경고 확인 — 경고 상세 (지표·심각도·관련 엔터티)</div>
        <a href="img/irm-3-2.png" target="_blank" rel="noopener"><img loading="lazy" src="img/irm-3-2.png" alt="경고 상세 - 지표·심각도·관련 엔터티"></a>
      </figure>
      <div class="note">① 경고를 열어 <b>심각도·위험 점수</b>를 확인하고, ② 우측 <b>경고 세부 정보</b> 패널에서 해당 경고와 연관된 <b>이벤트와 에이전트</b>를 파악합니다.</div>
      <figure class="fig" id="s64-3">
        <div class="fig-title"><span class="fig-num">3-3</span>에이전트 경고 확인 — 활동 탐색기 (활동·프롬프트·응답 세부)</div>
        <a href="img/irm-3-3.png" target="_blank" rel="noopener"><img loading="lazy" src="img/irm-3-3.png" alt="활동 탐색기 - 활동·프롬프트·응답 세부"></a>
      </figure>
      <div class="note">① <b>활동 탐색기</b>에서 개별 활동을 선택하면 우측 상세 패널에 <b>활동 세부 정보</b>(작업·워크로드·AI 애플리케이션)와 함께, ② <b>프롬프트 세부 정보</b>(실제 입력 프롬프트·프롬프트 ID), ③ <b>응답 세부 사항</b>(응답 ID·중요한 정보 유형)이 표시됩니다. 이를 통해 <b>어떤 프롬프트가 어떤 응답·리소스로 이어졌는지</b>를 활동 종류별로 추적할 수 있습니다. <span class="hl-note">프롬프트·응답 원문은 <b>내부 위험 관리 조사자</b> 역할을 가진 사용자만 볼 수 있습니다.</span></div>
      <figure class="fig" id="s64-4">
        <div class="fig-title"><span class="fig-num">3-4</span>에이전트 경고 확인 — 에이전트 활동·증거 (관련 자산 식별)</div>
        <a href="img/irm-3-4.png" target="_blank" rel="noopener"><img loading="lazy" src="img/irm-3-4.png" alt="에이전트 활동 - 증거·관련 자산"></a>
      </figure>
      <div class="note">① <b>에이전트 활동</b> 탭에서 ② 각 이벤트의 <b>증거</b>(예: 응답에 포함된 민감 정보 유형 — All Full Names·Diseases·Medical Terms 등)를 확인해 실제 어떤 자산·콘텐츠가 관련됐는지 식별합니다.</div>""",
 80: """
      <figure class="fig" id="s80-2">
        <div class="fig-title"><span class="fig-num">6-1</span>런타임 탐지 시나리오 — 탐지 경고 목록 (Defender 경고)</div>
        <a href="img/rt-alerts.png" target="_blank" rel="noopener"><img loading="lazy" src="img/rt-alerts.png" alt="Defender 경고 목록 - AI 탐지"></a>
      </figure>
      <div class="note"><code>Defender 포털 &gt; 사건 &amp; 경고 &gt; 경고</code>에서 준실시간 탐지 결과를 확인합니다. 조회 기간과 경고 건수를 확인하고, 목록에서 <b>AI agent abuse</b>·<b>프롬프트 인젝션(XPIA)</b> 등 AI 관련 경고를 찾습니다. Defender는 Agent 365 관측 데이터를 분석해 <b>탈옥(jailbreak)·간접 프롬프트 인젝션·악성 콘텐츠 전파·비밀 유출·회피 기법·LLM 정찰·의심 IP 접근</b> 등을 탐지합니다.</div>
      <figure class="fig" id="s80-3">
        <div class="fig-title"><span class="fig-num">6-2</span>런타임 탐지 시나리오 — 경고 세부사항 (활동 세부 정보 필드)</div>
        <a href="img/rt-detail.png" target="_blank" rel="noopener"><img loading="lazy" src="img/rt-detail.png" alt="경고 세부사항 - 에이전트·활동·증거"></a>
      </figure>
      <div class="note">경고를 클릭한 뒤 <b>활동 세부 정보</b> 탭을 열면(위 화면), 해당 탐지의 원천 데이터를 필드 단위로 확인할 수 있습니다. 대표 필드는 다음과 같습니다.<br><br>• <b>에이전트 식별</b> — <code>AgentName</code>·<code>AgentID</code>·<code>PlatformAgentType</code>(예: AzureAIFoundry)·<code>AgentBlueprintID</code>·<code>ChannelName</code>(예: msteams:COPILOT): <b>어떤 에이전트가 어떤 플랫폼·채널에서</b> 동작했는지<br>• <b>세션·요청</b> — <code>ConversationId</code>·<code>RequestId</code>·<code>ResponseId</code>·<code>RequestMessages</code>: 실제 <b>요청/응답과 대화 맥락</b><br>• <b>도구 호출</b> — <code>ToolName</code>(예: mcp_WorkIQWord.GetDocumentContent)·<code>ToolType</code>·<code>ToolID</code>·<code>ToolOutput</code>: 에이전트가 호출한 <b>도구와 그 출력</b>(주입 콘텐츠 포함)<br>• <b>위협 분류</b> — <code>MitreAtlasTactics/Techniques</code>·<code>OWASPCategory</code>·<code>PotentialCauses</code>: <b>어떤 공격 기법·원인</b>으로 분류됐는지<br><br>즉 이 탭 하나에서 <b>어떤 에이전트가, 어떤 채널에서, 어떤 도구를 호출해, 어떤 위협으로 탐지됐는지</b>를 한 번에 파악할 수 있습니다. 우측 <b>세부 정보</b> 패널에서는 심각도·상태·경고 ID·범주 등 경고 메타데이터를 확인합니다.</div>
      <figure class="fig" id="s80-4">
        <div class="fig-title"><span class="fig-num">6-3</span>런타임 탐지 시나리오 — AgentsInfo 조인 (에이전트 컨텍스트 보강)</div>
        <a href="img/rt-agentsinfo.png" target="_blank" rel="noopener"><img loading="lazy" src="img/rt-agentsinfo.png" alt="고급 헌팅 — AlertEvidence를 AgentsInfo와 EntraAgentID로 조인해 탐지에 에이전트 컨텍스트를 보강"></a>
        <figcaption class="fig-cap">위 화면은 <b>XPIA(간접 프롬프트 인젝션) 경고</b>를 <code>EntraAgentID</code>로 조인해, 탐지된 에이전트(<code>foundry-ops</code>)의 <b>소유자·상태(Active)·도구(web_search)</b>를 함께 확인한 결과입니다.</figcaption>
      </figure>
      <div class="note">고급 헌팅에서 탐지 데이터에 <b>에이전트 인벤토리·구성 컨텍스트</b>를 붙이려면 <code>AgentsInfo</code> 테이블을 조인합니다. <code>AgentsInfo</code>는 <b>Microsoft Agent 365의 에이전트 목록·구성·소유자</b> 정보를 담는 테이블로, 탐지 증거 테이블 <code>AlertEvidence</code>에서 <code>EntityType == "AIAgent"</code> 행의 <code>AdditionalFields.AgentId</code>(Entra 에이전트 ID)를 꺼내 <code>AgentsInfo.EntraAgentID</code>와 조인합니다.<br><br><b>주요 컬럼과 조회 가능 정보</b><br>• <code>Name</code> — 에이전트 표시 이름<br>• <code>Owners</code> — 소유자(Entra 개체 ID)<br>• <code>LifecycleStatus</code> — 운영 상태(<code>Active</code>·<code>Blocked</code>·<code>Uninstalled</code>·<code>Deleted</code>)<br>• <code>DeclaredTools</code>·<code>McpServers</code> — 선언된 도구·연결된 MCP 서버<br>• <code>Permissions</code>·<code>PublishedStatus</code> — 요청·부여 권한과 게시 상태<br>이를 통해 <b>어떤 에이전트가·누구 소유이고·무슨 도구를 쓰며·현재 상태(Active/Blocked)가 무엇인지</b>를 경고 한 건에 활동 단위로 보강할 수 있습니다. <span class="hl-note">참고: 이 테이블은 기존 <code>AIAgentsInfo</code>를 대체하며(<code>AIAgentsInfo</code>는 2026-07-01 폐기 예정), Agent 365 환경에서는 <code>AgentsInfo</code>를 사용합니다.</span></div>
      <div class="code"><div class="code-head"><span>KQL — 탐지(경고)에 에이전트 컨텍스트 보강 (EntraAgentID 조인)</span><button class="copy-btn" type="button">복사</button></div><pre><code>AlertEvidence
| where Timestamp &gt; ago(30d)
| where ServiceSource == "Security for AI"
| where EntityType == "AIAgent"
| extend EntraAgentID = tostring(todynamic(AdditionalFields).AgentId)
| join kind=inner (AlertInfo | project AlertId, Title, Severity) on AlertId
| join kind=inner (
    AgentsInfo
    | summarize arg_max(Timestamp, *) by AgentId
    | mv-apply t = DeclaredTools on (summarize Tools = make_set(t.type))
    | project EntraAgentID, AgentName = Name, Owners, LifecycleStatus, Tools
  ) on EntraAgentID
| project AgentName, Owners, LifecycleStatus, Tools, Detection = Title, Severity, EntraAgentID
| order by AgentName asc</code></pre></div>
      <div class="code"><div class="code-head"><span>KQL — 에이전트 인벤토리·구성 단독 조회 (소유자·도구·MCP·상태)</span><button class="copy-btn" type="button">복사</button></div><pre><code>AgentsInfo
| summarize arg_max(Timestamp, *) by AgentId
| project Name, Platform, EntraAgentID, LifecycleStatus, PublishedStatus,
          Owners, DeclaredTools, McpServers, Permissions
| order by Name asc</code></pre></div>
      <figure class="fig" id="s80-5">
        <div class="fig-title"><span class="fig-num">6-4</span>런타임 탐지 시나리오 — CloudAppEvents (고급 헌팅)</div>
        <a href="img/rt-cloudapp.png" target="_blank" rel="noopener"><img loading="lazy" src="img/rt-cloudapp.png" alt="고급 헌팅 CloudAppEvents"></a>
      </figure>
      <div class="note"><code>CloudAppEvents</code> 테이블(Agent 365 관측 데이터)을 <code>ActionType == "ExecuteToolByGateway"</code>로 필터링해 에이전트의 <b>실제 도구 호출</b>을 조회합니다. 경고(<code>AlertInfo</code>)·증거(<code>AlertEvidence</code>)와 상관 분석하면 하나의 실행 흐름을 재구성할 수 있습니다.<br><br><b>주요 컬럼과 조회 가능 정보</b><br>• <code>Timestamp</code> — 도구 호출 시각<br>• <code>ActionType</code> — 작업 유형(에이전트 도구 호출은 <code>ExecuteToolByGateway</code>)<br>• <code>Application</code>·<code>AccountDisplayName</code>·<code>AccountObjectId</code> — 어떤 앱·실행 계정이 호출했는지<br>• <code>IPAddress</code>·<code>CountryCode</code> — 호출 출처 IP·국가<br>• <code>RawEventData</code> — 도구 호출의 원천 JSON. 여기에 <code>ToolServerName</code>(MCP 서버명)·<code>ServerAddress</code>·<code>AgentName</code>·<code>ToolName</code>·<code>ToolDescription</code>·<code>Operation</code>·<code>ErrorMessage</code> 등 <b>실제 호출된 도구와 파라미터·결과</b>가 담깁니다<br>이를 통해 <b>어떤 에이전트가 어떤 MCP 도구를, 어디서(IP·국가), 어떤 앱·계정으로 호출했는지</b>를 활동 단위로 추적할 수 있습니다. <span class="hl-note">참고: 실시간 보호의 감사·차단 동작은 <code>BehaviorInfo</code>에 기록되지만, <b>Copilot Studio 에이전트의 차단 이벤트는 아직 지원되지 않습니다</b>.</span></div>
      <div class="code"><div class="code-head"><span>KQL — 최근 에이전트 도구 호출 조회</span><button class="copy-btn" type="button">복사</button></div><pre><code>CloudAppEvents
| where Timestamp &gt; ago(7d)
| where ActionType == "ExecuteToolByGateway"
| project Timestamp, Application, AccountDisplayName, IPAddress, CountryCode, RawEventData
| order by Timestamp desc</code></pre></div>
      <div class="code"><div class="code-head"><span>KQL — RawEventData에서 도구·서버 추출</span><button class="copy-btn" type="button">복사</button></div><pre><code>CloudAppEvents
| where Timestamp &gt; ago(7d)
| where ActionType == "ExecuteToolByGateway"
| extend d = todynamic(RawEventData)
| project Timestamp,
          AgentName = tostring(d.AgentName),
          ToolServerName = tostring(d.ToolServerName),
          ToolName = tostring(d.ToolName),
          Operation = tostring(d.Operation),
          ErrorMessage = tostring(d.ErrorMessage),
          IPAddress, CountryCode
| order by Timestamp desc</code></pre></div>""",
}

# 챕터 intro 표에 덱 외 추가 행(항목, 설정 위치, 확인 포인트)과 점프 대상
EXTRA_ROWS = {
    "ch7": [
        (["6", "런타임 탐지 시나리오", "Defender > 사건 & 경고 / 고급 헌팅(AgentsInfo·CloudAppEvents)",
          "실제 에이전트 실행에서 발생한 위험 신호를 준실시간 탐지·조사"], "s80-2"),
    ],
}

CH5_TABLE = [
    ["#", "항목", "설정 위치", "확인 포인트", ""],
    ["0", "역할/권한 준비", "Entra 관리 센터 > 역할 및 관리자 > 조건부 액세스 관리자",
     "정책 생성 전 조건부 액세스 관리자 역할 확인", ""],
    ["1", "사용자 차단 정책 생성", "조건부 액세스 > 정책 > 새 정책 (사용자 / 대상 리소스 / 네트워크 / 액세스 제어)",
     "모든 사용자 → Copilot Studio 에이전트, 사외(비신뢰 네트워크)에서 액세스 차단 → 정책 On", "sca1"],
    ["2", "실제 차단·정책 평가 확인", "Teams / M365 Copilot에서 에이전트 실행 후 Entra > 모니터링 및 상태 > 로그인 로그",
     "사외에서 Copilot Studio 에이전트 실행이 실제로 차단되는지, 로그인 로그의 CA 결과를 확인", "sca7"],
]

CH5_FIGS = [
    ("sca1", "1-1", "사용자 차단 정책 생성 — 조건부 액세스 새 정책 만들기", "img/ca-5-1a.png",
     "① <b>Entra ID</b>에서 ② <b>조건부 액세스</b>로 이동해 ③ <b>새 정책 만들기</b>를 선택합니다. 이 작업에는 <b>조건부 액세스 관리자</b> 역할이 필요합니다."),
    ("sca2", "1-2", "사용자 차단 정책 생성 — 정책 이름 및 행위자(사용자) 지정", "img/ca-5-2.png",
     "① <b>정책 이름</b>을 지정합니다. 이름에 적용 대상·조건(예: <i>사외 위험 에이전트 사용 차단</i>)을 드러내면 이후 운영·감사에서 구분이 쉽습니다. ② 할당의 <b>사용자 또는 에이전트</b>에서 정책이 적용될 행위자를 지정하는데, 이번 시나리오는 <b>사용자가 에이전트를 사용하는 행위</b>를 통제하므로 ③ <b>모든 사용자</b>를 선택합니다(운영 시에는 특정 그룹으로 좁히는 것을 권장). 안내에 나오듯 사용자 기반 정책은 사용자가 직접 접근하거나 <b>사용자를 대신해 작동하는 에이전트를 통해</b> 접근할 때 함께 적용됩니다."),
    ("sca3", "1-3", "사용자 차단 정책 생성 — 대상 리소스(에이전트) 지정", "img/ca-5-3.png",
     "① <b>대상 리소스</b>에서 접근을 통제할 대상을 지정합니다. ② <b>리소스 선택 &gt; 특정 리소스 선택</b>에서 <code>Microsoft Copilot Studio agent identity blueprint</code>를 지정하면 <b>Copilot Studio로 만든 에이전트</b>가 접근 대상이 됩니다.<br><br><b>Note —</b> 현재 조건부 액세스 리소스 선택기에서 <b>개별 에이전트 ID는 '지원되지 않는 리소스'</b>로 표시되어 단일 에이전트만 개별적으로 지정할 수는 없습니다. 대신 위 <b>블루프린트</b>로 Copilot Studio 에이전트 전체를, 또는 <b>모든 에이전트 리소스</b>로 테넌트의 모든 에이전트를 대상으로 지정합니다."),
    ("sca4", "1-4", "사용자 차단 정책 생성 — 네트워크 조건(사외) 지정", "img/ca-5-4.png",
     "① <b>네트워크</b> 조건을 켜고 <b>포함</b>은 <b>모든 네트워크 또는 위치</b>로 둔 뒤, ② <b>제외</b> 탭에서 <b>모든 신뢰할 수 있는 네트워크 및 위치</b>를 제외합니다. 이렇게 하면 <b>사내(신뢰 네트워크)는 정책에서 빠지고, 사외(비신뢰 네트워크)에서 접근할 때만 정책이 적용</b>됩니다."),
    ("sca4b", "예시", "명명된 위치 — 신뢰할 수 있는 위치 사전 정의 화면", "img/ca-5-nl.png",
     "여기서 말하는 '신뢰할 수 있는 위치'는 <code>조건부 액세스 &gt; 관리 &gt; 명명된 위치</code>에서 회사 IP 대역 등을 등록하고 <b>신뢰할 수 있음 = 예</b>로 표시해 둔 위치입니다. 본 실습 테넌트에는 회사 IP 대역(예: <code>ME Services</code>·<code>Provisioning/Stockpiling/Teams Workers</code>)이 이미 신뢰 위치로 등록되어 있어, 이 대역 밖(사외)에서 접근할 때 앞의 정책이 적용됩니다."),
    ("sca5", "1-5", "사용자 차단 정책 생성 — 액세스 제어(차단) 지정", "img/ca-5-5.png",
     "① <b>액세스 제어 &gt; 허용</b>을 열고 ② <b>액세스 차단</b>을 선택합니다. 이 조합으로 '<b>모든 사용자</b>가 <b>사외</b>에서 <b>Copilot Studio 에이전트</b>에 접근하면 <b>차단</b>'이라는 정책이 완성됩니다."),
    ("sca6", "1-6", "사용자 차단 정책 생성 — 정책 사용 지정 및 생성", "img/ca-5-6.png",
     "정책 요약을 확인하고 ① <b>정책 사용</b>을 지정한 뒤 ② <b>만들기</b>로 생성합니다. 운영 반영 전 영향도를 먼저 보려면 <b>보고 전용(Report-only)</b>으로 만들어 로그로만 평가하고, <b>실제로 차단하려면 '설정(On)'으로 전환</b>합니다.<br><br><b>주의 —</b> <b>모든 사용자</b> + <b>차단</b> 조합은 광범위 영향을 줄 수 있으므로, 운영에서는 반드시 소규모 그룹으로 먼저 검증한 뒤 확대합니다."),
    ("sca7", "2-1", "실제 차단 확인 — 사외에서 에이전트 실행 차단", "img/ca-5-7.png",
     "정책을 <b>On</b>으로 둔 상태에서 <b>Teams / M365 Copilot</b>로 대상 Copilot Studio 에이전트를 <b>사외(비신뢰 네트워크)에서 실행</b>하면, 에이전트가 도구 호출을 위해 토큰을 요청하는 시점에 조건부 액세스가 이를 거부해 <b>실제로 차단</b>됩니다. 화면과 같이 <code>오류 코드: IntegratedAuthConditionalAccessBlocked</code> 메시지가 표시되며, 이는 <b>통합 인증이 조건부 액세스 정책에 의해 차단</b>됐음을 명시적으로 나타냅니다.<br><br><span class='hl-note'>참고: 조건부 액세스는 <b>새 토큰 요청 시</b> 평가되므로, 정책을 켠 직후 이미 로그인된 세션에서는 토큰 캐시로 인해 즉시 차단되지 않을 수 있습니다. 토큰이 갱신되거나 새 세션·새 도구 연결로 접근할 때 차단이 적용됩니다.</span>"),
    ("sca8", "2-2", "정책 평가 확인 — 로그인 로그(조건부 액세스 결과)", "img/ca-5-8.png",
     "<code>Entra &gt; 모니터링 및 상태 &gt; 로그인 로그</code>에서 <b>사용자 로그인(비대화형)</b> 탭을 열고, <b>조건부 액세스</b> 열(및 로그인 상세의 조건부 액세스 탭)에서 이 정책의 평가 결과를 확인합니다. 사외에서 대상 에이전트 리소스에 접근한 로그인은 이 정책에 의해 <b>실패(차단)</b>로 기록됩니다.<br><br><span class='hl-note'>참고: 비대화형 로그인 로그는 수집·반영까지 다소 지연될 수 있어, 차단 직후에는 로그가 보이지 않을 수 있습니다.</span>"),
]

def ch5_custom_html():
    ths = "".join(f"<th>{esc(x)}</th>" for x in CH5_TABLE[0][:-1])
    trs = []
    for r in CH5_TABLE[1:]:
        cells, tgt = r[:-1], r[-1]
        tds = "".join("<td>" + esc(x).replace("\n", "<br>") + "</td>" for x in cells)
        if tgt:
            trs.append(f'<tr class="jump" data-target="{tgt}" tabindex="0">{tds}</tr>')
        else:
            trs.append(f"<tr>{tds}</tr>")
    steps = []
    for fid, label, title, img, note in CH5_FIGS:
        if not img:
            imgs_html = '<div class="ph">스크린샷 준비 중 — 로그 수집 후 추가 예정</div>'
        else:
            imgs_list = img if isinstance(img, (list, tuple)) else [img]
            imgs_html = "".join(
                f'<a href="{p}" target="_blank" rel="noopener"><img loading="lazy" src="{p}" alt="{esc(title)}"></a>'
                for p in imgs_list)
        if label == "예시":
            numspan = '<span class="fig-num" style="background:var(--surface-2);color:var(--text-soft);">예시</span>'
        else:
            numspan = f'<span class="fig-num">{label}</span>'
        steps.append(f"""
      <figure class="fig" id="{fid}">
        <div class="fig-title">{numspan}{esc(title)}</div>
        {imgs_html}
      </figure>
      <div class="note">{note}</div>""")
    return "".join(f"<th>{x}</th>" for x in []), ths, "".join(trs), "".join(steps)


# ===== Chapter 8 (실행 텔레메트리 / App Insights) 커스텀 =====
CH8_TABLE = [
    ["#", "항목", "설정 위치", "확인 포인트", ""],
    ["0", "역할/권한 준비", "Power Platform 관리 센터 + Azure 구독",
     "Power Platform 관리자 + 대상 환경의 시스템 관리자, Azure에서 App Insights 생성·연결 권한. 대상 환경은 Managed Environment여야 함", ""],
    ["1", "PowerPlatform 설정", "PPAC > 관리 > 데이터 내보내기 > App Insights > 새 데이터 내보내기",
     "Copilot Studio 텔레메트리를 대상 환경 → App Insights로 연결 (환경/App Insights 1:1)", "s81a"],
    ["2", "App Insights에서 텔레메트리 조회", "Azure Portal > App Insights > 조사 > Agents / Logs (KQL)",
     "모든 텔레메트리는 dependencies 테이블에 OpenTelemetry span으로 기록(InvokeAgent·ExecuteTool·OutputMessages), 데이터 도착 SLA 최대 24시간", "s82a"],
]
CH8_FIGS = [
    ("s81a", "1-1", "PowerPlatform 설정 — 데이터 내보내기 진입", "img/ai-8-1.png",
     "<code>Power Platform 관리 센터</code> 맨 좌측의 ① <b>관리</b> 탭에서 ② <b>데이터 내보내기</b>를 열고, ③ <b>App Insights</b> 탭에서 ④ <b>새 데이터 내보내기</b>를 시작합니다. 이 작업에는 <b>Power Platform 관리자</b>와 대상 환경의 <b>시스템 관리자</b> 권한이 필요하며, 대상 환경은 <b>Managed Environment</b>여야 합니다."),
    ("s81b", "1-2", "PowerPlatform 설정 — 이름·데이터 종류 지정", "img/ai-8-2.png",
     "① <b>내보내기 패키지 이름</b>을 지정하고, ② 내보낼 데이터 종류에서 <b>Copilot Studio(미리 보기)</b>를 선택합니다. 필요 시 Dataverse 진단·Power Automate 등 다른 종류도 함께 선택할 수 있습니다."),
    ("s81c", "1-3", "PowerPlatform 설정 — 환경 선택 (Managed Environment)", "img/ai-8-3.png",
     "텔레메트리를 수집할 <b>환경</b>을 선택합니다. 이 기능은 <b>관리형 환경(Managed Environment)</b>만 대상이 되며, 이 실습에서는 데모 에이전트가 있는 <code>Agent-Demo</code> 환경을 선택했습니다."),
    ("s81d", "1-4", "PowerPlatform 설정 — App Insights 인스턴스 생성 (Azure 포털)", "img/ai-8-4.png",
     "연결할 Application Insights 인스턴스가 없으면 마법사의 <b>“Azure 포털로 이동합니다”</b> 링크에서 인스턴스를 새로 만듭니다. 대상 <b>구독·리소스 그룹·이름·리전</b>을 지정하고 생성합니다(이 실습에서는 <code>rg-agent-sec</code>에 <code>agent365-appinsights</code>를 생성). ① 배포 완료를 확인하고 ② 리소스로 이동할 수 있습니다.<br><br><span class=\"hl-note\">참고: 이미 인스턴스가 있으면 이 단계는 건너뛰고 바로 다음 단계에서 선택하면 됩니다. 새로 만든 인스턴스는 PPAC 목록에 반영되기까지 수 분의 전파 지연이 있을 수 있습니다.</span>"),
    ("s81e", "1-5", "PowerPlatform 설정 — App Insights 연결 (구독·리소스 그룹·인스턴스)", "img/ai-8-5.png",
     "① <b>구독</b>, ② <b>리소스 그룹</b>, ③ <b>Application Insights 인스턴스</b>를 차례로 선택해 연결 대상을 지정합니다. App Insights 인스턴스는 환경/테넌트당 <b>1:1</b>로 연결하는 것을 권장합니다(여러 환경을 하나에 섞으면 기본 리포트가 깨질 수 있음)."),
    ("s81g", "1-6", "PowerPlatform 설정 — 검토 및 생성", "img/ai-8-6.png",
     "① 패키지 이름·환경·데이터 종류·<b>연결 세부 정보</b>(구독·리소스 그룹·인스턴스)를 검토하고 ② <b>만들기</b>로 데이터 내보내기를 생성합니다."),
    ("s81h", "1-7", "PowerPlatform 설정 — 연결 완료", "img/ai-8-7.png",
     "① <b>“Application Insights에 대한 데이터 내보내기가 설정되었습니다”</b> 안내가 표시되고, ② 목록에 생성된 내보내기(이름·환경·데이터 선택·App Insights·<b>상태=연결됨</b>)가 나타납니다.<br><br><span class=\"hl-note\">참고: 설정 후 실제 데이터가 App Insights에 도착하기까지 <b>최대 24시간(SLA)</b>이 걸릴 수 있습니다.</span>"),
    ("callout", '<h2 class="ov-h" style="margin-top:40px;">2단계 — 에이전트 텔레메트리 조회</h2>'),
    ("s82a", "2-1", "에이전트 텔레메트리 조회 — App Insights 에이전트 세부 정보(Agents)", "img/ai-8-agents.png",
     "생성한 Application Insights 리소스(<code>agent365-appinsights</code>)를 열고 ① 좌측 <b>조사(Investigate)</b> 섹션을 펼쳐 ② <b>Agents (Preview)</b> 페이지로 이동합니다. 이 <b>AI 에이전트 모니터링</b> 화면은 기본 리포트로 <b>에이전트 사용량·도구 호출(tool calls)·토큰 사용(token usage)·지연(latency)·오류</b> 인사이트를 보여줍니다.<br><br><span class=\"hl-note\">참고: 이 <b>Agents(에이전트 세부 정보) 페이지</b>는 기존 <b>Copilot Studio 대시보드(미리 보기) 워크북(2026-01-31 제거 예정)</b>을 대체하는 <b>권장 화면</b>입니다. 화면은 데이터 내보내기를 방금 설정한 직후라 아직 활동이 없어 “AI 에이전트 모니터링 시작” 안내가 표시되며, 텔레메트리는 데이터 내보내기 설정 후 <b>최대 24시간(SLA)</b> 내에 도착합니다.</span>"),
    ("callout",
     "<figure class=\"fig\">"
     "<div class=\"fig-title\"><span class=\"fig-num\" style=\"background:var(--surface-2);color:var(--text-soft);\">참고</span>App Insights에서 확인 가능한 텔레메트리 — 무엇이 span으로 남는가</div>"
     "<div class=\"ref-card\">"
     "<p style=\"margin:0 0 12px;font-size:14px;\">1단계 내보내기를 켜면, 에이전트가 실행될 때마다 그 과정이 <b>자동으로</b> Application Insights의 <code>dependencies</code> 테이블에 쌓입니다(따로 켤 설정은 없습니다). 기록 단위는 <b>span</b>이며, 사용자가 한 번 말하고 에이전트가 답하는 <b>한 턴(turn)</b>이 다음 3개 span으로 남습니다 — <code>InvokeAgent</code>(사용자 입력을 받은 시작점) → <code>ExecuteTool</code>(도구·커넥터 호출) → <code>OutputMessages</code>(에이전트 응답).</p>"
     "<div class=\"tw tw-fields\"><table><thead><tr>"
     "<th>이벤트 (span)</th><th>무엇을 기록</th><th>주요 <code>gen_ai.*</code> 속성 (customDimensions)</th></tr></thead><tbody>"
     "<tr><td><code>InvokeAgent</code><br>(턴 루트)</td><td>에이전트 턴 시작 · 사용자 입력</td>"
     "<td><code>gen_ai.input.messages</code> (사용자 프롬프트)</td></tr>"
     "<tr><td><code>ExecuteTool</code></td><td>도구·커넥터 호출</td>"
     "<td><code>gen_ai.tool.name</code> · <code>gen_ai.tool.type</code> · <b>입력</b> <code>gen_ai.tool.call.arguments</code> · <b>출력</b> <code>gen_ai.tool.call.result</code></td></tr>"
     "<tr><td><code>OutputMessages</code></td><td>에이전트 응답</td>"
     "<td><code>gen_ai.output.messages</code> (에이전트 답변)</td></tr>"
     "<tr><td>모든 span 공통</td><td>트레이스·대화 상관관계</td>"
     "<td><code>gen_ai.agent.name</code> · <code>gen_ai.conversation.id</code> · <code>gen_ai.request.model</code> · <code>operation_Id</code>(턴) · <code>operation_ParentId</code>(중첩)</td></tr>"
     "</tbody></table></div>"
     "<div class=\"ref-links\"><b>필드 레퍼런스:</b> "
     "<a class='xref-ext' href='https://learn.microsoft.com/ko-kr/microsoft-copilot-studio/advanced-environment-level-agent-telemetry' target='_blank' rel='noopener'>환경 단위 텔레메트리 — dependencies span·gen_ai 필드(공식 문서)</a> · "
     "<a class='xref-ext' href='https://learn.microsoft.com/ko-kr/azure/azure-monitor/reference/tables/dependencies' target='_blank' rel='noopener'>dependencies 테이블 스키마</a> · "
     "<a class='xref-ext' href='https://learn.microsoft.com/en-us/power-platform/admin/set-up-export-application-insights' target='_blank' rel='noopener'>환경 단위 App Insights 내보내기 설정</a></div>"
     "</div></figure>"),
    ("s82b", "2-2", "에이전트 텔레메트리 조회 — App Insights Logs (KQL)", "",
     "Agents 뷰 외에 직접 KQL로 조회하려면 <code>Application Insights &gt; 모니터링 &gt; 로그</code>에서 <b>KQL 모드</b>로 쿼리를 실행합니다. 환경 단위 내보내기 텔레메트리는 모두 <code>dependencies</code> 테이블에 <code>gen_ai.*</code> 속성을 가진 span으로 저장되므로, 아래 예시는 공식 문서 기준 <code>dependencies</code> 쿼리입니다. (현재는 데이터 수집 전이라 스크린샷은 데이터 도착 후 추가 예정)"),
    ("callout",
     "<div class=\"code\"><div class=\"code-head\"><span>KQL — span 종류별 개수(데이터 도착 확인)</span><button class=\"copy-btn\" type=\"button\">복사</button></div><pre><code>dependencies\n| where timestamp &gt; ago(24h)\n| where type == \"GenAI\"\n| summarize count() by name\n| order by count_ desc   // InvokeAgent · ExecuteTool · OutputMessages</code></pre></div>"
     "<div class=\"code\"><div class=\"code-head\"><span>KQL — 도구 호출 입력·출력 조회 (ExecuteTool)</span><button class=\"copy-btn\" type=\"button\">복사</button></div><pre><code>dependencies\n| where timestamp &gt; ago(24h)\n| where name == \"ExecuteTool\"\n| project timestamp,\n          ToolName  = tostring(customDimensions[\"gen_ai.tool.name\"]),\n          ToolType  = tostring(customDimensions[\"gen_ai.tool.type\"]),\n          Arguments = tostring(customDimensions[\"gen_ai.tool.call.arguments\"]),\n          Result    = tostring(customDimensions[\"gen_ai.tool.call.result\"]),\n          Conversation = tostring(customDimensions[\"gen_ai.conversation.id\"]),\n          resultCode, duration\n| order by timestamp desc</code></pre></div>"
     "<div class=\"code\"><div class=\"code-head\"><span>KQL — 도구별 호출량·지연·성공률</span><button class=\"copy-btn\" type=\"button\">복사</button></div><pre><code>dependencies\n| where timestamp &gt; ago(24h)\n| where name == \"ExecuteTool\"\n| extend ToolName = tostring(customDimensions[\"gen_ai.tool.name\"])\n| summarize calls = count(),\n            avgDurationMs = avg(duration),\n            successRate = 100.0 * countif(success == true) / count()\n          by ToolName\n| order by calls desc</code></pre></div>"
     "<div class=\"code\"><div class=\"code-head\"><span>KQL — 특정 대화의 전체 트레이스(턴 재구성)</span><button class=\"copy-btn\" type=\"button\">복사</button></div><pre><code>// 대화 ID는 테스트 중 /debug conversationid 로 확인\nlet Convo = \"&lt;conversation id&gt;\";\ndependencies\n| where tostring(customDimensions[\"gen_ai.conversation.id\"]) == Convo\n| order by operation_Id asc, iff(name == \"InvokeAgent\", 0, 1) asc, timestamp asc\n| project timestamp, name, operation_Id, operation_ParentId,\n          duration, resultCode, customDimensions</code></pre></div>"),
    ("callout", '<h2 class="ov-h" style="margin-top:40px;">부록 — Foundry 기반 에이전트 Tracing</h2>'),
    ("callout",
     "<div class=\"scope-box\" id=\"s81f\"><p>이 장은 <b>Copilot Studio 에이전트</b>의 텔레메트리를 다룹니다. 반면 <b>Azure AI Foundry</b>로 만든 에이전트는 PPAC 데이터 내보내기가 아니라 <b>Foundry 포털의 Tracing</b>에서 Application Insights 리소스를 연결해 관측합니다(<b>OpenTelemetry → Azure Application Insights</b>).</p>"
     "<a class='cta-link' href='https://learn.microsoft.com/ko-kr/azure/foundry/observability/how-to/trace-agent-setup?tabs=python' target='_blank' rel='noopener'>Foundry 에이전트 추적 설정(공식 문서) →</a></div>"),
]

def custom_section_html(table, steps_html):
    ths = "".join(f"<th>{esc(x)}</th>" for x in table[0][:-1])
    trs = []
    for r in table[1:]:
        cells, tgt = r[:-1], r[-1]
        tds = "".join("<td>" + esc(x).replace("\n", "<br>") + "</td>" for x in cells)
        if tgt:
            trs.append(f'<tr class="jump" data-target="{tgt}" tabindex="0">{tds}</tr>')
        else:
            trs.append(f"<tr>{tds}</tr>")
    return ths, "".join(trs)


def render_figs(figs):
    steps = []
    for item in figs:
        # callout item: ("callout", html)
        if item[0] == "callout":
            steps.append(item[1])
            continue
        fid, label, title, img, note = item
        if not img:
            imgs_html = '<div class="ph">스크린샷 준비 중 — 캡처 후 추가 예정</div>'
        else:
            imgs_list = img if isinstance(img, (list, tuple)) else [img]
            imgs_html = "".join(
                f'<a href="{p}" target="_blank" rel="noopener"><img loading="lazy" src="{p}" alt="{esc(title)}"></a>'
                for p in imgs_list)
        if label == "예시":
            numspan = '<span class="fig-num" style="background:var(--surface-2);color:var(--text-soft);">예시</span>'
        else:
            numspan = f'<span class="fig-num">{label}</span>'
        steps.append(f"""
      <figure class="fig" id="{fid}">
        <div class="fig-title">{numspan}{esc(title)}</div>
        {imgs_html}
      </figure>
      <div class="note">{note}</div>""")
    return "".join(steps)


def title_of(n):
    for sh in deck[n-1]["shapes"]:
        if sh["kind"] == "text" and sh["name"] in ("제목 1",) or (sh["kind"]=="text" and "title" in sh["name"].lower()):
            return sh["text"].replace("\n", " ").strip()
    return f"슬라이드 {n}"

def esc(s): return html.escape(s)

parts = []
nav = []
SKIP = {63}  # slides excluded from the guide
PLACEHOLDER = {86}  # slides shown as placeholder (screenshot pending)
for c in CH:
    nav.append(f'<a href="#{c["id"]}" data-sec="{c["id"]}"><span class="n">{c["num"]}</span><span>{esc(c["name"])}</span></a>')

def anchor_for(c, firstcol):
    fc = firstcol.strip()
    if not fc.isdigit():
        return None
    for n in range(c["range"][0], c["range"][1]+1):
        if n in SKIP:
            continue
        t = title_of(n)
        if t.startswith(f"{c['orig']}-{fc}.") or t.startswith(f"{c['orig']}-{fc} "):
            return n
    return None

for c in CH:
    if c.get("custom") and c["id"] == "ch9":
        ths, trs_html = custom_section_html(CH8_TABLE, "")
        steps_html = render_figs(CH8_FIGS)
        parts.append(f"""
  <section id="{c['id']}" class="page">
    <div class="hero">
      <span class="tag">Chapter {c['num']} · Microsoft Agent 365</span>
      <h1>{c['num']}. {esc(c['name'])}</h1>
      <p>{c['lead']}</p>
    </div>
    <h2 class="ov-h">전체 순서 한눈에 보기</h2>
    <div class="tw"><table><thead><tr>{ths}</tr></thead><tbody>{trs_html}</tbody></table></div>
    <h2 class="ov-h">단계별 상세</h2>
    {steps_html}
    <div class="pagenav">__PN{c['num']}__</div>
  </section>""")
        continue
    if c.get("custom") and c["id"] == "ch4":
        _, ths, trs_html, steps_html = ch5_custom_html()
        parts.append(f"""
  <section id="{c['id']}" class="page">
    <div class="hero">
      <span class="tag">Chapter {c['num']} · Microsoft Agent 365</span>
      <h1>{c['num']}. {esc(c['name'])}</h1>
      <p>{c['lead']}</p>
    </div>
    <h2 class="ov-h">전체 순서 한눈에 보기</h2>
    <div class="tw"><table><thead><tr>{ths}</tr></thead><tbody>{trs_html}</tbody></table></div>
    <h2 class="ov-h">단계별 상세</h2>
    {steps_html}
    <div class="pagenav">__PN{c['num']}__</div>
  </section>""")
        continue
    tbl = [list(r) for r in table_of(c["intro"])]
    if tbl and not tbl[0][-1].strip():
        for r in tbl:
            tail = r.pop().strip()
            if tail:
                r[-1] = (r[-1].rstrip() + "\n" + tail) if r[-1].strip() else tail
    hdr = tbl[0]
    ncol = len(hdr)
    ths = "".join(f"<th>{esc(x.replace(chr(10),' '))}</th>" for x in hdr)
    trs = []
    for r in tbl[1:]:
        anc = anchor_for(c, r[0])
        tds = "".join("<td>" + esc(x).replace("\n", "<br>") + "</td>" for x in r)
        if anc:
            trs.append(f'<tr class="jump" data-target="s{anc}" tabindex="0">{tds}</tr>')
        else:
            trs.append(f"<tr>{tds}</tr>")
    for row, tgt in EXTRA_ROWS.get(c["id"], []):
        tds = "".join("<td>" + esc(x).replace("\n", "<br>") + "</td>" for x in row)
        if tgt:
            trs.append(f'<tr class="jump" data-target="{tgt}" tabindex="0">{tds}</tr>')
        else:
            trs.append(f"<tr>{tds}</tr>")
    steps = []
    substep = {}
    valid_steps = {int(r[0]) for r in tbl[1:] if r[0].strip().isdigit() and int(r[0]) > 0}
    last_valid = None
    for k, n in enumerate(range(c["range"][0], c["range"][1]+1), 1):
        if n in SKIP:
            continue
        t = title_of(n)
        ct = re.sub(r'^\s*\d+\s*-\s*\d+(\s*[~∼]\s*\d+\s*-\s*\d+)?\.?\s*', '', t).strip().rstrip('|').strip()
        ct = TITLE_OVERRIDE.get(n, ct)
        m = re.match(r'^\s*((?:\d+\s*-\s*\d+\s*[~∼]?\s*)+)', t)
        if m:
            pairs = re.findall(r'\d+\s*-\s*(\d+)', m.group(1))
            step = int(pairs[-1]) if pairs else k
        else:
            step = k
        if valid_steps and step not in valid_steps:
            step = last_valid if last_valid is not None else min(valid_steps)
        last_valid = step
        substep[step] = substep.get(step, 0) + 1
        label = f"{step}-{substep[step]}"
        d = DESC.get(n, "")
        code_html = ""
        if n in CODE:
            lang, src = CODE[n]
            code_html = (f'<div class="code"><div class="code-head"><span>{esc(lang)}</span>'
                         f'<button class="copy-btn" type="button">복사</button></div>'
                         f'<pre><code>{esc(src)}</code></pre></div>')
        if n in PLACEHOLDER:
            imgs = '<div class="ph">스크린샷 준비 중 — 로그 수집 후 추가 예정</div>'
        elif os.path.exists(os.path.join(BASE, "img", f"slide-{n:02d}a.png")):
            imgs = "".join(
                f'<a href="img/slide-{n:02d}{p}.png" target="_blank" rel="noopener"><img loading="lazy" src="img/slide-{n:02d}{p}.png" alt="{esc(ct)}"></a>'
                for p in ("a", "b"))
        else:
            imgs = f'<a href="img/slide-{n:02d}.png" target="_blank" rel="noopener"><img loading="lazy" src="img/slide-{n:02d}.png" alt="{esc(ct)}"></a>'
        steps.append(f"""
      <figure class="fig" id="s{n}">
        <div class="fig-title"><span class="fig-num">{label}</span>{esc(ct)}</div>
        {code_html}
        {imgs}
      </figure>
      <div class="note">{d}</div>{EXTRA.get(n, "")}""")
    parts.append(f"""
  <section id="{c['id']}" class="page">
    <div class="hero">
      <span class="tag">Chapter {c['num']} · Microsoft Agent 365</span>
      <h1>{c['num']}. {esc(c['name'])}</h1>
      <p>{esc(c['lead'])}</p>
    </div>
    <h2 class="ov-h">전체 순서 한눈에 보기</h2>
    <div class="tw"><table><thead><tr>{ths}</tr></thead><tbody>{''.join(trs)}</tbody></table></div>
    <h2 class="ov-h">단계별 상세</h2>
    {''.join(steps)}
    <div class="pagenav">__PN{c['num']}__</div>
  </section>""")

# pager links
for i, c in enumerate(CH):
    prev_html = ""
    nxt_html = ""
    if i > 0:
        p = CH[i-1]
        prev_html = f'<a class="prv" href="#{p["id"]}" data-go="{p["id"]}"><span class="lbl">← 이전</span><br>{p["num"]}. {esc(p["name"])}</a>'
    else:
        prev_html = '<span class="pn-empty"></span>'
    if i < len(CH)-1:
        nx = CH[i+1]
        nxt_html = f'<a class="nxt" href="#{nx["id"]}" data-go="{nx["id"]}"><span class="lbl">다음 →</span><br>{nx["num"]}. {esc(nx["name"])}</a>'
    else:
        nxt_html = '<span class="pn-empty"></span>'
    parts[i] = parts[i].replace(f"__PN{c['num']}__", prev_html + nxt_html)

CSS = """
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css");
:root{--bg:#f6f8fb;--surface:#fff;--surface-2:#eef1f4;--border:#e2e6ec;--text:#1f2328;--text-soft:#57606a;--accent:#0f6cbd;--accent-2:#8a5cf6;--accent-pink:#d63aa0;--code-bg:#1e2430;--code-text:#e6edf3;--crit:#b3261e;--low:#3a7d34;--shadow:0 1px 3px rgba(20,30,50,.06),0 8px 24px rgba(20,30,50,.06);--radius:14px;}
html[data-theme="dark"]{--bg:#0f141b;--surface:#171d26;--surface-2:#212a35;--border:#2b3542;--text:#e6edf3;--text-soft:#9aa7b4;--accent:#58a6ff;--accent-2:#b18cff;--accent-pink:#ff6bbd;--code-bg:#0b0e13;--code-text:#e6edf3;--crit:#f0655d;--low:#6bbf5f;--shadow:0 1px 3px rgba(0,0,0,.5),0 8px 24px rgba(0,0,0,.4);}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{margin:0;font-family:Pretendard,-apple-system,BlinkMacSystemFont,"Segoe UI","Malgun Gothic",sans-serif;background:var(--bg);color:var(--text);line-height:1.7;font-size:16px;}
a{color:var(--accent);text-decoration:none;}
a:hover{text-decoration:underline;}
code{background:var(--surface-2);padding:2px 6px;border-radius:5px;font-family:"Cascadia Code",Consolas,monospace;font-size:13.5px;color:#b0387c;}
html[data-theme="dark"] code{color:#ff9dd4;}
.layout{display:flex;min-height:100vh;}
.sidebar{width:290px;flex-shrink:0;background:var(--surface);border-right:1px solid var(--border);padding:26px 18px;position:sticky;top:0;height:100vh;overflow-y:auto;display:flex;flex-direction:column;}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:14px;margin-bottom:8px;letter-spacing:-.3px;line-height:1.3;}
.brand .dot{width:24px;height:24px;border-radius:8px;background:linear-gradient(135deg,var(--accent) 0%,var(--accent-2) 55%,var(--accent-pink) 100%);flex-shrink:0;}
.brand-sub{font-size:12px;color:var(--text-soft);margin:0 0 22px 34px;}
.nav-group{margin-bottom:18px;}
.nav-group h4{font-size:11px;text-transform:uppercase;letter-spacing:.8px;color:var(--accent);margin:0 0 8px 8px;font-weight:700;}
.nav-group a{display:flex;gap:10px;align-items:center;padding:8px 10px;border-radius:8px;color:var(--text);font-size:14px;margin-bottom:2px;}
.nav-group a:hover{background:var(--surface-2);text-decoration:none;}
.nav-group a.active{background:linear-gradient(135deg,rgba(15,108,189,.12),rgba(138,92,246,.12));color:var(--accent);font-weight:600;}
.nav-group a .n{flex:0 0 22px;height:22px;display:grid;place-items:center;border-radius:6px;background:var(--surface-2);border:1px solid var(--border);font-size:12px;font-weight:700;}
.nav-group a.active .n{background:linear-gradient(135deg,var(--accent),var(--accent-2));color:#fff;border-color:transparent;}
.nav-parent{font-weight:600;}
.nav-children{margin:2px 0 2px 10px;padding-left:12px;border-left:1.5px solid var(--border);}
.nav-sub .n{flex:0 0 20px;height:20px;font-size:11px;}
.nav-sub{font-size:13.5px;padding:7px 10px;}
.theme-toggle{display:inline-flex;align-items:center;gap:6px;margin:auto 8px 2px;align-self:flex-start;padding:8px 15px;background:var(--surface-2);border:1px solid var(--border);border-radius:999px;color:var(--text);font-size:13px;font-weight:600;cursor:pointer;font-family:inherit;}
.theme-toggle:hover{border-color:var(--accent);background:var(--surface);}
.main{flex:1;min-width:0;}
.content{max-width:940px;margin:0 auto;padding:46px 40px 90px;}
.page{display:none;}
.page.active{display:block;animation:fade .18s ease;}
@keyframes fade{from{opacity:0;transform:translateY(4px);}to{opacity:1;transform:none;}}
.hero{background:linear-gradient(135deg,#0f6cbd 0%,#6a4bd8 55%,#c0389a 100%);color:#fff;border-radius:var(--radius);padding:36px 34px;margin-bottom:30px;box-shadow:var(--shadow);}
.hero .tag{display:inline-block;background:rgba(255,255,255,.18);backdrop-filter:blur(4px);padding:4px 12px;border-radius:999px;font-size:12px;font-weight:600;margin-bottom:14px;}
.hero h1{margin:0 0 12px;font-size:29px;line-height:1.25;letter-spacing:-.5px;}
.hero p{margin:0;font-size:15.5px;opacity:.95;}
h2.ov-h{font-size:20px;letter-spacing:-.3px;margin:38px 0 14px;padding:4px 0 10px 14px;position:relative;border-bottom:1px solid var(--border);}
h2.ov-h::before{content:"";position:absolute;left:0;top:2px;bottom:10px;width:5px;border-radius:5px;background:linear-gradient(180deg,var(--accent),var(--accent-2) 55%,var(--accent-pink));}
.ov-sub{color:var(--text-soft);font-size:14px;margin:0 0 12px;}
.page-lead{color:var(--text-soft);font-size:15.5px;margin:0 0 8px;}
.pname{font-weight:700;white-space:nowrap;}
.portal-link{font-family:"Cascadia Code",Consolas,monospace;font-size:12.5px;white-space:nowrap;}
.scope-box{background:var(--surface);border:1px solid var(--border);border-left:4px solid var(--accent-2);border-radius:10px;padding:16px 18px;box-shadow:var(--shadow);margin:6px 0 8px;}
.scope-box p{margin:0 0 10px;font-size:14.5px;}
.cta-link{display:inline-block;margin-top:4px;padding:9px 16px;border-radius:8px;font-weight:600;font-size:14px;color:#fff;background:linear-gradient(135deg,var(--accent),var(--accent-2));text-decoration:none;}
.cta-link:hover{text-decoration:none;opacity:.92;}
.download-btn{display:inline-flex;align-items:center;gap:8px;margin:2px 0 14px;padding:9px 15px;border-radius:8px;font-weight:600;font-size:13.5px;color:var(--accent);background:var(--surface);border:1px solid var(--border);text-decoration:none;}
.download-btn:hover{text-decoration:none;border-color:var(--accent);background:var(--surface-2);}
.method{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px 18px;box-shadow:var(--shadow);margin:0 0 12px;}
.method-head{display:flex;align-items:center;gap:10px;font-weight:700;font-size:15px;margin-bottom:6px;}
.method-no{flex:0 0 24px;height:24px;display:inline-flex;align-items:center;justify-content:center;border-radius:7px;background:linear-gradient(135deg,var(--accent),var(--accent-2));color:#fff;font-size:13px;}
.method p{margin:6px 0;font-size:14px;}
.method-cond{color:var(--text-soft);font-size:13px;}
.rec{font-size:11px;font-weight:700;color:#fff;background:var(--low,#3a7d34);border-radius:999px;padding:2px 9px;margin-left:2px;}
table{width:100%;border-collapse:collapse;margin:6px 0 8px;font-size:14px;background:var(--surface);border-radius:10px;overflow:hidden;box-shadow:var(--shadow);}
.tw{overflow-x:auto;}
.ref-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:16px 18px;box-shadow:var(--shadow);}
.ref-card .tw-fields table{margin:0;box-shadow:none;}
.ref-links{margin-top:12px;font-size:13px;color:var(--text-soft);line-height:1.8;}
.tw-fields td:first-child,.tw-fields th:first-child{text-align:left;font-weight:600;width:auto;color:inherit;white-space:nowrap;}
.tw-fields table{width:100%;border-collapse:collapse;font-size:13.5px;}
.tw-fields code{white-space:nowrap;}
th,td{text-align:left;padding:11px 14px;border-bottom:1px solid var(--border);vertical-align:top;}
th{background:var(--surface-2);font-weight:600;font-size:13px;white-space:nowrap;}
td:first-child,th:first-child{text-align:center;font-weight:700;width:42px;color:var(--accent);}
tr:last-child td{border-bottom:none;}
tr.jump{cursor:pointer;transition:background .12s;}
tr.jump td:last-child::after{content:"→ 이동";color:var(--accent);font-weight:700;float:right;opacity:0;transition:opacity .12s;padding-left:8px;font-size:12px;}
tr.jump:hover td,tr.jump:focus td{background:linear-gradient(135deg,rgba(15,108,189,.08),rgba(138,92,246,.08));}
tr.jump:hover td:last-child::after,tr.jump:focus td:last-child::after{opacity:1;}
tr.jump:focus{outline:none;}
@keyframes flash{0%{box-shadow:0 0 0 3px var(--accent) inset;}100%{box-shadow:0 0 0 0 transparent inset;}}
figure.fig.flash img{animation:flash 1.2s ease-out;}
figure.fig{margin:24px 0 6px;}
figure.fig img{display:block;width:100%;height:auto;border:1px solid var(--border);border-radius:10px;box-shadow:var(--shadow);background:var(--surface);}
figure.fig a + a img{margin-top:14px;}
.fig-title{display:flex;align-items:center;gap:10px;font-size:15.5px;font-weight:600;margin:0 0 10px;letter-spacing:-.2px;color:var(--text);}
.fig-num{flex:0 0 auto;min-width:34px;height:26px;padding:0 9px;display:inline-flex;align-items:center;justify-content:center;border-radius:8px;background:linear-gradient(135deg,var(--accent),var(--accent-2));color:#fff;font-size:13px;font-weight:700;letter-spacing:.2px;}
.fig-cap{margin:8px 2px 0;font-size:13px;color:var(--text-soft);line-height:1.6;}
.fig-cap b{color:var(--text);}
.hl-note{display:block;margin-top:8px;padding-top:8px;border-top:1px dashed var(--border);color:var(--text-soft);}
.ph{display:flex;align-items:center;justify-content:center;min-height:200px;border:2px dashed var(--border);border-radius:10px;color:var(--text-soft);font-size:14px;font-weight:600;background:repeating-linear-gradient(45deg,var(--surface-2),var(--surface-2) 10px,var(--surface) 10px,var(--surface) 20px);}
.code{margin:14px 0 4px;border:1px solid var(--border);border-radius:10px;overflow:hidden;box-shadow:var(--shadow);}
.code-head{display:flex;align-items:center;justify-content:space-between;padding:8px 12px;background:var(--surface-2);border-bottom:1px solid var(--border);font-size:12.5px;font-weight:700;color:var(--text-soft);}
.copy-btn{font:inherit;font-size:12px;font-weight:600;padding:4px 12px;border-radius:7px;border:1px solid var(--border);background:var(--surface);color:var(--text);cursor:pointer;}
.copy-btn:hover{border-color:var(--accent);color:var(--accent);}
.copy-btn.done{border-color:var(--success);color:var(--success);}
.code pre{margin:0;background:var(--code-bg);color:var(--code-text);padding:14px 16px;overflow-x:auto;font-family:"Cascadia Code",Consolas,monospace;font-size:13px;line-height:1.6;}
.code pre code{background:none;padding:0;color:inherit;font-size:inherit;white-space:pre;}
.note{background:#eef4fb;border-left:4px solid var(--accent);border-radius:10px;padding:13px 16px;margin:8px 0 26px;font-size:14.5px;color:var(--text);}
html[data-theme="dark"] .note{background:#13243a;}
.note b{color:var(--text);}
.xref{color:var(--accent);font-weight:600;text-decoration:none;border-bottom:1px dashed var(--accent);cursor:pointer;}
.xref:hover{text-decoration:none;background:var(--accent-soft,rgba(15,108,189,.1));border-radius:4px;}
html[data-theme="dark"] .xref{color:var(--accent);}
.xref-ext{color:var(--accent);font-weight:600;text-decoration:underline;text-underline-offset:2px;}
.xref-ext:hover{opacity:.85;}
.pagenav{display:flex;justify-content:space-between;gap:14px;margin-top:44px;}
.pagenav a{flex:1;background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px 18px;box-shadow:var(--shadow);color:var(--text);}
.pagenav a:hover{text-decoration:none;border-color:var(--accent);}
.pagenav a.nxt{text-align:right;}
.pagenav .lbl{font-size:12px;color:var(--text-soft);}
.pn-empty{flex:1;}
.footer{margin-top:50px;padding-top:18px;border-top:1px solid var(--border);color:var(--text-soft);font-size:13px;}
@media(max-width:860px){.layout{flex-direction:column;}.sidebar{width:100%;height:auto;position:static;border-right:none;border-bottom:1px solid var(--border);}.content{padding:30px 20px 60px;}}
"""

HTML = """<!DOCTYPE html>
<html lang="ko" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agent 365 초기 설정 및 구성 가이드</title>
<script>
(()=>{const p=new URLSearchParams(location.search).get("scoutTheme");const s=localStorage&&localStorage.getItem?localStorage.getItem("a365theme"):null;const t=p||s||(window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light");document.documentElement.setAttribute("data-theme",t);})();
</script>
<style>__CSS__</style>
</head>
<body>
<div class="layout">
<aside class="sidebar">
  <div class="brand"><span class="dot"></span><span>Agent 365 초기 설정 및 구성 가이드</span></div>
  <div class="brand-sub">Copilot Studio · 관리 · 보안 실습 (0–8)</div>
  <nav class="nav-group">
    <h4>가이드</h4>
    <a href="#overview" data-sec="overview" class="nav-parent"><span class="n">◆</span><span>Copilot Studio 에이전트</span></a>
    <div class="nav-children">
    __NAV__
    </div>
  </nav>
  <button class="theme-toggle" id="tt">🌓 테마 전환</button>
</aside>
<main class="main"><div class="content">
  __SECTIONS__
  <div class="footer">Microsoft Agent 365 초기 설정 및 구성 가이드 · 스크린샷은 Copilot Studio(New experience) 실습 기준 · 각 장 상단 표가 전체 순서입니다.</div>
</div></main>
</div>
<script>
const links=Array.from(document.querySelectorAll('.nav-group a'));
const ids=links.map(a=>a.dataset.sec);
function show(id,push){if(!ids.includes(id))id=ids[0];
 document.querySelectorAll('.page').forEach(s=>s.classList.toggle('active',s.id===id));
 links.forEach(a=>a.classList.toggle('active',a.dataset.sec===id));
 if(push)history.replaceState(null,'','#'+id);
 window.scrollTo({top:0,behavior:'smooth'});}
links.forEach(a=>a.addEventListener('click',e=>{e.preventDefault();show(a.dataset.sec,true);}));
document.querySelectorAll('[data-go]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();show(a.dataset.go,true);}));
show((location.hash||'').replace('#','')||ids[0],false);
window.addEventListener('hashchange',()=>show((location.hash||'').replace('#',''),false));
document.querySelectorAll('tr.jump').forEach(row=>{
  const go=()=>{const tgt=row.dataset.target;
    if(ids.includes(tgt)){show(tgt,true);return;}
    const el=document.getElementById(tgt);if(!el)return;el.scrollIntoView({behavior:'smooth',block:'start'});el.classList.remove('flash');void el.offsetWidth;el.classList.add('flash');};
  row.addEventListener('click',go);
  row.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();go();}});
});
document.querySelectorAll('.copy-btn').forEach(btn=>{
  btn.addEventListener('click',()=>{
    const code=btn.closest('.code').querySelector('code').innerText;
    const done=()=>{btn.classList.add('done');const o=btn.dataset.label||btn.textContent;btn.dataset.label=o;btn.textContent='복사됨';setTimeout(()=>{btn.textContent=o;btn.classList.remove('done');},1500);};
    const fallback=()=>{const ta=document.createElement('textarea');ta.value=code;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.focus();ta.select();try{document.execCommand('copy');}catch(e){}document.body.removeChild(ta);done();};
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(code).then(done).catch(fallback);}
    else{fallback();}
  });
});
document.querySelectorAll('.xref').forEach(a=>{
  a.addEventListener('click',e=>{e.preventDefault();const t=a.dataset.target;
    if(ids.includes(t)){show(t,true);return;}
    const el=document.getElementById(t);if(!el)return;el.scrollIntoView({behavior:'smooth',block:'start'});el.classList.remove('flash');void el.offsetWidth;el.classList.add('flash');});
});
const tt=document.getElementById('tt');
tt.addEventListener('click',()=>{const c=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';document.documentElement.setAttribute('data-theme',c);try{localStorage.setItem('a365theme',c);}catch(e){}});
</script>
</body>
</html>"""

PORTALS = [
 ("Copilot Studio", "에이전트 생성 · 지침/지식/도구 구성 · 게시", "https://copilotstudio.microsoft.com"),
 ("Microsoft 365 관리 센터 (MAC)", "에이전트 승인 · 전사 배포 · 인벤토리(레지스트리)", "https://admin.microsoft.com"),
 ("Microsoft Entra 관리 센터", "역할 할당 · 조건부 액세스 · 로그인 로그 · Gen AI 인사이트", "https://entra.microsoft.com"),
 ("Power Platform 관리 센터 (PPAC)", "환경 보안 · 위협 탐지 · 에이전트용 전역 보안 액세스(GSA)", "https://admin.powerplatform.microsoft.com"),
 ("Microsoft Defender 포털", "AI 보안 커넥터 · Copilot Studio 런타임 보호 정책", "https://security.microsoft.com"),
 ("Microsoft Purview 포털", "내부 위험 관리(IRM) · 감사 · 에이전트 리스크 경고", "https://purview.microsoft.com"),
]
ROLES = [
 ("0", "에이전트 생성", "환경 제작자(Maker) 이상", "Power Platform 관리 센터 · 환경/보안 역할"),
 ("1", "승인 및 전사 배포", "AI 관리자", "Entra > 사용자 > 할당된 역할"),
 ("2", "인벤토리 확인", "AI 읽기 권한자", "Entra > 사용자 > 할당된 역할"),
 ("3", "에이전트 차단", "AI 관리자 · 에이전트 ID 관리자", "Entra > 사용자 > 할당된 역할"),
 ("4", "기본 접근제어", "조건부 액세스 관리자", "Entra > 사용자 > 할당된 역할"),
 ("5", "리스크 탐지", "내부자 위험 관리 분석가 또는 조사자", "Purview > 역할 및 범위 > 역할 그룹"),
 ("6", "리스크 기반 접근제어", "조건부 액세스 관리자", "Entra > 사용자 > 할당된 역할"),
 ("7", "런타임 보호", "애플리케이션 관리자 · 보안 관리자 · Power Platform 관리자", "Entra > 역할 / Power Platform 관리 센터"),
 ("8", "트래픽 모니터링", "전역 보안 액세스 관리자", "Entra > 사용자 > 할당된 역할"),
]

portal_rows = "".join(
    f'<tr><td class="pname">{esc(nm)}</td><td>{esc(desc)}</td>'
    f'<td><a class="portal-link" href="{url}" target="_blank" rel="noopener">{url.replace("https://","")} ↗</a></td></tr>'
    for nm, desc, url in PORTALS)
role_rows = "".join(
    f'<tr class="jump" data-target="{CH[int(num)]["id"]}" tabindex="0">'
    f'<td>{num}</td><td>{esc(step)}</td><td>{esc(role)}</td><td>{esc(loc)}</td></tr>'
    for num, step, role, loc in ROLES)

overview = f"""
  <section id="overview" class="page">
    <div class="hero">
      <span class="tag">Microsoft Agent 365 · Copilot Studio</span>
      <h1>Copilot Studio 에이전트</h1>
      <p>Copilot Studio(New experience)에서 만든 에이전트를 안전하게 운영하기 위한 <b>기본 보안 설정</b>을 처음부터 끝까지 안내합니다. 에이전트 생성 → 승인·배포 → 인벤토리 → 차단 → 기본 접근제어 → 리스크 탐지 → 리스크 기반 접근제어 → 런타임 보호 → 트래픽 모니터링까지, 각 단계에서 어떤 포털에 들어가 무엇을 설정하는지 스크린샷과 함께 순서대로 짚어 드립니다.</p>
    </div>
    <p class="page-lead">이 가이드는 하나의 실습 환경에서 만든 데모 에이전트(<code>Agent365-Guide-Demo</code>)를 대상으로, 관리자·보안 담당자가 실제로 수행하는 구성 흐름을 재현합니다. 왼쪽 <b>구성 단계(0–8)</b> 목차에서 각 장으로 이동하고, 아래 표의 역할 행을 클릭하면 해당 단계로 바로 이동합니다.</p>

    <h2 class="ov-h">이 가이드의 범위 · Copilot Studio 참고</h2>
    <div class="scope-box">
      <p>본 가이드는 <b>Microsoft Agent 365의 관리·보안 기능</b>을 메인으로 다룹니다. 따라서 아래 <b>0. 에이전트 생성</b> 장은 실습에 필요한 최소한의 Copilot Studio 에이전트 생성 흐름만 담고 있습니다.</p>
      <p>지침 설계, 지식·도구(MCP) 심화 구성, 오케스트레이션, 채널·게시 등 <b>Copilot Studio 자체에 대한 더 자세한 내용</b>은 아래 문서를 참고하세요.</p>
      <a class="cta-link" href="https://chichoi1991.github.io/Agent_Blog/chapters/newcs0-overview/" target="_blank" rel="noopener">New Copilot Studio 핸즈온 가이드 바로가기 ↗</a>
    </div>

    <h2 class="ov-h">주요 진입 포털</h2>
    <p class="ov-sub">각 단계에서 사용하는 관리 포털입니다. 링크를 누르면 새 탭에서 해당 포털이 열립니다. 실제 접근에는 아래 <b>필요한 역할</b>이 선행되어야 합니다.</p>
    <div class="tw"><table><thead><tr><th>포털</th><th>이 가이드에서의 용도</th><th>바로가기</th></tr></thead><tbody>{portal_rows}</tbody></table></div>

    <h2 class="ov-h">단계별 필요한 역할 한눈에</h2>
    <p class="ov-sub">각 단계를 수행하기 전에 아래 역할을 미리 할당해 두세요. 대부분 <b>Entra 관리 센터 &gt; 사용자 &gt; 할당된 역할 &gt; 할당 추가</b>에서 부여하며, 5장은 Purview 역할 그룹, 7장 일부는 Power Platform 관리자 지정이 필요합니다. 행을 클릭하면 해당 단계로 이동합니다.</p>
    <div class="tw"><table><thead><tr><th>#</th><th>단계</th><th>필요한 역할</th><th>할당 위치</th></tr></thead><tbody>{role_rows}</tbody></table></div>
    <div class="note">역할은 <b>최소 권한 원칙</b>에 따라 필요한 단계에만 부여하고, 실습이 끝나면 회수하는 것을 권장합니다. AI 관리자·에이전트 ID 관리자·조건부 액세스 관리자 등은 테넌트 전체에 영향을 주는 상위 권한이므로 할당 대상을 신중히 관리하세요.</div>

    <h2 class="ov-h">0단계를 건너뛰고 바로 시작하기 · 에이전트 Import</h2>
    <p class="ov-sub"><b>0. 에이전트 생성</b>을 건너뛰고 준비된 실습용 에이전트로 시작하려면, 아래 앱 패키지를 <b>Microsoft 365 관리 센터(MAC)</b>에 직접 업로드합니다. 업로드 이후에는 <a class="xref" data-target="ch1">1. 에이전트 승인 및 전사 배포</a> 절차를 그대로 이어서 진행해 전사에 게시한 뒤, 2장부터 관리·보안 기능을 실습합니다.</p>
    <a class="download-btn" href="files/Agent365-Guide-Demo.zip" download>⬇ 실습용 에이전트 패키지 내려받기 (Agent365-Guide-Demo.zip)</a>

    <figure class="fig">
      <div class="fig-title"><span class="fig-num">1</span>에이전트 추가 진입 — Microsoft 365 관리 센터</div>
      <a href="img/import-mac-1.png" target="_blank" rel="noopener"><img loading="lazy" src="img/import-mac-1.png" alt="MAC 에이전트 추가 진입"></a>
    </figure>
    <div class="note"><a href="https://admin.microsoft.com" target="_blank" rel="noopener">Microsoft 365 관리 센터</a>에서 ① <b>에이전트</b> → ② <b>모든 에이전트</b>(레지스트리)로 이동한 뒤 ③ <b>에이전트 추가</b>를 선택합니다. 이 작업에는 <b>AI 관리자</b> 역할이 필요합니다.</div>

    <figure class="fig">
      <div class="fig-title"><span class="fig-num">2</span>매니페스트(.zip) 업로드 — 게시할 에이전트 업로드</div>
      <a href="img/import-mac-2.png" target="_blank" rel="noopener"><img loading="lazy" src="img/import-mac-2.png" alt="MAC 매니페스트 zip 업로드"></a>
    </figure>
    <div class="note">① <b>파일 선택</b>으로 위에서 내려받은 <code>Agent365-Guide-Demo.zip</code>(매니페스트 패키지)을 업로드하고 유효성 검사를 통과시킵니다. 파일 선택 이후에는 <a class="xref" data-target="ch1">1. 에이전트 승인 및 전사 배포</a> 절차와 <b>동일하게</b> 대상 지정·권한 검토·게시를 진행하면 전사에 배포됩니다.</div>

    <div class="pagenav"><span class="pn-empty"></span><a class="nxt" href="#ch0" data-go="ch0"><span class="lbl">다음 →</span><br>0. 에이전트 생성</a></div>
  </section>"""
parts.insert(0, overview)

nav_html = "\n    ".join(
    f'<a href="#{c["id"]}" data-sec="{c["id"]}" class="nav-sub"><span class="n">{c["num"]}</span><span>{esc(c["name"])}</span></a>'
    for c in CH)
out = HTML.replace("__CSS__", CSS).replace("__NAV__", nav_html).replace("__SECTIONS__", "\n".join(parts))
path = os.path.join(BASE, "index.html")
open(path, "w", encoding="utf-8").write(out)
print("written", len(out))
