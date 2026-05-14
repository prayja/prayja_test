import streamlit as st
import base64
import urllib.parse

st.set_page_config(page_title="Magic Decoder", page_icon="🔓")
st.title("🔓 초간단 복호화/디코딩 툴")

# 1. URL 파라미터를 통해 데이터 가져오기 (편의 기능)
# 예: yoursite.com/?data=SGVsbG8=
query_params = st.query_params
initial_data = query_params.get("data", "")

# 2. 입력 UI
input_text = st.text_area("디코딩할 내용을 입력하세요:", value=initial_data, height=150)

col1, col2 = st.columns(2)

with col1:
    if st.button("Base64 디코딩", use_container_width=True):
        try:
            decoded = base64.b64decode(input_text).decode('utf-8')
            st.success("Base64 결과:")
            st.code(decoded)
        except Exception as e:
            st.error("Base64 형식이 아닙니다.")

with col2:
    if st.button("URL 디코딩", use_container_width=True):
        try:
            decoded = urllib.parse.unquote(input_text)
            st.success("URL 디코딩 결과:")
            st.code(decoded)
        except Exception as e:
            st.error("디코딩 중 오류가 발생했습니다.")

# 3. 링크 생성 기능 (복호화로 바로 연결되는 링크)
st.divider()
st.subheader("🔗 공유용 링크 만들기")
share_data = st.text_input("공유할 원본 데이터 입력:")
if share_data:
    # 실제 배포 시 사이트 주소로 변경 필요
    base_url = "https://your-app.streamlit.app/" 
    encoded_link = f"{base_url}?data={share_data}"
    st.write("아래 링크를 공유하면 접속 즉시 입력창에 데이터가 들어갑니다:")
    st.code(encoded_link)