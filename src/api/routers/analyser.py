# -*- coding: utf-8 -*-

from fastapi import APIRouter

router = APIRouter(
    prefix="/analyser",
    responses={404: {"description": "Not found"}},
)


@router.get('/all_projects')
def get_topic_for_text():
    return 200


@router.get('/all_projects')
def get_visualization():
    return 200
