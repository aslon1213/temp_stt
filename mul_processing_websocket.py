import asyncio
import websockets
import json
from multiprocessing import Process, Queue
import io
import time
from faster_whisper import WhisperModel

num_models = 1
counter = 0
models_list = []
import torch.multiprocessing as mp
import multiprocessing



def load_model(model_name, i, device="cpu", available_devices=[]) -> WhisperModel:
    if device == "cuda":
        device_id = i % len(available_devices)
        model = WhisperModel(model_name, device=device, device_index=device_id)
    else:
        model = WhisperModel(model_name, device=device)
    return model


for i in range(num_models):
    models_list.append(
        load_model(
            "Systran/faster-whisper-small",
            i,
            device="cuda",
            available_devices=[0]
        )
    )


async def handle_client(websocket, path, task_queue):
    global counter
    global num_models
    global models_list
    print(f"New client connected: {websocket.remote_address}")
    try:
        async for message in websocket:
            # selected_model_id = counter % num_models
            # selected_model = models_list[selected_model_id]
            print(f"Received message connections from: {websocket.remote_address}")
            # Put the message into the task queue
            task_queue.put(message)
            counter += 1
    except websockets.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")


def worker(task_queue, result_queue):
    model = WhisperModel("Systran/faster-whisper-small", device="cuda", device_index=0)
    while True:
        # Simulate a CPU-bound task
        message = task_queue.get()
        with open("./test_audios/aslon.wav", 'rb') as f:
            result = process_message(f.read(), model=model, id=1)
            result_queue.put(result)


def process_message(message, model, id):
    audio = io.BytesIO(message)
    model_used = "Systran/faster-whisper-small"
    segments, info = model.transcribe(audio, language="uz")
    start = time.time()
    text = ""
    for segment in segments:
        text += segment.text
    print(f"Time to process full text: {time.time() - start}")
    return text


async def start_server(task_queue):
    async with websockets.serve(
        lambda ws, path: handle_client(ws, path, task_queue), "0.0.0.0", 9000
    ):
        await asyncio.Future()  # Run forever


def run_server(task_queue):
    asyncio.run(start_server(task_queue))
    


def main():
    pass


if __name__ == "__main__":
    
    models_list = multiprocessing.Manager()
    
    task_queue = Queue()
    result_queue = Queue()

    server_process = Process(target=run_server, args=(task_queue,))
    server_process.start()
    print("Server started on ws://localhost:9000")
    # Create worker processes
    num_workers = 1
    workers = [
        Process(target=worker, args=(task_queue, result_queue))
        for _ in range(num_workers)
    ]

    for w in workers:
        w.start()

    try:
        while True:
            start = time.time()
            result = result_queue.get()
            print(f"Result: {result} --- time taken: {time.time() - start}")
    except KeyboardInterrupt:
        for _ in range(num_workers):
            task_queue.put("STOP")
        for w in workers:
            w.join()
        server_process.terminate()
        server_process.join()
