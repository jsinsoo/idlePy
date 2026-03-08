# @title 📝 전북과학고 파이썬 기초문법 학습 시스템 (제출 후 상세 해설 제공)
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
from datetime import datetime
from google.colab import files
import os

# --- 퀴즈 데이터 (문제 추가/수정 가능) ---
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

# --- 변수 및 위젯 설정 ---
user_answers = []
student_id_widget = widgets.Text(placeholder='학번 입력', description='학번:')
student_name_widget = widgets.Text(placeholder='이름 입력', description='이름:')

# --- [함수] 퀴즈 시작 화면 ---
def show_quiz(_):
    sid = student_id_widget.value.strip()
    sname = student_name_widget.value.strip()

    if not sid or not sname:
        print("⚠️ 학번과 이름을 먼저 입력하세요!")
        return

    clear_output()
    display(HTML(f"""
    <div style="background-color: #f0f4ff; padding: 20px; border-radius: 10px; border-left: 8px solid #4a90e2;">
        <h2 style="margin:0;">🐍 파이썬 기초문법 학습 시스템</h2>
        <p style="color: #555;">학생: <b>{sid} {sname}</b> | 일시: {datetime.now().strftime('%Y-%m-%d')}</p>
    </div>
    <br>
    """))

    user_answers.clear()
    for i, q in enumerate(questions_list, 1):
        q_box = widgets.VBox([
            widgets.HTML(f"<b style='font-size: 16px;'>Q{i}. {q['question']}</b>"),
            widgets.RadioButtons(options=q['choices'], value=None, layout={'width': 'max-content'}, style={'description_width': 'initial'})
        ], layout={'padding': '10px', 'border': '1px solid #ddd', 'margin': '5px 0'})
        user_answers.append(q_box.children[1]) # RadioButtons 객체만 저장
        display(q_box)

    submit_btn = widgets.Button(description="📝 최종 제출 및 성적표 다운로드", button_style='success', layout={'width': '350px', 'height': '50px'})
    submit_btn.on_click(lambda b: submit_and_review(sid, sname))
    display(HTML("<br>"), submit_btn)

# --- [함수] 제출 후 결과 리포트 및 다운로드 ---
def submit_and_review(sid, sname):
    score = 0
    total = len(questions_list)
    time_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{sid}_{sname}_{time_str}.txt"

    # 텍스트 성적표 내용 초기화
    report_text = f"[ 전북과학고 파이썬 학습 결과 보고서 ]\n"
    report_text += f"학번: {sid} | 이름: {sname}\n\n"

    # 리뷰 화면을 위한 HTML 구성
    review_html = f"""
    <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px;">
        <h2>✅ 학습 완료! 결과 리포트</h2>
        <p>학번: {sid} | 이름: {sname}</p>
    </div>
    <hr>
    """

    for i, (radio, q) in enumerate(zip(user_answers, questions_list), 1):
        ans = radio.value
        is_correct = (ans == q['answer'])
        color = "#28a745" if is_correct else "#d73a49"
        result_icon = "✅ 정답" if is_correct else f"❌ 오답 (정답: {q['answer']})"

        if is_correct: score += 1

        # 텍스트 파일용 데이터 쌓기
        report_text += f"문제 {i}. {q['question']}\n   - 결과: {'O' if is_correct else 'X'} | 선택: {ans if ans else '미선택'}\n   - 설명: {q['example']}\n\n"

        # 화면 출력용 리뷰 HTML 쌓기
        review_html += f"""
        <div style="padding: 15px; border-bottom: 1px solid #eee; background-color: {'#f9fff9' if is_correct else '#fff9f9'};">
            <b style="font-size: 15px;">문제 {i}. {q['question']}</b><br>
            <span style="color: {color}; font-weight: bold;">{result_icon}</span><br>
            <div style="margin-top: 5px; color: #555; font-style: italic;">
                💡 <b>해설:</b> {q['example']}
            </div>
        </div>
        """

    accuracy = (score / total) * 100
    final_score_html = f"""
    <div style="text-align: center; padding: 30px;">
        <h1 style="color: #4a90e2;">최종 점수: {score} / {total} 점</h1>
        <h3 style="color: #666;">정답률: {accuracy:.1f}%</h3>
        <p>성적표 파일(<b>{filename}</b>)이 자동으로 다운로드되었습니다.</p>
        <button onclick="window.scrollTo(0, 0)" style="padding: 10px 20px; cursor: pointer;">맨 위로 이동</button>
    </div>
    """

    # 파일 저장 및 다운로드
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_text + f"\n최종 점수: {score}/{total} ({accuracy:.1f}점)")

    # 화면 최종 업데이트
    clear_output()
    display(HTML(review_html + final_score_html))
    files.download(filename)

# --- 초기 진입 화면 ---
display(HTML("""
<div style="padding: 10px; border-bottom: 2px solid #4a90e2;">
    <h2 style="color: #4a90e2;">🏢 전북과학고 파이썬 학습 시스템</h2>
</div>
<br>
"""))
display(student_id_widget)
display(student_name_widget)
start_btn = widgets.Button(description="🚀 학습 시작", button_style='info', layout={'width': '200px', 'height': '40px'})
start_btn.on_click(show_quiz)
display(HTML("<br>"), start_btn)
