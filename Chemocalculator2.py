import streamlit as st
import math

# 웹페이지 기본 설정
st.set_page_config(page_title="항암제 용량 계산기", layout="centered")

st.title("💊 Chemotherapy Dose Calculator")
st.caption("대장암 항암 레지멘(FOLFOX, FOLFIRI, mFOLFOX6, XELOX, Autofuser, Accufuser) 용량 및 감량 계산기")

# 1. 신체 계측 정보 및 용량 조절 비율 입력
st.subheader("1. 신체 정보 입력")
col1, col2, col3 = st.columns(3)

with col1:
    height = st.number_input("키 (cm)", min_value=100.0, max_value=220.0, value=165.0, step=0.1)
with col2:
    weight = st.number_input("체중 (kg)", min_value=30.0, max_value=150.0, value=60.0, step=0.1)
with col3:
    dose_scale_percent = st.selectbox(
        "투여 용량 비율 (%)",
        options=[100, 90, 85, 80, 75, 70, 50],
        index=0
    )

# 표적치료제 선택 옵션
targeted_agent = st.selectbox(
    "🎯 동시 투여 표적치료제 선택 (선택 사항)",
    options=[
        "선택 안 함",
        "Bevacizumab (아바스틴 / 5 mg/kg)",
        "Zaltrap (잘트랩 / 4 mg/kg)",
        "Cetuximab (얼비툭스 / 500 mg/m²)"
    ],
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

# 표적치료제 용량 계산 함수 (마크다운 빨간색 적용)
def get_targeted_text():
    if targeted_agent == "Bevacizumab (아바스틴 / 5 mg/kg)":
        beva_dose = round(weight * 5 * scale, 1)
        targeted_text = f"\n* :red[**Bevacizumab (5 mg/kg): {beva_dose} mg**]"

    elif targeted_agent == "Zaltrap (잘트랩 / 4 mg/kg)":
        zaltrap_dose = round(weight * 4 * scale, 1)
        targeted_text = f"\n* :red[**Zaltrap (4 mg/kg): {zaltrap_dose} mg**]"

    elif targeted_agent == "Cetuximab (얼비툭스 / 500 mg/m²)":
        cetux_dose = round(bsa * 500 * scale, 1)
        targeted_text = f"\n* :red[**Cetuximab (500 mg/m²): {cetux_dose} mg**]"

    else:
        targeted_text = ""
        
    return targeted_text

targeted_text = get_targeted_text()

st.markdown("---")

# 2. 항암 레지멘 선택 (6가지 탭)
st.subheader("2. 항암 레지멘 선택")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "FOLFOX", 
    "FOLFIRI", 
    "mFOLFOX6", 
    "XELOX", 
    "mFOLFOX6 (Autofuser 230 mL)",
    "mFOLFOX6 (Accufuser 115 mL)"
])

# ==========================================
# TAB 1: FOLFOX
# ==========================================
with tab1:
    st.markdown("### 🔹 표준 FOLFOX Regimen")
    oxali_folfox = round(bsa * 85 * scale, 1)
    leucovorin_folfox = round(bsa * 200 * scale, 1)
    fu_bolus_folfox = round(bsa * 400 * scale, 1)
    fu_ci_folfox = round(bsa * 600 * scale, 1)
    
    st.info(f"""**[표준 FOLFOX 처방 가이드] ({dose_scale_percent}% 적용)**
* **Oxaliplatin (85 mg/m²)**: **{oxali_folfox} mg**
* **Leucovorin (200 mg/m²)**: **{leucovorin_folfox} mg**
* **5-FU Bolus (400 mg/m²)**: **{fu_bolus_folfox} mg**
* **5-FU Continuous Infusion (600 mg/m²/day, 2days)**: **{fu_ci_folfox} mg / day**{targeted_text}""")

