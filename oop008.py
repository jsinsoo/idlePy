import tkinter as tk  # GUI 제작을 위한 파이썬 기본 라이브러리
from tkinter import messagebox, ttk  # 알림창(messagebox)과 개선된 위젯(ttk) 임포트
from datetime import datetime  # 파일명 및 성적표에 시간을 기록하기 위함

# 1. 개별 문제의 데이터와 사용자의 선택 상태를 관리하는 클래스
class Question:
    def __init__(self, data):
        self.question = data["question"]  # 질문 텍스트
        self.choices = data["choices"]    # 4~5개의 선택지 리스트
        self.answer = data["answer"]      # 정답 텍스트
        self.example = data["example"]    # 오답 시 보여줄 상세 설명(예시)
        # tk.StringVar()는 라디오버튼의 선택 상태를 실시간으로 추적하는 GUI 전용 변수입니다.
        self.user_var = tk.StringVar() 

# 2. 메인 애플리케이션(화면 구성 및 로직) 클래스
class QuizApp:
    def __init__(self, root, questions_data):
        self.root = root  # 메인 윈도우 객체 저장
        self.root.title("전북과학고 파이썬 기초문법 학습 시스템")  # 창 제목 설정
        self.root.geometry("700x800")  # 초기 창 크기 설정 (가로 700, 세로 800)
        self.questions_data = questions_data  # 외부에서 전달받은 문제 리스트 저장
        
        self.student_id = ""    # 학번 저장용 변수 초기화
        self.student_name = ""  # 이름 저장용 변수 초기화
        
        # 프로그램 실행 시 로그인 화면을 먼저 띄움
        self.show_login_screen()

    # [로그인 화면] 학번과 이름을 입력받는 레이아웃
    def show_login_screen(self):
        self.login_frame = tk.Frame(self.root)  # 로그인 전용 프레임 생성
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")  # 창 정중앙에 배치

        tk.Label(self.login_frame, text="파이썬 기초문법 학습", font=("Arial", 18, "bold")).pack(pady=20)
        
        tk.Label(self.login_frame, text="학번:").pack()
        self.ent_id = tk.Entry(self.login_frame)  # 학번 입력창
        self.ent_id.pack(pady=5)

        tk.Label(self.login_frame, text="이름:").pack()
        self.ent_name = tk.Entry(self.login_frame)  # 이름 입력창
        self.ent_name.pack(pady=5)

        # 버튼 클릭 시 start_quiz 함수 실행
        tk.Button(self.login_frame, text="학습 시작", command=self.start_quiz, width=20, bg="lightblue").pack(pady=20)

    # [퀴즈 시작] 입력을 검증하고 메인 퀴즈 화면으로 전환
    def start_quiz(self):
        self.student_id = self.ent_id.get().strip()  # 입력창에서 학번 가져오기
        self.student_name = self.ent_name.get().strip()  # 입력창에서 이름 가져오기

        if not self.student_id or not self.student_name:
            messagebox.showwarning("알림", "학번과 이름을 입력해주세요.")  # 미입력 시 경고
            return

        self.login_frame.destroy()  # 로그인 프레임 제거
        self.setup_quiz_screen()    # 실제 퀴즈 화면 구성 시작

    # [퀴즈 화면 구성] 스크롤바와 문제들을 배치
    def setup_quiz_screen(self):
        # 상단에 응시자 정보 표시
        info_text = f"학생: {self.student_id} {self.student_name} | 응시일: {datetime.now().strftime('%Y-%m-%d')}"
        tk.Label(self.root, text=info_text, fg="gray").pack(pady=10)

        # 많은 문제를 보여주기 위한 Canvas와 스크롤바 설정
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)  # 실제 문제들이 배치될 프레임

        # 프레임 크기가 변하면 스크롤 영역을 자동으로 갱신하도록 바인딩
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # 캔버스 안에 프레임을 윈도우 객체로 삽입
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=20)
        self.scrollbar.pack(side="right", fill="y")

        # 문제 데이터를 기반으로 Question 객체 리스트 생성
        self.quiz_objs = [Question(q) for q in self.questions_data]
        self.feedback_labels = []  # 나중에 정답 여부를 보여줄 레이블들을 저장할 리스트

        # 화면에 문제와 보기들을 반복문으로 생성
        for i, q_obj in enumerate(self.quiz_objs, 1):
            q_frame = tk.Frame(self.scrollable_frame, pady=15)  # 한 문제당 하나의 프레임
            q_frame.pack(fill="x")

            # 문제 텍스트 레이블
            tk.Label(q_frame, text=f"Q{i}. {q_obj.question}", font=("Arial", 11, "bold"), wraplength=600, justify="left").pack(anchor="w")
            
            # 해당 문제의 선택지들을 라디오버튼으로 생성
            for choice in q_obj.choices:
                # variable에 q_obj.user_var를 연결하여 선택 값을 자동으로 추적함
                tk.Radiobutton(q_frame, text=choice, variable=q_obj.user_var, value=choice).pack(anchor="w", padx=20)

            # 제출 전까지는 비어있는 '피드백 레이블' 생성
            fb_lbl = tk.Label(q_frame, text="", justify="left", wraplength=550, fg="blue", font=("Arial", 10, "italic"))
            fb_lbl.pack(anchor="w", padx=20, pady=5)
            self.feedback_labels.append(fb_lbl)  # 리스트에 보관했다가 나중에 내용 수정

        # 맨 하단에 고정된 제출 버튼
        self.btn_submit = tk.Button(self.root, text="최종 제출 및 성적 확인", command=self.submit_quiz, bg="green", fg="white", font=("Arial", 12, "bold"), pady=10)
        self.btn_submit.pack(fill="x", padx=20, pady=10)

    # [제출 로직] 정답 채점, 화면 업데이트, 파일 저장 수행
    def submit_quiz(self):
        if not messagebox.askyesno("확인", "모든 문제를 풀었습니까? 제출 후에는 수정할 수 없습니다."):
            return

        score = 0  # 맞은 개수 초기화
        
        # 문제 객체와 피드백 레이블을 동시에 순회하며 채점
        for i, (q_obj, fb_lbl) in enumerate(zip(self.quiz_objs, self.feedback_labels), 1):
            user_ans = q_obj.user_var.get()  # 사용자가 선택한 라디오버튼의 값
            is_correct = (user_ans == q_obj.answer)  # 정답 비교
            
            if is_correct:
                score += 1
                result_text = "✅ 정답입니다!"
                fb_lbl.config(text=f"{result_text}\n설명: {q_obj.example}", fg="green")  # 맞으면 초록색
            else:
                result_text = f"❌ 오답 (정답: {q_obj.answer})"
                fb_lbl.config(text=f"{result_text}\n설명: {q_obj.example}", fg="red")    # 틀리면 빨간색
            
        # 백분율 점수 계산
        accuracy = (score / len(self.quiz_objs)) * 100
        # 학번_이름_시간.txt 파일로 결과 기록함수 호출
        self.save_report(score, accuracy)
        
        # 제출 후 상태 업데이트: 버튼 비활성화 및 점수 표시
        self.btn_submit.config(state="disabled", text=f"제출 완료 - 점수: {score}/{len(self.quiz_objs)} ({accuracy:.1f}점)")
        messagebox.showinfo("완료", f"학습이 완료되었습니다!\n점수: {score}/{len(self.quiz_objs)}\n화면에서 상세 해설을 확인하세요.")

    # [파일 저장] 상세 결과를 텍스트 파일로 내보냄
    def save_report(self, score, accuracy):
        # 요구사항에 맞춘 파일명 규격 생성
        time_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.student_id}_{self.student_name}_{time_str}.txt"
        
        # 'with open'을 사용하여 파일 쓰기 (자동으로 파일을 닫아줌)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"[ 전북과학고 파이썬 기초문법 학습 결과 보고서 ]\n")
            f.write(f"--------------------------------------------------\n")
            f.write(f"학번: {self.student_id}\n")
            f.write(f"이름: {self.student_name}\n")
            f.write(f"응시 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"최종 점수: {score} / {len(self.quiz_objs)} ({accuracy:.1f}점)\n")
            f.write(f"--------------------------------------------------\n\n")
            f.write(f"[ 문항별 상세 기록 ]\n")
            
            # 모든 문제의 데이터를 순회하며 파일에 텍스트로 기록
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

# 3. 퀴즈 문제 데이터 리스트 (딕셔너리 형태)
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

# 4. 프로그램의 진입점
if __name__ == "__main__":
    root = tk.Tk()  # Tkinter 엔진 시작
    app = QuizApp(root, questions_list)  # QuizApp 인스턴스 생성 및 실행
    root.mainloop()  # GUI 창이 닫힐 때까지 이벤트 루프 유지
