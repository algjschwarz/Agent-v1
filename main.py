from datetime import datetime
import agent
import memory

def main():
    memory.index_all_scripts()
    creator = agent.Agent(
        f'You act one step at a time, tool results come back and you continue, If recall_scripts returns a script similar to what you are about to write call the tool "read_file" to check if it is sufficient. Else you write Python code and test it by executing it. Make sure to specifiy return types for functions. Today is {datetime.now()}.',
        role_name="Creator",
        thinking=True,
        tools=agent.creator_tools
    )
    grader = agent.Grader(
        f'Create a plan to test a program, execute those tests and then call the tool "grade" if all tests pass, send True else send false.',
        role_name="Grader",
        thinking=True,
        tools=agent.grader_tools
    )
    creator.new_input("make a simple game", recall_enabled=True)
    grader.grade(creator)
    grader.new_input(input(), recall_enabled=False)

if __name__ == "__main__":
    main()

