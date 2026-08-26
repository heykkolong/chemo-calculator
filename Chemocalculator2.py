import streamlit as st
import math

# 웹페이지 기본 설정
st.set_page_config(page_title="항암제 용량 계산기", layout="centered")

st.title("💊 Chemotherapy Dose Calculator")
st.caption("대장암 항암 레지멘(FOLFOX, FOLFIRI, mFOLFOX6, XELOX, Autofuser) 용량 및 감량 계산기")

# 1. 신체 계측 정보 및 용량 조절 비율 입력
st.subheader("1. 신체 정보 입력")
col1, col2, col3 = st.columns(3)

with col1:
    height = st.number_input("키 (cm)", min_value=100.0, max_value=220.0, value=165.0, step=0.1)
with col2:
    weight = st.number_input("체중 (kg)", min_value=30.0, max_value=150.0, value=60.0, step=0.1)
with col3:
    # 용량 조절 옵션 선택 (기본값 100%)
    dose_scale_percent = st.selectbox(
        "투여 용량 비율 (%)",
        options=[100, 95, 90, 85, 80, 75, 70, 65, 60],
        index=0
    )

# 용량 비율 계수 (예: 80% -> 0.8)
scale = dose_scale_percent / 100.0

# Mosteller 공식 BSA 계산 (소수점 둘째자리 반올림)
bsa = round(math.sqrt((height * weight) / 3600), 2)

col_res1, col_res2 = st.columns(2)
with col_res1:
    st.success(f"**체표면적 (BSA): {bsa} m²**")
with col_res2:
    if dose_scale_percent == 100:
        st.info(f"**적용 용량: {dose_scale_percent}% (표준 용량)**")
    else:
        st.warning(f"**적용 용량: {dose_scale_percent}% (감량 투여)**")

st.markdown("---")

# 2. 항암 레지멘 선택 (5가지 탭)
st.subheader("2. 항암 레지멘 선택")
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "FOLFOX", 
    "FOLFIRI", 
    "mFOLFOX6", 
    "XELOX", 
    "mFOLFOX6 (Autofuser)"
])

# ==========================================
# TAB 1: FOLFOX
# ==========================================
with tab1:
    st.markdown("### 🔹 표준 FOLFOX Regimen")
    oxali_folfox = round(bsa * 85 * scale, 1)          # Oxaliplatin 85 mg/m²
    leucovorin_folfox = round(bsa * 200 * scale, 1)    # Leucovorin 200 mg/m²
    fu_bolus_folfox = round(bsa * 400 * scale, 1)      # 5-FU Bolus 400 mg/m²
    fu_ci_folfox = round(bsa * 600 * scale, 1)          # 5-FU CI 600 mg/m²
    
    st.info(f"""
    **[표준 FOLFOX 처방 가이드] ({dose_scale_percent}% 적용)**
    * **Oxaliplatin (85 mg/m²)**: **{oxali_folfox} mg**
    * **Leucovorin (200 mg/m²)**: **{leucovorin_folfox} mg**
    * **5-FU Bolus (400 mg/m²)**: **{fu_bolus_folfox} mg**
    * **5-FU Continuous Infusion (600 mg/m²/day, 2days)**: **{fu_ci_folfox} mg / day**
    """)

# ==========================================
# TAB 2: FOLFIRI
# ==========================================
with tab2:
    st.markdown("### 🔹 FOLFIRI Regimen")
    iri_dose = round(bsa * 180 * scale, 1)             # Irinotecan 180 mg/m²
    leucovorin_folfiri = round(bsa * 400 * scale, 1)   # Leucovorin 400 mg/m²
    fu_bolus_folfiri = round(bsa * 400 * scale, 1)     # 5-FU Bolus 400 mg/m²
    fu_ci_folfiri = round(bsa * 2400 * scale, 1)       # 5-FU CI 2400 mg/m²
    
    st.info(f"""
    **[FOLFIRI 처방 가이드] ({dose_scale_percent}% 적용)**
    * **Irinotecan (180 mg/m²)**: **{iri_dose} mg**
    * **Leucovorin (400 mg/m²)**: **{leucovorin_folfiri} mg**
    * **5-FU Bolus (400 mg/m²)**: **{fu_bolus_folfiri} mg**
    * **5-FU Continuous Infusion (2400 mg/m², 46h)**: **{fu_ci_folfiri} mg**
    """)

