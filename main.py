import json

# 개별 퀴즈
class Quiz:
    def __init__(self,question,choices,answer):
        self.question=question
        self.choices=choices
        self.answer=answer

    def print_quiz(self):
        print(self.question)
        for choice in self.choices:
            print(choice)

    def checkAnswer(self,userAnswer):
         return userAnswer==self.answer

    
# 퀴즈 게임
class QuizGame:
    def __init__(self,quizzes,bestScore):
            self.quizzes=[]
            self.bestScore=0
            self.loadDate()

    def loadData(self):
        try:
            with open('state.json','r',encoding='utf-8')as f:
                data=json.load(f)

            self.bestScore=data.get("best_score",0)

            for q_data in data.get("quizzes",[]):
                quiz_obj=Quiz(q_data["question"],q_data["choices"],q_data["answer"])
                self.quizzes.append(quiz_obj)

        except(FileNotFoundError,json.JSONDecodeError): 
            self.bestScore=0
            print("데이터를 불러오지 못했습니다. 기본 설정으로 시작합니다.")

    def show_quizzes(self):
        print("\n==퀴즈 목록==")

        if not self.quizzes:
            print("현재 등록된 퀴즈가 없습니다.")
            return

        for i, quiz in enumerate(self.quizzes,1):
            print("f\n[문제 {i}] {quiz.question}")

            for j,choice in enumerate(quiz.choice,1):
                print(f" {j}. {choice}")

    def save_date(self):
        quiz_data_list=[]
        for q in self.quizzes:
            quiz_data_list.append({
                "question" : q.question,
                "choices" : q.choices,
                "answer" : q.answer
            })

        data_to_save={
            "best_score" : self.bestScore
            "quizzes" : quiz_data_list
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

            if not answer_input:
                print("입력값이 없습니다. 다시 입력해주세요. ")
                continue

            try:
                answer =int(answer_input)
                if (1<=answer<=4):
                    break
                else:
                    print("1에서 4사이의 번호만 입력 가능합니다.")
            except ValueError:
                print("숫자만 입력 가능합니다. 다시 입력해주세요.")

            new_quiz=Quiz(question,choices, answer)
            self.quizzes.append(new_quiz)

            self.save_data()
            print("새로운 퀴즈가 등록되고 저장되었습니다. ")

    def play_quiz(self):
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다. 메뉴에서 퀴즈를 먼저 추가해주세요.")
            return

        print("\n===퀴즈 풀기 시작===")
        current_score=0
        total_quizzes=len(self.quizzes)

        for i,quiz in enumerate(self.quizzes,1):
            print(f"\n[문제 {i}/{total_quizzes}]{quiz.question}")

            for j,choice in enumerate(quiz.choices,1):
                print(f" {j}.{choice}")

            while True:
                answer_input=input("정답 번호(1~4)를 입력하세요: ").strip()
                if not answer_input:
                    print("입력값이 없습니다. 다시 입력해주세요. ")
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
                    current_score+=1
                else:
                    print(f"오답입니다. 정답은 {quiz.answer}번입니다. ")

            print(f"\n퀴즈 완료! 최종 점수:{current_score}/{total_quizzes}")
            if current_score>self.best_score:
                print(f"신기록 달성!(이전 최고 점수:{self.best_score})")
                self.best_score=current_score
                self.save_data()

    def show_score(self):
        print(f"\n현재까지의 역대 최고 점수는 {self.bestScore}점 입니다.")

    


def main():
    game=QuizGame()
#메뉴 화면
    while True:
        print("\n==Quiz 메뉴==")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")

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
            print("게임을 종료합니다.")
            break

        else:
            print("1에서 5사이의 올바른 번호를 선택해주세요.")

if __name__=="__main__":
    try:
        main()
    except(KeyboardInterrupt,EOFError):
        print("\n입력 스트림 종료가 감지되었습니다. 프로그램을 안전하게 종료합니다.")

