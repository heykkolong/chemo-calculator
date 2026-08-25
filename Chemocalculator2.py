import streamlit as st
import math

# 웹페이지 기본 설정
st.set_page_config(page_title="항암제 용량 계산기", layout="centered")

st.title("💊 Chemotherapy Dose Calculator")
st.caption("XELOX 및 mFOLFOX6 (Autofuser) 처방 용량 자동 계산기")

# 1. 신체 계측 정보 입력
st.subheader("1. 신체 정보 입력")
col1, col2 = st.columns(2)

with col1:
    height = st.number_input("키 (cm)", min_value=100.0, max_value=220.0, value=165.0, step=0.1)
with col2:
    weight = st.number_input("체중 (kg)", min_value=30.0, max_value=150.0, value=60.0, step=0.1)

# Mosteller 공식 BSA 계산 (소수점 둘째자리 반올림)
bsa = round(math.sqrt((height * weight) / 3600), 2)
st.success(f"**계산된 체표면적 (BSA): {bsa} m²**")

st.markdown("---")

# 2. 항암 레지멘 선택 (탭 방식)
st.subheader("2. 항암 레지멘 선택")
tab1, tab2 = st.tabs(["XELOX 레지멘", "mFOLFOX6 (Autofuser) 레지멘"])

# ==========================================
# TAB 1: XELOX
# ==========================================
with tab1:
    st.markdown("### 🔹 XELOX Regimen")
    oxali_dose = round(bsa * 130, 1)
    cape_dose = round(bsa * 1000, 1)
    
    # Capecitabine 알약 조제 로직 (500mg, 150mg)
    # 아침/저녁 분복 기준 예시 계산
    pills_500 = int(cape_dose // 500)
    rem_dose = cape_dose % 500
    pills_150 = round(rem_dose / 150)
    
    st.info(f"""
    **[XELOX 처방 가이드]**
    * **Oxaliplatin (130 mg/m²)**: **{oxali_dose} mg**
    * **Capecitabine (1000 mg/m² b.i.d)**: **{cape_dose} mg** (1회 용량)
      - 500mg 정제: **{pills_500} 알**
      - 150mg 정제: **{pills_150} 알**
    """)

# ==========================================
# TAB 2: mFOLFOX6 (Autofuser)
# ==========================================
with tab2:
    st.markdown("### 🔹 mFOLFOX6 (Autofuser) Regimen")
    
    # 5-FU 2400 mg/m² (46시간 지속주입), 농도 50 mg/mL, Autofuser 230 mL 기준
    fu_total_mg = bsa * 2400
    fu_volume_ml = round(fu_total_mg / 50, 2)
    
    autofuser_capacity = 230.0
    ns_diluent_ml = round(autofuser_capacity - fu_volume_ml, 2)
    
    st.info(f"""
    **[mFOLFOX6 5-FU Continuous Infusion]**
    * **5-FU 총 처방량 (2400 mg/m²)**: **{fu_total_mg:.1f} mg**
    * **5-FU 약물 부피 (50 mg/mL)**: **{fu_volume_ml} mL**
    * **Autofuser 용량**: **{autofuser_capacity} mL**
    * **생리식염수(NS) 희석 혼합량**: **{ns_diluent_ml} mL**
    """)
    
    if ns_diluent_ml < 0:
        st.error("⚠️ 5-FU 약물 용량이 Autofuser 용량(230mL)을 초과했습니다. 조제 용량을 확인해주세요.")