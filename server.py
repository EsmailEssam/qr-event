from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import csv
import os

app = FastAPI()

def load_tokens():
    tokens = {}
    if os.path.exists('tokens.csv'):
        with open('tokens.csv', mode='r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # row structure: invitee_id, token, status
                tokens[row[1]] = row[2]
    return tokens

def update_token(token, new_status):
    tokens_list = []
    if os.path.exists('tokens.csv'):
        with open('tokens.csv', mode='r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[1] == token:
                    row[2] = new_status
                tokens_list.append(row)
    with open('tokens.csv', mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(tokens_list)

@app.get("/")
async def wlcome():
    return {"message": "Welcome to the QR code scanner!"}


@app.get("/scan", response_class=HTMLResponse)
async def scan(token: str):
    if not token:
        raise HTTPException(status_code=400, detail="Invalid QR code")
    
    tokens = load_tokens()
    if token not in tokens:
        raise HTTPException(status_code=404, detail="Token not found")
    
    if tokens[token] == "unused":
        update_token(token, "used")
        return "<h1>Welcome! This QR code is valid.</h1>"
    else:
        return "<h1>This QR code has already been used.</h1>"

if __name__ == '__main__':
    import uvicorn
    # Run the FastAPI app on host 0.0.0.0 at port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
