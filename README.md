---
title: CNC QC Defect API
emoji: 🔧
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# CNC QC Defect API

AI ตรวจชิ้นงาน Normal / Defect จากคอร์ส Uncle Engineer ML & AI 2026 (Week 15)

- `GET /health` เช็คสถานะเซิร์ฟเวอร์
- `POST /predict` ส่งข้อมูลชิ้นงาน รับผลตรวจ
- เปิด `/docs` เพื่อทดลองยิง API ผ่านหน้าเว็บ

Deploy ได้ทั้ง Render.com (ฟรี) และ Hugging Face Spaces (ต้องมี PRO)
ส่วนหัวของไฟล์นี้ (ระหว่างขีด 3 ขีด) คือ config ของ HF Spaces ฝั่ง Render จะมองเป็นข้อความเฉย ๆ
