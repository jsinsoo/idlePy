import tkinter as tk  # 기본 그래픽 사용자 인터페이스(GUI) 제작 도구
from tkinter import messagebox, ttk  # 알림창(messagebox)과 개선된 위젯(ttk) 가져오기
from datetime import datetime  # 현재 날짜와 시각을 다루는 도구
import os  # 운영체제(파일 저장 등) 기능을 사용하기 위한 도구

# [환경 체크] 구글 코랩(Cloud) 환경인지 개인 PC(Local) 환경인지 확인합니다.
try:
    from google.colab import files  # 코랩 전용 파일 다운로드 도구 가져오기 시도
    IN_COLAB = True  # 성공하면 코랩 환경
except ImportError:
    IN_COLAB = False  # 실패하면 개인 PC 환경

# 1. 문제 객체 클래스 (붕어빵 틀)
# 문제 하나하나가 가져야 할 정보(질문, 보기, 정답, 해설)를 묶어줍니다.
class Question:
    def __init__(self, data):
        self.question = data["question"]  # 질문 문구 저장
        self.choices = data["choices"]    # 5지 선다 보기 리스트 저장
        self.answer = data["answer"]      # 정답 저장
        self.example = data["example"]    # 해설(설명) 저장
        self.user_var = tk.StringVar()    # 학생이 선택한 답을 실시간으로 저장할 변수

