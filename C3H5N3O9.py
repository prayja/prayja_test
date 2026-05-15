import streamlit as st
import time

st.set_page_config(page_title="생존형 화학 연금술", layout="wide")

# 스타일 설정
st.markdown("""
<style>
    .stButton>button { width: 100%; font-weight: bold; border-radius: 5px; height: 3em; }
    .stAlert { border-radius: 10px; }
    .inventory-card { padding: 10px; border: 1px solid #ddd; border-radius: 5px; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("🏚️ 포스트 아포칼립스: 현대 문명 재건 실험실")
st.caption("자원이 한정된 세상에서 당신의 화학 지식만이 유일한 무기입니다.")

# ---------------------------------------------------------
# 세션 상태 초기화 (요청하신 초기값 0 설정 포함)
# ---------------------------------------------------------
if 'inventory' not in st.session_state:
    st.session_state.inventory = {
        "물": 10, "배수구 클리너": 10, "질산칼륨 비료": 10, "식용유": 5, "락스": 5,
        "폐배터리(리튬)": 5, "피마자 씨앗": 5, "푸른 곰팡이": 5, "감기약 소모품": 5, "설탕": 10,
        "수산화나트륨": 5, "에탄올": 5, "생석회": 5, "구연산": 5,
        "산화철(녹)": 20, "알루미늄 캔": 15, "강력 자석": 5, "구리선": 30, "철 조각": 30, "산화철(촉매)": 5,
        "Al": 0, "Li": 0, 
        "아염소산나트륨": 0, "과망간산칼륨": 0, "황산구리": 0  # 초기값 0 설정
    }
if 'flask_elements' not in st.session_state: st.session_state.flask_elements = {}
if 'flask_compounds' not in st.session_state: st.session_state.flask_compounds = {}
if 'flask_everyday' not in st.session_state: st.session_state.flask_everyday = {}

def add_to_flask(item_type, name):
    if item_type == 'element':
        st.session_state.flask_elements[name] = st.session_state.flask_elements.get(name, 0) + 1
    elif item_type == 'compound' or item_type == 'everyday':
        if st.session_state.inventory.get(name, 0) > 0:
            target = st.session_state.flask_compounds if item_type == 'compound' else st.session_state.flask_everyday
            target[name] = target.get(name, 0) + 1
            st.session_state.inventory[name] -= 1

def clear_flask():
    for name, count in st.session_state.flask_compounds.items():
        st.session_state.inventory[name] = st.session_state.inventory.get(name, 0) + count
    for name, count in st.session_state.flask_everyday.items():
        st.session_state.inventory[name] = st.session_state.inventory.get(name, 0) + count
    st.session_state.flask_elements, st.session_state.flask_compounds, st.session_state.flask_everyday = {}, {}, {}

# ---------------------------------------------------------
# 레시피 시스템 (추가 합성법 포함)
# ---------------------------------------------------------
recipes = {
    # [원소 및 기초 화합물 정제]
    "Al": {
        "req_everyday": {"알루미늄 캔": 1}, "process": "가열", "temp": (150, 200), 
        "msg": "🔥 알루미늄 원소를 추출했습니다."
    },
    "Li": {
        "req_everyday": {"폐배터리(리튬)": 1}, "process": "증류", "temp": (150, 180),
        "msg": "🔋 리튬 원소를 분리해냈습니다."
    },
    "아염소산나트륨": {
        "req_elements": {"Na": 1, "Cl": 1, "O": 2}, "process": "일반 혼합", "temp": (10, 30),
        "msg": "✨ 소독제 원료인 아염소산나트륨($NaClO_2$)을 합성했습니다."
    },
    "과망간산칼륨": {
        "req_elements": {"K": 1, "Mn": 1, "O": 4}, "process": "가열", "temp": (80, 120),
        "msg": "🔮 보라색 결정의 과망간산칼륨($KMnO_4$)을 얻었습니다."
    },
    "황산구리": {
        "req_elements": {"Cu": 1, "S": 1, "O": 4}, "req_compounds": {"황산": 1},
        "process": "가열", "temp": (70, 100),
        "msg": "💎 푸른색의 황산구리($CuSO_4$) 결정을 합성했습니다."
    },

    # [생존 및 무기]
    "황산": {"req_everyday": {"배수구 클리너": 1}, "process": "증류", "temp": (80, 150), "msg": "황산을 정제했습니다."},
    "질산": {"req_everyday": {"질산칼륨 비료": 1, "배수구 클리너": 1}, "process": "증류", "temp": (60, 100), "msg": "질산을 얻었습니다."},
    "글리세린": {"req_everyday": {"식용유": 1}, "req_compounds": {"물": 1}, "process": "가열", "temp": (50, 90), "msg": "글리세린을 얻었습니다."},
    "푸른 결정": {
        "req_everyday": {"감기약 소모품": 1}, "req_elements": {"Li": 1}, "req_compounds": {"물": 1},
        "process": "증류", "temp": (100, 130), "msg": "💎 최고의 거래 가치, 푸른 결정입니다."
    },
    "리신": {
        "req_everyday": {"피마자 씨앗": 1}, "req_compounds": {"물": 1},
        "process": "일반 혼합", "temp": (10, 30), "msg": "💀 맹독 리신입니다. 바늘 끝에 묻혀 사용하세요."
    },
    "페니실린": {
        "req_everyday": {"푸른 곰팡이": 1, "설탕": 1}, "req_compounds": {"물": 1},
        "process": "가열", "temp": (20, 35), "msg": "💊 기적의 항생제입니다! 감염병으로부터 생존하세요."
    },
    "CL-20": {
        "req_compounds": {"질산": 3, "황산": 2}, "req_elements": {"C": 6, "H": 6, "N": 12, "O": 12},
        "process": "아이스바스 (냉각)", "temp": (-20, 5), "msg": "🧨 최강의 폭약 CL-20.", "explode_if_hot": True
    },
    "살균 소독제": {
        "req_everyday": {"아염소산나트륨": 1}, "req_compounds": {"물": 9},
        "process": "일반 혼합", "temp": (15, 30), "msg": "✨ 강력한 소독제입니다."
    },
    "정수된 물": {
        "req_everyday": {"과망간산칼륨": 1}, "req_compounds": {"물": 10},
        "process": "일반 혼합", "temp": (5, 40), "msg": "💧 식수를 확보했습니다."
    },
    "보르도액 (농약)": {
        "req_everyday": {"황산구리": 1, "생석회": 1}, "req_compounds": {"물": 5},
        "process": "일반 혼합", "temp": (10, 30), "msg": "🌾 식량을 보호할 농약입니다."
    },
    "수제 비누": {
        "req_everyday": {"식용유": 2, "수산화나트륨": 1}, "req_compounds": {"물": 1},
        "process": "가열", "temp": (60, 80), "msg": "🧼 위생 상태를 개선합니다."
    },
    "불 피우기 (발화)": {
        "req_everyday": {"과망간산칼륨": 1, "글리세린": 1}, "process": "일반 혼합", "temp": (20, 40), "msg": "🔥 비상시 불을 피우는 데 성공했습니다."
    },
    "구리 코일 발전기": {
        "req_elements": {"Cu": 10, "Fe": 5}, "req_everyday": {"강력 자석": 2},
        "process": "일반 혼합", "temp": (15, 30), "msg": "⚡ 전기를 사용할 수 있습니다!"
    },
    "재생 배터리": {
        "req_elements": {"Li": 2, "C": 2}, "req_everyday": {"폐배터리(리튬)": 1, "황산": 1},
        "process": "증류", "temp": (40, 60), "msg": "🔋 휴대용 전자기기 사용이 가능합니다."
    },
    "써마이트": {
        "req_elements": {"Al": 2}, "req_everyday": {"산화철(녹)": 3},
        "process": "일반 혼합", "temp": (10, 40), "msg": "🔥 철판을 녹이는 써마이트입니다."
    },
    "암모니아 (NH3)": {
        "req_elements": {"N": 1, "H": 3}, "req_everyday": {"산화철(촉매)": 1},
        "process": "가열", "temp": (180, 200), "msg": "🌾 비료 생산을 위한 암모니아입니다."
    },
    "니트로글리세린": {
        "req_elements": {}, "req_compounds": {"글리세린": 1, "질산": 3, "황산": 1}, "req_everyday": {},
        "process": "아이스바스 (냉각)", "temp": (-20, 5),
        "msg": "성공!! 💥 위험천만한 니트로글리세린(C3H5N3O9) 합성에 성공했습니다. 절대 충격을 주지 마세요!",
        "explode_if_hot": True,
}
}

# ---------------------------------------------------------
# UI 구성
# ---------------------------------------------------------
col_inv, col_lab = st.columns([5, 5])

with col_inv:
    st.subheader("🎒 생존자 배낭 (Inventory)")
    inv = {k: v for k, v in st.session_state.inventory.items() if v > 0}
    cols = st.columns(3)
    for i, (name, count) in enumerate(inv.items()):
        with cols[i % 3]:
            # 추출/합성 필요 아이템 강조
            if name in ["Al", "Li", "아염소산나트륨", "과망간산칼륨", "황산구리"]:
                btn_label = f"🧪 {name}\n({count})"
            elif name in ["푸른 결정", "CL-20"]:
                btn_label = f"✨ {name}\n({count})"
            else:
                btn_label = f"{name}\n({count})"
            
            if st.button(btn_label, key=f"inv_{name}"):
                # 합성된 아이템들은 다시 비커에 넣을 때 compound/element 적절히 분류
                if name in ["Al", "Li"]: itype = 'element'
                elif name in ["물", "황산", "질산", "글리세린", "아염소산나트륨", "과망간산칼륨", "황산구리"]: itype = 'compound'
                else: itype = 'everyday'
                add_to_flask(itype, name)
                st.rerun()

    st.markdown("---")
    st.subheader("🧪 원소 주기율표")
    # Mn, K 추가
    elements = ["H", "C", "N", "O", "S", "Li", "Cl", "Na", "Al", "Cu", "Fe", "K", "Mn"]
    el_cols = st.columns(4)
    for i, el in enumerate(elements):
        if el_cols[i % 4].button(el):
            add_to_flask('element', el)

with col_lab:
    st.subheader("⚗️ 비커 상태")
    curr_all = {**st.session_state.flask_elements, **st.session_state.flask_compounds, **st.session_state.flask_everyday}
    if not curr_all: st.info("재료를 추가하세요.")
    else:
        for k, v in curr_all.items(): st.code(f"{k} : {v}개")
    
    st.button("🔄 비커 비우기", on_click=clear_flask)
    st.markdown("---")
    
    process = st.selectbox("처리 공정", ["일반 혼합", "가열", "증류", "아이스바스 (냉각)"])
    temp = st.slider("온도 조절 (℃)", -20, 200, 25)

    if st.button("☣️ 실험 개시!", type="primary"):
        if not curr_all:
            st.error("비커가 비어있습니다!")
        else:
            with st.spinner("반응 중..."):
                time.sleep(1.2)
                
                # 즉사 기믹 (락스+산 / 써마이트 가열)
                has_bleach = st.session_state.flask_everyday.get("락스", 0) > 0
                has_acid = (st.session_state.flask_everyday.get("배수구 클리너", 0) > 0 or 
                            st.session_state.flask_compounds.get("황산", 0) > 0)
                if has_bleach and has_acid:
                    st.error("💀 **염소가스 중독 사망**")
                    st.stop()

                is_thermite = (st.session_state.flask_everyday.get("산화철(녹)", 0) >= 3 and 
                               st.session_state.flask_elements.get("Al", 0) >= 2)
                if is_thermite and process == "가열":
                    st.error("💀 **써마이트 폭발 사망**")
                    st.stop()

                found = False
                for res_name, data in recipes.items():
                    if (st.session_state.flask_elements == data.get("req_elements", {}) and
                        st.session_state.flask_compounds == data.get("req_compounds", {}) and
                        st.session_state.flask_everyday == data.get("req_everyday", {})):
                        
                        found = True
                        if res_name == "암모니아 (NH3)" and temp < 180:
                            st.error("⚠️ 온도가 너무 낮아 질소 결합을 끊지 못했습니다.")
                            break
                        
                        if data.get("explode_if_hot") and temp > data["temp"][1]:
                            st.error("💥 열폭주 폭발!")
                            st.stop()
                        
                        if data["temp"][0] <= temp <= data["temp"][1] and process == data["process"]:
                            st.balloons()
                            st.success(data["msg"])
                            st.session_state.inventory[res_name] = st.session_state.inventory.get(res_name, 0) + 1
                            break
                        else:
                            st.warning(f"조건 불일치 ({data['process']}, {data['temp'][0]}~{data['temp'][1]}도)")
                            break
                
                if not found: st.error("실패: 검은 타르만 남았습니다.")
                st.session_state.flask_elements, st.session_state.flask_compounds, st.session_state.flask_everyday = {}, {}, {}
                time.sleep(1.5)
                st.rerun()

# 사이드바 가이드
with st.sidebar:
    st.header("📋 고급 제조법 가이드")
    st.info("Li (리튬) = 폐배터리(리튬) x1")
    st.info("아염소산나트륨 = Na x1, Cl x1, O x2")
    st.info("과망간산칼륨 = K x1, Mn x1, O x4")
    st.info("황산구리 = Cu x1, S x1, O x4, 황산 x1")
    st.info("황산 = 배수구 클리너 x1")
    st.info("질산 = 질산칼륨 비료 x1, 배수구 클리너 x1")
    st.info("글리세린 = 식용유 x1, 물 x1")
    st.header("☣️ 생존 물자 및 특수 화합물")
    st.info("푸른 결정 = 감기약 소모품 x1, Li x1, 물 x1")
    st.info("수제비누 = 식용유x2 수산화나트륨x1" "물x1")
    st.info("CL-20 (폭약) = 질산 x3, 황산 x2, C x6, H x6, N x12, O x12")
    st.info("불피우기 = 과망간산칼륨x1, 글리세린x1")
    st.info("살균 소독제 = 아염소산나트륨 x1, 물 x9")
    st.info("구리 코일 발전기 = Cu x10 Fe x5" "강력 자석 x2")
    st.info("정수된 물 = 과망간산칼륨 x1, 물 x10")
    st.info("재생 배터리 = Li x2, C x2" "폐배터리(리튬) x1, 황산 x1")
    st.info("보르도액 (농약) = 황산구리 x1, 생석회 x1, 물 x5")
    st.info("리신 = 피마자 씨앗 x1, 물 x1")
    st.info("써마이트 = Al x2, 산화철(녹) x3")
    st.info("페니실린 = 푸른 곰팡이 x1, 설탕 x1, 물 x1")
    st.info("암모니아 (NH3) = N x1, H x3, 산화철(촉매) x1")
    st.info("니트로글리세린 = 글리세린 x1, 질산 x3, 황산 x1")
    st.divider()
    st.error("⚠️ 경고: 락스를 산성 물질과 절대 섞지 마십시오.")
    st.warning("⚠️ 써마이트는 절대 '가열'하지 마십시오.")