# ==========================================
# TAB 3: mFOLFOX6
# ==========================================
with tab3:
    st.markdown("### 🔹 mFOLFOX6 Regimen")
    oxali_mfolfox = round(bsa * 85 * scale, 1)         # Oxaliplatin 85 mg/m²
    leucovorin_mfolfox = round(bsa * 400 * scale, 1)   # Leucovorin 400 mg/m²
    fu_bolus_mfolfox = round(bsa * 400 * scale, 1)     # 5-FU Bolus 400 mg/m²
    fu_ci_mfolfox = round(bsa * 2400 * scale, 1)       # 5-FU CI 2400 mg/m²
    
    st.info(f"""
    **[mFOLFOX6 처방 가이드] ({dose_scale_percent}% 적용)**
    * **Oxaliplatin (85 mg/m²)**: **{oxali_mfolfox} mg**
    * **Leucovorin (400 mg/m²)**: **{leucovorin_mfolfox} mg**
    * **5-FU Bolus (400 mg/m²)**: **{fu_bolus_mfolfox} mg**
    * **5-FU Continuous Infusion (2400 mg/m², 46h)**: **{fu_ci_mfolfox} mg**
    """)

# ==========================================
# TAB 4: XELOX
# ==========================================
with tab4:
    st.markdown("### 🔹 XELOX Regimen")
    oxali_dose = round(bsa * 130 * scale, 1)
    
    # Capecitabine(젤로다) 계산 (감량 비율 적용)
    cape_single_dose = round(bsa * 1000 * scale, 1)
    cape_daily_dose = cape_single_dose * 2
    
    # 알약 수 계산
    pills_500_single = int(cape_single_dose // 500)
    rem_dose = cape_single_dose % 500
    pills_150_single = round(rem_dose / 150)
    
    pills_500_daily = pills_500_single * 2
    pills_150_daily = pills_150_single * 2
    
    st.info(f"""
    **[XELOX 처방 가이드] ({dose_scale_percent}% 적용)**
    * **Oxaliplatin (130 mg/m²)**: **{oxali_dose} mg**
    
    ---
    **[Capecitabine (젤로다) 용법 용량]**
    * **1회 용량 (1000 mg/m²)**: **{cape_single_dose} mg**
    * **하루 총 용량 (b.i.d.)**: **{cape_daily_dose} mg**
    * **1회 복용량 (아침 또는 저녁)**: 
      - 500mg 정제: **{pills_500_single} 알**
      - 150mg 정제: **{pills_150_single} 알**
    * **하루 총 복용 알약 수**: 
      - 500mg 정제: **총 {pills_500_daily} 알** (아침 {pills_500_single}알 / 저녁 {pills_500_single}알)
      - 150mg 정제: **총 {pills_150_daily} 알** (아침 {pills_150_single}알 / 저녁 {pills_150_single}알)
    """)

# ==========================================
# TAB 5: mFOLFOX6 (Autofuser)
# ==========================================
with tab5:
    st.markdown("### 🔹 mFOLFOX6 (Autofuser 230 mL) Regimen")
    
    oxali_folfox_auto = round(bsa * 85 * scale, 1)
    leucovorin_folfox_auto = round(bsa * 400 * scale, 1)
    fu_bolus_folfox_auto = round(bsa * 400 * scale, 1)
    
    # 5-FU 2400 mg/m² (감량 비율 적용)
    fu_total_mg = bsa * 2400 * scale
    fu_volume_ml = round(fu_total_mg / 50, 2)
    
    autofuser_capacity = 230.0
    ns_diluent_ml = round(autofuser_capacity - fu_volume_ml, 2)
    
    st.info(f"""
    **[mFOLFOX6 기본 처방] ({dose_scale_percent}% 적용)**
    * **Oxaliplatin (85 mg/m²)**: **{oxali_folfox_auto} mg**
    * **Leucovorin (400 mg/m²)**: **{leucovorin_folfox_auto} mg**
    * **5-FU Bolus (400 mg/m²)**: **{fu_bolus_folfox_auto} mg**
    
    ---
    **[5-FU Continuous Infusion (Autofuser 230 mL 계산)]**
    * **5-FU 총 처방량 (2400 mg/m²)**: **{fu_total_mg:.1f} mg**
    * **5-FU 약물 부피 (50 mg/mL)**: **{fu_volume_ml} mL**
    * **Autofuser 용량**: **{autofuser_capacity} mL**
    * **생리식염수(NS) 희석 혼합량**: **{ns_diluent_ml} mL**
    """)
    
    if ns_diluent_ml < 0:
        st.error("⚠️ 5-FU 약물 용량이 Autofuser 용량(230mL)을 초과했습니다. 조제 용량을 확인해주세요.")