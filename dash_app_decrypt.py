import streamlit as st
import base64
import urllib.parse

st.set_page_config(page_title="Magic Decoder", page_icon="🔓")
st.title("🔓 초간단 복호화/디코딩 툴")

# 1. URL 파라미터를 통해 데이터 가져오기
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

# 3. 링크 생성 기능 (원본 데이터를 Base64로 암호화하여 공유)
st.divider()
st.subheader("🔗 안전한 공유용 링크 만들기 (인코딩)")
share_data = st.text_input("숨기고 싶은 원본 데이터(예: 메가 링크) 입력:")

if share_data:
    # 1단계: 입력받은 데이터를 Base64로 인코딩(문자 섞기)
    encoded_bytes = base64.b64encode(share_data.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    
    # 실제 배포 시 본인의 스트림릿 사이트 주소로 변경
    base_url = "https://your-app.streamlit.app/" 
    
    # 2단계: 암호화된 데이터를 URL에 포함 (URL 형식에 맞게 한 번 더 안전하게 파싱)
    encoded_link = f"{base_url}?data={urllib.parse.quote(encoded_string)}"
    
    st.write("🔒 Base64로 변환된 텍스트 (이 글자만 복사해서 공유해도 됩니다):")
    st.code(encoded_string)
    
    st.write("🌐 접속 즉시 암호화된 텍스트가 입력되는 링크:")
    st.code(encoded_link)
    
    st.info("💡 **작동 방식:** 남들이 이 링크를 클릭하면 알 수 없는 영어/숫자 조합이 입력창에 뜹니다. 그 후 **[Base64 디코딩]** 버튼을 눌러야만 비로소 원본 메가 링크를 확인할 수 있습니다.")