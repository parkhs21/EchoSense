from myTool import contentTool, resTool
import gradio as gr
import numpy as np
import dotenv
dotenv.load_dotenv()

# def compose_payload(image: np.ndarray, prompt: str) -> dict:
#     base64_image = preTool.encode_image_to_base64(image)
#     return {
#         "model": "gpt-4-vision-preview",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "text",
#                         "text": prompt
#                     },
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": f"data:image/jpeg;base64,{base64_image}"
#                         }
#                     }
#                 ]
#             }
#         ],
#         "max_tokens": 300
#     }


# def compose_headers(api_key: str) -> dict:
#     return {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {api_key}"
#     }


# def prompt_image(api_key: str, image: np.ndarray, prompt: str) -> str:
#     headers = compose_headers(api_key=api_key)
#     payload = compose_payload(image=image, prompt=prompt)
#     response = requests.post(url=API_URL, headers=headers, json=payload).json()

#     if 'error' in response:
#         raise ValueError(response['error']['message'])
#     return response['choices'][0]['message']['content']

def respond(image: np.ndarray, audio: (int, np.ndarray), chat_history):

    # cached_image_path = preTool.cache_image(image)
    # response = prompt_image(api_key=os.environ['OPENAI_API_KEY'], image=image, prompt=prompt)
    # chat_history.append(((cached_image_path,), None))
    # chat_history.append((prompt, response))
    # chat_history.append(("1,",None))
    # yield chat_history


    if audio is None: raise gr.Error("음성이 있어야 합니다!!")
    cached_audio_path = contentTool.cache_audio(audio)

    transcript = resTool.prompt_stt(cached_audio_path)
    chat_history.append([transcript, None])
    yield chat_history

    if image is not None:
        image = contentTool.preprocess_image(image=image)
        cached_image_path = contentTool.cache_image(image)
        answer = resTool.prompt_image(cached_image_path, transcript)
    else:
        answer = resTool.prompt_chat(transcript)

    chat_history[-1][1] = answer
    yield chat_history

    return

with gr.Blocks(theme=gr.themes.Default(text_size=gr.themes.sizes.text_sm)) as demo:
    gr.Markdown("# EchoSense")
    with gr.Row():
        webcam = gr.Image(source="webcam", streaming=False)
        with gr.Column():
            chatbot = gr.Chatbot(height=420, bubble_full_width=False)
            audio = gr.Audio(source="microphone")
            with gr.Row():
                submit_button = gr.Button(value="Submit")
                clear_button = gr.ClearButton([webcam, chatbot, audio])

    submit_button.click(
        fn=respond,
        inputs=[webcam, audio, chatbot],
        outputs=[chatbot]
    )

demo.queue()
demo.launch(debug=False, show_error=True)