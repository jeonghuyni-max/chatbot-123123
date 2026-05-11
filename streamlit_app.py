import streamlit as st
from openai import OpenAI

# 페이지 설정 및 제목
st.set_page_config(page_title="MBTI 판별 챗봇", page_icon="🧪")
st.title("🧪 MBTI 맞춤형 챗봇")
st.write(
    "몇 가지 질문을 통해 당신의 MBTI를 추측해 드립니다. "
    "대화를 시작하면 챗봇이 질문을 던질 거예요!"
)

# API 키 입력 (보안을 위해 password 타입 유지)
openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("시작하려면 OpenAI API 키를 입력해 주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        # 시스템 프롬프트: 챗봇의 정체성과 임무를 부여합니다.
        st.session_state.messages = [
            {
                "role": "system", 
                "content": (
                    "너는 MBTI 전문가야. 사용자와의 대화를 통해 사용자의 MBTI를 맞추는 것이 목표야. "
                    "한 번에 너무 많은 질문을 하지 말고, 하나씩 질문하면서 답변을 유도해줘. "
                    "사용자의 답변에서 에너지 방향(E/I), 인식 기능(S/N), 판단 기능(T/F), 생활 양식(J/P)의 특징을 파악해. "
                    "모든 대화는 친절한 한국어로 진행해줘."
                )
            },
            {
                "role": "assistant",
                "content": "안녕하세요! 당신의 MBTI가 무엇인지 함께 알아볼까요? 먼저, 쉬는 날에 주로 무엇을 하며 시간을 보내시는지 궁금해요!"
            }
        ]

    # 채팅 메시지 표시 (시스템 메시지는 제외)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 사용자 입력 처리
    if prompt := st.chat_input("답변을 입력하세요..."):
        # 사용자 메시지 저장 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API를 통한 답변 생성
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        
        # 챗봇 답변 저장
        st.session_state.messages.append({"role": "assistant", "content": response})

# 초기화 버튼 (필요할 경우)
if st.button("대화 초기화"):
    st.session_state.messages = []
    st.rerun()
