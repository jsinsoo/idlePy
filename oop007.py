import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# 1. 문제 객체 클래스
class Question:
    def __init__(self, data):
        self.question = data["question"]
        self.choices = data["choices"]
        self.answer = data["answer"]
        self.example = data["example"]
        self.user_var = tk.StringVar() # 사용자의 선택을 저장할 변수

# 2. 메인 앱 클래스
class QuizApp:
    def __init__(self, root, questions_data):
        self.root = root
        self.root.title("전북과학고 파이썬 기초문법 학습 시스템")
        self.root.geometry("700x800")
        self.questions_data = questions_data
        
        # 로그인 정보 저장용
        self.student_id = ""
        self.student_name = ""
        
        # 첫 화면: 로그인 창 호출
        self.show_login_screen()

    def show_login_screen(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.login_frame, text="파이썬 기초문법 학습", font=("Arial", 18, "bold")).pack(pady=20)
        
        tk.Label(self.login_frame, text="학번:").pack()
        self.ent_id = tk.Entry(self.login_frame)
        self.ent_id.pack(pady=5)

        tk.Label(self.login_frame, text="이름:").pack()
        self.ent_name = tk.Entry(self.login_frame)
        self.ent_name.pack(pady=5)

        tk.Button(self.login_frame, text="학습 시작", command=self.start_quiz, width=20, bg="lightblue").pack(pady=20)

    def start_quiz(self):
        self.student_id = self.ent_id.get().strip()
        self.student_name = self.ent_name.get().strip()

        if not self.student_id or not self.student_name:
            messagebox.showwarning("알림", "학번과 이름을 입력해주세요.")
            return

        self.login_frame.destroy()
        self.setup_quiz_screen()

    def setup_quiz_screen(self):
        # 상단 정보 레이블
        info_text = f"학생: {self.student_id} {self.student_name} | 응시일: {datetime.now().strftime('%Y-%m-%d')}"
        tk.Label(self.root, text=info_text, fg="gray").pack(pady=10)

        # 스크롤 가능한 영역 생성
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=20)
        self.scrollbar.pack(side="right", fill="y")

        # 문제 나열
        self.quiz_objs = [Question(q) for q in self.questions_data]
        self.feedback_labels = [] # 피드백 레이블 저장 리스트

        for i, q_obj in enumerate(self.quiz_objs, 1):
            q_frame = tk.Frame(self.scrollable_frame, pady=15)
            q_frame.pack(fill="x")

            tk.Label(q_frame, text=f"Q{i}. {q_obj.question}", font=("Arial", 11, "bold"), wraplength=600, justify="left").pack(anchor="w")
            
            # 보기 라디오 버튼
            for choice in q_obj.choices:
                tk.Radiobutton(q_frame, text=choice, variable=q_obj.user_var, value=choice).pack(anchor="w", padx=20)

            # 피드백 레이블 (초기에는 숨김)
            fb_lbl = tk.Label(q_frame, text="", justify="left", wraplength=550, fg="blue", font=("Arial", 10, "italic"))
            fb_lbl.pack(anchor="w", padx=20, pady=5)
            self.feedback_labels.append(fb_lbl)

        # 제출 버튼
        self.btn_submit = tk.Button(self.root, text="최종 제출 및 성적 확인", command=self.submit_quiz, bg="green", fg="white", font=("Arial", 12, "bold"), pady=10)
        self.btn_submit.pack(fill="x", padx=20, pady=10)

    def submit_quiz(self):
        if not messagebox.askyesno("확인", "모든 문제를 풀었습니까? 제출 후에는 수정할 수 없습니다."):
            return

        score = 0
        report_log = []
        
        for i, (q_obj, fb_lbl) in enumerate(zip(self.quiz_objs, self.feedback_labels), 1):
            user_ans = q_obj.user_var.get()
            is_correct = (user_ans == q_obj.answer)
            
            if is_correct:
                score += 1
                result_text = "✅ 정답입니다!"
                fb_lbl.config(text=f"{result_text}\n설명: {q_obj.example}", fg="green")
            else:
                result_text = f"❌ 오답 (정답: {q_obj.answer})"
                fb_lbl.config(text=f"{result_text}\n설명: {q_obj.example}", fg="red")
            
            report_log.append(f"문제 {i}: {result_text}")

        # 점수 계산 및 파일 저장
        accuracy = (score / len(self.quiz_objs)) * 100
        self.save_report(score, accuracy)
        
        # 버튼 비활성화 및 결과 알림
        self.btn_submit.config(state="disabled", text=f"제출 완료 - 점수: {score}/{len(self.quiz_objs)} ({accuracy:.1f}점)")
        messagebox.showinfo("완료", f"학습이 완료되었습니다!\n점수: {score}/{len(self.quiz_objs)}\n화면에서 상세 해설을 확인하세요.")

    def save_report(self, score, accuracy):
        # 1. 파일명 생성 (학번_이름_응시시각)
        time_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.student_id}_{self.student_name}_{time_str}.txt"
        
        # 2. 파일 내용 작성
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"[ 전북과학고 파이썬 기초문법 학습 결과 보고서 ]\n")
            f.write(f"--------------------------------------------------\n")
            f.write(f"학번: {self.student_id}\n")
            f.write(f"이름: {self.student_name}\n")
            f.write(f"응시 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"최종 점수: {score} / {len(self.quiz_objs)} ({accuracy:.1f}점)\n")
            f.write(f"--------------------------------------------------\n\n")
            f.write(f"[ 문항별 상세 기록 ]\n")
            
            # 각 문제별 결과 순회하며 기록
            for i, q_obj in enumerate(self.quiz_objs, 1):
                user_ans = q_obj.user_var.get()
                is_correct = "O" if user_ans == q_obj.answer else "X"
                
                f.write(f"문제 {i}. {q_obj.question}\n")
                f.write(f"   - 결과: [{is_correct}]\n")
                f.write(f"   - 선택한 답: {user_ans if user_ans else '미선택'}\n")
                f.write(f"   - 실제 정답: {q_obj.answer}\n")
                f.write(f"   - 상세 설명: {q_obj.example}\n")
                f.write(f"--------------------------------------------------\n")
            
            f.write(f"\n수고하셨습니다. 파이썬 마스터가 되는 그날까지! 🐍\n")
            
        print(f"상세 성적표 저장 완료: {filename}")


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

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root, questions_list)
    root.mainloop()
