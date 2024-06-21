## LocakSocket Client

## `한개의 스레드에서 비동기  멀티테스크 소캣 및 http요청 구현`
>하나의 Thread에서 이벤트 루프를 돌린다.
>하나의 이벤트 루프에서 3가지의 task(업무)를 실행한다.
>task는 각각 다른업무를 동작한다.
> 소캣메세지 받기, 소캣메세지 보내기,  http 요청
> 소캣메세지 보내기와 http 요청은
> 소캣메세지 queue와 http요청 queue를 만들어서 각 task의 queue를 가져와 사용한다.
> 소캣메세지를 받으면 유효성 검사 후 httpQueue에 put 을 시킨다.
> 

 
>
>`task와 thread의 차이`
> 스레드는 cpu바운딩 작업으로 병렬 진행
> asyncio 는 비동기 함수 async와 def로 정의가 되어 await에 제어권이 양도된다.
> 태스크는 멀티테스킹으로 I/O 시스템에서 기다리는 동안 다른함수를 계속진행



## `task 와 thread 활용해서 소캣클라이언트 객채화`
파이썬 클라이언트 소캣 객체화

핸들러쉐이크
- `http get 요청으로 클라이언트의 요청 `
>  GET / HTTP/1.1           : `get 요청이 있어야함 http 와` </br>   
>  Host: 127.0.0.1:8811 </br>
> Connection: Upgrade </br>
> Pragma: no-cache </br>
> Cache-Control: no-cache </br>
> User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 </br>
> Upgrade: websocket                                    `Upgrade: websocket 핸들러쉐이크 이후 변경할 프로토클을 기제해야함` </br>
> Origin: http://192.168.0.136:8090 </br>
> Sec-WebSocket-Version: 13 </br>
> Accept-Encoding: gzip, deflate, br, zstd </br>
> Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7 </br>
> Sec-WebSocket-Key: DVqRpbDEv+q64+ABHCX0Rw== </br>
> Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits </br>
