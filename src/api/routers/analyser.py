# -*- coding: utf-8 -*-

from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse

from src.classifier.Analyser import Analyser

router = APIRouter(
    prefix="/analyser",
    responses={404: {"description": "Not found"}},
)


@router.get('/topic')
def get_topic_for_text():
    return 200


@router.get('/lda_visualization')
def get_visualization(model_id: str):
    analyser = Analyser(model_id)
    file_path = analyser.get_visualization_path()
    return FileResponse(file_path, filename="index.html", media_type="text/html")


