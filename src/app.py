from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import Algorithmia
from dotenv import load_dotenv
import os

from src.utils import *

app = Flask(__name__)

app.config.from_pyfile("config.py")

load_dotenv()
ALGORITHMIA_API_KEY = os.getenv('ALGORITHMIA_API_KEY', "NO_KEY")


class GenerateForm(FlaskForm):

    choices = ["anger", "anticipation", "disgust", "fear", "neutral"]

    emotion = SelectField(label="Select Emotion", choices=choices, validators=[DataRequired()])
    submit = SubmitField(label="Generate Poem")


@app.route('/', methods=['POST', 'GET'])
def index():
    poem = ""
    title = ""

    logo_path = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')

    form = GenerateForm()

    if form.validate_on_submit():

        emotion = form.emotion.data

        client = Algorithmia.client(ALGORITHMIA_API_KEY)

        # Create the algorithm object using the Summarizer algorithm
        algo = client.algo('pgcr/PoetryGeneration/1.0.0')

        try:
            # Get the result
            poem = algo.pipe(emotion).result
        except Exception as error:
            # Algorithm error if, for example, the input is not correctly formatted
            print("Error:", error)

        # # load the model corresponding to the selected emotion
        # if emotion == "neutral":
        #     print(emotion)
        #     model = GPT2LMHeadModel.from_pretrained("prajwalcr/poetry_gpt2")
        #     tokenizer = GPT2Tokenizer.from_pretrained("prajwalcr/poetry_gpt2")
        # else:
        #     model = GPT2LMHeadModel.from_pretrained("prajwalcr/poetry-"+emotion+"_gpt2")
        #     tokenizer = GPT2Tokenizer.from_pretrained("prajwalcr/poetry-"+emotion+"_gpt2")
        #
        # model.eval()
        #
        # prompt = "<|startoftext|>"
        #
        # generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0)
        #
        # sample_outputs = model.generate(
        #     generated,
        #     do_sample=True,
        #     top_k=50,
        #     max_length=300,
        #     top_p=0.95,
        #     num_return_sequences=1
        # )
        #
        # for i, sample_output in enumerate(sample_outputs):
        #     poem = tokenizer.decode(sample_output, skip_special_tokens=True)
        #     print("{}: {}\n\n".format(i, tokenizer.decode(sample_output, skip_special_tokens=True)))

        # poem = """So this is my heart,\nThat here it is, this is my spirit;\nMy right hand, my left hand,\nI see this now;\nMy right hand, I know;\nBut the right hand,\nI know not why."""

        title = generate_title(poem)
        poem = remove_weird_punctuation(poem)


        poem = poem.split("\n")

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error when generating poem {err_msg}', category='danger')

    context = {"form": form, "poem": poem, "logo": logo_path, "title": title}

    return render_template("index.html", context=context)


if __name__ == "__main__":
    app.run(debug=False)

