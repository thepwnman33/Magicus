import asyncio
import websockets
import json
from aiohttp import ClientSession

GPT_API_ENDPOINT = "https://api.openai.com/v1/engines/davinci-codex/completions"
API_KEY = "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"

async def send_gpt_request(prompt, api_settings):
    engine = api_settings["engine"]
    GPT_API_ENDPOINT = f"https://api.openai.com/v1/engines/{engine}/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": api_settings["maxTokens"],
        "temperature": api_settings["temperature"],
        "n": api_settings["n"],
        "stop": api_settings["stop"],
        "top_p": api_settings["topP"]
    }
    async with ClientSession() as session:
        async with session.post(GPT_API_ENDPOINT, headers=headers, json=data) as response:
            result = await response.json()
            if 'choices' in result:
                return result["choices"][0]["text"]
            else:
                print(f"Error in GPT API response: {result}")
                return "Error occurred while processing your request."

def segment_code(code, max_length=1000):
    lines = code.splitlines()
    segments = []
    current_segment = []
    current_length = 0

    for line in lines:
        line_length = len(line)
        if current_length + line_length <= max_length:
            current_segment.append(line)
            current_length += line_length
        else:
            segments.append("\n".join(current_segment))
            current_segment = [line]
            current_length = line_length

    if current_segment:
        segments.append("\n".join(current_segment))

    return segments

async def handle_send_message(websocket, prompt, api_settings):
    print(f"Received prompt: {prompt}, API settings: {api_settings}")

    segments = segment_code(prompt)
    responses = []

    for segment in segments:
        response = await send_gpt_request(segment, api_settings)
        responses.append(response)

    message = "".join(responses)
    await websocket.send(json.dumps({"action": "chat_response", "message": message}))

async def magicus_server(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        action = data.get("action")

        if action == "send_message":
            prompt = data.get("prompt")
            api_settings = data.get("apiSettings")
            await handle_send_message(websocket, prompt, api_settings)

start_server = websockets.serve(magicus_server, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
