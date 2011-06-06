#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

class MS:
  def __init__(self, x, y, network, p):
    self.__bts_list = set()
    self.bts = None
    self.pos_x = x
    self.pos_y = y
    self.pref_network = network
    self.p = p
    self.__last_move = random.randint(0, 7)

  def update_bts_list(self, bts_list):
    self.__bts_list = bts_list

    # TODO
    self.bts = random.choice(list(bts_list))

  def random_move(self, max_x, max_y):
    # Move MS randomly
    dir_change = random.randint(0, 300)

    # Change direction ?
    if dir_change in range(5):
      self.__last_move = (self.__last_move + 7) % 8
    elif dir_change in range(5, 10):
      self.__last_move = (self.__last_move + 1) % 8
    elif dir_change in range(10, 12):
      self.__last_move = (self.__last_move + 6) % 8
    elif dir_change in range(12, 14):
      self.__last_move = (self.__last_move + 2) % 8
    elif dir_change in range(14, 80):
      return

    # Move
    if self.__last_move in (7, 0, 1):
      self.pos_x += 1
    if self.__last_move in (1, 2, 3):
      self.pos_y += 1
    if self.__last_move in (3, 4, 5):
      self.pos_x -= 1
    if self.__last_move in (5, 6, 7):
      self.pos_y -= 1

    # MS on border of the map : go back !
    if self.pos_x < 0:
      self.pos_x = 0
      self.__last_move = (self.__last_move + 4) % 8
    elif self.pos_x > max_x:
      self.pos_x = max_x
      self.__last_move = (self.__last_move + 4) % 8
    elif self.pos_y < 0:
      self.pos_y = 0
      self.__last_move = (self.__last_move + 4) % 8
    elif self.pos_y > max_y:
      self.pos_y = max_y
      self.__last_move = (self.__last_move + 4) % 8




