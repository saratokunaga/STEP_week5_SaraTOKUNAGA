#!/usr/bin/env python3

import sys
import math
import random

from common import print_tour, read_input

# cities = [(x0, y0), (x1, y1), ...]
def solve(cities):
    
    current_city = 0 # ０を最初のノードに指定
    visited = set([0]) # ０を格納
    whole_distance = 0 #全体の長さを計測
    tour = [0] #探索にsetを使いたいので、答えになる都市のインデックスの配列は別で用意する
    
    while len(visited) <= len(cities) - 1: # visitedに最後から一個前までのインデックスが入るまで続ける、最終的にcurrent_cityは最後の都市を指す
        current_donyoku = donyoku(cities, current_city, visited) #計算が一回で済むように格納
        (current_city, visited) = (current_donyoku[0], current_donyoku[1]) #nodeとvisitedの更新
        whole_distance += current_donyoku[2] #distanceを更新
        tour.append(current_city) #answerに更新された都市を格納

    whole_distance += distance(cities[current_city], cities[0]) #最後の都市と０を結んで全体距離に加える

    answer = heuristic(cities, tour, whole_distance)

    return answer


    

def donyoku(cities, current_city, visited): # 貪欲法（各都市のxy座標の配列、現在の都市のインデックス、既訪都市のリスト）
    #current_cityから、一番近い都市を見つけ、その都市のインデックスと、その都市を加えた新しいvisitedと、その都市までの距離の累計を返す

    min_distance = 10000 # 絶対にあとで更新されるように大きな数に

    for i in range(len(cities)): # インデックスで探す
        
        if i not in visited: # visitedにないものだけ取り出す
            current_distance = distance(cities[current_city], cities[i])

            if current_distance < min_distance:
                min_distance = current_distance # current_cityとの距離がより短いノードが見つかったら更新
                nearest_city = i # ノードのインデックスを記録

    visited.add(nearest_city) # 最短を記録するノードが見つかったら、visitedの更新
    
    return(nearest_city, visited, min_distance)


def heuristic(cities, tour, whole_distance):
    
    swaps = True
    min_distance = whole_distance #最短のルートを記録しておく
    count = 1

    while swaps:
        swaps = False

        for i in range(len(tour) - 3):
            for j in range(i + 1, len(tour) - 2): # j+1を右端にするため調整
                
                distance_prev = distance(cities[tour[i]], cities[tour[i + 1]]) + distance(cities[tour[j]], cities[tour[j + 1]])
                # i番目からi+1番目へ伸びるエッジj番目からj+1番目へ伸びるエッジ
                distance_new = distance(cities[tour[i]], cities[tour[j]]) + distance(cities[tour[i + 1]], cities[tour[j + 1]])
                # i番目からj番目へ伸びるエッジi+1番目からj+1番目へ伸びるエッジ 
                # i+1とj, j+1とiはつながっているので、連結にするためにiとj, j+1とiとをつなぎたい

                if distance_prev > distance_new: #元の長さの方が長かったら
                    
                    whole_distance = whole_distance - distance_prev + distance_new
                  
                    tour = tour[:i+1] + tour[(i+1):(j+1)][::-1] + tour[j+1:] #tourの、i+1からjまでを反転させる

                    if min_distance > whole_distance: #ランダム変化によって、最小じゃない局所解に落ちる可能性があるので、対策として最小値とそのルートを記録しておく
                        min_distance = whole_distance
                        min_tour = tour[:]
                    swaps = True

                else: #ルートを変えることで長くなるとしても変えてみる（焼きなまし法）
                    count += 1
                    distance_ratio = int(distance_new * 100000 / distance_prev) #変えることで1.23456倍の長さになるとしたら、12345を示す
                    # 距離の、変化前後での比が、実際に変化させるかどうかの確率に比例。つまり、変えることで２倍になるなら、1/20000で変える。3倍になるなら、1/30000で変える。

                    if random.randrange(distance_ratio * count) == 0:
                        whole_distance = whole_distance + distance_new - distance_prev
                        tour = tour[:i+1] + tour[(i+1):(j+1)][::-1] + tour[j+1:] #tourの、i+1からjまでを反転させる
                        swaps = True

    return (min_tour, min_distance)


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)



if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
