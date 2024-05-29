import pandas as pd

# 레벤슈타인 거리 계산 함수
def calc_distance(a, b):
    ''' 레벤슈타인 거리 계산하기 '''
    if a == b: return 0  # 두 문자열이 같으면 거리 0을 반환
    a_len = len(a)  # 문자열 a의 길이
    b_len = len(b)  # 문자열 b의 길이
    if a == "": return b_len  # 문자열 a가 비어 있으면 b의 길이를 반환
    if b == "": return a_len  # 문자열 b가 비어 있으면 a의 길이를 반환
    
    # 2차원 표 (a_len+1, b_len+1) 준비하기
    matrix = [[] for i in range(a_len+1)]  # 리스트 컴프리헨션을 사용하여 1차원 초기화
    for i in range(a_len+1):  # 각 행을 0으로 초기화
        matrix[i] = [0 for j in range(b_len+1)]  # 리스트 컴프리헨션을 사용하여 2차원 초기화
    
    # 0일 때 초깃값을 설정
    for i in range(a_len+1):
        matrix[i][0] = i  # 첫 열을 0, 1, 2, ..., a_len으로 설정
    for j in range(b_len+1):
        matrix[0][j] = j  # 첫 행을 0, 1, 2, ..., b_len으로 설정
    
    # 표 채우기
    for i in range(1, a_len+1):
        ac = a[i-1]  # 문자열 a의 현재 문자
        for j in range(1, b_len+1):
            bc = b[j-1]  # 문자열 b의 현재 문자
            cost = 0 if (ac == bc) else 1  # 문자가 같으면 비용 0, 다르면 1
            matrix[i][j] = min([
                matrix[i-1][j] + 1,     # 문자 제거: 위쪽에서 +1
                matrix[i][j-1] + 1,     # 문자 삽입: 왼쪽 수에서 +1   
                matrix[i-1][j-1] + cost # 문자 변경: 대각선에서 +1, 문자가 동일하면 대각선 숫자 복사
            ])
    return matrix[a_len][b_len]  # 최종 거리 반환

# 챗봇 클래스를 정의
class SimpleChatBot:
    # 챗봇 객체를 초기화하는 메서드, 초기화 시에는 입력된 데이터 파일을 로드함
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)  # 데이터 파일에서 질문과 답변을 로드

    # CSV 파일로부터 질문과 답변 데이터를 불러오는 메서드
    def load_data(self, filepath):
        data = pd.read_csv(filepath)  # CSV 파일을 읽어옴
        questions = data['Q'].tolist()  # 질문 컬럼을 리스트로 변환
        answers = data['A'].tolist()  # 답변 컬럼을 리스트로 변환
        return questions, answers  # 질문과 답변 리스트를 반환

    # 입력 문장에 가장 잘 맞는 답변을 찾는 메서드, 레벤슈타인 거리를 이용하여 가장 유사한 질문을 찾음
    def find_best_answer(self, input_sentence):
        # 레벤슈타인 거리를 계산하여 가장 가까운 질문의 인덱스를 찾음
        distances = [calc_distance(input_sentence, question) for question in self.questions]  # 각 질문과 입력 문장 간의 거리를 계산
        best_match_index = distances.index(min(distances))  # 가장 작은 거리를 가진 질문의 인덱스를 찾음
        # 가장 유사한 질문에 해당하는 답변을 반환
        return self.answers[best_match_index]

# 데이터 파일의 경로를 지정합니다.
filepath = 'ChatbotData.csv'

# 챗봇 객체를 생성합니다.
chatbot = SimpleChatBot(filepath)  # 챗봇 객체를 생성하고 초기화

# '종료'라는 입력이 나올 때까지 사용자의 입력에 따라 챗봇의 응답을 출력하는 무한 루프를 실행합니다.
while True:
    input_sentence = input('You: ')  # 사용자로부터 입력을 받음
    if input_sentence.lower() == '종료':  # '종료'를 입력하면 루프를 종료
        break
    response = chatbot.find_best_answer(input_sentence)  # 사용자 입력에 가장 유사한 질문의 답변을 찾음
    print('Chatbot:', response)  # 챗봇의 응답을 출력