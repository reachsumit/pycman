## Simple Pacman game simulator in Python

#### Please do not misuse this code. It's intended for my personal coding experiments only. I am not responsible for any damage/misuse of the code in this repository.

This is a simple Pacman game simulator in Python.

### Compilation Instructions:
python setup.py develop  
python setup.py sdist bdist_wheel  
twine upload dist/*  

pip install --no-cache-dir --upgrade pycman  

### Install via Pip
```
pip install pycman2
```
(also requires pyglet: conda install -c conda-forge pyglet)

### Usage instructions
```python
from pycman import simulator
simulator.play() ## starts the game
simulator.scorecard() ## shows your current score at each level and current average score
simulator.export() ## dumps a game state json file
```

* You can play only a few levels at one time by passing start and end parameters in the play function call.
e.g. simulator.play(start=13, end=28)

* Game will save all your progress and stepwise environment states even if you shutdown your pc. Note that it won't save progress if you quit prematurely using Esc or Ctrl+C etc

* In simulator.export() you can also pass name and path parameters to specify name and path of the output file you want. Otherwise it will simply dump the result in current folder. e.g. export(name="test_pacman_log.json", path=".")  

![gameplay](https://i.imgur.com/eKAdv5e.png)
