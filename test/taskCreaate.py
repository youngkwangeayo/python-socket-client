import asyncio
import threading
import time

class taskTast:

    def __init__(self) -> None:
        # threading.Thread(target=self.start())
        # loop = threading.Thread(target=)
        # asyncio.run(self.start())
        # self.thread = threading.Thread(target=self.start_loop)
        # self.thread.start()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.start())

        pass
    
    # def start_loop(self)->None:
        # asyncio.set_event_loop(self.loop)
        # self.loop.run_until_complete(self.start())

    async def start(self)->None:
        t1 = asyncio.create_task(self.def1("시작"))
        t2 = asyncio.create_task(self.def2("너도시작"))
        await t1
        await t2

    async def def2(self,what)->None:
        while True:
            await asyncio.sleep(1)
            print(f"def2 : {what}")
        
    
    async def def1(self,what)->None:
        while True:
            await asyncio.sleep(2)
            print(f"def1 : {what}")

    def call(self,what)->None:
        print(f"call! : {what}")
        
    

if __name__ == "__main__":
    # t=threading.Thread(taskTast())
    tInstance = taskTast()
    tInstance.call("첫번째!")
    # t.start()
    # t = asyncio.create_task(taskTast())
    
    
    time.sleep(3)
    tInstance.call("두번쨰!")
    print("ddd")