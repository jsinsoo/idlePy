import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import os

# [추가] 코랩 환경 확인 및 다운로드 라이브러리 임포트
try:
    from google.colab import files
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

# 1. 문제 객체 클래스
class Question:
    def __init__(self, data):
        self.question = data["question"]
        self.choices = data["choices"]
        self.answer = data["answer"]
        self.example = data["example"]
        self.user_var = tk.StringVar()

# 2. 메인 앱 클래스
class QuizApp:
    def __init__(self, root, questions_data):
        self.root = root
        self.root.title("전북과학고 파이썬 기초문법 학습 시스템")
        self.root.geometry("800x900")
        self.questions_data = questions_data
        
        self.student_id = ""
        self.student_name = ""
        self.colors = ["#F0F4FF", "#FFFFFF"] # 파스텔톤 배경색
        
        self.show_login_screen()

    def show_login_screen(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.login_frame, text="🐍 파이썬 기초문법 학습", font=("Malgun Gothic", 22, "bold")).pack(pady=30)
        
        tk.Label(self.login_frame, text="학번", font=("Malgun Gothic", 12)).pack()
        self.ent_id = tk.Entry(self.login_frame, font=("Arial", 14), justify="center")
        self.ent_id.pack(pady=10)

        tk.Label(self.login_frame, text="이름", font=("Malgun Gothic", 12)).pack()
        self.ent_name = tk.Entry(self.login_frame, font=("Arial", 14), justify="center")
        self.ent_name.pack(pady=10)

        btn_start = tk.Button(self.login_frame, text="학습 시작하기", command=self.start_quiz, 
                              width=20, bg="#4A90E2", fg="white", font=("Malgun Gothic", 13, "bold"),
                              relief="flat", cursor="hand2")
        btn_start.pack(pady=30)

    def start_quiz(self):
        self.student_id = self.ent_id.get().strip()
        self.student_name = self.ent_name.get().strip()

        if not self.student_id or not self.student_name:
            messagebox.showwarning("알림", "학번과 이름을 입력해주세요.")
            return

        self.login_frame.destroy()
        self.setup_quiz_screen()

    def setup_quiz_screen(self):
        header = tk.Frame(self.root, bg="#333333", pady=10)
        header.pack(fill="x")
        info_text = f"Student: {self.student_id} {self.student_name} | Date: {datetime.now().strftime('%Y-%m-%d')}"
        tk.Label(header, text=info_text, fg="white", bg="#333333", font=("Arial", 11)).pack()

        # 스크롤 캔버스 설정
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=780)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # 마우스 휠 바인딩
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.quiz_objs = [Question(q) for q in self.questions_data]
        self.feedback_labels = []

        for i, q_obj in enumerate(self.quiz_objs, 1):
            bg_color = self.colors[i % 2]
            q_frame = tk.Frame(self.scrollable_frame, pady=25, padx=30, bg=bg_color)
            q_frame.pack(fill="x")

            tk.Label(q_frame, text=f"Q{i}. {q_obj.question}", 
                     font=("Malgun Gothic", 14, "bold"), bg=bg_color, 
                     wraplength=700, justify="left").pack(anchor="w", pady=(0, 10))
            
            for choice in q_obj.choices:
                rb = tk.Radiobutton(q_frame, text=choice, variable=q_obj.user_var, 
                                    value=choice, bg=bg_color, font=("Malgun Gothic", 12),
                                    activebackground=bg_color, cursor="hand2")
                rb.pack(anchor="w", padx=20, pady=2)

            fb_lbl = tk.Label(q_frame, text="", justify="left", wraplength=700, 
                              bg=bg_color, font=("Malgun Gothic", 11, "italic"), fg="#555555")
            fb_lbl.pack(anchor="w", padx=20, pady=10)
            self.feedback_labels.append(fb_lbl)

        footer = tk.Frame(self.root, pady=20)
        footer.pack(fill="x")
        self.btn_submit = tk.Button(footer, text="📝 최종 제출 및 성적 확인", command=self.submit_quiz, 
                                    bg="#28A745", fg="white", font=("Malgun Gothic", 15, "bold"), 
                                    padx=50, pady=10, relief="flat", cursor="hand2")
        self.btn_submit.pack()

    def _on_mousewheel(self, event):
        if event.num == 4: self.canvas.yview_scroll(-1, "units")
        elif event.num == 5: self.canvas.yview_scroll(1, "units")
        else: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def submit_quiz(self):
        if not messagebox.askyesno("확인", "모든 문제를 풀었습니까? 제출 후에는 수정할 수 없습니다."):
            return

        score = 0
        for i, (q_obj, fb_lbl) in enumerate(zip(self.quiz_objs, self.feedback_labels), 1):
            user_ans = q_obj.user_var.get()
            is_correct = (user_ans == q_obj.answer)
            if is_correct:
                score += 1
                fb_lbl.config(text=f"✅ 정답입니다!\n💡 설명: {q_obj.example}", fg="#28A745")
            else:
                fb_lbl.config(text=f"❌ 오답 (정답: {q_obj.answer})\n💡 설명: {q_obj.example}", fg="#D73A49")
            
        accuracy = (score / len(self.quiz_objs)) * 100
        
        # 성적표 파일 생성 및 다운로드 실행
        self.save_report_and_download(score, accuracy)
        
        self.btn_submit.config(state="disabled", text=f"학습 완료! ({score}/{len(self.quiz_objs)})", bg="#6C757D")
        messagebox.showinfo("완료", "학습이 완료되었습니다!\n성적표가 자동으로 다운로드됩니다. (다운로드 폴더 확인)")

    # [핵심 함수] 파일 저장 후 브라우저 다운로드 실행
    def save_report_and_download(self, score, accuracy):
        time_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.student_id}_{self.student_name}_{time_str}.txt"
        
        # 1. 파일 작성
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"[ 전북과학고 파이썬 기초문법 학습 결과 보고서 ]\n")
            f.write(f"--------------------------------------------------\n")
            f.write(f"학번: {self.student_id} | 이름: {self.student_name}\n")
            f.write(f"최종 점수: {score} / {len(self.quiz_objs)} ({accuracy:.1f}점)\n")
            f.write(f"--------------------------------------------------\n\n")
            for i, q_obj in enumerate(self.quiz_objs, 1):
                user_ans = q_obj.user_var.get()
                is_correct = "O" if user_ans == q_obj.answer else "X"
                f.write(f"문제 {i}. {q_obj.question}\n")
                f.write(f"   - 결과: [{is_correct}] | 선택: {user_ans if user_ans else '미선택'}\n")
                f.write(f"   - 설명: {q_obj.example}\n")
                f.write(f"--------------------------------------------------\n")

        # 2. 코랩 브라우저 다운로드 트리거
        if IN_COLAB:
            files.download(filename)
        else:
            print(f"로컬 저장 완료: {os.path.abspath(filename)}")

# 데이터 리스트
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
    # 화면 중앙 배치
    window_width = 800
    window_height = 900
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    app = QuizApp(root, questions_list)
    root.mainloop()
