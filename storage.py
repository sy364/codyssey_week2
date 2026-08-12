import json
from quiz import Quiz

class QuizStorage:
    def __init__(self,filepath='state.json'):
        self.filepath=filepath

    def load(self):
         """
        state.json을 읽어서 (quizzes, best_score, history) 튜플로 반환.
        파일이 없거나 깨졌으면 기본 퀴즈 5개 + best_score=0 + history=[] 로 반환.
        """
         try:
             with open(self.filepath,'r',encoding='utf-8')as f :
                data=json.load(f)
                best_score=data.get("best_score",0)
                history=data.get("history",[])
                quizzes=[]
                for q_data in data.get("quizzes",[]):
                    hint = q_data.get("hint", "힌트가 없습니다.")
                    quiz_obj = Quiz(q_data["question"], q_data["choices"], q_data["answer"], hint)
                    quizzes.append(quiz_obj)
                return quizzes,best_score,history

         except(FileNotFoundError,json.JSONDecodeError): 
                best_score=0
                history=[]
                quizzes=[]
                print("데이터 파일이 없거나 손상되었습니다. 기본 퀴즈 데이터로 복구합니다.")
                
                # 기본 퀴즈 데이터 5개 하드코딩
                default_quizzes = [
                    {"question": "다음 중 파이썬의 키워드가 아닌 것은?", "choices": ["def", "class", "this", "pass"], "answer": 3, "hint": "파이썬에는 객체 자신을 가리킬 때 this 대신 다른 단어(self)를 관습적으로 쓴다."},
                    {"question": "운영체제 커널의 핵심 역할이 아닌 것은?", "choices": ["프로세스 관리", "메모리 관리", "웹 브라우저 렌더링", "파일 시스템 관리"], "answer": 3, "hint": "화면을 그리는 작업은 응용 프로그램 영역(브라우저 엔진)의 역할이다."},
                    {"question": "Multi-Level Feedback Queue (MLFQ) 스케줄러의 특징으로 옳지 않은 것은?", "choices": ["I/O 작업이 많은 프로세스를 높은 우선순위로 유지한다.", "CPU 할당 시간을 모두 소모한 프로세스는 우선순위가 낮아진다.", "모든 단계의 큐(Queue)는 동일한 타임 슬라이스(Time Slice)를 갖는다.", "기아 현상(Starvation)을 막기 위해 우선순위를 상향 조정하는 에이징(Aging) 기법을 사용한다."], "answer": 3, "hint": "우선순위가 낮은 큐일수록 CPU를 한 번에 길게 쓸 수 있도록 타임 슬라이스를 크게 부여한다."},
                    {"question": "데이터베이스 트랜잭션이 안전하게 수행되기 위한 4가지 핵심 속성(ACID)에 해당하지 않는 것은?", "choices": ["Atomicity (원자성)", "Consistency (일관성)", "Isolation (격리성)", "Coupling (결합성)"], "answer": 4, "hint": "D는 Durability(지속성)를 의미한다."},
                    {"question": "파이썬(Python)의 pass 키워드에 대한 설명으로 가장 알맞은 것은?", "choices": ["반복문의 현재 순서를 건너뛰고 다음 반복으로 넘어간다.", "함수나 클래스의 실행을 즉시 종료하고 값을 반환한다.", "구문상 코드가 필요하지만 아무 동작도 하지 않아야 할 때 사용하는 자리 표시자(Null operation)이다.", "발생한 예외(Error)를 무시하고 프로그램이 계속 실행되도록 강제한다."], "answer": 3, "hint": "문법적 오류를 막기 위해 임시로 채워넣는 껍데기 역할을 한다."}
                ]
                
                for q_data in default_quizzes:
                    quiz_obj=Quiz(q_data["question"],q_data["choices"],q_data["answer"],q_data["hint"])
                    quizzes.append(quiz_obj)


                return quizzes,best_score,history
            

    def save(self,quizzes,best_score,history):
        """
        quizzes(Quiz 객체 리스트), best_score, history를 받아서 state.json에 저장.
        """
        quiz_data_list=[]
        for q in quizzes:
            quiz_data_list.append({
                    "question" : q.question,
                    "choices" : q.choices,
                    "answer" : q.answer,
                    "hint": getattr(q, 'hint', "힌트가 없습니다.")
                })

        data_to_save={
            "best_score" : best_score,
            "quizzes" : quiz_data_list,
            "history": history
        }

        with open(self.filepath,'w',encoding='utf-8') as f:
            json.dump(data_to_save,f,ensure_ascii=False,indent=4)


