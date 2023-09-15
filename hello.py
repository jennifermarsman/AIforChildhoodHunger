import time
import gradio as gr
import numpy as np
import json
from prototype import chat
from constants import states

def buildInfoAboutUserFromQues1(zipCode, kidsBelow5, kidsAbove5Below18):
        promptInfo = "My zipcode is " + zipCode + " and have " + kidsBelow5 + " kids below 5 and " + kidsAbove5Below18 + " kids above 5 below 18. "
        return promptInfo

def buildInfoAboutUserFromQues2(enrolled):
        promptInfo = "I am enrolled in " + enrolled + ". "
        return promptInfo

def buildInfoAboutUserFromQues3(householdSize, housholdAbove60, usCitizen, jobOrSelfEmpIncome, otherSourcesIncome, collegeStudies, ageBucket, pregnancyStatus, childrenAgeStatus):
        promptInfo = "My household size is " + householdSize + " and " + housholdAbove60 + ", for people in my household above 60. " + '.'.join(usCitizen) + ". " + jobOrSelfEmpIncome + " is my income from my job. " + otherSourcesIncome + " is my income from other sources." + collegeStudies + ", for am I enrolled in college." + '.'.join(ageBucket) + ". " + pregnancyStatus + ", for am I pregnant." + childrenAgeStatus + ", for do I have children below 5."
        return promptInfo


def nextQuestionnaire2(check, promptInfo):
        enrolled = check
        questionnairePage3 = gr.update(visible=True)
        questionnairePage2 = gr.update(visible=False)
        #promptInfo += buildInfoAboutUserFromQues2(enrolled)
        print(promptInfo)
        return questionnairePage3, questionnairePage2, enrolled, promptInfo

def nextQuestionnaire1(ques1Input, ques2Input, ques3Input, promptInfo):
        zipCode = ques1Input
        kidsBelow5 = ques2Input
        kidsAbove5Below18 = ques3Input
        # prompt = ques1 + " " + ques2 + " " + ques3
        # print(prompt)
        introQuestionnaire = gr.update(visible=False)
        questionnairePage2 = gr.update(visible=True)
        promptInfo += buildInfoAboutUserFromQues1(zipCode, kidsBelow5, kidsAbove5Below18)
        print(promptInfo)
        return introQuestionnaire, questionnairePage2, zipCode, kidsBelow5, kidsAbove5Below18, promptInfo

def start():
        introQuestionnaire = gr.update(visible=True)
        introPage = gr.update(visible=False)
        return introQuestionnaire, introPage

def startbot(ques1, ques2, ques3, ques4, ques5, ques6, ques7, ques8, ques9, promptInfo):
        householdSize = ques1
        housholdAbove60 = ques2
        usCitizen = ques3
        jobOrSelfEmpIncome = ques4
        otherSourcesIncome = ques5
        collegeStudies = ques6
        ageBucket = ques7
        pregnancyStatus = ques8
        childrenAgeStatus = ques9
        promptInfo += buildInfoAboutUserFromQues3(ques1, ques2, ques3, ques4, ques5, ques6, ques7, ques8, ques9)
        print(promptInfo)
        botScreen = gr.update(visible=True)
        questionnairePage3 = gr.update(visible=False)
        return botScreen, questionnairePage3, householdSize, housholdAbove60, usCitizen, jobOrSelfEmpIncome, otherSourcesIncome, collegeStudies, ageBucket, pregnancyStatus, childrenAgeStatus, promptInfo

def chatInvoke(msg, promptInfo, statesDropdown, chat_history):
        userMsg = msg
        prompt = "given the following information about me: " + "I am from the state " + statesDropdown +  ". " + promptInfo + " " + msg
        response = chat(prompt, statesDropdown)
        chat_history.append((userMsg, response))
        print(prompt)
        print(response)
        print(chat_history)
        return "", chat_history

 
