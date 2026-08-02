# app.py - Week 15: ห่อโมเดล QC เป็น REST API ดัวย FastAPI (Uncle Engineer ML & AI 2026)
import json
import time

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

# ----- 1) โหลดโมเดลครั้งเดียวตอนเปิดเซิร์ฟเวอร์ (ไม่โหลดใหม่ทุก request) -----
model = joblib.load("models/qc_pipeline_v1.joblib")
with open("models/qc_pipeline_v1_meta.json", encoding="utf-8") as f:
    meta = json.load(f)

CONFIDENCE_THRESHOLD = 0.7  # ต่ำกว่านี้ = AI ไม่มั่นใจพอ ส่งให้คนตรวจ (human-in-the-loop จาก Week 8)

app = FastAPI(
    title="CNC QC Defect API",
    description="AI ตรวจชิ้นงาน Normal / Defect - คอร์ส Uncle Engineer ML & AI 2026",
    version=meta["version"],
)

# ----- 2) Schema ของ input: FastAPI ตรวจความถูกต้องให้อัตโนมัติ -----
class WorkpieceInput(BaseModel):
    vibration: float = Field(..., ge=0.0, le=5.0, description="แรงสั่นสะเทือน (mm/s)")
    temperature: float = Field(..., ge=0.0, le=150.0, description="อุณหภูมิหัวกัด (C)")
    current: float = Field(..., ge=0.0, le=50.0, description="กระแสมอเตอร์ (A)")
    dimension_diff: float = Field(..., ge=0.0, le=1.0, description="ขนาดเพี้ยนจากสเปก (mm)")
    surface_score: float = Field(..., ge=0.0, le=100.0, description="คะแนนผิวงาน")
    machine_id: str = Field(..., description="M01 ถึง M05")
    shift: str = Field(..., description="เช้า บ่าย หรือ ดึก")
    material: str = Field(..., description="Steel Aluminum หรือ Brass")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "vibration": 1.45, "temperature": 74.0, "current": 12.1,
                "dimension_diff": 0.02, "surface_score": 80.0,
                "machine_id": "M01", "shift": "ดึก", "material": "Steel",
            }]
        }
    }

# ----- 3) Endpoints: ประตูของบริการ -----
@app.get("/")
def root():
    #return {"message": "CNC QC Defect API พร้อมใช้งาน ลองเปิด /docs"}
    return {"message": "CNC QC Defect API พร้อมใช้งาน ลองเปิด /docs -> ตอนนี้ออนไลน์บน Render เรียบร้อยแล้ว!"}

@app.get("/model-info")
def root():
    #return {"model": meta["model_name"], "version": meta["version"], "feature used": meta["WorkpieceInput"]}
    return {"model": meta["model_name"], "version": meta["version"]}
    
@app.get("/health")
def health():
    return {"status": "ok", "model": meta["model_name"], "version": meta["version"]}

@app.post("/predict")
def predict(item: WorkpieceInput):
    t0 = time.perf_counter()
    X = pd.DataFrame([item.model_dump()])          # แปลง JSON -> DataFrame 1 แถว
    pred = int(model.predict(X)[0])
    proba = float(model.predict_proba(X)[0][pred])
    latency_ms = (time.perf_counter() - t0) * 1000
    return {
        "result": meta["target_classes"][pred],
        "confidence": round(proba, 3),
        "needs_human_check": proba < CONFIDENCE_THRESHOLD,
        "latency_ms": round(latency_ms, 1),
    }
