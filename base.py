#not in use

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq

import re
from agents import Agents
from tasks import Tasks

load_dotenv()

APP_NAME = ''


llm = ChatGroq(
            temperature=0,
            groq_api_key = os.environ.get("GROQ_API_KEY"),
            model_name='llama3-70b-8192'
        )

def make_app(app_name: str, sql_code_raw, app_code_raw, frontend_code_raw):

    if not os.path.exists(app_name) and app_name != '':
                os.makedirs(app_name)

    if not os.path.exists(os.path.join(app_name, 'templates')):
         os.makedirs(os.path.join(app_name, 'templates'))

    os.system(f'touch {app_name}/app.py')
    os.system(f'touch {app_name}/models.py')

    pattern = r'```(.*)```'
    sql_match = re.search(pattern, sql_code_raw, re.DOTALL)

    if sql_match:
        text_inside_backticks = sql_match.group(1).strip()
        with open(f'{app_name}/models.py', 'w') as f:
            f.write(text_inside_backticks)
        
    app_match = re.search(pattern, app_code_raw, re.DOTALL)

    if app_match:
        text_inside_backticks = app_match.group(1).strip()
        with open(f'{app_name}/app.py', 'w') as f:
            f.write(text_inside_backticks)

    pattern_f = r'\*\*(.*?)\*\*'
    pattern_c = r'```(.*?)```'

    f_names = re.findall(pattern_f, frontend_code_raw, re.DOTALL)
    f_codes = re.findall(pattern_c, frontend_code_raw, re.DOTALL)

    assert len(f_names) == len(f_codes)

    for file, code in zip(f_names, f_codes):
         with open(f'{app_name}/templates/{file}', 'w') as f:
              f.write(code)


def initial():

    #Dividing task and Agent for Individual Task
    planning_agent = Agents.Planning_Agent()
    sql_agent = Agents.sql_agent()
    frontend_agent = Agents.frontend_agent()
    app_agent = Agents.app_agent()


    planning_task = Tasks.planning_Task(agent=planning_agent, requirement= 'ToDoList App')
    
    planning_crew = Crew(
            agents=[planning_agent], 
            tasks=[planning_task],
            verbose=1
        )
    planning = planning_crew.kickoff()

    sql_task = Tasks.sql_Task(agent=sql_agent, requirement=planning)
    app_task = Tasks.app_development_task(agent=app_agent, requirement=planning)
    frontend_task = Tasks.frontend_task(agent=frontend_agent, requirement=frontend_task)


    sql_crew = Crew(
            agents=[sql_agent],
            tasks=[sql_task], 
            verbose=1
        )

    sql_code = sql_crew.kickoff()

    app_crew = Crew(
                agents=[app_agent],
                tasks=[app_task], 
                verbose=1
            )
    
    app_code = app_crew.kickoff()

    frontend_crew = Crew(
                agents=[frontend_agent],
                tasks=[frontend_task], 
                verbose=1
            )

    frontend_code = frontend_crew.kickoff()

    make_app(APP_NAME, sql_code_raw=sql_code, app_code_raw=app_code, frontend_code_raw=frontend_code)

def write_debugged_code(code_raw, file_name):
    pattern = r'```(.*)```'
    app_match = re.search(pattern, code_raw, re.DOTALL)
    if app_match:
        text_inside_backticks = app_match.group(1).strip()
        with open(file_name, 'w') as f:
            f.write(text_inside_backticks)

def debugging():

    with open(os.path.join(APP_NAME, 'app.py')) as f:
         app_code = f.read()

    with open(os.path.join(APP_NAME, 'models.py')) as f:
         model_code = f.read()

    debugging_agent = Agents.debugger_agent(llm)
    app_debugging_task = Tasks.app_debugging_task(debugging_agent, model_code, app_code)

    debugged_crew = Crew(
            agents=[debugging_agent], 
            tasks=[app_debugging_task], 
            verbose=1
        )

    debugged_code = debugged_crew.kickoff()
    write_debugged_code(debugging_agent, APP_NAME + '/app.py')


    #templates debugging
    templates_file = os.listdir(os.path.join(APP_NAME, 'templates'))

    for file in templates_file:
        with open(file) as f:
            html_content = f.read()

        template_debugging_task = Tasks.template_debugging_task(debugging_agent, model_code, app_code, file, html_content)
        debugged_crew = Crew(
            agents=[debugging_agent], 
            tasks=[template_debugging_task], 
            verbose=1
        )

        debugged_code = debugged_crew.kickoff()
        write_debugged_code(debugging_agent, APP_NAME + '/templates' +f'/{file}')


def main():
    initial()
    debugging()



if __name__ == '__main__':
    main()