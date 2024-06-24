# import torch
import torch.multiprocessing as mp

# import torchvision.models as models
import json
import io

# from PIL import Image
# from torchvision import transforms
from faster_whisper import WhisperModel
import io
import time
import asyncio
import websockets
from multiprocessing import Queue, Process


# Define a worker function
def inference_worker(task_queue, result_queue, i):
    # print(f"Worker {mp.current_process().name} started")

    # Initialize the model and move it to GPU
    gpu_id = i % 4

    model = WhisperModel(
        "Systran/faster-whisper-small", device="cuda", device_index=gpu_id
    )

    print(f"Model Loaded ----id: {i} ---- gpu id:{gpu_id}")
    while True:
        message = task_queue.get()
        if message == "STOP":
            # print(f"Worker {mp.current_process().name} stopping")
            break
        # Deserialize the message
        audio = io.BytesIO(message)
        segments, info = model.transcribe(audio)
        start = time.time()
        text = ""
        for segment in segments:
            text += segment.text
        print(f"Time to process full text: {time.time() - start} -- gpu id:{gpu_id}")
        result_queue.put(
            json.dumps(
                {
                    "text": text,
                },
                ensure_ascii=False,
            )
        )

    # Release GPU memory
    del model
    # torch.cuda.empty_cache()


async def handle_client(websocket, path, task_queue, result_queue):
    print(f"New client connected: {websocket.remote_address}")
    try:
        async for message in websocket:
            # print(f"Received message from {websocket.remote_address}")
            task_queue.put(message)
            result = await asyncio.to_thread(
                result_queue.get
            )  # Await result from worker
            await websocket.send(result)
    except websockets.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")


async def start_server(task_queue, result_queue):
    async with websockets.serve(
        lambda ws, path: handle_client(ws, path, task_queue, result_queue),
        "0.0.0.0",
        9000,
        max_size=10**8,
    ):
        await asyncio.Future()  # Run forever


def run_server(task_queue, result_queue):
    asyncio.run(start_server(task_queue, result_queue))


if __name__ == "__main__":
    # Use 'spawn' to start new processes to avoid CUDA initialization issues
    mp.set_start_method("spawn")

    task_queue = Queue()
    result_queue = Queue()

    # Start the WebSocket server process
    server_process = Process(target=run_server, args=(task_queue, result_queue))
    server_process.start()
    print("WebSocket server started on ws://localhost:9000")

    # Create and start worker processes for inference
    num_workers = int(input("Number of processes: "))
    workers = [
        Process(target=inference_worker, args=(task_queue, result_queue, i))
        for i in range(num_workers)
    ]

    for w in workers:
        w.start()

    try:
        # Keep the main process alive to manage results and worker processes
        while True:
            time.sleep(100)
            print("Time elapsed :) - 100")
            # result = result_queue.get()
            # print(f"Result: {result}")
    except KeyboardInterrupt:
        print("Shutting down...")

        # Send "STOP" signal to workers
        for _ in range(num_workers):
            task_queue.put("STOP")

        for w in workers:
            w.join()

        # Terminate the server process
        server_process.terminate()
        server_process.join()
