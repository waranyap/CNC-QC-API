# Dockerfile - สูตรสร้างกล่องสำหรับ CNC QC API (ใช้ได้ทั้ง Render และ Hugging Face Spaces)

# เริ่มจากกล่องพื้นฐานที่มี Python 3.11 ติดตั้งไว้แล้ว (รุ่น slim = ตัดของไม่จำเป็นออก เบากว่า)
FROM python:3.11-slim

# สร้างผู้ใช้ธรรมดา (ไม่ใช่ root) เพื่อความปลอดภัย - เป็นกติกาของ HF Spaces และ best practice ทั่วไป
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# กำหนดโฟลเดอร์ทำงานในกล่อง
WORKDIR /app

# คัดลอกใบสั่งยาเข้าไปก่อน แล้วติดตั้งไลบรารีตามที่ pin ไว้
COPY --chown=user requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดและโมเดลทั้งหมดเข้ากล่อง
COPY --chown=user . /app

# คำสั่งที่จะรันเมื่อกล่องถูกเปิด: เปิดเซิร์ฟเวอร์
# เคล็ดลับ: อ่านพอร์ตจากตัวแปร PORT ถ้าไม่มีให้ใช้ 7860
#   Render จะตั้งตัวแปร PORT มาให้เอง / HF Spaces ไม่ตั้ง จึงตกไปใช้ 7860 ตามที่ HF คาดหวัง
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-7860}
