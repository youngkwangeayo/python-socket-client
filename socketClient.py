import asyncio
import websockets
import time
import json
import threading
class BaristaCall :
    
    isConnect = False
    socket = None
    messgeQueue = asyncio.Queue()

    def __init__(self, url:str=None) -> None:
        self.socket = None
        if url is None :
            self.url = "ws://192.168.0.136:8811"
        else :
            self.url = url

        self.socketLoop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.start_loop)
        self.thread.start()
        
    def start_loop(self) ->None:
        print("루프시작")
        asyncio.set_event_loop(self.socketLoop)
        print("루프셋완료")
        self.socketLoop.run_until_complete(self.start())
        

    async def start(self):
        print("스타트")
        con = await self.connect(1)
        print(f"connect 완료{con}")
        if con ==True :
            t1 = asyncio.create_task(self.socketReceive())
            t2 = asyncio.create_task(self.socketSendForQueue())

            await t1
            await t2
            

        else :
            print("연결실패")

    async def callRobot(self,data) -> None :
        # if dataCheck()
        await self.messgeQueue.put(data)
        print(f"메시지가 큐에 추가되었습니다: {data}")
        
    async def connect(self, count:int) -> bool:

        if self.socket is None :
            self.socket = websockets
            
        while True:

            try :
                self.socket = await self.socket.connect(self.url)
                BaristaCall.isConnect = True
                print("연결!")
                return True
                async with self.socket.connect(self.url) as socket:
                    self.socket = socket
                    BaristaCall.isConnect = True
                    print("연결!")
                    return True
                    
            except Exception as e :
                count = count + 1
                BaristaCall.isConnect = False
                print(f"e : {e}")
                if count >3 :
                    count = count + 1
                    return False
            
        

    async def connect2(self, count:int) -> bool:
        if self.socket is None :
            self.socket = websockets
        
            try :
                async with self.socket.connect(self.url) as socket:
                    self.socket = socket
                    BaristaCall.isConnect = True
                    return True
                    

            except Exception as e:
                BaristaCall.isConnect = False
                print(f"(e) {self.url} : {e}")
                if count <3 :
                    count = count + 1
                    print(f"여기 들어와? {count, type(count)}" )
                    return await self.connect(count)
                else :
                    print("여기가 왜나와?")
                return False
        
    
    async def socketReceive(self)-> str :
        print("리시버실행")
        # self.socket
        while True:
           messgeRecv = await self.socket.recv()
           print(messgeRecv)
        #    return messgeRecv
    
    async def socketSendForQueue(self) ->None :
        print("socketSendForQueue")
        while True:
            if not self.messgeQueue.empty():
                massege = self.messgeQueue.get()
                print(f"보낸다! {massege}")
                await self.socket.send(massege)
            else :
                # await asyncio.sleep(1)
                time.sleep(1)
                print("tq",self.messgeQueue.empty())




if __name__ == "__main__":
    call = BaristaCall()
    print("실행이?")
    # time.sleep(30)
    # call.callRobot("반가워!!")
    # time.sleep(3)
    # call.callRobot("니이름??")
    # time.sleep(1)
    # call.callRobot("어쩔??")
    # time.sleep(30)
    # loop = asyncio.get_event_loop()
    # loop.create_task(call.connect())
    # loop.close()
    # asyncio.
    # threading.Thread(target=theardTest, args=(call,)).start()
    async def main():
        await asyncio.sleep(5)
        await call.callRobot("반가워!!")
        await asyncio.sleep(3)
        await call.callRobot("니이름??")
        await asyncio.sleep(1)
        await call.callRobot("어쩔??")

    asyncio.run(main())
    