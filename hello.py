import time
import gradio as gr
import numpy as np
import json
from prototype import chat
from constants import states

with open('.\labels-en.json', 'r') as labels:
    englishLabels = json.load(labels)

with open('.\labels-sp.json', 'r') as labels:
    spanishLabels = json.load(labels)
    
def buildInfoAboutUserFromQues1(zipCode, kidsBelow5, kidsAbove5Below18):
        promptInfo = "My zipcode is " + zipCode + " and have " + kidsBelow5 + " kids below 5 and " + kidsAbove5Below18 + " kids above 5 below 18. "
        return promptInfo

def buildInfoAboutUserFromQues2(enrolledSnap, enrolledWic):
        enrolledPrompt = ""
        if(enrolledSnap):
             enrolledPrompt += "I am already enrolled in SNAP."
        if(enrolledWic):
             enrolledPrompt += "I am already enrolled in WIC."
        promptInfo = enrolledPrompt
        return promptInfo

def buildInfoAboutUserFromQues3(householdSize, housholdAbove60, usCitizen, jobOrSelfEmpIncome, otherSourcesIncome, collegeStudies, ageBucket, pregnancyStatus, childrenAgeStatus):
        promptInfo = "My household size is " + householdSize + " and " + housholdAbove60 + ", for people in my household above 60. " + '.'.join(usCitizen) + ". " + jobOrSelfEmpIncome + " is my income from my job. " + otherSourcesIncome + " is my income from other sources." + collegeStudies + ", for am I enrolled in college." + '.'.join(ageBucket) + ". " + pregnancyStatus + ", for am I pregnant." + childrenAgeStatus + ", for do I have children below 5."
        return promptInfo


