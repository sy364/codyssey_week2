from quiz_game import QuizGame
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

