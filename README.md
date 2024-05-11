# mytetration
Make your own tetration Image!

# 목차
- [**프로그램 설치**](#프로그램-설치)
- 
- [test](#test)

## 프로그램 설치
- mytetration 챌린지에 필요한 프로그램은 총 4가지 입니다 : Visual Studio[^1], Python, NumPy, Matplotlib
- 아래 설치과정에서 문제가 생길시, 문제상황을 [chat GPT](https://chatgpt.com/)에 설명하면 쉽게 해결할 수 있을 겁니다.

---
**Visual Studio 설치 (Window)**
1. [Visual Studio 공식 웹사이트](https://visualstudio.microsoft.com/)에 접속합니다.
2. 'Downloads' 섹션을 찾아 'Community 2024' 버전을 클릭합니다. 이 버전은 무료로 사용할 수 있으며 개인 개발자나 소규모 팀에 적합합니다.
3. 다운로드 페이지에서 'Download' 버튼을 클릭하여 설치 파일을 내려받습니다.
4. 다운로드한 설치 파일을 실행하면 설치 마법사가 시작됩니다.
5. 설치가 완료되면, 컴퓨터를 재시작하라는 메시지가 나타날 수 있습니다. 재시작 후 Visual Studio를 실행할 수 있습니다.

**Visual Studio 설치 (Mac)**
1. [Visual Studio 공식 웹사이트](https://visualstudio.microsoft.com/)에 접속합니다.
2. 화면 상단의 'Download for Mac' 버튼을 클릭합니다.
3. 'Visual Studio 2024 for Mac' 버튼을 클릭하여 Mac용 설치 파일을 다운로드합니다.
4. 다운로드한 .dmg 파일을 열어 설치 프로세스를 시작합니다.
5. 열린 창에서 Visual Studio 아이콘을 'Applications' 폴더로 드래그하여 설치합니다.
---
**Python 설치 (Window)**
1. [파이썬 공식 웹사이트](https://www.python.org/) 상단 메뉴에서 "Downloads"를 클릭한 후, 윈도우 운영체제용 파이썬을 클릭합니다. 보통 "Download Python 3.x.x" (x는 버전 번호) 형식으로 표시됩니다.
2. 다운로드 페이지에서 "Download" 버튼을 클릭하여 설치 파일을 내려받습니다.
3. 다운로드한 설치 파일을 실행합니다. 설치 시작 화면에서 "Add Python 3.x to PATH" 체크박스를 선택하는 것을 잊지 마세요. 이 옵션은 파이썬과 pip을 시스템의 PATH에 자동으로 추가해 줍니다.
4. "Install Now" 버튼을 클릭하여 파이썬 설치를 시작합니다.
5. Visual Studio 실행 후 상단에 보기(View) 메뉴에서 터미널(Terminal)을 클릭하면 화면하단에 터미널 창이 나타납니다.
6. 터미널창에 `python3 --version` 또는 `pip3 --version`을 입력하여 파이썬과 pip이 정상적으로 설치되었는지 확인할 수 있습니다.

**Python 설치 (Mac)**
1. [파이썬 공식 웹사이트](https://www.python.org/) 상단 메뉴에서 "Downloads"를 클릭한 후, macOS 운영체제용 파이썬을 클릭합니다.
2. "Download Python 3.x.x" 버튼을 클릭하여 맥용 설치 파일을 내려받습니다.
3. 다운로드한 .pkg 파일을 더블 클릭하여 설치 마법사를 실행합니다.
4. 화면의 지시에 따라 설치를 진행합니다. 대부분 '계속', '동의', '설치' 버튼을 순서대로 클릭하면 됩니다.
5. Visual Studio 실행 후 상단에 보기(View) 메뉴에서 터미널(Terminal)을 클릭하면 화면하단에 터미널 창이 나타납니다.
6. 터미널창에 `python3 --version` 또는 `pip3 --version`을 입력하여 파이썬과 pip이 정상적으로 설치되었는지 확인할 수 있습니다.
---
**NumPy, Matplotlib 설치**
- 다음명령어를 터미널에 입력하여 NumPy와 Matplotlib를 설치합니다 : `pip3 install numpy matplotlib`
- 설치가 완료되면 터미널에 다음 명령어를 입력하여 각각의 버젼을 확인하여 설치완료여부를 확인 할 수 있습니다 :
  - `python3 -c "import numpy; print(numpy.__version__)"`
  - `python3 -c "import matplotlib; print(matplotlib.__version__)"`


## test
 


[^1]: 다른 IDE를 사용하셔도 됩니다. 초보자분들을 위해 대표적인 프로그램을 선정한것입니다.
