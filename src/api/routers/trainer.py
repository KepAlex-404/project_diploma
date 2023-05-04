# -*- coding: utf-8 -*-

import uuid

import pandas as pd
from fastapi import APIRouter, BackgroundTasks, UploadFile, File, Depends, Security

from src.api.routers.Dependency import get_current_active_user
from src.api.utils.DataBodies import Meta
from src.classifier.Trainer import Trainer

router = APIRouter(
    prefix="/trainer",
    responses={404: {"description": "Not found"}},
    dependencies=[Security(get_current_active_user, scopes=["User"])]
)


@router.post('/train_model/')
async def train_model(background_tasks: BackgroundTasks, file: UploadFile = File(...), meta: Meta = Depends()):
    # todo chose column
    df = pd.read_csv(file.file, delimiter=meta.delimiter)
    data = df[meta.column].tolist()
    random_id = uuid.uuid4()
    trainer = Trainer(num_topics=meta.topics_num, stop_words=meta.stop_words)
    background_tasks.add_task(trainer.process, data, random_id)
    # return id on which we can call for a model
    return random_id
