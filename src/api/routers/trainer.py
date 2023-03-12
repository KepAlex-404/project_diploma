# -*- coding: utf-8 -*-

from fastapi import APIRouter

router = APIRouter(
    prefix="/trainer",
    responses={404: {"description": "Not found"}},
)


@router.post('/all_projects')
def train_model():
    return 200
