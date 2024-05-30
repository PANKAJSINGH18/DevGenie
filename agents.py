from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq


class Agents:

    def Planning_Agent(llm):
        return  Agent(
        role='Problem_Definition_Agent',
        goal="""Give the Technical Planning for the developer""",
        backstory="""You are an expert in Planning of SDLC Flask App lifecycle.
        You define all of the functions in detail that needs to be implemented in app.py file.
        You define the models.py file in detail according to the requirement.
        You define the template and it's files in detail for UI.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    def sql_agent(llm):
        return  Agent(
        role='Sql Developer',
        goal="""Go through the Technical details and create models.py file for flask app.""",
        backstory="""You are an expert in understanding requirement and developing database design for Flask SDLC.
        You are expert in creation of models.py file for the given requirement""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    def frontend_agent(llm):
        return Agent(
        role='Frontend Developer',
        goal="""Go through the Technical Architecture and write html files for flask application.""",
        backstory="""You are an expert in Frontend development of flask application.
        You are an expert in understanding the technical architecture of flask application and designing beautiful frontend.
        You are expert in writing the respective files inside template directory of flask application.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )


    def app_agent(llm):
        return Agent(
        role='Developer',
        goal="""Go through the Technical Architecture and Write the code for app.py for flask application""",
        backstory="""You are an expert in understanding requirement and developing code of SDLC Flask App lifecycle.
        You are expert in writing app.py file of flask application and for connecting it to the database.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    def debugger_agent(llm):
        return  Agent(
            role='Flask App Debugger',
            goal="""Go through the Files and make the changes as stated for flask Application""",
            backstory="""You are an expert in understanding the code dependencies and debugging of Flask App.
            You are experienced in debugging and correcting the code for flask application.""",
            verbose=True,
            allow_delegation=False,
            llm=llm,
        )
    

    #Testing
    def Junit_Agent(llm):
        return  Agent(
            role='Junit Tester',
            goal="""Write a set of JUnit test in python cases that cover different scenarios for Flask app""",
            backstory="""You are an expert in Junit testing of the Flask Application.
            You are experienced in writing the Junit code for flask application.""",
            verbose=True,
            allow_delegation=False,
            llm=llm,
        )
    
    def Reference_Testing_Agent(llm):
        return  Agent(
            role='Reference Tester',
            goal="""Write the detail reference documentation guide for flask application""",
            backstory="""The reference documentation agent will create a reference document that explains how to use the Flask application.
            You are an expert in Reference testing of the Flask Application.
            You are experienced in writing detailed reference guide with instructions on how to interact with your app for flask application.""",
            verbose=True,
            allow_delegation=False,
            llm=llm,
        )
    
    def System_Testing_Agent(llm):
        return  Agent(
            role='System Tester',
            goal="""Write the System Testing for flask application""",
            backstory="""You are expert in system testing and  will perform system testing on the Flask application.""",
            verbose=True,
            allow_delegation=False,
            llm=llm,
        )
    
    def Integration_Testing_Agent(llm):
        return  Agent(
            role='Integration Tester',
            goal="""Write the System Testing in python for flask application""",
            backstory="""Integration testing is a set of test cases that verify the interaction between different components of your app.
            You are expert in Integration testing and  will perform Integration test for the Flask application.""",
            verbose=True,
            allow_delegation=False,
            llm=llm,
        )
    
    def end2end_Testing_Agent(llm):
        return  Agent(
            role='End2End Tester',
            goal="""Write the End2End Testing in python for flask application""",
            backstory="""E2E tests simulate real user interactions.
            You are an expert in E2E testing and will perform End2End test for the Flask application.""",
            verbose=True,
            allow_delegation=False,
            llm=llm,
        )