def nextQuestionnaire2(isEnrolledForSnap, isEnrolledForWic, promptInfo):
        enrolledSnap = isEnrolledForSnap
        enrolledWic = isEnrolledForWic
        questionnairePage3 = gr.update(visible=True)
        questionnairePage2 = gr.update(visible=False)
        promptInfo += buildInfoAboutUserFromQues2(enrolledSnap, enrolledWic)
        print(promptInfo)
        return questionnairePage3, questionnairePage2, promptInfo

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
        with gr.Tab(englishLabels['lang-1']):
            gr.Markdown("# <p style='text-align: center;'>{}</p>".format("Our AI Helper can save you time!"))
            gr.Markdown("<p style='text-align: center;'>{}</p>".format("Here are the 9 questions we need you to answer so the AI Helper knows what programs you qualify for, then it will find links or phone numbers to help you apply. Make sure you have a good internet connection, and your phone battery is charged or plugged in."))
            gr.Markdown("<p style='text-align: center;'>{}</p>".format("All of your answers are private to you, and will not be shared with anybody."))
            ques1 = gr.Textbox(label="1. Household size", info="Your household is the people you live with and buy food with. You must include children 21 or younger, parents and spouses if you are living together. ")
            ques2 = gr.Radio(["Yes", "No"], label="2. Does your household include someone who is 60 or older, or someone who has a disability?")
            ques3 = gr.CheckboxGroup(["I'm a US citizen", "I've been a Legal Permanent Resident for 5 or more years", "I'm a refugee or asylee", "I have a child that has one of the above statuses"], label="3. Do any of these apply to you?")
            ques4 = gr.Textbox(label="4. Monthly household income before taxes from jobs or self-employment")
            ques5 = gr.Textbox(label="5. Monthly household income from other sources", info="This includes Social Security disability, Child Support, Worker's Comp, Unemployment, Pension Income, or other sources of income.")
            ques6 = gr.Radio(["Yes", "No"], label="6. Are you enrolled in a college or vocational school half-time or more?")
            ques7 = gr.CheckboxGroup(["I'm 17 or younger", "I'm 50 or older", "I'm receiving TANF (cash assistance) or disability payments", "I have parental control of a child under age 12", "I'm in a job training program", "I'm being paid to work an average of 20 hours per week", "I'm approved for work study and anticipate working during the term", "I'm unable to work as determined by a health professional"], label="7. If yes, which of the following apply to you?")
            ques8 = gr.Radio(["Yes", "No"], label="8. Are any of the members of your household pregnant, or was pregnant in the last 6 months?")
            ques9 = gr.Radio(["Yes", "No"], label="9. Are any of the members of your household an infant or child up that hasn't yet had their 5th birthday?")
            aiHelper = gr.Button("Send to AI Helper")
            aiHelper.click(startbot, inputs=[ques1,ques2,ques3,ques4,ques5,ques6,ques7,ques8,ques9, promptInfo], outputs=[botScreen,questionnairePage3,householdSize,housholdAbove60,usCitizen,jobOrSelfEmpIncome,otherSourcesIncome,collegeStudies,ageBucket,pregnancyStatus,childrenAgeStatus,promptInfo])
        with gr.Tab(englishLabels['lang-2']):
            gr.Markdown("# <p style='text-align: center;'>{}</p>".format("¡Nuestro ayudante de IA puede ahorrarle tiempo!"))
            gr.Markdown("<p style='text-align: center;'>{}</p>".format("Estas son las 9 preguntas que necesitamos que respondas para que el Ayudante de IA sepa para qué programas calificas, luego encontrará enlaces o números de teléfono para ayudarte a postularte. Asegúrate de tener una buena conexión a Internet y de que la batería de tu teléfono esté cargada o enchufada."))
            gr.Markdown("<p style='text-align: center;'>{}</p>".format("Todas sus respuestas son privadas para usted y no se compartirán con nadie."))
            ques1 = gr.Textbox(label="1. Cuántas personas viven en el hogar", info="Su hogar son las personas con las que vive y con las que compra alimentos. Debe incluir a los niños de 21 años o menos, padres y cónyuges si viven juntos. ")
            ques2 = gr.Radio(["Sí", "No"], label="2. ¿Su hogar incluye a alguien que tiene 60 años o más, o alguien que tiene una discapacidad?")
            ques3 = gr.CheckboxGroup(["No soy ciudadano de Estados Unidos", "He sido residente legal permanente durante 5 años o más", "I'm a refugee or asylee", "Tengo un hijo que tiene uno de los estados anteriores"], label="¿Alguno de estos casos se aplican a tí?")
            ques4 = gr.Textbox(label="4. Ingresos mensuales del hogar antes de impuestos por trabajo o trabajo por cuenta propia")
            ques5 = gr.Textbox(label="5. Ingresos mensuales del hogar de otras fuentes", info="Esto incluye discapacidad del Seguro Social, manutención de los hijos, compensación laboral, desempleo, ingresos de pensiones u otras fuentes de ingresos.")
            ques6 = gr.Radio(["Sí", "No"], label="6. ¿Está inscrito en una universidad o escuela vocacional a medio tiempo o más?")
            ques7 = gr.CheckboxGroup(["Tengo 17 años o menos", "Tengo 50 años o más", "Estoy recibiendo TANF (asistencia en efectivo) o pagos por discapacidad", "Tengo el control parental de un niño menor de 12 años", "Estoy en un programa de capacitación laboral", "Me pagan por trabajar una media de 20 horas semanales", "Estoy aprobado para el estudio de trabajo y preveo trabajar durante el plazo", "No puedo trabajar según lo determine un profesional de la salud"], label="7. ¿Cuál de las siguientes opciones se aplica a usted?")
            ques8 = gr.Radio(["Sí", "No"], label="8. ¿Alguno de los miembros de su hogar está embarazada o estuvo embarazada en los últimos 6 meses?")
            ques9 = gr.Radio(["Sí", "No"], label="9. ¿Alguno de los miembros de su hogar es un bebé o niño que aún no ha cumplido 5 años?")
            aiHelper = gr.Button("Enviar al ayudante de IA")
            aiHelper.click(startbot, inputs=[ques1,ques2,ques3,ques4,ques5,ques6,ques7,ques8,ques9, promptInfo], outputs=[botScreen,questionnairePage3,householdSize,housholdAbove60,usCitizen,jobOrSelfEmpIncome,otherSourcesIncome,collegeStudies,ageBucket,pregnancyStatus,childrenAgeStatus,promptInfo])

    with gr.Group(visible=False) as questionnairePage2:
        logo=gr.Image(r".\images\NoHungry.svg", height=40, width=100, interactive=False, show_label=False, show_download_button=False)
        introPic=gr.Image(r".\images\basic-program-list.jpg", interactive=False, show_label=False, show_download_button=False)
        with gr.Tab(englishLabels['lang-1']):
            gr.Markdown("# <p style='text-align: center;'>{}</p>".format("We found 2 programs in your area that you may be eligible for:"))
            gr.Markdown("<p style='text-align: left;'>{}</p>".format("You may be eligible for Basic Food (SNAP)."))
            isEnrolledForSnap = gr.Checkbox(label="I'm already enrolled", default=False)
            gr.Markdown("<p style='text-align: left;'>{}</p>".format("You may be eligible for the Nutrition Program for Women, Infants and Children (WIC)."))
            isEnrolledForWic = gr.Checkbox(label="I'm already enrolled", default=False)
            gr.Markdown("# <p style='text-align: left;'>{}</p>".format("How to apply "))
            gr.Markdown("<p style='text-align: left;'>{}</p>".format("While each program has a unique application process, our questionnaire (9 questions) can tell you which programs you qualify for - then give you the links or phone number number"))
            gr.Markdown("<p style='text-align: left;'>{}</p>".format("All of your answers are private to you, and will not be shared with anybody."))
            questionnairePage2Button = gr.Button("Start questionnaire", variant="primary")
            gr.Markdown("<a style='text-align: center;font-weight:400' href='https://foodfinder.us'>{}</a>".format(englishLabels['intro-footer-title']+ englishLabels['intro-footer-content']))
            questionnairePage2Button.click(nextQuestionnaire2, inputs=[isEnrolledForSnap, isEnrolledForWic, promptInfo], outputs=[questionnairePage3,questionnairePage2, promptInfo])
        with gr.Tab(englishLabels['lang-2']):
            gr.Markdown("# <p style='text-align: center;'>{}</p>".format("Encontramos programas en su área para los que puede ser elegible:"))
            gr.Markdown("<p style='text-align: left;'>{}</p>".format("Puede ser elegible para alimentos básicos (SNAP)."))
            isEnrolledForSnap = gr.Checkbox(label="Ya estoy inscrita.", default=False)
            gr.Markdown("<p style='text-align: left;'>{}</p>".format("Puede ser elegible para el Programa de Nutrición para Mujeres, Bebés y Niños (WIC)."))
            isEnrolledForWic = gr.Checkbox(label="Ya estoy inscrita.", default=False)

            gr.Markdown("# <p style='text-align: left;'>{}</p>".format("Cómo presentar la solicitud "))
            gr.Markdown("<p style='text-align: left;'>{}</p>".format("Si bien cada programa tiene un proceso de solicitud único, nuestro cuestionario (9 preguntas) puede decirle para qué programas califica y luego darle los enlaces o el número de teléfono"))
            gr.Markdown("<p style='text-align: left;'>{}</p>".format("Todas sus respuestas son privadas para usted y no se compartirán con nadie."))
            questionnairePage2Button = gr.Button("Empezar cuestionario", variant="primary")
            gr.Markdown("<a style='text-align: center;font-weight:400' href='https://foodfinder.us'>{}</a>".format(spanishLabels['intro-footer-title']+ spanishLabels['intro-footer-content']))
            questionnairePage2Button.click(nextQuestionnaire2, inputs=[isEnrolledForSnap, isEnrolledForWic, promptInfo], outputs=[questionnairePage3,questionnairePage2, promptInfo])

    with gr.Group(visible=False) as introQuestionnaire:
        logo=gr.Image(r".\images\NoHungry.svg", height=40, width=100, interactive=False, show_label=False, show_download_button=False)
        introPic=gr.Image(r".\images\basic-form.jpg", interactive=False, show_label=False, show_download_button=False)
        with gr.Tab(englishLabels['lang-1']):
            gr.Markdown("# <p style='text-align: center;'>{}</p>".format("Your location and family details"))
            gr.Markdown("<p style='text-align: center;'>{}</p>".format("These 3 questions help determine program eligibility."))
            gr.Markdown("<p style='text-align: center;'>{}</p>".format("All of your answers are private to you, and will not be shared with anybody."))
            ques1 = gr.Textbox(label="1. What is your location's ZIP code?", info="We're asking where you live so we can help you find all the benefits available in your area")
            ques2 = gr.Textbox(label="2. How many kids do you have below age 5?", info="More programs may be available depending on your answer")
            ques3 = gr.Textbox(label="3. How many kids do you have aged 5-18?", info="More programs may be available depending on your answer.")
            nextButton = gr.Button("Show nearby programs", variant="primary")
            nextButton.click(nextQuestionnaire1, inputs = [ques1, ques2, ques3, promptInfo],outputs=[introQuestionnaire, questionnairePage2,zipCode,kidsBelow5,kidsAbove5Below18,promptInfo] )

        with gr.Tab(englishLabels['lang-2']):
            gr.Markdown("# <p style='text-align: center;'>{}</p>".format("Tu ubicación y datos familiares"))
            gr.Markdown("<p style='text-align: center;'>{}</p>".format("Estas 3 preguntas ayudan a determinar la elegibilidad para el programa."))
            gr.Markdown("<p style='text-align: center;'>{}</p>".format("Todas sus respuestas son privadas para usted y no se compartirán con nadie."))
            ques1 = gr.Textbox(label="1. ¿Cuál es el código POSTAL de tu ubicación?", info="Te preguntamos dónde vives para ayudarte a encontrar todas las ventajas disponibles en tu zona.")
            ques2 = gr.Textbox(label="2. ¿Cuántos hijos tiene por debajo de los 5 años?", info="Es posible que haya más programas disponibles dependiendo de su respuesta")
            ques3 = gr.Textbox(label="3. ¿Cuántos hijos tiene de 5 a 18 años?", info="Es posible que haya más programas disponibles dependiendo de su respuesta.")
            nextButton = gr.Button("Mostrar programas cercanos", variant="primary")
            nextButton.click(nextQuestionnaire1, inputs = [ques1, ques2, ques3, promptInfo],outputs=[introQuestionnaire, questionnairePage2,zipCode,kidsBelow5,kidsAbove5Below18,promptInfo] )
    with gr.Group(visible=True) as introPage:
      
        logo=gr.Image(r".\images\NoHungry.svg", height=40, width=100, interactive=False, show_label=False, show_download_button=False)
        introPic=gr.Image(r".\images\intro-page.jpg", interactive=False, show_label=False, show_download_button=False)

        with gr.Tab(englishLabels['lang-1']):
            with open('.\labels-en.json', 'r') as labels:
                data = json.load(labels)

            gr.Markdown("# <p style='text-align: center;'>{}</p>".format(data['intro-title']))
            gr.Markdown("<p style='text-align: center;'>{}</p>".format(data['intro-desc-1']))
            gr.Markdown("<p style='text-align: center;weight:400;font-size:14px;font:Gotham;'>{}</p>".format(data['intro-desc-2']))
            getStarted = gr.Button(data['get-started'], variant="primary")
            getStarted.click(start,[],[introQuestionnaire,introPage])
            gr.Markdown("<a style='text-align: center;font-weight:400' href='https://foodfinder.us'>{}</a>".format(data['intro-footer-title']+ data['intro-footer-content']))

        with gr.Tab(englishLabels['lang-2']):
            with open('.\labels-sp.json', 'r') as labelsSpanish:
                data = json.load(labelsSpanish)

            gr.Markdown("# <p style='text-align: center;'>{}</p>".format(data['intro-title']))
            gr.Markdown("<p style='text-align: center;'>{}</p>".format(data['intro-desc-1']))
            gr.Markdown("<p style='text-align: center;weight:400;font-size:14px;font:Gotham;'>{}</p>".format(data['intro-desc-2']))
            getStarted = gr.Button(data['get-started'], variant="primary")
            gr.Markdown("<a style='text-align: center;font-weight:400' href='https://foodfinder.us'>{}</a>".format(data['intro-footer-title']+ data['intro-footer-content']))

demo.launch()