# 2. 메인 앱 클래스 (프로그램 전체 관리자)
class QuizApp:
    def __init__(self, root, questions_data):
        self.root = root  # 메인 창 객체 저장
        self.root.title("전북과학고 파이썬 기초문법 학습 시스템")  # 창 제목 설정
        self.root.geometry("800x900")  # 창 크기 설정 (가로 800 x 세로 900)
        self.questions_data = questions_data  # 원본 문제 데이터 보관
        
        self.student_id = ""    # 학번 저장용 변수 초기화
        self.student_name = ""  # 이름 저장용 변수 초기화
        self.colors = ["#F0F4FF", "#FFFFFF"]  # 문제별 배경색 (연한 파랑과 하양 교대)
        
        self.show_login_screen()  # 시작하자마자 로그인 화면을 보여줌

    # [로그인 화면] 학번과 이름을 입력받는 화면을 그립니다.
    def show_login_screen(self):
        self.login_frame = tk.Frame(self.root)  # 로그인용 상자(프레임) 만들기
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")  # 화면 정중앙에 배치

        # 큰 제목 라벨
        tk.Label(self.login_frame, text="🐍 파이썬 기초문법 학습", font=("Malgun Gothic", 22, "bold")).pack(pady=30)
        
        # 학번 입력란
        tk.Label(self.login_frame, text="학번", font=("Malgun Gothic", 12)).pack()
        self.ent_id = tk.Entry(self.login_frame, font=("Arial", 14), justify="center")
        self.ent_id.pack(pady=10)

        # 이름 입력란
        tk.Label(self.login_frame, text="이름", font=("Malgun Gothic", 12)).pack()
        self.ent_name = tk.Entry(self.login_frame, font=("Arial", 14), justify="center")
        self.ent_name.pack(pady=10)

        # 학습 시작 버튼
        btn_start = tk.Button(self.login_frame, text="학습 시작하기", command=self.start_quiz, 
                              width=20, bg="#4A90E2", fg="white", font=("Malgun Gothic", 13, "bold"),
                              relief="flat", cursor="hand2")
        btn_start.pack(pady=30)

    # [로그인 처리] 입력값을 확인하고 퀴즈 화면으로 전환합니다.
    def start_quiz(self):
        self.student_id = self.ent_id.get().strip()    # 입력된 학번 가져오기 (공백 제거)
        self.student_name = self.ent_name.get().strip()  # 입력된 이름 가져오기 (공백 제거)

        if not self.student_id or not self.student_name:  # 비어있으면 경고
            messagebox.showwarning("알림", "학번과 이름을 입력해주세요.")
            return

        self.login_frame.destroy()  # 로그인 상자 지우기
        self.setup_quiz_screen()    # 퀴즈 화면 구성 시작

    # [퀴즈 화면] 스크롤 기능이 포함된 퀴즈 화면을 만듭니다.
    def setup_quiz_screen(self):
        # 상단 정보 표시줄 (검정 배경)
        header = tk.Frame(self.root, bg="#333333", pady=10)
        header.pack(fill="x")
        info_text = f"Student: {self.student_id} {self.student_name} | Date: {datetime.now().strftime('%Y-%m-%d')}"
        tk.Label(header, text=info_text, fg="white", bg="#333333", font=("Arial", 11)).pack()

        # [중요] 스크롤 가능한 영역(Canvas) 설정
        self.canvas = tk.Canvas(self.root, highlightthickness=0)  # 그림 그리는 캔버스 생성
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)  # 세로 스크롤바
        self.scrollable_frame = tk.Frame(self.canvas)  # 실제로 문제가 배치될 도화지(프레임)

        # 도화지의 크기가 변하면 스크롤 범위가 자동으로 조절되도록 설정
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # 캔버스 안에 도화지를 고정시킴
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=780)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # 마우스 휠을 굴렸을 때 스크롤이 작동하도록 연결
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)  # 왼쪽에 캔버스 배치
        self.scrollbar.pack(side="right", fill="y")  # 오른쪽에 스크롤바 배치

        # 문제 데이터를 클래스 객체 리스트로 변환하여 생성
        self.quiz_objs = [Question(q) for q in self.questions_data]
        self.feedback_labels = []  # 정답/오답 결과 문구를 표시할 라벨들을 모아둘 곳

        # 반복문을 돌며 문제를 하나씩 화면에 그리기
        for i, q_obj in enumerate(self.quiz_objs, 1):
            bg_color = self.colors[i % 2]  # 배경색 결정 (교대)
            q_frame = tk.Frame(self.scrollable_frame, pady=25, padx=30, bg=bg_color)
            q_frame.pack(fill="x")

            # 문제 질문 출력
            tk.Label(q_frame, text=f"Q{i}. {q_obj.question}", 
                     font=("Malgun Gothic", 14, "bold"), bg=bg_color, 
                     wraplength=700, justify="left").pack(anchor="w", pady=(0, 10))
            
            # 5개 선택지(Radiobutton) 출력
            for choice in q_obj.choices:
                rb = tk.Radiobutton(q_frame, text=choice, variable=q_obj.user_var, 
                                    value=choice, bg=bg_color, font=("Malgun Gothic", 12),
                                    activebackground=bg_color, cursor="hand2")
                rb.pack(anchor="w", padx=20, pady=2)

            # 제출 후 "정답입니다/오답입니다" 해설이 나타날 빈 공간(라벨)
            fb_lbl = tk.Label(q_frame, text="", justify="left", wraplength=700, 
                              bg=bg_color, font=("Malgun Gothic", 11, "italic"), fg="#555555")
            fb_lbl.pack(anchor="w", padx=20, pady=10)
            self.feedback_labels.append(fb_lbl)

        # 맨 하단 제출 버튼 영역
        footer = tk.Frame(self.root, pady=20)
        footer.pack(fill="x")
        self.btn_submit = tk.Button(footer, text="📝 최종 제출 및 성적 확인", command=self.submit_quiz, 
                                    bg="#28A745", fg="white", font=("Malgun Gothic", 15, "bold"), 
                                    padx=50, pady=10, relief="flat", cursor="hand2")
        self.btn_submit.pack()

    # 마우스 휠 이벤트 처리 함수
    def _on_mousewheel(self, event):
        if event.num == 4: self.canvas.yview_scroll(-1, "units")
        elif event.num == 5: self.canvas.yview_scroll(1, "units")
        else: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # [채점 및 제출] 답을 맞추고 파일로 저장합니다.
    def submit_quiz(self):
        if not messagebox.askyesno("확인", "모든 문제를 풀었습니까? 제출 후에는 수정할 수 없습니다."):
            return

        score = 0  # 맞은 개수
        for i, (q_obj, fb_lbl) in enumerate(zip(self.quiz_objs, self.feedback_labels), 1):
            user_ans = q_obj.user_var.get()  # 학생이 선택한 답 가져오기
            is_correct = (user_ans == q_obj.answer)  # 실제 정답과 비교
            
            if is_correct:
                score += 1
                fb_lbl.config(text=f"✅ 정답입니다!\n💡 설명: {q_obj.example}", fg="#28A745")
            else:
                fb_lbl.config(text=f"❌ 오답 (정답: {q_obj.answer})\n💡 설명: {q_obj.example}", fg="#D73A49")
            
        accuracy = (score / len(self.quiz_objs)) * 100  # 정답률 계산
        
        # 성적표 파일 생성 및 다운로드 실행 함수 호출
        self.save_report_and_download(score, accuracy)
        
        # 제출 버튼 비활성화 (중복 제출 방지)
        self.btn_submit.config(state="disabled", text=f"학습 완료! ({score}/{len(self.quiz_objs)})", bg="#6C757D")
        messagebox.showinfo("완료", "학습이 완료되었습니다!\n성적표가 자동으로 다운로드됩니다. (다운로드 폴더 확인)")

    # [파일 저장] 결과 보고서를 텍스트 파일로 만듭니다.
    def save_report_and_download(self, score, accuracy):
        time_str = datetime.now().strftime('%Y%m%d_%H%M%S')  # 현재 시각 문자열
        filename = f"{self.student_id}_{self.student_name}_{time_str}.txt"  # 파일명 조합
        
        # 1. 파일 쓰기(Write) 모드로 열어서 내용 작성
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

        # 2. 코랩 환경이라면 웹 브라우저 다운로드 기능을 실행
        if IN_COLAB:
            files.download(filename)
        else:
            # 로컬 PC라면 파일이 저장된 절대 경로를 터미널에 출력
            print(f"로컬 저장 완료: {os.path.abspath(filename)}")

# ---------------------------------------------------------
# [데이터] 실제 퀴즈 문제들이 담긴 리스트입니다.
# ---------------------------------------------------------
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

# 프로그램의 시작점
if __name__ == "__main__":
    root = tk.Tk()  # 메인 윈도우 창 생성
    
    # [창 화면 중앙 배치 로직]
    window_width = 800
    window_height = 900
    screen_width = root.winfo_screenwidth()  # 사용자의 모니터 가로 해상도
    screen_height = root.winfo_screenheight() # 사용자의 모니터 세로 해상도
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}') # 계산된 위치로 창 이동
    
    app = QuizApp(root, questions_list)  # 앱 객체 생성 및 실행
    root.mainloop()  # 창이 닫힐 때까지 프로그램 유지 (이벤트 루프)
