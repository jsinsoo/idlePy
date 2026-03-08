import math
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# 1. 개별 문제 정보 클래스 (기존 로직 유지)
class Question:
    def __init__(self, question, choices, answer, example):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.example = example

    def check_answer(self, choice_text):
        return choice_text == self.answer

# 2. Tkinter GUI 및 퀴즈 로직 관리 클래스
class QuizApp:
    def __init__(self, root, questions_data, s_id, s_name):
        self.root = root
        self.root.title("전북과학고 파이썬 기초문법 학습")
        self.root.geometry("600x500")

        # 데이터 초기화
        self.questions = [Question(**q) for q in questions_data]
        self.current_q_idx = 0
        self.score = 0
        self.results_log = []
        self.student_id = s_id
        self.student_name = s_name
        self.start_time = datetime.now()

        # UI 요소 생성
        self.setup_ui()
        self.display_question()

    def setup_ui(self):
        """화면 레이아웃 설정"""
        self.lbl_info = tk.Label(self.root, text=f"학생: {self.student_id} {self.student_name}", fg="blue")
        self.lbl_info.pack(pady=5)

        self.lbl_question = tk.Label(self.root, text="", font=("Arial", 12, "bold"), wraplength=500, justify="left")
        self.lbl_question.pack(pady=20)

        # 보기 버튼들을 담을 리스트
        self.btn_choices = []
        for i in range(5):
            btn = tk.Button(self.root, text="", width=50, command=lambda i=i: self.process_answer(i))
            btn.pack(pady=5)
            self.btn_choices.append(btn)

        self.lbl_status = tk.Label(self.root, text="", fg="red")
        self.lbl_status.pack(pady=10)

    def display_question(self):
        """현재 인덱스의 문제를 화면에 표시"""
        if self.current_q_idx < len(self.questions):
            q = self.questions[self.current_q_idx]
            self.lbl_question.config(text=f"문제 {self.current_q_idx + 1}: {q.question}")
            
            # 보기 버튼 텍스트 업데이트
            for i, choice in enumerate(q.choices):
                self.btn_choices[i].config(text=choice, state="normal")
            
            # 보기가 5개보다 적을 경우 버튼 숨기기 처리
            for j in range(len(q.choices), 5):
                self.btn_choices[j].pack_forget()
        else:
            self.finish_quiz()

    def process_answer(self, idx):
        """정답 확인 및 다음 문제로 전환"""
        q = self.questions[self.current_q_idx]
        user_choice = q.choices[idx]
        is_correct = q.check_answer(user_choice)

        if is_correct:
            self.score += 1
            status = "O"
            messagebox.showinfo("정답", f"정답입니다! 🎉\n\n예시: {q.example}")
        else:
            status = "X"
            messagebox.showerror("오답", f"오답입니다.\n정답: {q.answer}\n\n예시: {q.example}")

        # 로그 기록
        self.results_log.append({
            "no": self.current_q_idx + 1,
            "q_text": q.question,
            "user_ans": user_choice,
            "correct_ans": q.answer,
            "status": status,
            "example": q.example
        })

        self.current_q_idx += 1
        self.display_question()

    def finish_quiz(self):
        """퀴즈 종료 및 성적표 저장"""
        self.save_detailed_report()
        accuracy = (self.score / len(self.questions)) * 100
        messagebox.showinfo("종료", f"퀴즈가 끝났습니다!\n최종 점수: {self.score}/{len(self.questions)} ({accuracy:.1f}점)\n성적표 파일이 생성되었습니다.")
        self.root.destroy()

    def save_detailed_report(self):
        """파일 저장 (기존 로직과 동일)"""
        time_str = self.start_time.strftime("%Y%m%d_%H%M%S")
        file_name = f"{self.student_id}_{self.student_name}_{time_str}.txt"
        accuracy = (self.score / len(self.questions)) * 100

        report = f"[ 파이썬 기초문법 GUI 퀴즈 성적표 ]\n"
        report += f"학번: {self.student_id} / 이름: {self.student_name}\n"
        report += f"점수: {self.score} / {len(self.questions)} ({accuracy:.1f}점)\n"
        report += "-"*50 + "\n"
        
        for res in self.results_log:
            report += f"\n문제 {res['no']}. {res['q_text']}\n - 결과: [{res['status']}]\n - 정답: {res['correct_ans']}\n - 설명: {res['example']}\n"
        
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(report)

