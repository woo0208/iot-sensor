import json
from pathlib import Path

def load_json(p: Path) -> dict | None:
    if not p.exists():
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    base_p = Path("metrics_baseline.json")
    lstm_p = Path("metrics_lstm.json")
    
    base = load_json(base_p)
    lstm = load_json(lstm_p)
    
    if not base or not lstm:
        print("[오류] 비교할 지표 파일이 존재하지 않습니다.")
        print(f"  파일 확인 -> baseline 존재여부: {base_p.exists()}, lstm 존재여부: {lstm_p.exists()}")
        print("  15절과 16절이 정상적으로 실행되어 json 파일들이 생성되었는지 확인하세요.")
        return

    print("=" * 60)
    print(f" {'평가 지표 (Metric)':<18} | {'비교군 (Baseline)':<18} | {'실험군 (LSTM)':<18}")
    print("-" * 60)
    print(f" {'test MAE (오차)':<18} | {base['mae_kw']:<18.4f} | {lstm['mae_kw']:<18.4f}")
    print(f" {'test RMSE (오차)':<18} | {base['rmse_kw']:<18.4f} | {lstm['rmse_kw']:<18.4f}")
    print(f" {'test R² (결정계수)':<18} | {base['r2']:<18.4f} | {lstm['r2']:<18.4f}")
    print("=" * 60)

    # 두 모델의 성능 판정 및 해석
    print("\n[🤖 모델 성능 비교 분석 결과]")
    if lstm['r2'] > base['r2']:
        diff = lstm['r2'] - base['r2']
        print(f"-> 시퀀스(35시간 흐름)를 학습한 딥러닝 LSTM 모델이 정확도(R²)면에서 {diff:.4f}만큼 더 우세합니다.")
        print("   즉, 과거의 기상 변화 패턴을 누적해서 보는 것이 미래 예측에 더 효과적임이 증명되었습니다.")
    else:
        diff = base['r2'] - lstm['r2']
        print(f"-> 현재 데이터셋에서는 직전 시각의 값만 본 베이스라인 모델이 {diff:.4f}만큼 소폭 우세하거나 동등합니다.")
        print("   데이터의 패턴이 단순하거나 학습 Epoch(반복수)가 더 필요할 수 있습니다.")
    print("=" * 60)

if __name__ == "__main__":
    main()
