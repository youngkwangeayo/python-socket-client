import asyncio

class taskTast:

    def __init__(self) -> None:
        asyncio.run(self.start())
        pass

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
    

if __name__ == "__main__":
    taskTast()