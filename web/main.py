from myTool import contentTool, resTool
import gradio as gr
import numpy as np
import dotenv
dotenv.load_dotenv()


def respond(image: np.ndarray, audio: (int, np.ndarray), chat_history):

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