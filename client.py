import asyncio
import websockets


# async def connect_to_server():
#     async with websockets.connect("ws://localhost:9000") as websocket:
#         with open("../test_audios/pul_kerak.mp3", "r") as f:
#             await websocket.send(f.buffer.read(-1))
#             response = await websocket.recv()
#             print(f"Received: {response}")


# asyncio.get_event_loop().run_until_complete(connect_to_server())


import asyncio
import websockets

import time

reset = "\033[0m"
red = "\033[31m"
green = "\033[32m"


def timer(func):
    def wrapper(*arg, **kwargs):

        start = time.time()
        result = func(*arg, **kwargs)
        end = time.time()
        print(
            f"           {green} {func.__name__} took to complete:  {red} {end - start}{reset}          "
        )
        return result

    return wrapper


##### specify audio language code - uz/ru/en
custom_headers = [("language_code", "uz")]
import json


async def hello():
    # uri = "ws://104.167.17.11:49142"
    uri = "ws://127.0.0.1:9000"
    async with websockets.connect(uri, extra_headers=custom_headers) as websocket:
        print("Connected to the server")
        while True:
            with open("./test_audios/aslon.wav", "r") as f:
                buffer = f.buffer.read(-1)
                # length = len(buffer)
                # num = 10
                # for i in range(num):
                #     start = time.time()
                #     print(
                #         "Giving the server a chunk of the audio file length: ",
                #         length // num * (i + 1),
                #     )
                #     await websocket.send(buffer[: length // num * (i + 1)])
                #     response = await websocket.recv()
                #     print(f"Received length of string: ", len(response))
                #     print("Time taken: ", time.time() - start)

                # pre_message = json.dumps({"state": 2})
                # print("Giving the server the half audio file")
                start = time.time()
                # await websocket.send(pre_message)
                await websocket.send(buffer)
                response = await websocket.recv()
                response = json.loads(response)
                print("Finished string :", response)
                print("Time taken: ", time.time() - start)
                # input("Press enter to continue")
                ###########
                ###########
                # start = time.time()
                # pre_message = json.dumps({"state": 1})
                # await websocket.send(pre_message)
                # print("Giving the server the whole audio file")
                # await websocket.send(buffer)
                # response = await websocket.recv()
                # response = json.loads(response)
                # print("Finished string :", response)
                # print("Time taken: ", time.time() - start)
                # input("Press enter to continue")
                # ###########
                # ###########
                # start = time.time()
                # print("Giving the server the half audio file")
                # pre_message = json.dumps({"state": 2})
                # await websocket.send(pre_message)
                # await websocket.send(buffer[: length // 2])
                # response = await websocket.recv()
                # response = json.loads(response)
                # print("Finished string :", response)
                # print("Time taken: ", time.time() - start)
                # input("Press enter to continue")
                # ###########
                # start = time.time()
                # print(
                #     "Giving the server the half audio file again but this time the rank should be freed on server"
                # )
                # pre_message = json.dumps({"state": 2})
                # await websocket.send(pre_message)
                # await websocket.send(buffer[: length // 2])
                # response = await websocket.recv()
                # response = json.loads(response)
                # print("Finished string :", response)
                # print("Time taken: ", time.time() - start)
                # input("Press enter to continue")
                # break


if __name__ == "__main__":
    asyncio.run(hello())
