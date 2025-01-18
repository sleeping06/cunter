import tkinter as tk
from datetime import datetime
import json
import os

# 메인 애플리케이션 클래스
class NumberApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("숫자 증감기")
        self.geometry("300x300")

        # UI 컴포넌트 초기화
        self.count = 0
        self.timestamps = []

        # 숫자를 표시하는 레이블
        self.label = tk.Label(self, text=str(self.count), font=("Arial", 24))
        self.label.pack(pady=20)

        # 증가 버튼
        self.increment_button = tk.Button(self, text="증가", command=self.increment)
        self.increment_button.pack(pady=5)

        # 감소 버튼
        self.decrement_button = tk.Button(self, text="감소", command=self.decrement)
        self.decrement_button.pack(pady=5)

        # 상세 내역을 표시할 텍스트 위젯
        self.details_text = tk.Text(self, height=10, width=30, state='disabled')
        self.details_text.pack(pady=10)

        # 데이터 로드
        self.load_data()

    # 증가 버튼 클릭 시 호출되는 메서드
    def increment(self):
        self.count += 1
        self.label.config(text=str(self.count))
        self.timestamps.append(datetime.now())
        self.update_details()
        self.save_data()  # 데이터 저장

    # 감소 버튼 클릭 시 호출되는 메서드
    def decrement(self):
        if self.count > 0:
            self.count -= 1
            self.label.config(text=str(self.count))
            if self.timestamps:
                self.timestamps.pop()  # 가장 최근 타임스탬프 삭제
            self.update_details()
            self.save_data()  # 데이터 저장

    # 상세 내역 업데이트
    def update_details(self):
        self.details_text.config(state='normal')
        self.details_text.delete(1.0, tk.END)  # 기존 내용 삭제
        if self.timestamps:
            # 내림차순으로 정렬
            sorted_timestamps = sorted(self.timestamps, reverse=True)
            details = "\n".join(ts.strftime("%Y-%m-%d %H:%M:%S") for ts in sorted_timestamps)
            self.details_text.insert(tk.END, details)
        else:
            self.details_text.insert(tk.END, "아직 증가 기록이 없습니다!")
        self.details_text.config(state='disabled')

    # 데이터 저장
    def save_data(self):
        data = {
            'count': self.count,
            'timestamps': [ts.isoformat() for ts in self.timestamps]
        }
        with open('data.json', 'w') as f:
            json.dump(data, f)

    # 데이터 로드
    def load_data(self):
        if os.path.exists('data.json'):
            with open('data.json', 'r') as f:
                data = json.load(f)
                self.count = data.get('count', 0)
                self.timestamps = [datetime.fromisoformat(ts) for ts in data.get('timestamps', [])]
            self.label.config(text=str(self.count))  # 카운트 업데이트
            self.update_details()  # UI 업데이트

# 애플리케이션 실행
if __name__ == "__main__":
    app = NumberApp()
    app.mainloop()
