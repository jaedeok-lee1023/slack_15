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

def send_slack_message(message, channel):
    try:
        client = WebClient(token=SLACK_TOKEN)
        client.chat_postMessage(channel=channel, text=message)
    except SlackApiError as e:
        print(f"⚠️ Error sending message to {channel} : {e}")

def main():
    for cluster in clusters:
        # 메시지 제목 설정
        header = f"*[공지｜사내 추천제도 안내]*\n\n\n"

        notice_msg = ( 
            f"1. *중요도* : 중\n"
            f"2. *대상* : 평택 클러스터 구성원 전체\n"
            f"3. *주요 내용*\n\n"
            f"\n"
            f"안녕하세요? 평택 클러스터 구성원 여러분!:blush:\n\n"
            f"우리 클러스터에서 함께할 인재를 찾기 위해 사내 *추천제도* 를 운영하고 있습니다.\n"
            f":2776724f56a9beff08:주변에 *컬리와 잘 맞는 인재가 있다면* 6층 컬리스라운지(직원휴게실) 또는 2층 통합사무실에 방문하여 추천 해주시면 됩니다!:2776724f56a9beff08:\n\n" 
            f":감사콩gif:구성원 여러분들의 많은 추천 부탁드립니다.:감사콩gif:\n"
            f"\n\n"
            f":bulb: *사내추천제도란?*\n"
            f">컬리 구성원의 추천받은 지원자의 서류 및 검토 후 입사 시 일정 기간 근속에 따라 *추천자에게 보상금* 이 지급되는 제도 입니다!\n"
            f">\"2026년 6월부터 온라인 / 대면 접수가 모두 가능합니다!\"\n"
            f">제출 방법 및 자세한 안내 사항 은 <https://kurlyptrc.notion.site/5eb394b593ac4784bc4dc4a3ff82087a|추천 채용 제도 안내> 에서 확인해 주시기 바랍니다.\n\n"
            f"\n\n"
            f":pushpin: *추천 채용 보상 안내*\n"
            f">:ck11: 선임/사원/스탭(계약직) : (직/간접 추천 동일) *추천 대상자 근속 3개월 후 300,000원*\n"
            f">:ck11: 스탭(정규직) 이상 : (간접 추천) *추천 대상자 근속 3개월 후 500,000원*\n"
            f">:ck11: 스탭(정규직) 이상 : (직접 추천) *추천 대상자 근속 3개월 후 500,000원 / 추천대상자 근속 6개월 후 500,000원*\n\n"
            f"\n"
            f":purple_heart: *채용 및 추천 관련 문의* :purple_heart:\n"
            f"*:slack: 문의사항 : <@U094ZMCF1T2>,<@U05P7LCBQ8H>*\n"
            f":phone:  *010-5820-9367*\n\n"
            f"\n"
            f"감사합니다.\n"
        )
 
# 메시지 본문
        body = header + notice_msg

        # 슬랙 채널에 전송
        send_slack_message(body, cluster.channel)

if __name__ == "__main__":
    main()
