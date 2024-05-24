Requirement 
1. NVIDIA GPU 설치
2. (아마도) CUDA Toolkit 설치
3. cupy 라이브러리 설치 : 
- pip install cupy 는 컴파일 과정을 거치는데 오래걸리고 실패가능성 있음(본인 실패함). 
- pip install cupy-cuda11x 또는 pip install cupy-cuda12x 로 바이너리 설치하는 것 추천. (툴킷버전 따라서)

ChatGPT 따라한거라 자세한 내용은 모름. 
그 외 특별한 것은 없는 듯 함. 

---

노트북 기준
CPU(5800h, 싱글쓰레드)보다 
GPU(3050Ti Laptop) 이 *14배 정도 빠른 듯 합니다. 
생각보다 차이가 안나는 것은, 아마도 코드가 병렬연산에 적합하게 짜여지지 않았기 때문일 것으로 추정합니다.

***

___ 
