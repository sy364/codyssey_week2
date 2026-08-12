import json
import random
from quiz import Quiz 
from datetime import datetime 
from storage import QuizStorage
# 퀴즈 게임
class QuizGame:
    def __init__(self):
            self.storage=QuizStorage()
            self.quizzes,self.best_score,self.history=self.storage.load()
            self.save_data()

    def save_data(self):
        self.storage.save(self.quizzes,self.best_score,self.history)

    def show_quizzes(self):
        print("\n==퀴즈 목록==")

        if not self.quizzes:
            print("현재 등록된 퀴즈가 없습니다.")
            return

        for i, quiz in enumerate(self.quizzes,1):
            print(f"\n[문제 {i}] {quiz.question}")

            for j,choice in enumerate(quiz.choices,1):
                print(f" {j}. {choice}")


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
                    self.deleted_quiz=self.quizzes.pop(del_idx-1)
                    self.save_data()
                    print(f"'{self.deleted_quiz.question}' 퀴즈가 삭제되었습니다. ")
                    break
                else:
                    print("목록에 있는 올바른 번호를 입력해주세요.")
            except ValueError:
                print("숫자만 입력 가능합니다. ")

