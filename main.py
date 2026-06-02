import os
import sys
import datetime
# import arrow  # 현재 코드에서 사용하지 않는다면 지워도 무방합니다.
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from kurly import clusters

# 🎯 한국 공휴일 목록 (YYYY-MM-DD 형식)
HOLIDAYS = {
    "2026-01-01",  # 신정
    "2026-02-16",  # 설 연휴
    "2026-02-17",  # 설날
    "2026-02-18",  # 설 연휴
    "2026-03-02",  # 대체공휴일
    "2026-05-05",  # 어린이날
    "2026-05-25",  # 대체공휴일
    "2026-06-03",  # 지방선거
    "2026-08-17",  # 대체공휴일
    "2026-09-24",  # 추석 연휴
    "2026-09-25",  # 추석
    "2026-10-05",  # 대체공휴일
    "2026-10-09",  # 한글날
    "2026-12-25",  # 크리스마스
}

# 📆 오늘 날짜 가져오기
today = datetime.date.today().strftime("%Y-%m-%d")

# 🚫 오늘이 공휴일이면 실행하지 않고 종료
if today in HOLIDAYS:
    print(f"📢 오늘({today})은 공휴일이므로 실행하지 않습니다.")
    sys.exit(0)

# 환경 변수에서 Slack 토큰 로드
load_dotenv()
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

def send_slack_message(blocks_data, fallback_text, channel):
    try:
        client = WebClient(token=SLACK_TOKEN)
        # 텍스트 대신 blocks 매개변수를 사용하여 전송 (text는 알림 팝업용 텍스트)
        client.chat_postMessage(channel=channel, text=fallback_text, blocks=blocks_data)
    except SlackApiError as e:
        print(f"⚠️ Error sending message to {channel} : {e}")

def main():
    for cluster in clusters:
        # 📝 Block Kit 구조로 메시지 본문 작성
        message_blocks = [
            {
                # [블록 1] 상단 공지 내용 (일반 마크다운)
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*[공지｜사내 추천제도 안내]*\n\n\n1. *중요도* : 중\n2. *대상* : 평택 클러스터 구성원 전체\n3. *주요 내용*\n\n안녕하세요? 평택 클러스터 구성원 여러분!:blush:\n\n우리 클러스터에서 함께할 인재를 찾기 위해 사내 *추천제도* 를 운영하고 있습니다.\n:2776724f56a9beff08:주변에 *컬리와 잘 맞는 인재가 있다면* 아래 링크를 확인하시어, 비대면 (온라인) 또는 대면 (추천서&입사지원서)으로 제출 해주시면 됩니다!!:2776724f56a9beff08:\n\n:감사콩gif:구성원 여러분들의 많은 추천 부탁드립니다.:감사콩gif:\n\n\n:bulb: *사내추천제도란?*"
                }
            },
            {
                # [블록 2] 인용구 + 밑줄 적용 영역 (Rich Text 블록)
                "type": "rich_text",
                "elements": [
                    {
                        "type": "rich_text_quote",
                        "elements": [
                            {
                                "type": "text",
                                "text": "컬리 구성원의 추천받은 지원자의 서류 및 검토 후 입사 시 일정 기간 근속에 따라 "
                            },
                            {
                                "type": "text",
                                "text": "추천자에게 보상금",
                                "style": {"bold": True}
                            },
                            {
                                "type": "text",
                                "text": " 이 지급되는 제도 입니다!\n\n"
                            },
                            {
                                # ✨ 원하시던 굵은 글씨 + 밑줄 동시 적용 부분 ✨
                                "type": "text",
                                "text": "\"2026년 6월부터 온라인 / 대면 접수가 모두 가능합니다!\"\n",
                                "style": {
                                    "bold": True,
                                    "underline": True
                                }
                            },
                            {
                                "type": "text",
                                "text": "제출 방법 및 자세한 안내 사항 은 "
                            },
                            {
                                "type": "link",
                                "url": "https://kurlyptrc.notion.site/5eb394b593ac4784bc4dc4a3ff82087a",
                                "text": "추천 채용 제도 안내",
                                "style": {"bold": True}
                            },
                            {
                                "type": "text",
                                "text": " 에서 확인해 주시기 바랍니다.\n"
                            }
                        ]
                    }
                ]
            },
            {
                # [블록 3] 하단 내용 (일반 마크다운)
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "\n\n:pushpin: *추천 채용 보상 안내*\n>:ck11: 선임/사원/스탭(계약직) : (직/간접 추천 동일) *추천 대상자 근속 3개월 후 300,000원*\n>:ck11: 스탭(정규직) 이상 : (간접 추천) *추천 대상자 근속 3개월 후 500,000원*\n>:ck11: 스탭(정규직) 이상 : (직접 추천) *추천 대상자 근속 3개월 후 500,000원 / 추천대상자 근속 6개월 후 500,000원*\n\n\n:purple_heart: *채용 및 추천 관련 문의* :purple_heart:\n*:slack: 문의사항 : <@U094ZMCF1T2>,<@U05P7LCBQ8H>*\n:phone:  *010-5820-9367*\n\n\n감사합니다."
                }
            }
        ]

        # 모바일 푸시 알림용 미리보기 텍스트 (필수)
        fallback_text = "[공지] 사내 추천제도 안내"

        # 슬랙 채널에 전송 (blocks 구조체 통째로 넘김)
        send_slack_message(message_blocks, fallback_text, cluster.channel)

if __name__ == "__main__":
    main()
