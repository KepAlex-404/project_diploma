# -*- coding: utf-8 -*-

from fastapi import APIRouter
from fastapi.responses import FileResponse

from src.api.utils.DataBodies import AnalyserBody
from src.classifier.Analyser import Analyser

router = APIRouter(
    prefix="/analyser",
    responses={404: {"description": "Not found"}},
)


@router.post('/topic')
def get_topic_for_text(body: AnalyserBody):
    analyser = Analyser(body.model_id)
    prediction = analyser.define_text(body.text)
    return str(prediction)


@router.post('/lda_visualization')
def get_visualization(body: AnalyserBody):
    analyser = Analyser(body.model_id)
    file_path = analyser.get_visualization_path()
    return FileResponse(file_path, filename="index.html", media_type="text/html")


