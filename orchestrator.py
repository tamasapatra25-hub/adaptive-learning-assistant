from agents.planner_agent import create_planner_agent, generate_learning_path
from agents.rag_agent import create_rag_agent, query_rag_agent
from agents.feedback_agent import create_feedback_agent, evaluate_answer, generate_quiz
from agents.progress_tracker import create_progress_tracker, update_learner_state, get_progress_report


class LearningOrchestrator:
    def __init__(self):
        print("Initializing Adaptive Learning Assistant...")
        print("Creating agents...")

        self.planner_client, self.planner = create_planner_agent()
        self.rag_client, self.rag = create_rag_agent()
        self.feedback_client, self.feedback = create_feedback_agent()
        self.progress_client, self.progress = create_progress_tracker()

        print("All agents ready!\n")

    def onboard_learner(self, name, topic, level):
        print(f"\n{'='*60}")
        print(f"Welcome, {name}! Let's create your learning path.")
        print(f"Topic: {topic} | Level: {level}")
        print(f"{'='*60}\n")

        print("Generating your personalized learning path...")
        path = generate_learning_path(self.planner_client, self.planner, name, topic, level)
        print(path)
        return path

    def teach_topic(self, topic):
        print(f"\n{'='*60}")
        print(f"Retrieving content for: {topic}")
        print(f"{'='*60}\n")

        content = query_rag_agent(self.rag_client, self.rag, topic)
        print(content)
        return content

    def quiz_learner(self, topic):
        print(f"\n{'='*60}")
        print(f"Quiz time! Topic: {topic}")
        print(f"{'='*60}\n")

        quiz = generate_quiz(self.feedback_client, self.feedback, topic)
        print(quiz)
        return quiz

    def check_answer(self, topic, question, answer, learner_name):
        print(f"\n{'='*60}")
        print(f"Evaluating your answer...")
        print(f"{'='*60}\n")

        feedback = evaluate_answer(self.feedback_client, self.feedback, topic, question, answer)
        print(feedback)

        score = 5
        if feedback:
            for line in feedback.split('\n'):
                if 'score' in line.lower() and '/10' in line:
                    try:
                        score = int(''.join(filter(str.isdigit, line.split('/10')[0][-2:])))
                    except:
                        pass

        update_learner_state(learner_name, topic, score)
        return feedback

    def show_progress(self, learner_name):
        print(f"\n{'='*60}")
        print(f"Progress Report for {learner_name}")
        print(f"{'='*60}\n")

        report = get_progress_report(self.progress_client, self.progress, learner_name)
        print(report)
        return report

    def cleanup(self):
        print("\nCleaning up agents...")
        self.planner_client.delete_agent(self.planner.id)
        self.rag_client.delete_agent(self.rag.id)
        self.feedback_client.delete_agent(self.feedback.id)
        self.progress_client.delete_agent(self.progress.id)
        print("All agents deleted.")


def main():
    orchestrator = LearningOrchestrator()

    try:
        name = input("Enter your name: ")
        topic = input("What topic are you interested in? (e.g., Semantic Kernel, RAG, multi-agent systems): ")
        level = input("Your level (beginner/intermediate/advanced): ")

        orchestrator.onboard_learner(name, topic, level)

        while True:
            print(f"\n{'='*60}")
            print("What would you like to do?")
            print("1. Learn a topic (RAG retrieval)")
            print("2. Take a quiz")
            print("3. Check my answer")
            print("4. View progress report")
            print("5. Exit")
            print(f"{'='*60}")

            choice = input("Enter choice (1-5): ").strip()

            if choice == "1":
                t = input("Enter topic to learn: ")
                orchestrator.teach_topic(t)
            elif choice == "2":
                t = input("Enter topic for quiz: ")
                orchestrator.quiz_learner(t)
            elif choice == "3":
                t = input("Topic: ")
                q = input("Question: ")
                a = input("Your answer: ")
                orchestrator.check_answer(t, q, a, name)
            elif choice == "4":
                orchestrator.show_progress(name)
            elif choice == "5":
                break
            else:
                print("Invalid choice. Try again.")

    finally:
        orchestrator.cleanup()


if __name__ == "__main__":
    main()