import streamlit as st
import base64
import urllib.parse

st.set_page_config(page_title="Magic Decoder", page_icon="🔓")
st.title("🔓 초간단 암/복호화 툴")

# 1. URL 파라미터 확인 (링크로 접속한 경우 자동 입력)
query_params = st.query_params
initial_data = query_params.get("data", "")

# 2. 메인 해독(디코딩) 영역
# 화면을 4:1 비율로 나누어 텍스트 입력창과 아이콘 배치
col_dec_text, col_dec_img = st.columns([4, 1])

with col_dec_text:
    st.subheader("🔓 데이터 해독하기 (디코딩)")
    input_text = st.text_area("암호화된 텍스트를 입력하세요 예)aHR~~~ :", value=initial_data, height=150)

with col_dec_img:
    # 빈 공간을 살짝 띄워서 위치를 맞춤
    st.write("")
    st.write("")
    st.write("")
    st.write("") 
    st.write("")
    st.image("icon_5.gif", use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("Base64 해독", use_container_width=True):
        if input_text:
            try:
                decoded = base64.b64decode(input_text).decode('utf-8')
                st.success("해독 성공!")
                st.code(decoded)
            except Exception:
                st.error("유효한 Base64 형식이 아닙니다.")
        else:
            st.warning("텍스트를 먼저 입력해 주세요.")

with col2:
    if st.button("URL 해독", use_container_width=True):
        if input_text:
            try:
                decoded = urllib.parse.unquote(input_text)
                st.success("해독 성공!")
                st.code(decoded)
            except Exception:
                st.error("해독 중 오류가 발생했습니다.")
        else:
            st.warning("텍스트를 먼저 입력해 주세요.")

st.divider()

# 3. 암호화(인코딩) 영역 - 공유용 데이터 생성
st.subheader("🔒 나만의 비밀 데이터 만들기 (인코딩)")
share_data = st.text_input("숨기고 싶은 원본 데이터(예: 공유 링크, 비밀 메모)를 입력하세요:")

if share_data:
    # Base64로 텍스트 변환
    encoded_bytes = base64.b64encode(share_data.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    
    # 성공했을 때만 화면을 나누어 아이콘 표시
    col_enc_text, col_enc_img = st.columns([4, 1])
    
    with col_enc_text:
        st.success("암호화 완료! 아래 텍스트를 복사해서 공유하세요.")
        st.code(encoded_string)
        
    with col_enc_img:
        st.image("icon_15.gif", use_container_width=True)