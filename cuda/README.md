# CUDA 명령어용 실행파일 (for Nvidia GPU)

## 요구 사항
1. NVIDIA GPU 설치
2. (아마도) CUDA Toolkit 설치
3. 라이브러리 설치:
   - `pip install cupy`는 컴파일 과정을 거쳐 오래 걸리고 실패 가능성이 있습니다. 
   - 바이너리 설치를 권장합니다: `pip install cupy-cuda11x` 또는 `pip install cupy-cuda12x` (툴킷 버전에 따라)
   - 그 외에도 `tqdm`, `tkinter` 등의 라이브러리가 설치되어 있어야 합니다.

**Note:** ChatGPT에 의해 수정되었으며, 자세한 내용은 ChatGPT의 지식에 따라 작성되었습니다. 특별한 변경 사항은 없습니다.

## 성능 개선

노트북 기준 CPU(5800h, 싱글 쓰레드)보다 GPU(3050Ti Laptop)가 *14배 정도 빠른 것으로 나타났습니다. 하지만 코드가 병렬 연산에 적합하게 작성되지 않았기 때문에 생각보다 차이가 크지 않은 것으로 보입니다.

**참고:** 병렬 연산 최적화를 위해 ChatGPT에 요청했지만, 개선이 이루어지지 않았습니다.

## 파일 설명

### ptf2_cuda.py
- 샘플의 기본 파일을 CUDA에서 실행되도록 수정했습니다.

### ptf2_cuda_zoom.py
- ptf2_cuda.py + 기능 확장된 파일입니다.
- 마우스로 확대할 구역을 지정하여 확대합니다.
- 더블 클릭 시 무시되도록 변경했습니다. 
- Zoom Out 버튼을 추가하였습니다. 
