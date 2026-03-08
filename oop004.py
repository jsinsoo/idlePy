import math
from datetime import datetime

# 1. 개별 문제 정보를 담는 클래스
class Question:
    def __init__(self, question, choices, answer, example):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.example = example

    def check_answer(self, user_input):
        try:
            index = int(user_input) - 1
            is_correct = self.choices[index] == self.answer
            return is_correct, self.choices[index] # 정답여부와 사용자가 선택한 텍스트 반환
        except (ValueError, IndexError):
            return False, "유효하지 않은 입력"

# 2. 퀴즈 시스템 및 상세 성적표 생성을 관리하는 클래스
class QuizManager:
    def __init__(self, questions_data, student_id, student_name):
        self.questions = [Question(**q) for q in questions_data]
        self.score = 0
        self.results_log = []  # 문항별 상세 기록을 위한 리스트
        self.student_id = student_id
        self.student_name = student_name
        self.start_time = datetime.now()

    def run(self):
        print(f"\n[ {self.student_id} {self.student_name}님, 퀴즈를 시작합니다! ]\n")
        
        for i, q in enumerate(self.questions, 1):
            print(f"문제 {i}: {q.question}")
            for idx, choice in enumerate(q.choices, 1):
                print(f"  {idx}. {choice}")

            user_input = input("정답 번호: ").strip()

            # 정답 확인 및 기록
            is_correct, user_choice_text = q.check_answer(user_input)
            
            if is_correct:
                print("정답입니다! 🎉")
                self.score += 1
                status = "O"
            else:
                print(f"오답입니다. 정답은: {q.answer}")
                status = "X"
            
            # 상세 결과 로그 저장
            self.results_log.append({
                "no": i,
                "q_text": q.question,
                "user_ans": user_choice_text,
                "correct_ans": q.answer,
                "status": status,
                "example": q.example
            })
            print(f"예시: {q.example}\n")

        self.save_detailed_report()

    def save_detailed_report(self):
        # 1. 파일명 설정
        time_str = self.start_time.strftime("%Y%m%d_%H%M%S")
        file_name = f"{self.student_id}_{self.student_name}_{time_str}.txt"
        
        accuracy = (self.score / len(self.questions)) * 100

        # 2. 성적표 상단 정보
        report = f"""[ 파이썬 기초문법 학습 상세 성적표 ]
--------------------------------------------------
학번: {self.student_id}
이름: {self.student_name}
응시 시각: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
최종 점수: {self.score} / {len(self.questions)} ({accuracy:.1f}점)
--------------------------------------------------

[ 문항별 상세 분석 ]
"""
        # 3. 각 문항별 결과 추가 (반복문)
        for res in self.results_log:
            report += f"""
문제 {res['no']}. {res['q_text']}
  - 결과: [{res['status']}]
  - 당신의 선택: {res['user_ans']}
  - 실제 정답: {res['correct_ans']}
  - 상세 설명: {res['example']}
--------------------------------------------------"""

        report += "\n학습에 성공하세요! 전북과학고 파이팅! 🐍"

        # 4. 파일 저장
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"상세 성적표가 생성되었습니다: {file_name}")

# [3. 데이터 정의 및 4. 실행부는 이전과 동일하므로 생략 가능하나, 구조 유지를 위해 유지]
questions_list = [
    {"question": "파이썬에서 두 숫자의 합을 구하는 연산자는?", "choices": ["+", "-", "*", "/", "%"], "answer": "+", "example": "3 + 5 -> 8"},
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
    print("--- 전북과학고등학교 파이썬 기초문법 학습 시스템 ---")
    s_id = input("학번을 입력하세요: ").strip()
    s_name = input("이름을 입력하세요: ").strip()
    
    if s_id and s_name:
        quiz = QuizManager(questions_list, s_id, s_name)
        quiz.run()
    else:
        print("학번과 이름을 정확히 입력해야 합니다.")
