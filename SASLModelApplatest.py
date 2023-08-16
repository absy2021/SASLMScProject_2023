from PIL import Image, ImageTk
import tkinter as tk
import cv2
import os
from PIL import Image as Img
import textblob
from tkinter import*
from tkinter import ttk ,messagebox
import numpy as np
from keras.models import model_from_json
import operator
import time
import googletrans
import sys, os
import matplotlib.pyplot as plt
import enchant
from string import ascii_uppercase

class Application:
    def __init__(self):

        self.vs = cv2.VideoCapture(0)
        self.current_image = None
        self.current_image2 = None

        self.selected_symbol = None
        self.selected_symbol_frame_count = 0
        self.blank_symbol_frame_count = 0

        self.word = ""
        
        self.json_file = open("betterSASLmodel.json", "r")
        self.model_json = self.json_file.read()
        self.json_file.close()
        self.loaded_model = model_from_json(self.model_json)
        self.loaded_model.load_weights("betterSASLmodel.h5")

        self.json_file_dru = open("betterSASLmodelDUnew.json" , "r")
        self.model_json_dru = self.json_file_dru.read()
        self.json_file_dru.close()
        self.loaded_model_dru = model_from_json(self.model_json_dru)
        self.loaded_model_dru.load_weights("betterSASLmodelDUnew.h5")

        self.json_file_tkdi = open("betterSASLmodelTInew.json" , "r")
        self.model_json_tkdi = self.json_file_tkdi.read()
        self.json_file_tkdi.close()
        self.loaded_model_tkdi = model_from_json(self.model_json_tkdi)
        self.loaded_model_tkdi.load_weights("betterSASLmodelTInew.h5")

        self.json_file_smn = open("betterSASLmodelSNnew.json" , "r")
        self.model_json_smn = self.json_file_smn.read()
        self.json_file_smn.close()
        self.loaded_model_smn = model_from_json(self.model_json_smn)
        self.loaded_model_smn.load_weights("betterSASLmodelSNnew.h5")
        
        self.ct = {}
        self.ct['blank'] = 0
        self.blank_flag = 0
        for i in ascii_uppercase:
          self.ct[i] = 0
        #print("Loaded model from disk")
        self.root =tk.Tk()
        self.root.title("SASL MODEL")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.root.geometry("900x1100")
        self.panel = tk.Label(self.root)
        self.panel.place(x = 135, y = 10, width = 640, height = 640)
        self.panel2 = tk.Label(self.root) # initialize image panel
        self.panel2.place(x = 460, y = 95, width = 310, height = 310)
        
        self.T = tk.Label(self.root)
        self.T.place(x=400,y = 17)
        self.T.config(text = "SASL TRANSLATOR",font=("courier",35,"bold"))
        self.panel3 = tk.Label(self.root) # Current SYmbol
        self.panel3.place(x = 200,y=565)
        self.T1 = tk.Label(self.root)
        self.T1.place(x = 10,y = 570)
        self.T1.config(text="LETTER:",font=("Courier",20,"bold"))
        self.panel4 = tk.Label(self.root) # Word
        self.panel4.place(x = 200,y=605)
        self.T2 = tk.Label(self.root)
        self.T2.place(x = 10,y = 610)
        self.T2.config(text ="WORD:",font=("Courier",20,"bold"))
        self.panel5 = tk.Label(self.root) # Sentence
        self.panel5.place(x = 180,y=645)

        self.T3 = tk.Label(self.root)
        self.T3.place(x = 10,y = 650)
        self.T3.config(text ="SENTENCE:",font=("Courier",20,"bold"))
        ##self.T4.place(x=250, y=700)
        #self.T4.config(text="HINTS FOR WORDS", fg="green", font=("Courier", 15, "bold"))
        self.T5 = tk.Label(self.root)
        self.T5.place(x=860, y=540)
        self.T5.config(text="TRANSLATOR", fg="blue", font=("Courier", 20, "bold"))

        self.frame1 = tk.Frame(self.root, bg="wheat")
        self.frame1.grid(row=0, column=0, padx=10, pady=5)
        self.frame1.place(x=770, y=580)
        def translate_it():
            # delete  any  previous  translations
            self.translated_text.delete("0.0", "end")

            try:
                # get the  languages  from  the  dictionary keys
                # get the  from  language key
                for key, value in self.languages.items():
                    if (value == self.original_combo.get()):
                        self.from_language_key = key
                # get  the  to language key
                for key, value in self.languages.items():
                    if (value == self.translated_combo.get()):
                        self.to_language_key = key

                self.words = textblob.TextBlob(self.panel5.cget('text'))
                # translate  the  text
                # output translated  text to  screen
                self.translated_text.insert("0.0", self.words.translate(from_lang=self.from_language_key, to=self.to_language_key))

            except Exception as e:
                messagebox.showerror("Translator", e)



        self.languages = googletrans.LANGUAGES
        self.language_list = list(self.languages.values())
        self.original_text = Text(self.frame1,width=25,height=5,  bg="white" ,font=("Helvetica",15))
        #self.original_text.insert("0.0".0, "hello")
        #self.original_text=self.words
        self.original_text.grid(row=0, column=0, padx=10, pady=10)
        self.translate_button = Button(self.frame1, text="Translate", font=("Helvetica",10),bg="grey",command=translate_it)
        self.translate_button.grid(row=0, column=1, padx=10, pady=10)
        self.translated_text = Text(self.frame1, height=5, width=25 ,font=("Helvetica",15))
        self.translated_text.grid(row=0, column=2, padx=10, pady=10)
        # combo boxes
        self.original_combo = ttk.Combobox(self.frame1, width=30, value=self.language_list)
        self.original_combo.current(21)
        self.original_combo.grid(row=1, column=0)

        def clear():
            # clear textboxes
            self.original_text.delete(1.0, END)
            self.translated_text.delete(1.0, END)
        self.translated_combo = ttk.Combobox(self.frame1, width=30, value=self.language_list)
        self.translated_combo.current(81)
        self.translated_combo.grid(row=1, column=2)
        # clear button
        self.clear_button = Button(self.frame1, text="clear", command=clear)
        self.clear_button.grid(row=2, column=1)
        self.str=" "
        self.word=" "
        self.sentence=" "
        self.current_symbol="Empty"
        self.photo="Empty"
        self.video_loop()

    def video_loop(self):
        ok, frame = self.vs.read()
        if ok:
            cv2image = cv2.flip(frame, 1)
            x1 = int(0.5*frame.shape[1])
            y1 = 10
            x2 = frame.shape[1]-10
            y2 = int(0.5*frame.shape[1])
            cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,0,0) ,1)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)
            self.current_image = Img.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)
            cv2image = cv2image[y1:y2, x1:x2]
            gray = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray,(5,5),2)
            th3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
            ret, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            
            self.predict(res)
            self.selectWordBasedOnFrameRate()

            self.current_image2 = Img.fromarray(res)
            imgtk = ImageTk.PhotoImage(image=self.current_image2)
            self.panel2.imgtk = imgtk
            self.panel2.config(image=imgtk)
            self.panel3.config(text=self.current_symbol,font=("Courier",25))
            self.panel4.config(text=self.word,font=("Courier",25))
            self.panel5.config(text=self.str,font=("Courier",25))
            self.predicts = self.word
        self.root.after(30, self.video_loop)


    def predict(self,test_image):
        test_image = cv2.resize(test_image, (128,128))
        result = self.loaded_model.predict(test_image.reshape(1, 128, 128, 1))
        result_dru = self.loaded_model_dru.predict(test_image.reshape(1 , 128 , 128 , 1))
        result_tkdi = self.loaded_model_tkdi.predict(test_image.reshape(1 , 128 , 128 , 1))
        result_smn = self.loaded_model_smn.predict(test_image.reshape(1 , 128 , 128 , 1))
        prediction={}
        prediction['blank'] = result[0][0]
        inde = 1
        for i in ascii_uppercase:
            prediction[i] = result[0][inde]
            inde += 1
        #LAYER 1
        prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
        self.current_symbol = prediction[0][0]
        #LAYER 2
        if(self.current_symbol == 'D' or self.current_symbol == 'R' or self.current_symbol == 'U'):
        	prediction = {}
        	prediction['D'] = result_dru[0][0]
        	prediction['R'] = result_dru[0][1]
        	prediction['U'] = result_dru[0][2]
        	prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
        	self.current_symbol = prediction[0][0]

        if(self.current_symbol == 'D' or self.current_symbol == 'I' or self.current_symbol == 'K' or self.current_symbol == 'T'):
        	prediction = {}
        	prediction['D'] = result_tkdi[0][0]
        	prediction['I'] = result_tkdi[0][1]
        	prediction['K'] = result_tkdi[0][2]
        	prediction['T'] = result_tkdi[0][3]
        	prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
        	self.current_symbol = prediction[0][0]

        if(self.current_symbol == 'M' or self.current_symbol == 'N' or self.current_symbol == 'S'):
        	prediction1 = {}
        	prediction1['M'] = result_smn[0][0]
        	prediction1['N'] = result_smn[0][1]
        	prediction1['S'] = result_smn[0][2]
        	prediction1 = sorted(prediction1.items(), key=operator.itemgetter(1), reverse=True)
        	if(prediction1[0][0] == 'S'):
        		self.current_symbol = prediction1[0][0]
        	else:
        		self.current_symbol = prediction[0][0]
 
    def selectWordBasedOnFrameRate(self):                       

        print("SYMBOL = " + self.current_symbol)

        # count the frame rate
        if(self.current_symbol == self.selected_symbol):
             self.selected_symbol_frame_count += 1
             if(self.current_symbol == 'blank'):
                  self.blank_symbol_frame_count += 1
        else:
             self.selected_symbol = self.current_symbol
             self.selected_symbol_frame_count = 0
             self.blank_symbol_frame_count = 0
             
        if(self.selected_symbol_frame_count  > 10 or self.blank_symbol_frame_count >3):

            if self.current_symbol == 'blank':
                if self.blank_flag == 0:
                    self.blank_flag = 1
                    if len(self.str) > 0:
                        self.str += " "
                    self.str += self.word
                    self.word = " "
                    self.original_text.delete("0.0", "end")
                    self.original_text.insert("0.0",self.str)

            else:
                if(len(self.str)>60):
                    self.str = " "
                self.blank_flag = 0

                self.word += self.current_symbol
                self.sentence += self.word

            # Clear current symbol and frame count
            self.current_symbol = None
            self.selected_symbol_frame_count = 0
            self.blank_symbol_frame_count = 0

    def destructor(self):
        print("Closing Application...")
        self.root.destroy()
        self.vs.release()
        cv2.destroyAllWindows()
    
    def destructor1(self):
        print("Closing Application...")
        self.root1.destroy()

    def action_call(self):
        
        self.root1 = tk.Toplevel(self.root)
        self.root1.title(" SASLMODEL")
        self.root1.protocol('SASLMODEL_DELETE_WINDOW', self.destructor1)
        self.root1.geometry("900x900")
        

print("Starting Application...")
pba = Application()
pba.root.mainloop()
