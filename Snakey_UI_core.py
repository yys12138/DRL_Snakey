#!/usr/bin/env python3

__author__ = "Yxzh"

import pygame
import sys
from pygame.locals import *
from pygame.color import THECOLORS
import pygame.font


class UI(object):
	def __init__(self, full_screen = False, fps = 60):
		"""
		初始化游戏界面。
		:param full_screen: 是否全屏
		:param fps: 游戏帧率
					根据计算性能，会有实际帧率低于设定帧率的情况。
		"""
		self.PLAYGROUND_WIDTH = 20
		self.PLAYGROUND_HEIGHT = 20  # 游戏区域大小
		self.INFOAREA_WIDTH = 100
		self.INFOAREA_HEIGHT = 200  # 信息区域大小
		WINDOW_TITLE = "Snacky"  # 屏幕标题
		allowed_event = [pygame.KEYDOWN, pygame.QUIT]  # 事件列表
		pygame.init()  # 初始化pygame
		pygame.display.set_caption(WINDOW_TITLE)  # 窗口标题
		self.fps_clock = pygame.time.Clock()  # 创建FPS时钟对象
		pygame.event.set_allowed(allowed_event)  # 设置事件过滤
		if full_screen:  # 根据是否全屏创建屏幕Surface
			self.s_screen = pygame.display.set_mode(
				(self.PLAYGROUND_WIDTH * 10 + self.INFOAREA_WIDTH, self.PLAYGROUND_HEIGHT * 10), pygame.FULLSCREEN, 0,
				32)
		else:
			self.s_screen = pygame.display.set_mode(
				(self.PLAYGROUND_WIDTH * 10 + self.INFOAREA_WIDTH, self.PLAYGROUND_HEIGHT * 10), 0,
				32)
		self.s_infoarea = pygame.Surface((self.PLAYGROUND_WIDTH * 10, self.PLAYGROUND_HEIGHT * 10), 0,
		                                 32)  # 信息区域Surface
		self.s_gray = pygame.Surface((35, 37), 0, 32)  # 信息区域灰色实时刷新块
		self.s_gray.fill(THECOLORS["gray"])
		self.r_fast_update = pygame.Rect((65, 80), (100, 117))  # 信息区域实时刷新范围
		self.si_snake = pygame.image.load("images/snake.png").convert_alpha()  # 加载图片
		self.si_food = pygame.image.load("images/Pineapple.png").convert_alpha()
		self.si_deadsnake = pygame.image.load("images/dead_snake.png").convert_alpha()
		self.si_gamestart = pygame.image.load("images/game_start.png").convert_alpha()
		self.si_bomb = pygame.image.load("images/bm.png").convert_alpha()
		pygame.font.init()  # 初始化字体
		f_arial = pygame.font.SysFont("arial", 24)  # 加载字体
		f_optima = pygame.font.SysFont("optima", 35)
		f_small_arial = pygame.font.SysFont("arial", 12, 1)
		self.sf_arial_gameover = f_arial.render("GAMEOVER!", 1, THECOLORS["black"])  # 渲染文字
		self.sf_arial_scoreboad = f_arial.render("SCOREBOARD", 1, THECOLORS["black"])
		self.sf_small_arial_restart = f_small_arial.render("Press 'R' to restart.", 1, THECOLORS["black"])
		self.sf_small_arial_scoreboard = f_small_arial.render("Press 'S' to open Scoreboard.", 1, THECOLORS["black"])
		self.sf_small_arial_gamestart = f_small_arial.render("SPACE to start and 'Q' to exit.", 1, THECOLORS["black"])
		self.sf_small_arial_back = f_small_arial.render("Press 'R' to return.", 1, THECOLORS["black"])
		self.sf_small_arial_score = f_small_arial.render("Score: ", 1, THECOLORS["red"])
		self.sf_optima_caption = f_optima.render("SNACKY", 1, THECOLORS["orange"])
		self.sf_small_arial_level = f_small_arial.render("level: ", 1, THECOLORS["black"])
		self.sf_small_arial_current_fps = f_small_arial.render("fps: ", 1, THECOLORS["black"])
		self.sf_small_arial_ate = f_small_arial.render("ate: ", 1, THECOLORS["black"])
		self.sf_small_arial_position = f_small_arial.render("pos: ", 1, THECOLORS["black"])
		self.sf_small_arial_botton = f_small_arial.render("btnreg: ", 1, THECOLORS["black"])
		self.sf_small_arial_direction = f_small_arial.render("direction: ", 1, THECOLORS["black"])
		self.sf_small_arial_dot = f_small_arial.render(".", 1, THECOLORS["black"])
		self.Lsf_small_arial_direction = {
			"W": f_small_arial.render("W", 1, THECOLORS["black"]),
			"S": f_small_arial.render("S", 1, THECOLORS["black"]),
			"A": f_small_arial.render("A", 1, THECOLORS["black"]),
			"D": f_small_arial.render("D", 1, THECOLORS["black"]),
		}
		self.Lsf_small_arial_numbers_black = []
		for i in range(0, 10):
			self.Lsf_small_arial_numbers_black.append(f_small_arial.render(str(i), 1, THECOLORS["black"]))
		self.fps = fps  # 帧率
	
	def show(self, game_core, agent):
		"""
		显示图形界面。
		:param game_core: 游戏物理引擎类
		:param agent: 决策逻辑类
		"""
		self.f_gamestart(self.s_screen, self.fps_clock)  # 开始游戏画面
		while True:  # 屏幕循环
			for event in pygame.event.get():  # 事件循环
				if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_q:  # 退出事件
					pygame.quit()
					sys.exit()
			game_core.next(agent.get_next_direction(game_core.pos, game_core.food_pos, game_core.snakes))  # 获取下一步方向
			self.s_screen.fill(THECOLORS["white"])  # 填充白屏
			self.s_screen.blit(self.si_food,
			                   (game_core.food_pos[0] * 10 - 4, game_core.food_pos[1] * 10 - 5))  # 填充食物图片
			for i in game_core.bombs:  # 填充炸弹图片
				self.s_screen.blit(self.si_bomb, [x * 10 - 2 for x in i])
			for i in game_core.snakes:  # 填充蛇图片
				self.s_screen.blit(self.si_snake, [x * 10 for x in i])
			self.s_infoarea.fill(THECOLORS["gray"])  # 填充信息区域各种信息
			pygame.draw.line(self.s_infoarea, THECOLORS["black"], (0, 0), (0, self.INFOAREA_HEIGHT), 3)  # 分隔线
			self.s_infoarea.blit(self.sf_small_arial_level, (10, 5))  # 难度信息提示
			self.s_infoarea.blit(self.sf_small_arial_ate, (10, 20))  # 食物数量信息
			self.s_infoarea.blit(self.sf_small_arial_position, (10, 35))  # 位置信息
			self.s_infoarea.blit(self.sf_small_arial_direction, (10, 65))  # 方向信息
			self.s_infoarea.blit(self.sf_small_arial_botton, (10, 80))  # 按键寄存信息 （实时刷新）
			self.s_infoarea.blit(self.sf_small_arial_current_fps, (10, 95))  # FPS（实时刷新）
			self.s_infoarea.blit(self.sf_small_arial_dot, (65, 5))
			self.f_show_number(self.s_infoarea, game_core.ate, (65, 20))
			self.f_show_number(self.s_infoarea, game_core.pos[0], (65, 35))
			self.f_show_number(self.s_infoarea, game_core.pos[1], (65, 50))
			self.s_infoarea.blit(self.Lsf_small_arial_direction[game_core.direction], (65, 65))
			self.s_screen.blit(self.s_infoarea, (self.PLAYGROUND_WIDTH * 10, 0))  # 信息Surface填充至屏幕Surface
			pygame.display.flip()  # 将图像内存缓冲刷新至屏幕
			if game_core.deathflag:  # 死亡判定
				self.f_gameover(self.s_screen, self.fps_clock, game_core.ate)  # 游戏结束画面
				return
			self.s_infoarea.blit(self.s_gray, (65, 80))  # 填充实时刷新块（灰色背景）
			self.s_infoarea.blit(self.Lsf_small_arial_direction[game_core.direction], (65, 80))  # 填充按键寄存
			current_fps = self.fps_clock.get_fps() * 10  # 获取实时FPS
			self.s_infoarea.blit(self.Lsf_small_arial_numbers_black[int(current_fps / 100)], (65, 95))  # 填充FPS
			self.s_infoarea.blit(self.Lsf_small_arial_numbers_black[int((current_fps % 100) / 10)], (72, 95))
			self.s_infoarea.blit(self.sf_small_arial_dot, (79, 95))
			self.s_infoarea.blit(self.Lsf_small_arial_numbers_black[int((current_fps % 100) % 10)], (86, 95))
			self.s_screen.blit(self.s_infoarea, (self.PLAYGROUND_WIDTH * 10, 0))  # 将实时填充后的信息Surface填充至屏幕Surface
			pygame.display.update(self.r_fast_update)  # 局部实时屏幕刷新
			self.fps_clock.tick(self.fps)  # FPS等待时钟
	
	def f_show_number(self, surface, number, position):
		"""
		在目标Surface上填充数字
		:param surface: 目标Surface
		:param number: 数字
		:param position: 位置
		"""
		
		surface.blit(self.Lsf_small_arial_numbers_black[int(number / 100)], (position[0], position[1]))
		surface.blit(self.Lsf_small_arial_numbers_black[int((number % 100) / 10)], (position[0] + 7, position[1]))
		surface.blit(self.Lsf_small_arial_numbers_black[int((number % 100) % 10)], (position[0] + 14, position[1]))
		return
	
	def f_gamestart(self, _s_screen, _fps_clock):
		"""
		游戏开始画面
		:param _s_screen: 屏幕Surface
		:param _fps_clock: FPS时钟对象
		"""
		
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_q):  # 退出事件
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN and event.key == K_s:  # 进入计分板画面
					self.f_scoreboard(_s_screen, _fps_clock)
				if event.type == pygame.KEYDOWN and event.key == K_SPACE:  # 进入main()函数
					return
			_s_screen.fill(THECOLORS["white"])
			_s_screen.blit(self.sf_optima_caption, (81, 3))
			_s_screen.blit(self.si_gamestart, (93, 90))
			_s_screen.blit(self.sf_small_arial_gamestart, (62, 52))
			_s_screen.blit(self.sf_small_arial_scoreboard, (62, 70))
			pygame.display.flip()
			_fps_clock.tick(5)
	
	def f_gameover(self, _s_screen, _fps_clock, ate):
		"""
		游戏结束画面
		:param _s_screen: 屏幕Surface
		:param _fps_clock: FPS时钟对象
		:param ate: 食物计数
		"""
		
		fi_score = open("score.s", "a+")  # 将分数写入分数文件 不存在就新建
		fi_score.write(str(ate) + "\n")
		fi_score.close()  # 关闭文件IO流
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_q:  # 退出事件
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN and event.key == K_s:  # 进入计分板画面
					self.f_scoreboard(_s_screen, _fps_clock)
					return
				if event.type == pygame.KEYDOWN and event.key == K_r:  # 重新开始
					return
			_s_screen.fill(THECOLORS["white"])
			_s_screen.blit(self.sf_arial_gameover, (72, 4))
			_s_screen.blit(self.sf_small_arial_score, (100, 35))
			_s_screen.blit(self.sf_small_arial_restart, (92, 50))
			_s_screen.blit(self.sf_small_arial_scoreboard, (62, 65))
			_s_screen.blit(self.si_deadsnake, (80, 75))
			self.f_show_number(_s_screen, ate, (150, 35))  # 填充该局得分
			pygame.display.flip()
			_fps_clock.tick(5)
	
	def f_scoreboard(self, _s_screen, _fps_clock):  # 计分板画面
		"""
		计分板画面
		:param _s_screen: 屏幕Surface
		:param _fps_clock: FPS时钟对象
		"""
		
		fi_score = open("score.s", "r")  # 读取分数文件
		scores = []
		for i in fi_score.readlines():  # 转换为int
			scores.append(int(i))
		fi_score.close()
		scores.sort(reverse = True)  # 倒序排列
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_q:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN and event.key == K_r:  # 重新开始
					return
			_s_screen.fill(THECOLORS["white"])
			_s_screen.blit(self.sf_arial_scoreboad, (65, 4))
			_s_screen.blit(self.sf_small_arial_back, (100, 40))
			for i in range(0, len(scores)):  # 填充排行榜
				_s_screen.blit(self.Lsf_small_arial_numbers_black[i + 1], (130, 60 + 15 * i))
				_s_screen.blit(self.sf_small_arial_dot, (137, 60 + 15 * i))
				self.f_show_number(_s_screen, scores[i], (150, 60 + 15 * i))
				if i > 7:
					break
			pygame.display.flip()
			_fps_clock.tick(5)