with gr.Blocks() as demo:

    #states for questionnaire 1
    zipCode = gr.State(value="")
    kidsAbove5Below18 = gr.State(value="")
    kidsBelow5 = gr.State(value="")

    #states for questionnaire 2
    enrolled = gr.State(value="")

    #states for questionnaire 3
    householdSize = gr.State(value="")
    housholdAbove60 = gr.State(value="")
    usCitizen = gr.State(value="")
    jobOrSelfEmpIncome = gr.State(value="")
    otherSourcesIncome = gr.State(value="")
    collegeStudies = gr.State(value="")
    ageBucket = gr.State(value="")
    pregnancyStatus = gr.State(value="")
    childrenAgeStatus = gr.State(value="")

    promptInfo = gr.State(value="")

    response = gr.State(value="")
    state = gr.State(value="")

    with gr.Group(visible=False) as botScreen:
        with gr.Blocks() as sosChatBot:
            with gr.Row():
                statesArray = states
                statesDropdown = gr.Dropdown(statesArray, label="States", info="Choose your state")
            with gr.Row():
                chatbot = gr.Chatbot(bubble_full_width = False)
                msg = gr.Textbox()
                clear = gr.ClearButton([msg, chatbot])
                msg.submit(chatInvoke, [msg, promptInfo,statesDropdown, chatbot], [msg, chatbot])
                #chat_interface = gr.ChatInterface(fn=chat, chatbot=chatbot)

    with gr.Group(visible=False) as questionnairePage3:

        gr.Markdown("# <p style='text-align: center;'>{}</p>".format("Our AI Helper can save you time!"))
        gr.Markdown("<p style='text-align: center;'>{}</p>".format("Here are the 9 questions we need you to answer so the AI Helper knows what programs you qualify for, then it will find links or phone numbers to help you apply. Make sure you have a good internet connection, and your phone battery is charged or plugged in."))
        gr.Markdown("<p style='text-align: center;'>{}</p>".format("All of your answers are private to you, and will not be shared with anybody."))
        ques1 = gr.Textbox(label="1. Household size", info="Your household is the people you live with and buy food with. You must include children 21 or younger, parents and spouses if you are living together. ")
        ques2 = gr.Radio(["Yes", "No"], label="2. Does your household include someone who is 60 or older, or someone who has a disability?")
        ques3 = gr.CheckboxGroup(["I’m a US citizen", "I’ve been a Legal Permanent Resident for 5 or more years", "I’m a refugee or asylee", "I have a child that has one of the above statuses"], label="3. Do any of these apply to you?")
        ques4 = gr.Textbox(label="4. Monthly household income before taxes from jobs or self-employment")
        ques5 = gr.Textbox(label="5. Monthly household income from other sources", info="This includes Social Security disability, Child Support, Worker’s Comp, Unemployment, Pension Income, or other sources of income.")
        ques6 = gr.Radio(["Yes", "No"], label="6. Are you enrolled in a college or vocational school half-time or more?")
        ques7 = gr.CheckboxGroup(["I’m 17 or younger", "I’m 50 or older", "I’m receiving TANF (cash assistance) or disability payments", "I have parental control of a child under age 12", "I’m in a job training program", "I’m being paid to work an average of 20 hours per week", "I’m approved for work study and anticipate working during the term", "I’m unable to work as determined by a health professional"], label="7. If yes, which of the following apply to you?")
        ques8 = gr.Radio(["Yes", "No"], label="8. Are any of the members of your household pregnant, or was pregnant in the last 6 months?")
        ques9 = gr.Radio(["Yes", "No"], label="9. Are any of the members of your household an infant or child up that hasn’t yet had their 5th birthday?")
        aiHelper = gr.Button("Send to AI Helper")
        aiHelper.click(startbot, inputs=[ques1,ques2,ques3,ques4,ques5,ques6,ques7,ques8,ques9, promptInfo], outputs=[botScreen,questionnairePage3,householdSize,housholdAbove60,usCitizen,jobOrSelfEmpIncome,otherSourcesIncome,collegeStudies,ageBucket,pregnancyStatus,childrenAgeStatus,promptInfo])

    with gr.Group(visible=False) as questionnairePage2:

        gr.Markdown("# <p style='text-align: center;'>{}</p>".format("We found programs in your area that you may be eligible for:"))
        gr.Markdown("<p style='text-align: center;'>{}</p>".format("You may be eligible for Basic Food (SNAP)."))

        check = gr.Checkbox(label="I’m already enrolled")

        gr.Markdown("# <p style='text-align: center;'>{}</p>".format("How to apply "))
        gr.Markdown("<p style='text-align: center;'>{}</p>".format("While each program has a unique application process, our questionnaire (9 questions) can tell you which programs you qualify for — then give you the links or phone number number"))
        gr.Markdown("<p style='text-align: center;'>{}</p>".format("All of your answers are private to you, and will not be shared with anybody."))
        questionnairePage2Button = gr.Button("Start questionnaire")
        questionnairePage2Button.click(nextQuestionnaire2, inputs=[check, promptInfo], outputs=[questionnairePage3,questionnairePage2, enrolled, promptInfo])

    with gr.Group(visible=False) as introQuestionnaire:

        gr.Markdown("# <p style='text-align: center;'>{}</p>".format("Your location and family details"))
        gr.Markdown("<p style='text-align: center;'>{}</p>".format("These 3 questions help determine program eligibility."))
        gr.Markdown("<p style='text-align: center;'>{}</p>".format("All of your answers are private to you, and will not be shared with anybody."))
        ques1 = gr.Textbox(label="1. What is your location’s ZIP code?", info="We’re asking where you live so we can help you find all the benefits available in your area")
        ques2 = gr.Textbox(label="2. How many kids do you have below age 5?", info="More programs may be available depending on your answer")
        ques3 = gr.Textbox(label="3. How many kids do you have aged 5-18?", info="More programs may be available depending on your answer.")
        nextButton = gr.Button("Show nearby programs")
        nextButton.click(nextQuestionnaire1, inputs = [ques1, ques2, ques3, promptInfo],outputs=[introQuestionnaire, questionnairePage2,zipCode,kidsBelow5,kidsAbove5Below18,promptInfo] )

    with gr.Group(visible=True) as introPage:
      
        logo=gr.Image(r".\images\NoHungry.svg", height=40, width=100, )
        introPic=gr.Image(r".\images\intro-page.jpg")
        #Merge conflicts - leaving this version in for testing to compare
        #logo=gr.Image(r".\images\NoHungry.svg", height=20, width=60, )
        #introPic=gr.Image(r".\images\Home.svg")
        #gr.Dropdown(choices=[])

        with gr.Tab("English"):
            with open('.\labels-en.json', 'r') as labels:
                data = json.load(labels)

            gr.Markdown("# <p style='text-align: center;'>{}</p>".format(data['intro-title']))
            gr.Markdown("<p style='text-align: center;'>{}</p>".format(data['intro-desc-1']))
            gr.Markdown("<p style='text-align: center;weight:400;font-size:14px;font:Gotham;'>{}</p>".format(data['intro-desc-2']))
            getStarted = gr.Button(data['get-started'], variant="primary")
            getStarted.click(start,[],[introQuestionnaire,introPage])
            gr.Markdown("<a style='text-align: center;font-weight:400' href='https://foodfinder.us'>{}</a>".format(data['intro-footer-title']+ data['intro-footer-content']))

        with gr.Tab("Spanish"):
            with open('.\labels-sp.json', 'r') as labelsSpanish:
                data = json.load(labelsSpanish)

            gr.Markdown("# <p style='text-align: center;'>{}</p>".format(data['intro-title']))
            gr.Markdown("<p style='text-align: center;'>{}</p>".format(data['intro-desc-1']))
            gr.Markdown("<p style='text-align: center;weight:400;font-size:14px;font:Gotham;'>{}</p>".format(data['intro-desc-2']))
            getStarted = gr.Button(data['get-started'], variant="primary")
            gr.Markdown("<a style='text-align: center;font-weight:400' href='https://foodfinder.us'>{}</a>".format(data['intro-footer-title']+ data['intro-footer-content']))

demo.launch()
