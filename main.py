import os
import sys
import datetime
import arrow
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from kurly import clusters

# 🎯 한국 공휴일 목록 (YYYY-MM-DD 형식)
HOLIDAYS = {
    "2025-01-01",  # 신정
    "2025-03-01",  # 삼일절
    "2025-05-05",  # 어린이날
    "2025-05-06",  # 대체공휴일
    "2025-10-03",  # 개천절
    "2025-10-06",  # 추석
    "2025-10-07",  # 추석연휴
    "2025-10-08",  # 대체공휴일
    "2025-10-09",  # 한글날
    "2025-12-25",  # 크리스마스
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

def send_slack_message(message, channel):
    try:
        client = WebClient(token=SLACK_TOKEN)
        client.chat_postMessage(channel=channel, text=message)
    except SlackApiError as e:
        print(f"⚠️ Error sending message to {channel} : {e}")

def main():
    for cluster in clusters:
        # 메시지 제목 설정
        header = f":loudspeaker: *『인사총무팀 공지』* <!channel>\n\n"

        notice_msg = (
            f"안녕하세요? 평택 클러스터 구성원 여러분! 채용팀 입니다. :blush:\n"
            f"\n"
            f"평택센터에서 함께할 인재를 찾기 위해 사내 *추천제도* 를 운영하고 있습니다.\n"
            f":2776724f56a9beff08: 주변에 *컬리와 잘 맞는 인재가 있다면* 많은 추천 부탁드립니다. :2776724f56a9beff08:\n\n"
            f"\n"
            f"\n"
            f":bulb: *사내추천제도란?*\n"
            f"컬리 구성원이 인재를 추천하면, 추천받은 지원자가 입사 후 일정 기간 근속 시 *추천자에게 보상금* 이 지급되는 제도 입니다!\n"
            f"( *자세한 안내 사항* 은 아래 첨부 드리는 링크에서 확인해 주시기 바랍니다.)\n"
            f"* <https://kurlyptrc.notion.site/5eb394b593ac4784bc4dc4a3ff82087a|:page_with_curl: [ 사내추천 제도 안내페이지 ]>*\n\n"
            f"\n"
            f"\n"
            f":pushpin: *추천 채용 보상 안내*\n"
            f":ck11: 선임/사원/스탭(계약직) : (직/간접 추천 동일) *추천 대상자 근속 3개월 후 300,000원*\n"
            f":ck11: 스탭(정규직) 이상 : (간접 추천) *추천 대상자 근속 3개월 후 500,000원*\n"
            f":ck11: 스탭(정규직) 이상 : (직접 추천) *추천 대상자 근속 3개월 후 500,000원 / 추천대상자 근속 6개월 후 500,000원*\n\n"
            f"\n"
            f"\n"
            f":purple_heart: *채용 및 추천 관련 문의* :purple_heart:\n"
            f":slack:  <@U05NXEF1W5S> , <@U04S96F1G20>\n"
            f":phone:  *010-5820-9367 / 010-5820-6897*\n\n"
            f"\n"
            f"\n"
            f"궁금한 사항이 있으시다면 언제든지 문의해 주시기 바랍니다.\n"
            f"감사합니다.\n"
            f"\n"
        )
 
# 메시지 본문
        body = header + notice_msg

        # 슬랙 채널에 전송
        send_slack_message(body, cluster.channel)

if __name__ == "__main__":
    main()