# 3. 데이터 정의
questions_list = [
    {"question": "파이썬에서 두 숫자의 합을 구하는 연산자는 무엇인가요?", "choices": ["+", "-", "*", "/", "%"], "answer": "+", "example": "3 + 5 -> 8"},
    {"question": "문자열 'hello'의 길이를 반환하는 함수는?", "choices": ["len()", "size()", "count()", "length()"], "answer": "len()", "example": "len('hello') -> 5"},
    {"question": "리스트 [1, 3, 2, 8, 5]에서 최대값을 반환하는 함수는?", "choices": ["max()", "min()", "sum()", "sorted()"], "answer": "max()", "example": "max([1, 3, 2, 8, 5]) -> 8"},
    {"question": "숫자 7이 짝수인지 확인하는 코드는 무엇인가요?", "choices": ["7 % 2 == 0", "7 % 2 == 1", "7 // 2 == 0", "7 / 2 == 1"], "answer": "7 % 2 == 0", "example": "7 % 2 -> 1 (False)"},
    {"question": "리스트 [1, 2, 3, 4, 5]에서 짝수만 필터링하는 방법은?", "choices": ["[x for x in lst if x % 2 == 0]", "filter(lambda x: x % 2 == 0, lst)", "lst.remove(odd)", "lst.append(even)"], "answer": "[x for x in lst if x % 2 == 0]", "example": "[1, 2, 3, 4, 5] -> [2, 4]"},
    {"question": "'hello world'에서 단어 'hello'가 포함되어 있는지 확인하는 방법은?", "choices": ["'hello' in 'hello world'", "'hello'.contains('hello world')", "contains('hello', 'hello world')", "search('hello', 'hello world')"], "answer": "'hello' in 'hello world'", "example": "'hello' in 'hello world' -> True"},
    {"question": "문자열 'hello'를 뒤집는 코드는 무엇인가요?", "choices": ["s[::-1]", "reverse(s)", "s.reverse()", "reversed(s)"], "answer": "s[::-1]", "example": "'hello'[::-1] -> 'olleh'"},
    {"question": "리스트 [1, 2, 3, 4]의 합을 계산하는 함수는?", "choices": ["sum()", "add()", "reduce()", "total()"], "answer": "sum()", "example": "sum([1, 2, 3, 4]) -> 10"},
    {"question": "숫자 4의 팩토리얼을 계산하는 함수는?", "choices": ["math.factorial()", "factorial()", "math.factor()", "factor()"], "answer": "math.factorial()", "example": "math.factorial(4) -> 24"},
    {"question": "피보나치 수열의 n번째 항을 반환하는 코드는?", "choices": ["재귀 함수", "for 반복문", "while 반복문", "위의 모든 방법"], "answer": "위의 모든 방법", "example": "fibonacci(6) -> 8"}
]

# 4. 실행
if __name__ == "__main__":
    # 초기 정보 입력을 위한 간단한 콘솔 입력 (이것도 GUI로 만들 수 있지만 구조상 유지)
    print("--- 전북과학고 파이썬 학습 시스템 (GUI 모드) ---")
    s_id = input("학번: ").strip()
    s_name = input("이름: ").strip()

    if s_id and s_name:
        root = tk.Tk()
        app = QuizApp(root, questions_list, s_id, s_name)
        root.mainloop()
    else:
        print("입력 정보가 부족합니다.")
