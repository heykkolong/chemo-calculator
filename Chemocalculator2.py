import streamlit as st
import math

st.set_page_config(page_title="항암 용량 계산기", layout="centered")

st.title("💊 항암제 용량 계산기")

# 신장, 체중 입력
col1, col2 = st.columns(2)
with col1:
    height = st.number_input("키 (cm)", value=165.0, step=0.5)
with col2:
    weight = st.number_input("몸무게 (kg)", value=60.0, step=0.5)

# 요법 및 감량률 선택
regimen = st.selectbox("항암 요법 선택", ["FOLFOX", "mFOLFOX6", "FOLFIRI", "XELOX (CAPOX)"])
reduction = st.slider("투여 비율 (%)", min_value=50, max_value=100, value=100, step=5)

# BSA 및 용량 계산
bsa = math.sqrt((height * weight) / 3600)
factor = reduction / 100.0

st.divider()
st.subheader(f"📊 BSA: {bsa:.2f} m² (투여 비율: {reduction}%)")

# 요법별 계산 로직
if regimen == "FOLFOX":
    st.write(f"• **Oxaliplatin**: {bsa * 85 * factor:.1f} mg")
    st.write(f"• **Leucovorin**: {bsa * 200 * factor:.1f} mg")
    st.write(f"• **5-FU Bolus**: {bsa * 400 * factor:.1f} mg")
    st.write(f"• **5-FU Infusion**: {bsa * 600 * factor:.1f} mg")

elif regimen == "mFOLFOX6":
    st.write(f"• **Oxaliplatin**: {bsa * 85 * factor:.1f} mg")
    st.write(f"• **Leucovorin**: {bsa * 400 * factor:.1f} mg")
    st.write(f"• **5-FU Bolus**: {bsa * 400 * factor:.1f} mg")
    st.write(f"• **5-FU Infusion**: {bsa * 2400 * factor:.1f} mg")

elif regimen == "FOLFIRI":
    st.write(f"• **Irinotecan**: {bsa * 180 * factor:.1f} mg")
    st.write(f"• **Leucovorin**: {bsa * 200 * factor:.1f} mg")
    st.write(f"• **5-FU Bolus**: {bsa * 400 * factor:.1f} mg")
    st.write(f"• **5-FU Infusion**: {bsa * 600 * factor:.1f} mg")

elif regimen == "XELOX (CAPOX)":
    # 1. Oxaliplatin 계산
    oxali_dose = bsa * 130 * factor
    
    # 2. Capecitabine 계산
    cape_daily = bsa * 2000 * factor  # 하루 총 용량
    single_dose = cape_daily / 2       # 1회 복용량
    
    # 알약 개수 계산 (500mg 우선, 남은 용량 150mg 배분)
    tabs_500_single = int(single_dose // 500)
    rem_after_500 = single_dose % 500
    tabs_150_single = int(rem_after_500 // 150)
    rem_final = rem_after_500 % 150
    
    tabs_500_daily = tabs_500_single * 2
    tabs_150_daily = tabs_150_single * 2

    # --- UI 화면 구성 (동일한 상자 & 글자 크기 통일) ---
    
    # 💉 주사제 (Oxaliplatin)
    st.subheader("💉 Oxaliplatin (주사제)")
    st.info(f"**투여 용량**: **{oxali_dose:.1f} mg**")
    
    st.divider()
    
    # 💊 경구제 (Capecitabine)
    st.subheader("💊 Capecitabine / 젤로다 (경구제)")
    st.info(
        f"**하루 총 복용량**: **{cape_daily:.1f} mg** (1일 2회)\n\n"
        f"**1회 복용량 (아침/저녁)**: **{single_dose:.1f} mg**"
    )
    
    # 알약 처방 수량 요약
    st.info(
        f"**[ 정제 처방 수량 ]**\n\n"
        f"**1회 복용 (아침 / 저녁 각각)** • **500mg 정**: **{tabs_500_single} 정** • **150mg 정**: **{tabs_150_single} 정**\n\n"
        f"---\n\n"
        f"**1일 총 복용 (하루 전체 합산)** • **500mg 정**: **총 {tabs_500_daily} 정** • **150mg 정**: **총 {tabs_150_daily} 정**"
    )
    
    st.caption(f"*(1회 실제 처방 용량: {tabs_500_single*500 + tabs_150_single*150} mg / 잔여 오차: {rem_final:.1f} mg)*")