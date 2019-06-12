import json

from flask import render_template, request, make_response, jsonify
import dialogflow_v2
import dialogflow

from EagleBot.FAQQA import handle_FAQ_QA
from EagleBot.UnsupervisedQAWithSentenceEmbedding import handle_qa_extraction_using_machine_learning
from EagleBotWebUI.app import app
from google.protobuf.json_format import MessageToJson
import os
import timeit
import multiprocessing



@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/handle_data', methods=['POST'])
def handle_data():
    projectpath = request.form['projectFilepath']
    # your code
    # return a response
    print(projectpath)
    return "thanks"


def extract_result_using_dialogflow(input_question):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/rana/Thesis/DrQA/EagleBotWebUI/NewAgent-4befe1007ccf.json"
    final_json_result = detect_intent_texts("newagent-b687f", "abcd", [input_question], "en-US")
    return final_json_result


def extract_result_without_using_dialogflow(input_question):
    start = timeit.default_timer()
    most_probable_FAQ_result_list = handle_FAQ_QA(input_question)

    candidate_url_list, most_probable_supervised_answer, most_probable_answer_from_bert = handle_qa_extraction_using_machine_learning(
        input_question)

    # final_result_from_EagleBot_without_using_Dialogflow =

    # result = "Thanks!!!"

    result = {
        "text1": "From EagleBot FAQ KB: ",
        "text2": most_probable_FAQ_result_list[0][1],
        "text3": "Confidence: " + str(round(most_probable_FAQ_result_list[0][2] * 100, 2)) + "%",
        "text4": "Using EagleBot AI: ",
        "text5": "Shortly: " + most_probable_answer_from_bert[0],
        "text6": "Broadly: " + most_probable_answer_from_bert[1],
        "text7": "Most Probable URLs: ",
        "text8": candidate_url_list[0],
        "text9": candidate_url_list[1]
        # "text10": candidate_url_list[2]
        # "text8": str(candidate_url_list[0])
    }
    stop = timeit.default_timer()

    print('Time Required: ', stop - start)
    return jsonify(result)


@app.route('/login', methods=['GET', 'POST'])
def login():
   start = timeit.default_timer()
   message = None
   if request.method == 'POST':
        input_question = request.form['mydata']
        print(input_question)

        p = multiprocessing.Process(target=extract_result_using_dialogflow(input_question))
        t = multiprocessing.Process(target=extract_result_without_using_dialogflow(input_question))
        p.start()
        t.start()

        # Wait for 2 seconds or until process finishes
        p.join(1)

        # If thread is still active
        if p.is_alive():
            print("running... let's kill it...")

            # Terminate
            p.terminate()
            p.join()

        # extract_result_using_dialogflow(input_question)
        # extract_result_without_using_dialogflow(input_question)

        # most_probable_FAQ_result_list = handle_FAQ_QA(input_question)
        #
        # candidate_url_list, most_probable_supervised_answer, most_probable_answer_from_bert = handle_qa_extraction_using_machine_learning(
        #     input_question)
        #
        # # final_result_from_EagleBot_without_using_Dialogflow =
        #
        #
        # # result = "Thanks!!!"
        #
        # result = {
        #     "text1": "From EagleBot FAQ KB: ",
        #     "text2": most_probable_FAQ_result_list[0][1],
        #     "text3": "Confidence: " + str(round(most_probable_FAQ_result_list[0][2]*100, 2)) + "%",
        #     "text4": "Using EagleBot AI: ",
        #     "text5": "Shortly: " + most_probable_answer_from_bert[0],
        #     "text6": "Broadly: " + most_probable_answer_from_bert[1],
        #     "text7": "Most Probable URLs: ",
        #     "text8": candidate_url_list[0],
        #     "text9": candidate_url_list[1]
        #     # "text10": candidate_url_list[2]
        #     # "text8": str(candidate_url_list[0])
        # }
        # stop = timeit.default_timer()
        #
        # print('Time Required: ', stop - start)
        # return jsonify(result)

        # # TODO: Uncomment below portion
        # start = timeit.default_timer()
        # while(timeit.default_timer()-start<2):
        #     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/rana/Thesis/DrQA/EagleBotWebUI/NewAgent-4befe1007ccf.json"
        #     final_json_result = detect_intent_texts("newagent-b687f", "abcd", [input_question], "en-US")
        #     return final_json_result
        #
        # result = "Thanks!!!"
        # return jsonify(result)

def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    for text in texts:
        start = timeit.default_timer()
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)
        print("**************")
        print(timeit.default_timer()-start)
        # print('=' * 20)
        # print('Query text: {}'.format(response.query_result.query_text))
        # print('Detected intent: {} (confidence: {})\n'.format(
        #     response.query_result.intent.display_name,
        #     response.query_result.intent_detection_confidence))
        # print('Fulfillment text: {}\n'.format(
        #     response.query_result.fulfillment_text))
        #
        # print('Fulfillment Message: {}\n'.format(
        #     response.query_result.fulfillment_messages))
        #
        # print('Fulfillment text: {}\n'.format(response.query_result.fulfillment_text))

        fulfillment_message_list = response.query_result.fulfillment_messages
        # print(fulfillment_message_list)
        jsonObj = MessageToJson(response.query_result)
        print(jsonObj)
        j = json.loads(jsonObj)
        fulfillment_message_list = j['fulfillmentMessages']
        print(len(fulfillment_message_list))

        data = {}
        for i in range (len(fulfillment_message_list)):
            try:
                print(fulfillment_message_list[i]['text']['text'][0])
                data[i] = fulfillment_message_list[i]['text']['text'][0]
            except:
                pass

        final_json_result = json.dumps(data)
        return final_json_result

