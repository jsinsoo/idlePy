import math

# 1. 개별 문제의 정보를 담는 클래스
class Question:
    def __init__(self, question, choices, answer, example):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.example = example

    def check_answer(self, user_input):
        """사용자가 입력한 번호가 정답인지 확인"""
        try:
            index = int(user_input) - 1
            return self.choices[index] == self.answer
        except (ValueError, IndexError):
            return False

# 2. 퀴즈 시스템을 관리하는 클래스
class QuizManager:
    def __init__(self, questions_data):
        # 외부에서 전달받은 데이터를 Question 객체 리스트로 변환하여 저장
        self.questions = [Question(**q) for q in questions_data]
        self.score = 0
        self.total_questions = len(self.questions)

    def run(self):
        print("파이썬 기초문법 객관식 퀴즈에 오신 것을 환영합니다!\n")
        
        for i, q in enumerate(self.questions, 1):
            print(f"문제 {i}: {q.question}")
            for idx, choice in enumerate(q.choices, 1):
                print(f"  {idx}. {choice}")

            user_input = input("정답 번호를 입력하세요: ").strip()

            if q.check_answer(user_input):
                print("정답입니다! 🎉")
                self.score += 1
            else:
                print(f"오답입니다. 정답은: {q.answer}")
            
            print(f"예시: {q.example}\n")

        self.display_final_result()

    def display_final_result(self):
        accuracy = (self.score / self.total_questions) * 100
        print(f"총 점수: {self.score}/{self.total_questions}")
        print(f"정답률: {accuracy:.1f}점 입니다.")
        print("퀴즈가 끝났습니다. 파이썬 학습에 성공하세요! 🐍")

# 3. 데이터 정의 (questions 리스트는 클래스 외부나 메인 함수에 위치)
questions_list = [
    {
        "question": "파이썬에서 두 숫자의 합을 구하는 연산자는?",
        "choices": ["+", "-", "*", "/", "%"],
        "answer": "+",
        "example": "3 + 5 -> 8"
    },
    {
        "question": "문자열 'hello'의 길이를 반환하는 함수는?",
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
    quiz = QuizManager(questions_list)
    quiz.run()
