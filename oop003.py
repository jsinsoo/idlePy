import math
from datetime import datetime  # 시간 기록을 위해 추가

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
            return self.choices[index] == self.answer
        except (ValueError, IndexError):
            return False

# 2. 퀴즈 시스템 및 성적표 생성을 관리하는 클래스
class QuizManager:
    def __init__(self, questions_data, student_id, student_name):
        self.questions = [Question(**q) for q in questions_data]
        self.score = 0
        self.total_questions = len(self.questions)
        self.student_id = student_id
        self.student_name = student_name
        self.start_time = datetime.now() # 응시 시작 시간 저장

    def run(self):
        print(f"\n[ {self.student_id} {self.student_name}님, 퀴즈를 시작합니다! ]\n")
        
        for i, q in enumerate(self.questions, 1):
            print(f"문제 {i}: {q.question}")
            for idx, choice in enumerate(q.choices, 1):
                print(f"  {idx}. {choice}")

            user_input = input("정답 번호: ").strip()

            if q.check_answer(user_input):
                print("정답입니다! 🎉")
                self.score += 1
            else:
                print(f"오답입니다. 정답은: {q.answer}")
            print(f"예시: {q.example}\n")

        self.save_report() # 퀴즈 종료 후 성적표 저장

    def save_report(self):
        # 1. 파일명 생성 (학번_이름_응시시각)
        # 시각 형식: YYYYMMDD_HHMMSS (파일명에 콜론 : 사용 불가 방지)
        time_str = self.start_time.strftime("%Y%m%d_%H%M%S")
        file_name = f"{self.student_id}_{self.student_name}_{time_str}.txt"
        
        accuracy = (self.score / self.total_questions) * 100

        # 2. 성적표 내용 구성 및 파일 쓰기
        report_content = f"""[ 파이썬 기초문법 퀴즈 성적표 ]
----------------------------------
학번: {self.student_id}
이름: {self.student_name}
응시 시각: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
----------------------------------
맞은 개수: {self.score} / {self.total_questions}
최종 점수: {accuracy:.1f}점
----------------------------------
학습에 성공하세요! 🐍
"""
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(report_content)
        
        print(f"성적표가 생성되었습니다: {file_name}")
        print(f"최종 결과: {accuracy:.1f}점")

# 3. 데이터 정의
questions_list = [
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
    ]

# 4. 실행부
if __name__ == "__main__":
    print("--- 전북과학고등학교 파이썬 기초문법 학습 시스템 ---")
    s_id = input("학번을 입력하세요: ").strip()
    s_name = input("이름을 입력하세요: ").strip()
    
    if s_id and s_name:
        quiz = QuizManager(questions_list, s_id, s_name)
        quiz.run()
    else:
        print("학번과 이름을 정확히 입력해야 합니다.")