# ==========================================
# TAB 2: FOLFIRI
# ==========================================
with tab2:
    st.markdown("### 🔹 FOLFIRI Regimen")
    iri_dose = round(bsa * 180 * scale, 1)
    leucovorin_folfiri = round(bsa * 400 * scale, 1)
    fu_bolus_folfiri = round(bsa * 400 * scale, 1)
    fu_ci_folfiri = round(bsa * 2400 * scale, 1)
    
    st.info(f"""**[FOLFIRI 처방 가이드] ({dose_scale_percent}% 적용)**
* **Irinotecan (180 mg/m²)**: **{iri_dose} mg**
* **Leucovorin (400 mg/m²)**: **{leucovorin_folfiri} mg**
* **5-FU Bolus (400 mg/m²)**: **{fu_bolus_folfiri} mg**
* **5-FU Continuous Infusion (2400 mg/m², 46h)**: **{fu_ci_folfiri} mg**{targeted_text}""")

# ==========================================
# TAB 3: mFOLFOX6
# ==========================================
with tab3:
    st.markdown("### 🔹 mFOLFOX6 Regimen")
    oxali_mfolfox = round(bsa * 85 * scale, 1)
    leucovorin_mfolfox = round(bsa * 400 * scale, 1)
    fu_bolus_mfolfox = round(bsa * 400 * scale, 1)
    fu_ci_mfolfox = round(bsa * 2400 * scale, 1)
    
    st.info(f"""**[mFOLFOX6 처방 가이드] ({dose_scale_percent}% 적용)**
* **Oxaliplatin (85 mg/m²)**: **{oxali_mfolfox} mg**
* **Leucovorin (400 mg/m²)**: **{leucovorin_mfolfox} mg**
* **5-FU Bolus (400 mg/m²)**: **{fu_bolus_mfolfox} mg**
* **5-FU Continuous Infusion (2400 mg/m², 46h)**: **{fu_ci_mfolfox} mg**{targeted_text}""")

