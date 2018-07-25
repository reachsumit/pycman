# -*- coding: utf-8 -*-
import click
import json
import os, shutil
import numpy as np
from pycman.pacman import PacmanGame
import pkg_resources

def play(start=1, end=100):
    """
    Start simulator and play the game.
 
    Use numpad keys to play the game.
    7  -  8  -  9
    4  -  5  -  6
    1  -  2  -  3

    Parameters:
    start: start from this game number (default 1)
    end: end at this game number (default 100)
 
    Returns:
    None
    """
    _PacPlay(start, end)

def scorecard():
    """
    Show the saved full scorecard for all 100 games.
    Parameters:
    None

    Returns:
    None
    """
    with open(pkg_resources.resource_filename(__name__, 'test_pacman_log.json'), 'r') as file:
        saved_game = json.load(file)

    total_score = 0
    for index, game in enumerate(saved_game):
        total_score += game[-1]['total_score']
        print("Game:{} Score:{}".format(index+1, game[-1]['total_score']))
    print("Total score: {}. Average score: {}".format(total_score, (total_score/100.0)))

def export(name="test_pacman_log.json", path="."):
    """
    export the current scorecard to json file.
    Parameters:
    name: Name of the exported file. (default: test_pacman_log.json)
    path: Path for the exported file. (default: current directory)

    Returns:
    None
    """
    if os.path.exists(path):
        shutil.copy2(pkg_resources.resource_filename(__name__, 'test_pacman_log.json'),os.path.join(path,name))
        print("File successfully generated.")


class _PacPlay:
    def __init__(self, start=1, end=100):
        self.test(start, end)
    
    def recommend_next_step(self, obs, eps=0.05):
        print("Possible actions: ", obs['possible_actions'])
        print("press key: ")
        while True:
            key = click.getchar()
            if int(key) in obs['possible_actions']:
                break
            print("Invalid key. Try again: ")
        return int(key)
    
    def preprocess(self, start_state):
        # make tuples from lists
        start_state['player'] = tuple(start_state['player'])
        start_state['monsters'] = [tuple(m) for m in start_state['monsters']]
        start_state['diamonds'] = [tuple(m) for m in start_state['diamonds']]
        start_state['walls'] = [tuple(m) for m in start_state['walls']]


    def test(self, start=1, end=100, log_file='pycman/test_pacman_log.json'):
        with open(pkg_resources.resource_filename(__name__, 'test_params.json'), 'r') as file:
            read_params = json.load(file)

        with open(pkg_resources.resource_filename(__name__, 'test_pacman_log.json'), 'r') as file2:
            saved_game = json.load(file2)
        
        start -=1

        game_params = read_params['params']
        test_start_states = read_params['states']
        total_history = [None] * 100
        total_scores = [None] * 100

        env = PacmanGame(**game_params)
        env.render()
        current_mean = 0

        # Load everything before start
        for i in range(start):
            total_history[i] = saved_game[i]
            total_scores[i] = saved_game[i][-1]['total_score']
        # calculate existing scores for indices between start and end
        for i in range(start, end):
            total_scores[i] = saved_game[i][-1]['total_score']
        # Load everythin after end
        for i in range(end,100):
            total_history[i] = saved_game[i]
            total_scores[i] = saved_game[i][-1]['total_score']
        #total_scores_np = np.array(total_scores)
        if all(v is None for v in total_scores):
            current_mean = 0
        else:
            current_mean = np.mean(np.array(total_scores)[np.array(total_scores)!=None])

        for index, start_state in enumerate(test_start_states):
            if index < start or index>=end:
                print("PASS")
                continue
            self.preprocess(start_state)
            episode_history = []
            env.reset()
            env.player = start_state['player']
            env.monsters = start_state['monsters']
            env.diamonds = start_state['diamonds']
            env.walls = start_state['walls']
            assert len(env.monsters) == env.nmonsters and len(env.diamonds) == env.ndiamonds and len(env.walls) == env.nwalls

            obs = env.get_obs()
            episode_history.append(obs)
            while not obs['end_game']:
                action = self.recommend_next_step(obs)
                obs = env.make_action(action)
                env.render(current_mean=int(current_mean), game_number=index+1)
                episode_history.append(obs)
            total_history[index] = episode_history
            total_scores[index] = obs['total_score']
            current_mean = np.mean(np.array(total_scores)[np.array(total_scores)!=None])
            #print("NUMBER OF GAMES PLAYED: {}. Average Score: {}".format(index+1, np.mean(total_scores)))
        total_scores_np = np.array(total_scores)
        #current_mean = np.mean(total_scores_np[total_scores_np!=None])
        mean_score = np.mean(total_scores_np)
        env.close()
        with open(pkg_resources.resource_filename(__name__, 'test_pacman_log.json'), 'w') as file:
            json.dump(total_history, file)
        print("Your average score is {}!".format(mean_score))
        return mean_score

if __name__ == "__main__":
    _PacPlay()