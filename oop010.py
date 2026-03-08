import tkinter as tk  # GUI(창)를 만들기 위한 표준 파이썬 라이브러리
from tkinter import messagebox, ttk  # 메시지 박스(알림)와 개선된 위젯(스크롤바 등) 임포트
from datetime import datetime  # 현재 날짜와 시간을 가져오기 위한 모듈

# 1. 문제 객체 클래스: 각 문제의 데이터(질문, 보기, 정답 등)를 하나의 묶음으로 관리
class Question:
    def __init__(self, data):
        self.question = data["question"]  # 딕셔너리에서 질문 텍스트 추출
        self.choices = data["choices"]    # 딕셔너리에서 보기 리스트 추출
        self.answer = data["answer"]      # 정답 텍스트 저장
        self.example = data["example"]    # 해설/예시 텍스트 저장
        # tk.StringVar()는 GUI 위젯(라디오버튼)과 연결되어 사용자가 선택한 값을 실시간으로 저장하는 특수 변수
        self.user_var = tk.StringVar()

# 2. 메인 앱 클래스: 전체 프로그램의 화면 구성과 동작(로직)을 담당
class QuizApp:
    def __init__(self, root, questions_data):
        self.root = root  # 메인 창 객체를 클래스 내부 변수로 저장
        self.root.title("전북과학고 파이썬 기초문법 학습 시스템")  # 창의 제목 표시줄 설정
        self.root.geometry("800x900")  # 창의 초기 가로, 세로 크기 설정
        self.questions_data = questions_data  # 퀴즈 데이터 리스트 저장
        
        self.student_id = ""    # 로그인 전 학번을 담을 빈 변수
        self.student_name = ""  # 로그인 전 이름을 담을 빈 변수
        
        # 옅은 파스텔 배경색 설정: i % 2를 이용해 문항별로 교차 적용하여 가독성을 높임
        self.colors = ["#F0F4FF", "#FFFFFF"] # [연한 파랑, 흰색]
        
        # 프로그램이 실행되자마자 로그인 화면을 그림
        self.show_login_screen()

    # [함수] 로그인 화면 구성: 학번과 이름을 입력받는 프레임
    def show_login_screen(self):
        self.login_frame = tk.Frame(self.root)  # 로그인 요소들을 담을 프레임(상자) 생성
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")  # 창 전체의 50% 지점(중앙)에 배치

        # 큰 제목 레이블 배치
        tk.Label(self.login_frame, text="🐍 파이썬 기초문법 학습", font=("Malgun Gothic", 22, "bold")).pack(pady=30)
        
        # 학번 입력란 설명과 입력창(Entry)
        tk.Label(self.login_frame, text="학번", font=("Malgun Gothic", 12)).pack()
        self.ent_id = tk.Entry(self.login_frame, font=("Arial", 14), justify="center")
        self.ent_id.pack(pady=10)

        # 이름 입력란 설명과 입력창(Entry)
        tk.Label(self.login_frame, text="이름", font=("Malgun Gothic", 12)).pack()
        self.ent_name = tk.Entry(self.login_frame, font=("Arial", 14), justify="center")
        self.ent_name.pack(pady=10)

        # 시작 버튼: 클릭 시 self.start_quiz 함수를 호출
        btn_start = tk.Button(self.login_frame, text="학습 시작하기", command=self.start_quiz, 
                              width=20, bg="#4A90E2", fg="white", font=("Malgun Gothic", 13, "bold"),
                              relief="flat", cursor="hand2")
        btn_start.pack(pady=30)

    # [함수] 시작 로직: 입력을 확인하고 퀴즈 화면으로 전환
    def start_quiz(self):
        self.student_id = self.ent_id.get().strip()  # 입력창의 텍스트를 가져와서 양끝 공백 제거
        self.student_name = self.ent_name.get().strip()

        # 입력값이 하나라도 비어있으면 경고창을 띄우고 함수 중단
        if not self.student_id or not self.student_name:
            messagebox.showwarning("알림", "학번과 이름을 입력해주세요.")
            return

        self.login_frame.destroy()  # 로그인 프레임(상자)을 화면에서 제거
        self.setup_quiz_screen()    # 본격적인 퀴즈 화면 설정 함수 호출

    # [함수] 퀴즈 화면 구성: 스크롤 영역과 문제들을 배치
    def setup_quiz_screen(self):
        # 상단 정보바 (검은색 배경에 흰색 글씨)
        header = tk.Frame(self.root, bg="#333333", pady=10)
        header.pack(fill="x")
        info_text = f"Student: {self.student_id} {self.student_name} | Date: {datetime.now().strftime('%Y-%m-%d')}"
        tk.Label(header, text=info_text, fg="white", bg="#333333", font=("Arial", 11)).pack()

        # [스크롤 시스템] 캔버스(도화지)와 스크롤바 생성
        self.canvas = tk.Canvas(self.root, highlightthickness=0)  # 그림을 그릴 캔버스
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)  # 세로 스크롤바
        self.scrollable_frame = tk.Frame(self.canvas)  # 캔버스 위에 올라갈 실제 문제 프레임

        # 프레임 내부 크기가 변하면 캔버스의 스크롤 가능 범위(scrollregion)를 자동 갱신
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # 캔버스 내부에 문제 프레임을 윈도우 형태로 삽입
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=780)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)  # 캔버스와 스크롤바 연결

        # 마우스 휠 이벤트 바인딩: 사용자가 휠을 돌릴 때 _on_mousewheel 함수 실행
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel) # 윈도우용
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)   # 리눅스 휠 업
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)   # 리눅스 휠 다운

        self.canvas.pack(side="left", fill="both", expand=True)  # 왼쪽 배치
        self.scrollbar.pack(side="right", fill="y")  # 오른쪽 배치

        # 문제 데이터를 바탕으로 Question 인스턴스(객체) 리스트 생성
        self.quiz_objs = [Question(q) for q in self.questions_data]
        self.feedback_labels = []  # 제출 후 정답 설명을 보여줄 레이블 보관함

        # 문제들을 화면에 하나씩 생성
        for i, q_obj in enumerate(self.quiz_objs, 1):
            bg_color = self.colors[i % 2]  # 인덱스 홀/짝에 따라 배경색 결정
            q_frame = tk.Frame(self.scrollable_frame, pady=25, padx=30, bg=bg_color)  # 문항 상자 생성
            q_frame.pack(fill="x")

            # 질문 텍스트 출력
            tk.Label(q_frame, text=f"Q{i}. {q_obj.question}", 
                     font=("Malgun Gothic", 14, "bold"), bg=bg_color, 
                     wraplength=700, justify="left").pack(anchor="w", pady=(0, 10))
            
            # 해당 문제의 보기들을 라디오버튼으로 출력
            for choice in q_obj.choices:
                # variable에 q_obj.user_var를 연결하여 같은 문제 내에선 하나만 선택되게 함
                rb = tk.Radiobutton(q_frame, text=choice, variable=q_obj.user_var, 
                                    value=choice, bg=bg_color, font=("Malgun Gothic", 12),
                                    activebackground=bg_color, cursor="hand2")
                rb.pack(anchor="w", padx=20, pady=2)

            # 제출 후 나타날 피드백(정오답/설명) 레이블 (초기엔 빈 텍스트)
            fb_lbl = tk.Label(q_frame, text="", justify="left", wraplength=700, 
                              bg=bg_color, font=("Malgun Gothic", 11, "italic"), fg="#555555")
            fb_lbl.pack(anchor="w", padx=20, pady=10)
            self.feedback_labels.append(fb_lbl)  # 나중에 접근하기 위해 리스트에 저장

        # 맨 아래 제출 버튼 영역
        footer = tk.Frame(self.root, pady=20)
        footer.pack(fill="x")
        self.btn_submit = tk.Button(footer, text="📝 최종 제출 및 성적 확인", command=self.submit_quiz, 
                                    bg="#28A745", fg="white", font=("Malgun Gothic", 15, "bold"), 
                                    padx=50, pady=10, relief="flat", cursor="hand2")
        self.btn_submit.pack()

    # [함수] 마우스 휠 작동 로직: 플랫폼별 차이를 계산하여 스크롤
    def _on_mousewheel(self, event):
        if event.num == 4: # 리눅스용 휠 위로
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5: # 리눅스용 휠 아래로
            self.canvas.yview_scroll(1, "units")
        else: # 윈도우/맥용 (휠의 delta 값을 이용)
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # [함수] 제출 로직: 채점 수행, 화면 업데이트, 파일 저장
    def submit_quiz(self):
        # 사용자에게 정말 제출할지 묻는 팝업창
        if not messagebox.askyesno("확인", "모든 문제를 풀었습니까? 제출 후에는 수정할 수 없습니다."):
            return

        score = 0  # 정답 개수 변수
        # 퀴즈 객체 리스트와 피드백 레이블 리스트를 동시에 순회
        for i, (q_obj, fb_lbl) in enumerate(zip(self.quiz_objs, self.feedback_labels), 1):
            user_ans = q_obj.user_var.get()  # 사용자가 선택한 값 읽기
            is_correct = (user_ans == q_obj.answer)  # 정답과 비교
            
            if is_correct:
                score += 1
                fb_lbl.config(text=f"✅ 정답입니다!\n💡 설명: {q_obj.example}", fg="#28A745") # 초록색 텍스트
            else:
                fb_lbl.config(text=f"❌ 오답 (정답: {q_obj.answer})\n💡 설명: {q_obj.example}", fg="#D73A49") # 빨간색 텍스트
            
        # 정확도(%) 계산
        accuracy = (score / len(self.quiz_objs)) * 100
        # 텍스트 파일 저장 함수 호출
        self.save_report(score, accuracy)
        
        # 제출 버튼을 비활성화하고 문구 변경
        self.btn_submit.config(state="disabled", text=f"학습 완료! ({score}/{len(self.quiz_objs)})", bg="#6C757D")
        messagebox.showinfo("완료", f"학습이 완료되었습니다!\n최종 점수: {score} / {len(self.quiz_objs)}\n하단 성적표 파일이 생성되었습니다.")

    # [함수] 파일 저장: 상세 결과를 .txt 파일로 기록
    def save_report(self, score, accuracy):
        time_str = datetime.now().strftime('%Y%m%d_%H%M%S')  # 파일명에 쓸 시간 문자열 생성
        filename = f"{self.student_id}_{self.student_name}_{time_str}.txt" # 학번_이름_시간.txt
        
        # 'with open'을 사용해 파일을 안전하게 열고 작성 (자동으로 닫힘)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"[ 전북과학고 파이썬 기초문법 학습 결과 보고서 ]\n")
            f.write(f"--------------------------------------------------\n")
            f.write(f"학번: {self.student_id} | 이름: {self.student_name}\n")
            f.write(f"응시 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"최종 점수: {score} / {len(self.quiz_objs)} ({accuracy:.1f}점)\n")
            f.write(f"--------------------------------------------------\n\n")
            
            # 반복문을 돌며 문항별 상세 내용 기록
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
        print(f"상세 성적표 저장 완료: {filename}") # 개발용 콘솔 출력

# --- 퀴즈 데이터 리스트 (딕셔너리 구조) ---
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

# 프로그램의 시작점 (이 파일을 직접 실행했을 때만 동작)
if __name__ == "__main__":
    root = tk.Tk()  # Tkinter 엔진 인스턴스 생성
    
    # [화면 중앙 배치 로직]
    window_width = 800  # 설정할 창 너비
    window_height = 900 # 설정할 창 높이
    screen_width = root.winfo_screenwidth()   # 현재 모니터의 너비
    screen_height = root.winfo_screenheight() # 현재 모니터의 높이
    center_x = int(screen_width/2 - window_width / 2)   # 중앙 좌표 X 계산
    center_y = int(screen_height/2 - window_height / 2) # 중앙 좌표 Y 계산
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}') # 계산된 위치로 창 이동
    
    app = QuizApp(root, questions_list)  # 앱 인스턴스 생성 및 실행
    root.mainloop()  # 창이 닫힐 때까지 무한 루프 돌며 사용자 입력 대기
