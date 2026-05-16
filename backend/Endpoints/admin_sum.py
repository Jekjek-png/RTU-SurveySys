from pathlib import Path
from fastapi import APIRouter, FastAPI, HTTPException
import csv

router = APIRouter()

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "Survey_response.csv"
