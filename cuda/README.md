Requirement 
1. NVIDIA GPU 설치
2. (아마도) CUDA Toolkit 설치
3. cupy 라이브러리 설치 : 
- pip install cupy 는 컴파일 과정을 거치는데 오래걸리고 실패가능성 있음(본인 실패함). 
- pip install cupy-cuda11x 또는 pip install cupy-cuda12x 로 바이너리 설치하는 것 추천. (툴킷버전 따라서)

ChatGPT 따라한거라 자세한 내용은 모름. 
그 외 특별한 것은 없는 듯 함. 

노트북 기준
CPU(5800h, 싱글쓰레드)보다 
GPU(3050Ti Laptop) 이 *14배 정도 빠른 듯 함.


== CPU ==
C:\~~~>ptf2.py
Calculating Tetration:   4%|█▋                                     | 21/500 [00:00<00:07, 60.36it/s]C:\~~~\ptf2.py:28: RuntimeWarning: overflow encountered in power
  z = np.power(c, z)
C:\~~~\ptf2.py:28: RuntimeWarning: invalid value encountered in power
  z = np.power(c, z)
Calculating Tetration: 100%|██████████████████████████████████████| 500/500 [00:07<00:00, 69.74it/s]



C:\~~~>ptf2_cuda.py
Calculating Tetration: 100%|█████████████████████████████████████| 500/500 [00:00<00:00, 937.47it/s]

C:\~~~>ptf2_cuda.py
Calculating Tetration: 100%|████████████████████████████████████| 500/500 [00:00<00:00, 1053.61it/s]
