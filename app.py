import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import ml_shared as ms
import json
from pathlib import Path

# 웹페이지 기본 설정
st.set_page_config(page_title="태양광 발전 관제 대시보드", layout="wide")

st.title("☀️ 태양광 발전 및 기상 모니터링 AI 대시보드")
st.markdown("MySQL 데이터베이스의 실시간 데이터와 AI 모델 성적을 시각화합니다.")

# 1. 데이터 불러오기
try:
    df = ms.load_joined()
    st.success(f"✅ 성공: 데이터베이스 연동 완료! (총 {len(df)}개의 시간별 데이터 로드)")
except Exception as e:
    st.error(f"❌ 데이터베이스 연결 실패: {e}")
    st.stop()

# 화면을 두 구역(좌/우)으로 분할
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 최근 기상 및 발전량 트렌드 (최근 100시간)")
    recent_df = df.tail(100)
    
    # Plotly 시각화 그래프 그리기
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=recent_df.index, y=recent_df['power_kw'], name='발전량 (power_kw)', line=dict(color='orange', width=3)))
    fig.add_trace(go.Scatter(x=recent_df.index, y=recent_df['temperature'], name='기온 (temp)', line=dict(color='royalblue', dash='dot')))
    fig.add_trace(go.Scatter(x=recent_df.index, y=recent_df['humidity'], name='습도 (humidity)', line=dict(color='mediumseagreen', dash='dot'), visible='legendonly'))
    
    fig.update_layout(
        template="plotly_dark",
        xaxis_title="시간 (Time)",
        yaxis_title="수치 (Value)",
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

# 아래쪽에 최근 원본 데이터 표 보여주기
st.subheader("📋 최근 수집된 데이터 명세 (상위 5개 행)")
st.dataframe(df.tail(5).sort_index(ascending=False))
