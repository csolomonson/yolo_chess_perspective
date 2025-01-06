import gradio as gr
import os
from chess import set_orientation, get_board, next_move, to_fen
from chessMove2 import move, drop_capture
drop_capture()
M, rect_base = set_orientation(True)
board = [[' ' for n in range(8)] for i in range(8)]

input()
d = {'a':0,'b':1,'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
CONFIRM_BOARD = True

import cv2
import numpy as np
import gradio as gr

move_text = ""
booly = False
fen = ""

def get_return():
  out = []
  for i in range(3):
      img = f"latest_img_{i}.jpg"
      out.append(img)
  out.append(str(board))
  return out

def modify_board(veto, board):
  vetos = veto.split(" ")
  for v in vetos:
      #print(v)
      if len(v) >= 3:
          #board[d[v[0].lower()]][8-int(v[1])] = v[2] if v[2].lower() != 'x' else ' '
          board[8-int(v[1])][d[v[0].lower()]] = v[2] if v[2].lower() != 'x' else ' '
  move_bot("", board)
  return board


def move_bot(text, board):
      # placeholder
  fen, val = to_fen(board)
  if val:
    try:
      start, end, capture = next_move(fen)
    except:
      return get_return()
    if not text:
      move(start,end,capture)
    else:
      modify_board(text, board)
  drop_capture()
  return get_return()

def func(text, cap, move):
  if cap:
    ret = capture_image()
  if move:
    ret = move_bot(text, board)
  return ret

def capture_image():
    # Load the last 5 images from the file system
    global board
    drop_capture()
    board = get_board(M, rect_base)
    #print("By jove, we've got it")
    return get_return()



inputs = [gr.Textbox(lines=2, placeholder="Change board here"),
           gr.Checkbox(label="Capture"),
           gr.Checkbox(label="Move")]


#robot_control = gr.Interface(move_bot, robot_inputs, robot_outputs)

outputs = [gr.Image(type="pil"),
                 gr.Image(type='pil'),
                 gr.Image(type='pil'),
                 gr.Textbox(lines=8)]

thing = gr.Interface(func, inputs, outputs)

#demo = gr.TabbedInterface([robot_control, camera_pics], ["Robot Control", "Images"])

thing.launch()
