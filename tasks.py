from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
from textwrap import dedent


class Tasks:
    
    def planning_Task(agent, requirement):
        return Task(
                description="""Clarify and define the technical details for developer for flask Application.
                    Describe the requirement to implement app.py, models.py and templates in flask application.
                    Consider Login, Register of account if applicable and extended functionalities.

                    Here is the user's Requirement:

                    {requirement}
                    """.format(requirement=requirement),
                agent=agent,
                expected_output="The detailed architecture of the requirement for the code development."
            )

    def sql_Task(agent, requirement):
        return Task(
            description="""Conider the FLask Application Technical Architecture.
                Create the models.py file only for creating database and tables to build the App as Planned.
                The Database should include all necessary tables to run the app.

                Here is the Technical Planning:

                {requirement}
                """.format(requirement=requirement),
            agent=agent,
            expected_output="The models.py code only according to the architecure of flask application"
        )

    def frontend_task(agent, requirement):
        return Task(
            description="""Consider the Technical Architecture of Flask Application as requirement.
                Write the html code to build the App as Planned.
                The Frontend should have a beautiful Design
                
                Here is the Technical Planning:

                {requirement}
                """.format(requirement=requirement),
            agent=agent,
            expected_output="the code of beautiful UI with html files for flask application"
        )
    
    def app_development_task(agent, requirement):
        return Task(
            description="""Consider the Technical Architecture of Flask Application as requirement.
                Write the app.py code to build the App as Planned. It should be runnable on port 5000.
                
                Here is the Technical Planning:

                {requirement}
                """.format(requirement=requirement),
            agent=agent,
            expected_output="The app.py code only according to the architecure of flask application"
        )

    def app_debugging_task(agent, sql_code_from_file, app_code_from_file):
        return Task(
            description="""Consider the Models.py file and App.py file code of Flask Application.
                Write the app.py code again by making the changes required according to models.py file.
                
                Here is the Models.py file:

                {model}


                Here is the app.py file:

                {app}
                """.format(model=sql_code_from_file, app=app_code_from_file),
            agent=agent,
            expected_output="The corrected app.py code of flask application."
        )


    def template_debugging_task(agent, sql_code_from_file, app_code_from_file, template_file, template_code):
        return Task(
            description="""Consider the Models.py file and App.py file code of Flask Application.
                Write the {file} code again by making the changes required according to models.py and app.py file.
                
                Here is the Models.py file:

                {model}


                Here is the app.py file:

                {app}

                Here is the {file} file:

                {code}
                """.format(model=sql_code_from_file, app=app_code_from_file, file=template_file, code=template_code),
            agent=agent,
            expected_output=f"The corrected {template_file} code of flask application."
        )
    
    #Testing
    def JUnitTestingTask(agent, requirement):
        return Task(
            description=dedent(f"""Consider the Architecture Planning for the Flask Application.
                
                Write the Junit test cases using python for the Flask application.

                Here is the Technical Planning:

                {requirement}
                """),
            agent=agent,
            expected_output=f"A set of JUnit test cases that cover different scenarios for your Flask app."
        )
    
    def ReferenceTestingTask(agent, requirement):
        return Task(
            description="""Consider the Architecture Planning for the Flask Application.
                
                Create a reference document that explains how to use the Flask application.

                Here is the Technical Planning:

                {requirement}
                """.format(requirement=requirement),
            agent=agent,
            expected_output=f"A detailed reference guide with instructions on how to interact with your app."
        )
    
    def SystemTestingTask(agent, requirement):
        return Task(
            description="""Consider the Architecture Planning for the Flask Application.
                
                Perform system testing on the Flask application.

                Here is the Technical Planning:

                {requirement}
                """.format(requirement=requirement),
            agent=agent,
            expected_output=f"A report detailing the results of system tests, including any issues or bugs found."
        )
    
    def IntegrationTestingTask(agent, requirement):
        return Task(
            description="""Consider the Architecture Planning for the Flask Application.
                
                Write integration test cases using python for Flask app.

                Here is the Technical Planning:

                {requirement}
                """.format(requirement=requirement),
            agent=agent,
            expected_output=f"A set of Integration test cases that verify the interaction between different components of flask app."
        )
    
    def End2EndTestingTask(agent, requirement):
        return Task(
            description="""Consider the Architecture Planning for the Flask Application.
                
                Write End 2 End test cases using python for the Flask app.

                Here is the Technical Planning:

                {requirement}
                """.format(requirement=requirement),
            agent=agent,
            expected_output=f"A set of  End2End test cases that verify the interaction between different components of flask app."
        )