#import libraries

import os
from groq import Groq
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
import time
import pandas as pd

import streamlit as st
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

def write_app(app_name:str, app_code_raw:str) -> str:
    if not os.path.exists(app_name) and app_name != '':
                os.makedirs(app_name)  

    pattern = r'```(.*)```'
    app_match = re.search(pattern, app_code_raw, re.DOTALL)
    
    if app_match:
        text_inside_backticks = app_match.group(1).strip()
        with open(f'{app_name}/app.py', 'w') as f:
            f.write(text_inside_backticks)  
    
def write_model(app_name: str, sql_code_raw:str) -> str:

    if not os.path.exists(app_name) and app_name != '':
                os.makedirs(app_name)

    pattern = r'```(.*)```'
    sql_match = re.search(pattern, sql_code_raw, re.DOTALL)

    if sql_match:
        text_inside_backticks = sql_match.group(1).strip()
        with open(f'{app_name}/models.py', 'w') as f:
            f.write(text_inside_backticks)
        
def write_template(app_name: str, frontend_code_raw:str) -> list:

    if not os.path.exists(os.path.join(app_name, 'templates')):
         os.makedirs(os.path.join(app_name, 'templates'))

    pattern_f = r'\*\*(.*?)\*\*'
    pattern_c = r'```(.*?)```'
    f_names = re.findall(pattern_f, frontend_code_raw, re.DOTALL)
    f_codes = re.findall(pattern_c, frontend_code_raw, re.DOTALL)

    assert len(f_names) == len(f_codes)

    for file, code in zip(f_names, f_codes):
         with open(f'{app_name}/templates/{file}', 'w') as f:
              f.write(code)

def initial(requirement:str):

    #Dividing task and Agent for Individual Task
    planning_agent = Agents.Planning_Agent(llm=llm)
    sql_agent = Agents.sql_agent(llm=llm)
    frontend_agent = Agents.frontend_agent(llm=llm)
    app_agent = Agents.app_agent(llm=llm)

    planning_task = Tasks.planning_Task(agent=planning_agent, requirement= requirement)
    
    planning_crew = Crew(
            agents=[planning_agent], 
            tasks=[planning_task],
            verbose=1
        )
    planning = planning_crew.kickoff()

    yield f'Here is the Technical Architecutre Planning for {requirement}\n\n\n'
    yield planning

    sql_task = Tasks.sql_Task(agent=sql_agent, requirement=planning)
    app_task = Tasks.app_development_task(agent=app_agent, requirement=planning)
    frontend_task = Tasks.frontend_task(agent=frontend_agent, requirement=planning)

    sql_crew = Crew(
            agents=[sql_agent],
            tasks=[sql_task], 
            verbose=1
        )

    sql_code = sql_crew.kickoff()
    yield f'Here is the models.py code for application ...\n\n\n'
    yield sql_code
    write_model('Sample', sql_code_raw=sql_code)
    
    app_crew = Crew(
                agents=[app_agent],
                tasks=[app_task], 
                verbose=1
            )
    
    app_code = app_crew.kickoff()
    
    yield f'Here is the app.py code for application ...\n\n\n'
    yield app_code
    write_app('Sample', app_code_raw=app_code)
    
    frontend_crew = Crew(
                agents=[frontend_agent],
                tasks=[frontend_task], 
                verbose=1
            )

    frontend_code = frontend_crew.kickoff()
    print('\n\nfuck\n',frontend_code, '\n\n\n')
    yield f'Here are the templates ...\n\n\n'
    yield frontend_code
    write_template('Sample', frontend_code_raw=frontend_code)

    time.sleep(10)
    #Testing
    Junit_Agent = Agents.Junit_Agent(llm)
    Integration_Agent = Agents.Integration_Testing_Agent(llm)
    End2End_Agent = Agents.end2end_Testing_Agent(llm)

    Junit_Task = Tasks.JUnitTestingTask(Junit_Agent, planning)
    Integration_Task = Tasks.IntegrationTestingTask(Integration_Agent, planning)
    End2End_Task = Tasks.End2EndTestingTask(End2End_Agent, planning)

    Junit_Crew = Crew(
                agents=[Junit_Agent],
                tasks=[Junit_Task], 
                verbose=1
            )
    
    Junit_Test_raw = Junit_Crew.kickoff()
    yield Junit_Test_raw

    Integration_Crew = Crew(
                agents=[Integration_Agent],
                tasks=[Integration_Task], 
                verbose=1
            )
    
    Integration_Crew = Integration_Crew.kickoff()
    yield Integration_Crew

    End2End_Crew = Crew(
                agents=[End2End_Agent],
                tasks=[End2End_Task], 
                verbose=1
            )
    
    End2End_Crew = End2End_Crew.kickoff()
    yield End2End_Crew


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
    #load_dotenv()
    st.set_page_config(page_title="DevGenie")
    st.title("DevGenie💁 ")
    st.subheader("I can help you in Flask App Development")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    if prompt := st.chat_input("Please Enter your Requirement?"):
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({"role":"user", "content":prompt})

        with st.chat_message("assistant"):
            for result in initial(prompt):
                st.write(result)
                st.session_state.messages.append({"role":"assistant", "content":result})

        st.success("Hope, I was able to help you ❤️")


#Invoking main function
if __name__ == '__main__':
    main()