from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.async_api import async_playwright

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginData(BaseModel):
    email: str
    password: str

@app.get("/")
def home():
    return {"status": "السيرفر شغال تمام ومستعد للحل!"}

@app.post("/solve")
async def start_solving(data: LoginData):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu"
            ]
        )
        page = await browser.new_page()
        
        try:
            await page.goto("https://me-portal.qureo.education/login", timeout=60000)
            await page.wait_for_selector("input", timeout=20000)
            title = await page.title()
            await browser.close()
            
            return {
                "status": "success",
                "message": "تم فتح المنصة بنجاح من المتصفح الحقيقي!",
                "page_title": title
            }
            
        except Exception as e:
            await browser.close()
            return {"status": "error", "message": str(e)}
