# -*- coding: utf-8 -*-

from fastapi import APIRouter, Security, File, UploadFile
import speech_recognition as sr
from src.api.routers.Dependency import get_current_active_user
from src.api.utils.DataBodies import AnalyserBody
from src.classifier.Analyser import Analyser
from src.classifier.NER_Trainer import get_ner_model
from pydub import AudioSegment
import tempfile
router = APIRouter(
    prefix="/analyser",
    responses={404: {"description": "Not found"}},
    dependencies=[Security(get_current_active_user, scopes=["User"])]
)


def convert_to_wav(uploaded_file: UploadFile):
    try:
        audio = AudioSegment.from_file(uploaded_file.file)
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav_file:
            audio.export(tmp_wav_file.name, format="wav")
            return tmp_wav_file.name
    except Exception as e:
        raise ValueError(f"Audio file could not be processed: {str(e)}")


@router.post('/analyze_audio')
async def analyze_audio(file: UploadFile = File(...)):
    # AudioSegment.converter = r"ffmpeg.exe"
    # AudioSegment.ffprobe = r"ffprobe.exe"
    # recognizer = sr.Recognizer()
    # wav_file_path = convert_to_wav(file)
    # with sr.AudioFile(wav_file_path) as audiofile:
    #     audio_data = recognizer.record(audiofile)
    #
    #     try:
    #         text = recognizer.recognize_google_cloud(audio_data, language='uk-UA')
    #         print(text)
    #     except Exception as e:
    #         print(e)
    #     else:
    text = """
    Вовчік висувається на поляну
    """
    ner_model = get_ner_model()
    doc = ner_model(text)
    entities = [{"text": ent.text, 'labels': ent.label_} for ent in doc.ents]
    return {"text": text, "entities": entities}


@router.post('/topic')
def get_topic_for_text(body: AnalyserBody):
    analyser = Analyser(body.model_id)
    prediction = analyser.define_text(body.text)
    return str(prediction)


@router.post('/lda_visualization')
def get_visualization(body: AnalyserBody):
    analyser = Analyser(body.model_id)
    model = analyser.get_model()
    return model
