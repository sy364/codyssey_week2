import json
import random
from datetime import datetime 
# 개별 퀴즈
class Quiz:
    def __init__(self, question, choices, answer, hint="힌트가 없습니다."):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def print_quiz(self):
        print(self.question)
        for choice in self.choices:
            print(choice)

    def checkAnswer(self,userAnswer):
         return userAnswer==self.answer

    
# 퀴즈 게임
class QuizGame:
    def __init__(self):
            self.quizzes=[]
            self.best_score=0
            self.loadData()

    def loadData(self):
        try:
            with open('state.json','r',encoding='utf-8')as f:
                data=json.load(f)

            self.best_score=data.get("best_score",0)
            self.history=data.get("history",[])

            for q_data in data.get("quizzes",[]):
                hint = q_data.get("hint", "힌트가 없습니다.")
                quiz_obj = Quiz(q_data["question"], q_data["choices"], q_data["answer"], hint)
                self.quizzes.append(quiz_obj)

        except(FileNotFoundError,json.JSONDecodeError): 
            self.bestScore=0
            self.history=[]
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
                self.quizzes.append(quiz_obj)
            
            # 복구된 데이터로 즉시 파일 새로 생성(덮어쓰기)
            self.save_data()

    def show_quizzes(self):
        print("\n==퀴즈 목록==")

        if not self.quizzes:
            print("현재 등록된 퀴즈가 없습니다.")
            return

        for i, quiz in enumerate(self.quizzes,1):
            print(f"\n[문제 {i}] {quiz.question}")

            for j,choice in enumerate(quiz.choices,1):
                print(f" {j}. {choice}")

    def save_data(self):
        quiz_data_list=[]
        for q in self.quizzes:
            quiz_data_list.append({
                "question" : q.question,
                "choices" : q.choices,
                "answer" : q.answer,
                "hint": getattr(q, 'hint', "힌트가 없습니다.")
            })

        data_to_save={
            "best_score" : self.best_score,
            "quizzes" : quiz_data_list,
            "history": self.history
        }

        with open('state.json','w',encoding='utf-8') as f:
            json.dump(data_to_save,f,ensure_ascii=False,indent=4)


    def add_quiz(self):
        print("\n==퀴즈 추가==")
        question=input("문제를 입력하세요: ").strip()
        if not question:
            print("입력값이 없습니다. 메뉴로 돌아갑니다. ")
            return
        choices=[]
        for i in range(1,5):
            while True:
                choice=input(f"선택지 {i}번을 입력하시오: ").strip()
                if not choice:
                    print("입력값이 없습니다. 다시 입력해주세요. ")
                    continue
                choices.append(choice)
                break
        while True:
            answer_input=input("정답번호1-4를 입력하세요: ").strip()
            hint = input("힌트를 입력하세요 (없으면 그냥 엔터): ").strip()
   
            if not answer_input:
                print("입력값이 없습니다. 다시 입력해주세요. ")
                continue
            if not hint:
                hint = "힌트가 없습니다."

            try:
                answer =int(answer_input)
                if (1<=answer<=4):
                    break
                else:
                    print("1에서 4사이의 번호만 입력 가능합니다.")
            except ValueError:
                print("숫자만 입력 가능합니다. 다시 입력해주세요.")

        new_quiz=Quiz(question,choices, answer,hint)
        self.quizzes.append(new_quiz)

        self.save_data()
        print("새로운 퀴즈가 등록되고 저장되었습니다. ")

    def play_quiz(self):
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다. 메뉴에서 퀴즈를 먼저 추가해주세요.")
            return

        total_available=len(self.quizzes)
        print(f"\n== 퀴즈 풀기 시작==")
        print(f"현재 등록된 퀴즈는 총 {total_available}개입니다.")

        while True:
            count_input=input(f"몇 문제를 푸시겠습니까? (1~{total_available}): ").strip()
            if not count_input:
                print("입력값이 없습니다.")
                continue
            try:
                num_questions=int(count_input)
                if 1<=num_questions<=total_available:
                    break
                else:
                    print(f"1에서 {total_available} 사이의 숫자를 입력해주세요.")
            except ValueError:
                print("숫자만 입력 가능합니다.")


        selected_quizzes=random.sample(self.quizzes,num_questions)

        current_score=0

        for i,quiz in enumerate(selected_quizzes,1):
            print(f"\n[문제{i}/{num_questions}]{quiz.question}")
            for j, choice in enumerate(quiz.choices,1):
                print(f"{j}.{choice}")

            hint_used = False
            while True:
                answer_input=input("정답 번호(1~4)를 입력하세요(힌트 보기: h): ").strip().lower()
                if not answer_input:
                                    print("입력값이 없습니다. 다시 입력해주세요. ")
                                    continue

                if answer_input=='h':
                    if not hint_used:
                        print(f"\n[힌트]{quiz.hint}")
                        hint_used=True
                    else:
                        print("이미 힌트를 사용했습니다. ")
                        continue
                
                try:
                    user_answer=int(answer_input)
                    if 1<=user_answer<=4:
                        break
                    else:
                        print("1에서 4 사이의 번호만 입력 가능합니다.")

                except ValueError:
                    print("숫자만 입력 가능합니다. 다시 입력해주세요.")

    
            if quiz.checkAnswer(user_answer):
                print("정답입니다!")
                if hint_used:
                    print("(힌트 사용으로 0.5점만 인정됩니다.)")
                    current_score += 0.5
                else:
                    current_score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다. ")

        print(f"\n퀴즈 완료! 최종 점수:{current_score}/{num_questions}")
        if current_score>self.best_score:
            print(f"신기록 달성!(이전 최고 점수:{self.best_score})")
            self.best_score=current_score

        # 점수 기록 히스토리 추가
        play_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = {
            "date": play_date,
            "total": num_questions,
            "score": current_score
        }
        self.history.append(record)

        self.save_data()

    def show_score(self):
        print(f"\n현재까지의 역대 최고 점수는 {self.best_score}점 입니다.")
        print("\n=== 최근 플레이 기록 ===")
        
        if not self.history:
            print("아직 플레이 기록이 없습니다.")
            return

        #최근 기록 우선순   
        for i, record in enumerate(reversed(self.history), 1):
            print(f"[{i}] {record['date']} - {record['score']} / {record['total']}점")

    def delete_quiz(self):
        print("\n=== 퀴즈 삭제 ===")
        if not self.quizzes:
            print("현재 등록된 퀴즈가 없습니다.")
            return

        self.show_quizzes()

        while True:
            del_input=input("\n삭제할 퀴즈 번호를 입력하세요(취소: 0): ").strip()
            if not del_input:
                continue
            try:
                del_idx=int(del_input)
                if del_idx==0:
                    print("삭제를 취소합니다. ")
                    break

                if 1<=del_idx<=len(self.quizzes):
                    self.delete_quiz=self.quizzes.pop(del_idx-1)
                    self.save_data()
                    print(f"'{self.delete_quiz.qustion}' 퀴즈가 삭제되었습니다. ")
                    break
                else:
                    print("목록에 있는 올바른 번호를 입력해주세요.")
            except ValueError:
                print("숫자만 입력 가능합니다. ")



def main():
    game=QuizGame()
#메뉴 화면
    while True:
        print("\n==Quiz 메뉴==")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 종료")

        choice=input("메뉴 선택: ").strip()
#미선택시
        if not choice:
            print("메뉴가 선택되지 않았습니다. 다시 선택해주세요.")
            continue
#입력 오류
        try:
            choice=int(choice)
        except ValueError:
            print("숫자만 입력 가능합니다. 다시 선택해주세요. ") 
            continue

#메뉴별 실행
        if choice==1:
            print("퀴즈 풀기")
            game.play_quiz()


        elif choice==2:
            print("퀴즈 추가")
            game.add_quiz()

        elif choice==3:
            print("퀴즈 목록")
            game.show_quizzes()

        elif choice==4:
            print("점수 확인")
            game.show_score()

        elif choice==5:
            print("퀴즈 삭제")
            game.delete_quiz()

        elif choice==6:
            print("게임을 종료합니다.")
            break

        else:
            print("1에서 6사이의 올바른 번호를 선택해주세요.")

if __name__=="__main__":
    try:
        main()
    except(KeyboardInterrupt,EOFError):
        print("\n입력 스트림 종료가 감지되었습니다. 프로그램을 안전하게 종료합니다.")

