import streamlit as st
from openai import OpenAI

# 페이지 설정 및 제목 변경
st.set_page_config(page_title="너 T야?", page_icon="🧐")
st.title("🧐 너 T야?") # 요청하신 제목으로 변경
st.write(
    "채팅을 시작하면 챗봇이 당신의 성향을 파악하기 위한 질문을 던집니다. "
    "솔직하게 답변하다 보면 당신의 MBTI를 맞출 수 있을지도 몰라요!"
)

# API 키 입력
openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("시작하려면 OpenAI API 키를 입력해 주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        # 시스템 프롬프트: MBTI 분석 전문가로서의 정체성 강화
        st.session_state.messages = [
            {
                "role": "system", 
                "content": (
                    "너는 상대방의 대화를 통해 MBTI를 추측하는 전문가야. "
                    "상대방이 '너 T야?'라는 소리를 듣지 않도록 공감해주면서도 날카롭게 성향을 분석해줘. "
                    "질문은 한 번에 하나씩만 하고, 답변을 받으면 그에 대한 리액션을 짧게 한 뒤 다음 질문을 해줘. "
                    "4가지 지표(E/I, S/N, T/F, J/P)를 모두 확인하면 최종적으로 추측하는 MBTI를 알려줘."
                )
            },
            {
                "role": "assistant",
                "content": "반가워요! 당신의 MBTI를 파헤쳐 보겠습니다. 😎 \n\n 첫 번째 질문입니다! 주말에 갑자기 친구가 '지금 집 앞인데 나올래?'라고 한다면, 당신의 솔직한 속마음은 어떤가요?"
            }
        ]

    # 채팅 메시지 표시
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 사용자 입력 및 챗봇 응답 처리
    if prompt := st.chat_input("답변을 입력해 보세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

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
        
        st.session_state.messages.append({"role": "assistant", "content": response})

# 다시 시작하기 버튼
if st.sidebar.button("다시 테스트하기"):
    st.session_state.clear()
    st.rerun()
