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
questions_list =  [
            {
            "question": "1. 파이썬에서 두 숫자의 합을 구하는 연산자는 무엇인가요?",
            "choices": ["+", "-", "*", "/", "%"],
            "answer": "+",
            "example": "3 + 5 -> 8"
        },
        {
            "question": "2. 문자열 'hello'의 길이를 반환하는 함수는?",
            "choices": ["len()", "size()", "count()", "length()"],
            "answer": "len()",
            "example": "len('hello') -> 5"
        },
        {
            "question": "3. 리스트 [1, 3, 2, 8, 5]에서 최대값을 반환하는 함수는?",
            "choices": ["max()", "min()", "sum()", "sorted()"],
            "answer": "max()",
            "example": "max([1, 3, 2, 8, 5]) -> 8"
        },
        {
            "question": "4. 숫자 7이 짝수인지 확인하는 코드는 무엇인가요?",
            "choices": ["7 % 2 == 0", "7 % 2 == 1", "7 // 2 == 0", "7 / 2 == 1"],
            "answer": "7 % 2 == 0",
            "example": "7 % 2 -> 1 (False)"
        },
        {
            "question": "5. 리스트 [1, 2, 3, 4, 5]에서 짝수만 필터링하는 방법은?",
            "choices": [
                "[x for x in lst if x % 2 == 0]",
                "filter(lambda x: x % 2 == 0, lst)",
                "lst.remove(odd)",
                "lst.append(even)"
            ],
            "answer": "[x for x in lst if x % 2 == 0]",
            "example": "[1, 2, 3, 4, 5] -> [2, 4]"
        },
        {
            "question": "6. 'hello world'에서 단어 'hello'가 포함되어 있는지 확인하는 방법은?",
            "choices": [
                "'hello' in 'hello world'",
                "'hello'.contains('hello world')",
                "contains('hello', 'hello world')",
                "search('hello', 'hello world')"
            ],
            "answer": "'hello' in 'hello world'",
            "example": "'hello' in 'hello world' -> True"
        },
        {
            "question": "7. 문자열 'hello'를 뒤집는 코드는 무엇인가요?",
            "choices": [
                "s[::-1]",
                "reverse(s)",
                "s.reverse()",
                "reversed(s)"
            ],
            "answer": "s[::-1]",
            "example": "'hello'[::-1] -> 'olleh'"
        },
        {
            "question": "8. 리스트 [1, 2, 3, 4]의 합을 계산하는 함수는?",
            "choices": ["sum()", "add()", "reduce()", "total()"],
            "answer": "sum()",
            "example": "sum([1, 2, 3, 4]) -> 10"
        },
        {
            "question": "9. 숫자 4의 팩토리얼을 계산하는 함수는?",
            "choices": ["math.factorial()", "factorial()", "math.factor()", "factor()"],
            "answer": "math.factorial()",
            "example": "math.factorial(4) -> 24"
        },
        {
            "question": "10. 피보나치 수열의 n번째 항을 반환하는 코드는?",
            "choices": [
                "재귀 함수",
                "for 반복문",
                "while 반복문",
                "위의 모든 방법"
            ],
            "answer": "위의 모든 방법",
            "example": "fibonacci(6) -> 8"
        },
        {
            "question": "1. 변수에 값을 할당할 때 사용하는 연산자는 무엇인가요?",
            "choices": ["=", "==", "!=", "<", ">"],
            "answer": "=",
            "example": "x = 10"
        },
        {
            "question": "2. 리스트에서 첫 번째 요소에 접근하는 방법은 무엇인가요?",
            "choices": ["list[1]", "list[0]", "list.first()", "list.get(0)"],
            "answer": "list[0]",
            "example": "my_list = [1, 2, 3]; my_list[0] -> 1"
        },
        {
            "question": "3. 문자열의 모든 문자를 소문자로 변환하는 함수는?",
            "choices": ["lower()", "upper()", "capitalize()", "title()"],
            "answer": "lower()",
            "example": "'HELLO'.lower() -> 'hello'"
        },
        {
            "question": "4. 파이썬에서 반복문으로 리스트를 순회할 때 사용하는 키워드는?",
            "choices": ["for", "while", "do", "loop"],
            "answer": "for",
            "example": "for item in [1, 2, 3]: print(item)"
        },
        {
            "question": "5. 파이썬에서 조건문을 작성할 때 사용하는 키워드는?",
            "choices": ["if", "when", "switch", "case"],
            "answer": "if",
            "example": "if x > 0: print('Positive')"
        },
        {
            "question": "6. 딕셔너리에서 키에 해당하는 값을 가져오는 함수는?",
            "choices": ["get()", "fetch()", "retrieve()", "find()"],
            "answer": "get()",
            "example": "my_dict = {'key': 'value'}; my_dict.get('key') -> 'value'"
        },
        {
            "question": "7. 리스트에 요소를 추가하는 함수는?",
            "choices": ["append()", "add()", "insert()", "extend()"],
            "answer": "append()",
            "example": "my_list = [1, 2]; my_list.append(3) -> [1, 2, 3]"
        },
        {
            "question": "8. 숫자 3.5를 정수로 변환하는 함수는?",
            "choices": ["int()", "float()", "str()", "round()"],
            "answer": "int()",
            "example": "int(3.5) -> 3"
        },
        {
            "question": "9. 파이썬에서 주석을 작성할 때 사용하는 기호는?",
            "choices": ["#", "//", "/* */", "--"],
            "answer": "#",
            "example": "# This is a comment"
        },
        {
            "question": "10. 리스트의 길이를 반환하는 함수는?",
            "choices": ["len()", "size()", "count()", "length()"],
            "answer": "len()",
            "example": "len([1, 2, 3]) -> 3"
        },

            {
            "question": "1. 파이썬에서 숫자형 데이터 타입이 아닌 것은?",
            "choices": ["int", "float", "str", "complex"],
            "answer": "str",
            "example": "숫자형 데이터 타입은 int, float, complex입니다. str은 문자열 타입입니다."
        },
        {
            "question": "2. 리스트에 요소를 정렬하는 방법은 무엇인가요?",
            "choices": ["sort()", "order()", "arrange()", "sorted()"],
            "answer": "sort()",
            "example": "my_list = [3, 1, 2]; my_list.sort() -> [1, 2, 3]"
        },
        {
            "question": "3. 파이썬에서 무한 반복을 수행하는 반복문은?",
            "choices": ["for", "while", "do-while", "repeat"],
            "answer": "while",
            "example": "while True: print('무한 반복')"
        },
        {
            "question": "4. 파이썬에서 함수의 기본 값을 설정하는 방법은?",
            "choices": ["def func(x=10):", "def func(int x=10):", "def func(x):=10", "def func(x:int=10):"],
            "answer": "def func(x=10):",
            "example": "def greet(name='World'): print(f'Hello, {name}!')"
        },
        {
            "question": "5. 다음 중 파이썬에서 예외를 처리하는 키워드는 무엇인가요?",
            "choices": ["try", "except", "finally", "모두 해당"],
            "answer": "모두 해당",
            "example": "try: x = 1 / 0\nexcept ZeroDivisionError: print('에러 처리')\nfinally: print('완료')"
        },
        {
            "question": "6. 리스트를 복사할 때 사용하는 방법은?",
            "choices": ["copy()", "clone()", "replicate()", "duplicate()"],
            "answer": "copy()",
            "example": "my_list = [1, 2, 3]; new_list = my_list.copy()"
        },
        {
            "question": "7. 파이썬에서 현재 디렉토리를 확인하는 함수는?",
            "choices": ["os.getcwd()", "os.listdir()", "os.chdir()", "os.get()"],
            "answer": "os.getcwd()",
            "example": "import os; print(os.getcwd())"
        },
        {
            "question": "8. 문자열에서 공백을 제거하는 방법은?",
            "choices": ["strip()", "remove()", "trim()", "delete()"],
            "answer": "strip()",
            "example": "'  hello  '.strip() -> 'hello'"
        },
        {
            "question": "9. 다음 중 파이썬에서 변수를 삭제하는 키워드는?",
            "choices": ["del", "remove", "delete", "clear"],
            "answer": "del",
            "example": "x = 10; del x"
        },
        {
            "question": "10. 문자열에서 특정 문자를 대체하는 함수는?",
            "choices": ["replace()", "substitute()", "change()", "modify()"],
            "answer": "replace()",
            "example": "'hello world'.replace('world', 'Python') -> 'hello Python'"
        },

        {
            "question": "1. 파이썬에서 주어진 리스트에서 가장 작은 값을 반환하는 함수는 무엇인가요?",
            "choices": ["min()", "max()", "reduce()", "sorted()"],
            "answer": "min()",
            "example": "my_list = [3, 1, 2]; min(my_list) -> 1"
        },
        {
            "question": "2. 파이썬에서 반복 가능한 객체를 순회하며 처리하는 함수는?",
            "choices": ["map()", "filter()", "reduce()", "all()"],
            "answer": "map()",
            "example": "list(map(lambda x: x * 2, [1, 2, 3])) -> [2, 4, 6]"
        },
        {
            "question": "3. 문자열에서 모든 단어의 첫 글자를 대문자로 변환하는 함수는?",
            "choices": ["title()", "capitalize()", "upper()", "lower()"],
            "answer": "title()",
            "example": "'hello world'.title() -> 'Hello World'"
        },
        {
            "question": "4. 리스트를 뒤집는 함수는 무엇인가요?",
            "choices": ["reverse()", "reversed()", "flip()", "invert()"],
            "answer": "reverse()",
            "example": "my_list = [1, 2, 3]; my_list.reverse() -> [3, 2, 1]"
        },
        {
            "question": "5. 딕셔너리에서 키와 값을 튜플로 반환하는 함수는?",
            "choices": ["items()", "keys()", "values()", "pairs()"],
            "answer": "items()",
            "example": "my_dict = {'a': 1, 'b': 2}; my_dict.items() -> dict_items([('a', 1), ('b', 2)])"
        },
        {
            "question": "6. 튜플을 리스트로 변환하는 함수는?",
            "choices": ["list()", "tuple()", "convert()", "to_list()"],
            "answer": "list()",
            "example": "tuple_data = (1, 2, 3); list(tuple_data) -> [1, 2, 3]"
        },
        {
            "question": "7. 파이썬에서 함수를 호출할 때 키워드 인자를 사용하는 방법은?",
            "choices": ["func(name='John')", "func('John')", "func->name='John'", "func::name='John'"],
            "answer": "func(name='John')",
            "example": "def greet(name): print(f'Hello, {name}!'); greet(name='John') -> 'Hello, John!'"
        },
        {
            "question": "8. 문자열을 특정 구분자로 나누는 함수는?",
            "choices": ["split()", "join()", "partition()", "divide()"],
            "answer": "split()",
            "example": "'a,b,c'.split(',') -> ['a', 'b', 'c']"
        },
        {
            "question": "9. 파이썬에서 값을 거듭 제곱하는 연산자는?",
            "choices": ["**", "*", "^", "pow()"],
            "answer": "**",
            "example": "2 ** 3 -> 8"
        },
        {
            "question": "10. 리스트에서 요소를 제거하는 함수는?",
            "choices": ["remove()", "delete()", "pop()", "clear()"],
            "answer": "remove()",
            "example": "my_list = [1, 2, 3]; my_list.remove(2) -> [1, 3]"
        },

       {
            "question": "1. 파이썬에서 사용되지 않는 논리 연산자는 무엇인가요?",
            "choices": ["and", "or", "xor", "not"],
            "answer": "xor",
            "example": "파이썬에서는 xor 대신 비트 연산자 ^를 사용합니다."
        },
        {
            "question": "2. 리스트에 여러 요소를 한 번에 추가할 때 사용하는 함수는?",
            "choices": ["append()", "extend()", "insert()", "add()"],
            "answer": "extend()",
            "example": "my_list = [1, 2]; my_list.extend([3, 4]) -> [1, 2, 3, 4]"
        },
        {
            "question": "3. 함수에서 여러 값을 반환하려면 어떤 자료형을 주로 사용하나요?",
            "choices": ["리스트", "튜플", "딕셔너리", "집합"],
            "answer": "튜플",
            "example": "def get_values(): return 1, 2; x, y = get_values()"
        },
        {
            "question": "4. 파이썬에서 파일을 열 때 사용하는 기본 모드는 무엇인가요?",
            "choices": ["w", "r", "a", "x"],
            "answer": "r",
            "example": "open('file.txt', 'r') -> 파일을 읽기 모드로 엽니다."
        },
        {
            "question": "5. 파이썬에서 문자열의 공백을 제거하는 함수는?",
            "choices": ["strip()", "remove()", "delete()", "pop()"],
            "answer": "strip()",
            "example": "'  hello  '.strip() -> 'hello'"
        },
        {
            "question": "6. 딕셔너리에 새 키-값 쌍을 추가하는 올바른 방법은?",
            "choices": ["dict.add(key, value)", "dict[key] = value", "dict.update([key, value])", "dict.insert(key, value)"],
            "answer": "dict[key] = value",
            "example": "my_dict = {}; my_dict['name'] = 'Alice'"
        },
        {
            "question": "7. 파이썬에서 반복문을 즉시 종료하는 키워드는?",
            "choices": ["stop", "break", "continue", "exit"],
            "answer": "break",
            "example": "for x in range(5):\n    if x == 3:\n        break\n    print(x)"
        },
        {
            "question": "8. 리스트를 오름차순으로 정렬하는 함수는?",
            "choices": ["sort()", "sorted()", "order()", "arrange()"],
            "answer": "sort()",
            "example": "my_list = [3, 1, 2]; my_list.sort() -> [1, 2, 3]"
        },
        {
            "question": "9. 파이썬에서 조건이 참인 경우 실행되는 코드는?",
            "choices": ["if", "when", "case", "switch"],
            "answer": "if",
            "example": "if x > 0: print('Positive')"
        },
        {
            "question": "10. 숫자를 반올림하는 함수는 무엇인가요?",
            "choices": ["round()", "ceil()", "floor()", "truncate()"],
            "answer": "round()",
            "example": "round(3.5) -> 4"
        },
        {
            "question": "1. 파이썬에서 세미콜론(;)의 역할은 무엇인가요?",
            "choices": [
                "한 줄에 여러 명령어를 구분",
                "문장을 종료",
                "코드를 주석으로 만듦",
                "아무 역할도 하지 않음"
            ],
            "answer": "한 줄에 여러 명령어를 구분",
            "example": "print('Hello'); print('World')"
        },
        {
            "question": "2. 파이썬에서 전역 변수를 함수 안에서 수정하려면 어떤 키워드를 사용해야 하나요?",
            "choices": ["global", "local", "nonlocal", "const"],
            "answer": "global",
            "example": "global x; x = 5"
        },
        {
            "question": "3. 다음 중 파이썬에서 값을 비교하는 연산자는?",
            "choices": ["==", "=", "!=", "모두 해당"],
            "answer": "모두 해당",
            "example": "x == y, x != y"
        },
        {
            "question": "4. 리스트의 모든 요소에 대해 특정 작업을 적용한 결과를 반환하는 함수는?",
            "choices": ["map()", "filter()", "reduce()", "zip()"],
            "answer": "map()",
            "example": "list(map(lambda x: x * 2, [1, 2, 3])) -> [2, 4, 6]"
        },
        {
            "question": "5. 파이썬에서 객체의 타입을 확인하는 함수는?",
            "choices": ["type()", "id()", "isinstance()", "dir()"],
            "answer": "type()",
            "example": "type(10) -> <class 'int'>"
        },
        {
            "question": "6. 리스트에서 중복 요소를 제거하려면 어떤 자료형을 사용하나요?",
            "choices": ["set", "dict", "tuple", "list"],
            "answer": "set",
            "example": "list(set([1, 2, 2, 3])) -> [1, 2, 3]"
        },
        {
            "question": "7. 파이썬에서 비어 있는 값을 나타내는 키워드는?",
            "choices": ["None", "Null", "Empty", "Void"],
            "answer": "None",
            "example": "x = None"
        },
        {
            "question": "8. 다음 중 반복 가능한 객체를 생성하지 않는 것은?",
            "choices": ["range()", "enumerate()", "zip()", "break()"],
            "answer": "break()",
            "example": "break는 반복문을 종료하는 키워드입니다."
        },
        {
            "question": "9. 파이썬에서 False로 간주되지 않는 값은?",
            "choices": [
                "0",
                "빈 문자열('')",
                "빈 리스트([])",
                "1"
            ],
            "answer": "1",
            "example": "bool(1) -> True"
        },
        {
            "question": "10. 파이썬에서 반복문과 함께 사용하여 조건을 만족하는 경우만 실행되는 키워드는?",
            "choices": ["continue", "break", "pass", "return"],
            "answer": "continue",
            "example": "for x in range(5): if x % 2 == 0: continue; print(x)"
        },
        
         {
            "question": "1. 파이썬에서 리스트와 튜플의 주요 차이점은 무엇인가요?",
            "choices": [
                "튜플은 변경할 수 없고, 리스트는 변경 가능하다.",
                "리스트는 불변하고, 튜플은 변경 가능하다.",
                "튜플은 항상 정렬되어 있다.",
                "리스트는 딕셔너리의 키로 사용된다."
            ],
            "answer": "튜플은 변경할 수 없고, 리스트는 변경 가능하다.",
            "example": "my_list = [1, 2, 3]; my_list[0] = 10\nmy_tuple = (1, 2, 3); my_tuple[0] = 10 # Error"
        },
        {
            "question": "2. 파이썬에서 슬라이싱을 사용하여 리스트의 일부를 추출하는 방법은?",
            "choices": [
                "list[start:end]",
                "list[start->end]",
                "list(start:end)",
                "list[start to end]"
            ],
            "answer": "list[start:end]",
            "example": "my_list = [0, 1, 2, 3, 4]; my_list[1:4] -> [1, 2, 3]"
        },
        {
            "question": "3. 파이썬에서 리스트의 모든 요소를 합산하는 함수는?",
            "choices": ["sum()", "total()", "add()", "combine()"],
            "answer": "sum()",
            "example": "sum([1, 2, 3]) -> 6"
        },
        {
            "question": "4. 파이썬에서 None의 역할은 무엇인가요?",
            "choices": [
                "변수를 초기화하지 않은 상태를 나타냄",
                "오류 메시지를 나타냄",
                "무한 루프를 종료시킴",
                "값이 비어있음을 나타냄"
            ],
            "answer": "값이 비어있음을 나타냄",
            "example": "x = None; print(x) # 출력: None"
        },
        {
            "question": "5. 파이썬에서 딕셔너리의 모든 키를 가져오는 함수는?",
            "choices": ["keys()", "values()", "items()", "get()"],
            "answer": "keys()",
            "example": "my_dict = {'a': 1, 'b': 2}; my_dict.keys() -> dict_keys(['a', 'b'])"
        },
        {
            "question": "6. 파이썬에서 반복문을 중첩하여 사용하는 방법은?",
            "choices": [
                "for i in range(3): for j in range(2): ...",
                "while i in range(3): while j in range(2): ...",
                "loop i in range(3): loop j in range(2): ...",
                "nested for i in range(3), j in range(2): ..."
            ],
            "answer": "for i in range(3): for j in range(2): ...",
            "example": "for i in range(3):\n    for j in range(2):\n        print(i, j)"
        },
        {
            "question": "7. 파이썬에서 람다 함수의 특징은 무엇인가요?",
            "choices": [
                "이름 없는 익명 함수",
                "반드시 이름이 있어야 함",
                "한 줄로만 작성 가능",
                "이름 없는 익명 함수, 한 줄로만 작성 가능"
            ],
            "answer": "이름 없는 익명 함수, 한 줄로만 작성 가능",
            "example": "f = lambda x: x + 1; f(2) -> 3"
        },
        {
            "question": "8. 파이썬에서 리스트 요소를 역순으로 정렬하는 방법은?",
            "choices": [
                "list.reverse()",
                "reverse(list)",
                "sorted(list, reverse=True)",
                "모두 가능"
            ],
            "answer": "모두 가능",
            "example": "my_list = [3, 1, 2]; my_list.reverse() -> [2, 1, 3]"
        },
        {
            "question": "9. 파이썬에서 조건문과 반복문을 한 줄로 작성할 수 있는 기능은?",
            "choices": ["리스트 컴프리헨션", "조건문 함수", "반복문 조합", "조건식 반복"],
            "answer": "리스트 컴프리헨션",
            "example": "[x for x in range(5) if x % 2 == 0] -> [0, 2, 4]"
        },
        {
            "question": "10. 파이썬에서 예외를 발생시키는 키워드는?",
            "choices": ["raise", "try", "except", "throw"],
            "answer": "raise",
            "example": "raise ValueError('Invalid value')"
        },
         {
            "question": "1. 파이썬에서 기본적으로 제공하는 정렬 함수는?",
            "choices": ["sorted()", "order()", "arrange()", "sort()"],
            "answer": "sorted()",
            "example": "sorted([3, 1, 2]) -> [1, 2, 3]"
        },
        {
            "question": "2. 파이썬에서 불 자료형의 값이 아닌 것은?",
            "choices": ["True", "False", "1", "None"],
            "answer": "None",
            "example": "불 자료형은 True 또는 False로만 구성됩니다."
        },
        {
            "question": "3. 파이썬에서 임의의 요소를 선택하는 함수는 무엇인가요?",
            "choices": ["random.choice()", "random.pick()", "random.select()", "random.item()"],
            "answer": "random.choice()",
            "example": "import random; random.choice([1, 2, 3])"
        },
        {
            "question": "4. 파이썬에서 현재 시간을 가져오는 모듈은 무엇인가요?",
            "choices": ["datetime", "time", "date", "os"],
            "answer": "datetime",
            "example": "from datetime import datetime; print(datetime.now())"
        },
        {
            "question": "5. 파이썬에서 객체의 속성과 메서드를 나열하는 함수는?",
            "choices": ["dir()", "list()", "help()", "dict()"],
            "answer": "dir()",
            "example": "dir(object)"
        },
        {
            "question": "6. 파이썬에서 파일을 쓰기 모드로 여는 기본 명령은?",
            "choices": ["open('file.txt', 'w')", "write('file.txt')", "file('file.txt', 'w')", "open('file.txt', 'write')"],
            "answer": "open('file.txt', 'w')",
            "example": "with open('file.txt', 'w') as f: f.write('Hello')"
        },
        {
            "question": "7. 파이썬에서 무작위로 정수를 생성하는 함수는?",
            "choices": ["random.randint()", "random.random()", "random.int()", "random.range()"],
            "answer": "random.randint()",
            "example": "import random; random.randint(1, 10)"
        },
        {
            "question": "8. 파이썬에서 조건문을 여러 개 사용하는 키워드는?",
            "choices": ["elif", "else if", "elseif", "else"],
            "answer": "elif",
            "example": "if x > 10: pass elif x > 5: pass"
        },
        {
            "question": "9. 파이썬에서 빈 리스트를 생성하는 올바른 방법은?",
            "choices": ["[]", "list()", "both", "None"],
            "answer": "both",
            "example": "my_list = []; my_list = list()"
        },
        {
            "question": "10. 파이썬에서 파일을 읽기 모드로 여는 기본 명령은?",
            "choices": ["open('file.txt', 'r')", "file('file.txt', 'r')", "read('file.txt')", "open('file.txt')"],
            "answer": "open('file.txt', 'r')",
            "example": "with open('file.txt', 'r') as f: print(f.read())"
        },
           {
            "question": "1. 파이썬에서 딕셔너리에서 키가 존재하는지 확인하는 연산자는?",
            "choices": ["in", "exists", "has", "key"],
            "answer": "in",
            "example": "my_dict = {'a': 1}; 'a' in my_dict -> True"
        },
        {
            "question": "2. 파이썬에서 값을 나누고 소수점 이하를 버리는 연산자는?",
            "choices": ["//", "/", "%", "div"],
            "answer": "//",
            "example": "10 // 3 -> 3"
        },
        {
            "question": "3. 파이썬에서 집합(set)의 중복 제거 기능을 설명하는 올바른 것은?",
            "choices": [
                "중복된 값을 제거한다.",
                "값을 정렬한다.",
                "값을 키로 변환한다.",
                "값을 인덱스로 변환한다."
            ],
            "answer": "중복된 값을 제거한다.",
            "example": "set([1, 2, 2, 3]) -> {1, 2, 3}"
        },
        {
            "question": "4. 파이썬에서 반복문을 사용하여 문자열을 순회할 때 사용하는 기본 구조는?",
            "choices": ["for", "while", "do-while", "loop"],
            "answer": "for",
            "example": "for char in 'hello': print(char)"
        },
        {
            "question": "5. 파이썬에서 함수의 기본값을 설정하려면?",
            "choices": ["def func(x=10):", "def func(x==10):", "def func(int x=10):", "def func(x):=10"],
            "answer": "def func(x=10):",
            "example": "def greet(name='World'): print(f'Hello, {name}!')"
        },
        {
            "question": "6. 파이썬에서 여러 줄 문자열을 작성할 때 사용하는 기호는?",
            "choices": ["''' 또는 \"\"\"", "''", "\"", "//"],
            "answer": "''' 또는 \"\"\"",
            "example": "'''This is a\nmulti-line string'''"
        },
        {
            "question": "7. 파이썬에서 리스트에 요소를 추가하는 함수는?",
            "choices": ["append()", "add()", "insert()", "push()"],
            "answer": "append()",
            "example": "my_list = [1, 2]; my_list.append(3) -> [1, 2, 3]"
        },
        {
            "question": "8. 파이썬에서 클래스의 메서드가 첫 번째 매개변수로 self를 사용하는 이유는?",
            "choices": [
                "인스턴스 자신을 참조하기 위해",
                "클래스 변수를 선언하기 위해",
                "상속을 구현하기 위해",
                "오류를 방지하기 위해"
            ],
            "answer": "인스턴스 자신을 참조하기 위해",
            "example": "class MyClass: def method(self): pass"
        },
        {
            "question": "9. 파이썬에서 문자를 아스키 코드로 변환하는 함수는?",
            "choices": ["ord()", "chr()", "ascii()", "code()"],
            "answer": "ord()",
            "example": "ord('A') -> 65"
        },
        {
            "question": "10. 파이썬에서 한 줄 주석을 작성할 때 사용하는 기호는?",
            "choices": ["#", "//", "<!--", "**"],
            "answer": "#",
            "example": "# This is a comment"
        },
        {
            "question": "1. 파이썬에서 문자열을 대체하는 함수는 무엇인가요?",
            "choices": ["replace()", "sub()", "switch()", "change()"],
            "answer": "replace()",
            "example": "'hello world'.replace('world', 'Python') -> 'hello Python'"
        },
        {
            "question": "2. 파이썬에서 리스트를 정렬하여 새로운 리스트를 반환하는 함수는?",
            "choices": ["sorted()", "sort()", "arrange()", "organize()"],
            "answer": "sorted()",
            "example": "sorted([3, 1, 2]) -> [1, 2, 3]"
        },
        {
            "question": "3. 파이썬에서 문자열을 특정 문자로 나누는 함수는?",
            "choices": ["split()", "partition()", "divide()", "cut()"],
            "answer": "split()",
            "example": "'a,b,c'.split(',') -> ['a', 'b', 'c']"
        },
        {
            "question": "4. 파이썬에서 리스트의 마지막 요소를 제거하는 함수는?",
            "choices": ["pop()", "remove()", "delete()", "discard()"],
            "answer": "pop()",
            "example": "my_list = [1, 2, 3]; my_list.pop() -> 3, my_list -> [1, 2]"
        },
        {
            "question": "5. 파이썬에서 값을 거듭 제곱하는 연산자는?",
            "choices": ["**", "^", "pow()", "exp()"],
            "answer": "**",
            "example": "2 ** 3 -> 8"
        },
        {
            "question": "6. 파이썬에서 반복 가능한 객체의 길이를 반환하는 함수는?",
            "choices": ["len()", "size()", "count()", "length()"],
            "answer": "len()",
            "example": "len([1, 2, 3]) -> 3"
        },
        {
            "question": "7. 파이썬에서 조건이 거짓일 때 예외를 발생시키는 키워드는?",
            "choices": ["assert", "raise", "throw", "error"],
            "answer": "assert",
            "example": "assert 2 + 2 == 4, '계산 오류'"
        },
        {
            "question": "8. 파이썬에서 `range(5)`가 반환하는 것은?",
            "choices": ["0부터 4까지의 숫자", "1부터 5까지의 숫자", "리스트", "딕셔너리"],
            "answer": "0부터 4까지의 숫자",
            "example": "list(range(5)) -> [0, 1, 2, 3, 4]"
        },
        {
            "question": "9. 파이썬에서 리스트를 병합하는 올바른 방법은?",
            "choices": ["+ 연산자", "append()", "merge()", "join()"],
            "answer": "+ 연산자",
            "example": "[1, 2] + [3, 4] -> [1, 2, 3, 4]"
        },
        {
            "question": "10. 파이썬에서 for 반복문과 함께 값을 동시에 인덱스와 함께 얻는 함수는?",
            "choices": ["enumerate()", "index()", "range()", "zip()"],
            "answer": "enumerate()",
            "example": "for index, value in enumerate(['a', 'b', 'c']): print(index, value)"
        },
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
