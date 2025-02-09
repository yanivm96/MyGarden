import re
from fastapi import HTTPException

def extract_integer_from_text(text: str) -> int:
    numbers = [int(num) for num in re.findall(r'\d+', text)]
    if len(numbers) == 1:
        return numbers[0]
    elif len(numbers) > 1:
        return sum(numbers) // len(numbers)  
    else:
        raise ValueError("No valid sunny hours found")

def check_base64(data: dict) -> str:
    base64 = data.get('image_base64')
    if not base64:
        raise HTTPException(status_code=400, detail="image_base64 must not be empty")
    if not base64.startswith("data:image"):
        base64 = f"data:image/jpeg;base64,{base64}"
    return base64