# ==========================================
# TAB 4: XELOX
# ==========================================
with tab4:
    st.markdown("### 🔹 XELOX Regimen")
    oxali_dose = round(bsa * 130 * scale, 1)
    
    # Capecitabine 계산
    cape_single_dose = round(bsa * 1000 * scale, 1) # 1회 계산 용량 (절삭 전)
    cape_daily_dose = cape_single_dose * 2          # 하루 계산 용량 (절삭 전)
    
    # 1회 복용량 기준 정제 개수 (절삭)
    pills_500_single = int(cape_single_dose // 500)
    rem_dose = cape_single_dose - (pills_500_single * 500)
    pills_150_single = int(rem_dose // 150)
    
    # 실제 복용 결정 용량 계산 (절삭 후)
    actual_single_dose = (pills_500_single * 500) + (pills_150_single * 150)
    actual_daily_dose = actual_single_dose * 2
    
    # 하루 총 알약 수
    pills_500_daily = pills_500_single * 2
    pills_150_daily = pills_150_single * 2
    
    # 처방 용법 표기 생성 (# 2 po)
    presc_500_str = f"{pills_500_daily} T # 2 po (1회 {pills_500_single}T씩)" if pills_500_daily > 0 else "미처방"
    presc_150_str = f"{pills_150_daily} T # 2 po (1회 {pills_150_single}T씩)" if pills_150_daily > 0 else "미처방"
    
    st.info(f"""**[XELOX 처방 가이드] ({dose_scale_percent}% 적용)**
* **Oxaliplatin (130 mg/m²)**: **{oxali_dose} mg**
* **Capecitabine (1000 mg/m² b.i.d.)**: **1일 총 {cape_daily_dose} mg** (1회 {actual_single_dose} mg){targeted_text}

---
**[Capecitabine (젤로다) 세부 용법 용량]**
* **1회 계산 용량 (1000 mg/m²)**: **{cape_single_dose} mg** (하루 목표: {cape_daily_dose} mg)
* **실제 처방 용량**: **1회 {actual_single_dose} mg** (1일 총 복용 용량: **{actual_daily_dose} mg**)
* **1회 복용량 (아침 / 저녁 동일)**: 
  - 500mg 정제: **{pills_500_single} 알**
  - 150mg 정제: **{pills_150_single} 알**
* **1일 총 처방 용법**: 
  - 500mg 정제: **{presc_500_str}**
  - 150mg 정제: **{presc_150_str}**""")

# ==========================================
# TAB 5: mFOLFOX6 (Autofuser 230 mL)
# ==========================================
with tab5:
    st.markdown("### 🔹 mFOLFOX6 (Autofuser 230 mL) Regimen")
    
    oxali_folfox_auto = round(bsa * 85 * scale, 1)
    leucovorin_folfox_auto = round(bsa * 400 * scale, 1)
    fu_bolus_folfox_auto = round(bsa * 400 * scale, 1)
    
    fu_total_mg = bsa * 2400 * scale
    fu_volume_ml = round(fu_total_mg / 50, 2)
    
    autofuser_capacity = 230.0
    ns_diluent_ml = round(autofuser_capacity - fu_volume_ml, 2)
    
    st.info(f"""**[mFOLFOX6 기본 처방] ({dose_scale_percent}% 적용)**
* **Oxaliplatin (85 mg/m²)**: **{oxali_folfox_auto} mg**
* **Leucovorin (400 mg/m²)**: **{leucovorin_folfox_auto} mg**
* **5-FU Bolus (400 mg/m²)**: **{fu_bolus_folfox_auto} mg**{targeted_text}

---
**[5-FU Continuous Infusion (Autofuser 230 mL 계산)]**
* **5-FU 총 처방량 (2400 mg/m²)**: **{fu_total_mg:.1f} mg**
* **5-FU 약물 부피 (50 mg/mL)**: **{fu_volume_ml} mL**
* **Autofuser 용량**: **{autofuser_capacity} mL**
* **생리식염수(NS) 희석 혼합량**: **{ns_diluent_ml} mL**""")

    if ns_diluent_ml < 0:
        st.error("⚠️ 5-FU 약물 용량이 Autofuser 용량(230mL)을 초과했습니다. 조제 용량을 확인해주세요.")

# ==========================================
# TAB 6: mFOLFOX6 (Accufuser 115 mL)
# ==========================================
with tab6:
    st.markdown("### 🔹 mFOLFOX6 (Accufuser 115 mL) Regimen")
    
    oxali_folfox_accu = round(bsa * 85 * scale, 1)
    leucovorin_folfox_accu = round(bsa * 400 * scale, 1)
    fu_bolus_folfox_accu = round(bsa * 400 * scale, 1)
    
    fu_total_mg = bsa * 2400 * scale
    fu_volume_ml = round(fu_total_mg / 50, 2)
    
    accufuser_capacity = 115.0
    ns_diluent_ml_accu = round(accufuser_capacity - fu_volume_ml, 2)
    
    st.info(f"""**[mFOLFOX6 기본 처방] ({dose_scale_percent}% 적용)**
* **Oxaliplatin (85 mg/m²)**: **{oxali_folfox_accu} mg**
* **Leucovorin (400 mg/m²)**: **{leucovorin_folfox_accu} mg**
* **5-FU Bolus (400 mg/m²)**: **{fu_bolus_folfox_accu} mg**{targeted_text}

---
**[5-FU Continuous Infusion (Accufuser 115 mL 계산)]**
* **5-FU 총 처방량 (2400 mg/m²)**: **{fu_total_mg:.1f} mg**
* **5-FU 약물 부피 (50 mg/mL)**: **{fu_volume_ml} mL**
* **Accufuser 용량**: **{accufuser_capacity} mL**
* **생리식염수(NS) 희석 혼합량**: **{ns_diluent_ml_accu} mL**""")

    if ns_diluent_ml_accu < 0:
        st.error("⚠️ 5-FU 약물 용량이 Accufuser 용량(115mL)을 초과했습니다. 조제 용량을 확인해주세요.")