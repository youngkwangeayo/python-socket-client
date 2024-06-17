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
        loop = asyncio.get_event_loop()
        loop.create_task(self.start())
        loop.close()
        

    async def start(self):
        
        await self.connect(1)

    async def callRobot(self,data) -> None :
        # if dataCheck()
        self.messgeQueue.put(data)
        

    async def connect(self, count:int) -> bool:
        if self.socket is None :
            self.socket = websockets
        
            try :
                async with self.socket.connect(self.url) as socket:
                    self.socket = socket
                    BaristaCall.isConnect = True
                    asyncio.create_task(self.socketReceive())
                    asyncio.create_task(self.socketSendForQueue())
                    

            except Exception as e:
                BaristaCall.isConnect = False
                print("!",self.url, " : " ,e)
                if count <3 :
                    count = count + 1
                    return await self.connect(count)
                return False
        
    
    async def socketReceive(self)-> str :
        # self.socket
        while True:
           messgeRecv = await self.socket.recv()
           print(messgeRecv)
           return messgeRecv
    
    async def socketSendForQueue(self) ->None :
        
        while True:
            if self.messgeQueue.empty() == False:
                massege = self.messgeQueue.get()
                await self.socket.send(massege)
    




if __name__ == "__main__":
    call = BaristaCall()
    # print("실행이?")
    # time.sleep(30)
    # loop = asyncio.get_event_loop()
    # loop.create_task(call.connect())
    # loop.close()
    # asyncio.
    # threading.Thread(target=theardTest, args=(call,)).start()

    