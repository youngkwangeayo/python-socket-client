import asyncio
import websockets
import threading
import time

class BaristaCall:
    isConnect = False
    socket = None
    messageQueue = asyncio.Queue()

    def __init__(self, url: str = None) -> None:
        if url is None:
            self.url = "ws://192.168.0.136:8811"
        else:
            self.url = url

        self.socketLoop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.start_loop)
        self.thread.start()

    def start_loop(self) -> None:
        print("루프 시작")
        asyncio.set_event_loop(self.socketLoop)
        self.socketLoop.run_until_complete(self.start())

    async def start(self):
        print("스타트")
        start_time = time.time()  # 시작 시간 측정
        connect = await self.connect(1)
        end_time = time.time()  # 종료 시간 측정
        print(f"connect 완료 {connect} (소요 시간: {end_time - start_time:.2f}초)")
        if connect:
            t1 = asyncio.create_task(self.socketReceive())
            t2 = asyncio.create_task(self.socketSendForQueue())
            await asyncio.gather(t1, t2)
        else:
            print("연결 실패")

    async def callRobot(self, data) -> None:
        await self.messageQueue.put(data)
        print(f"메시지가 큐에 추가되었습니다: {data}")

    async def connect(self, count: int) -> bool:
        while True:
            try:
                print("연결 시도 중...")
                async with websockets.connect(self.url) as websocket:
                    self.socket = websocket
                    BaristaCall.isConnect = True
                    print("연결!")
                    return True
            except Exception as e:
                count += 1
                BaristaCall.isConnect = False
                print(f"e: {e}")
                if count > 3:
                    return False

    async def socketReceive(self):
        print("리시버 실행")
        while True:
            messageRecv = await self.socket.recv()
            print(f"받은 메시지: {messageRecv}")

    async def socketSendForQueue(self) -> None:
        print("socketSendForQueue")
        while True:
            message = await self.messageQueue.get()
            print(f"보낸다! {message}")
            await self.socket.send(message)

if __name__ == "__main__":
    call = BaristaCall()
    print("실행이?")

    async def main():
        await asyncio.sleep(5)  # 초기 연결 대기 시간
        await call.callRobot("반가워!!")
        await asyncio.sleep(3)
        await call.callRobot("니이름??")
        await asyncio.sleep(1)
        await call.callRobot("어쩔??")

    asyncio.run(main())
