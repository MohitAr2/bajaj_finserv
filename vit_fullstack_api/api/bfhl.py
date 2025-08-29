from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import re

app = FastAPI()

FULL_NAME = "john_doe"   # lowercase full name
DOB = "17091999"         # ddmmyyyy
EMAIL = "john@xyz.com"
ROLL_NUMBER = "ABCD123"


def alternate_caps_reverse(s: str) -> str:
    reversed_s = s[::-1]
    result = ""
    for i, ch in enumerate(reversed_s):
        result += ch.upper() if i % 2 == 0 else ch.lower()
    return result


@app.post("/bfhl")
async def bfhl(request: Request):
    try:
        body = await request.json()
        data = body.get("data", [])

        odd_numbers = []
        even_numbers = []
        alphabets = []
        special_chars = []
        sum_numbers = 0
        alpha_concat = ""

        for item in data:
            if re.fullmatch(r"-?\d+", item):  # check if number
                num = int(item)
                sum_numbers += num
                if num % 2 == 0:
                    even_numbers.append(item)
                else:
                    odd_numbers.append(item)
            elif re.fullmatch(r"[a-zA-Z]+", item):  # alphabets
                alphabets.append(item.upper())
                alpha_concat += item
            else:  # special character
                special_chars.append(item)

        return JSONResponse(content={
            "is_success": True,
            "user_id": f"{FULL_NAME}_{DOB}",
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": special_chars,
            "sum": str(sum_numbers),
            "concat_string": alternate_caps_reverse(alpha_concat)
        }, status_code=200)

    except Exception as e:
        return JSONResponse(content={
            "is_success": False,
            "message": "Server error",
            "error": str(e)
        }, status_code=500)
