import tkinter
from tkinter import *

from tkinter.simpledialog import askstring
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askokcancel

root = tkinter.Tk(className=" CoffeeEdit V0.01")



class Exit(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.pack()
		frm = Frame(parent)
		frm.pack(fill=X)
		Button(frm, text="Exit",  command=self.quit).pack(side=RIGHT)
	def quit(self):
		ans = askokcancel("Exit?", "Are you sure you want to exit?")
		if ans: Frame.quit(self)

class ScrolledText(Frame):
	def __init__(self, parent=None, text='', file=None):
		Frame.__init__(self, parent)
		self.pack(expand=YES, fill=BOTH)
		self.makewidgets()
		self.settext(text, file)
        
	def makewidgets(self):
		sbar = Scrollbar(self)
		text = Text(self, relief=SUNKEN)
		sbar.config(command=text.yview)
		text.config(yscrollcommand=sbar.set)
		sbar.pack(side=RIGHT, fill=Y)
		text.pack(side=LEFT, expand=YES, fill=BOTH)
		self.text = text
	def settext(self, text='', file=None):
		if file:
			text = open(file, 'r').read()
		self.text.delete('1.0', END)
		self.text.insert('1.0', text)
		self.text.mark_set(INSERT, '1.0')
		self.text.focus()
	def gettext(self):
		return self.text.get('1.0', END+'-1c')

class CoffeeEdit(ScrolledText):
	def __init__(self, parent=None, file=None):
		frm = Frame(parent)
		frm.pack(fill=X)
		Button(frm, text="Open",  command=self.onOpen).pack(side=LEFT)
		Button(frm, text="Save",  command=self.onSave).pack(side=LEFT)

		Button(frm, text="Find",  command=self.onFind).pack(side=LEFT)
		Exit(frm).pack(side=LEFT)
		ScrolledText.__init__(self, parent, file=file)
		self.text.config(font=('sans', 12, 'normal'))
	def onSave(self):
		filename = asksaveasfilename()
		if filename:
			alltext = self.gettext()
			open(filename, 'w').write(alltext)

	def onOpen(self):

		filename = askopenfilename()
		if filename:
			text = open(filename).read()
			self.text.delete('1.0', END)
			self.text.insert('1.0', text)
			self.text.mark_set(INSERT, '1.0')
			self.text.focus()
			# print(text) ******use this line to ensure opening of a file is working***************

	def onFind(self):
		target = askstring("Enter a search term", "Search")
		if target:
			where = self.text.search(target, INSERT, END)
			if where:
				print (where)
				pastit = where + ('+%dc' % len(target))
				#self.text.tag_remove(SEL, '1.0', END)
				self.text.tag_add(SEL, where, pastit)
				self.text.mark_set(INSERT, pastit)
				self.text.see(INSERT)
				self.text.focus()

if __name__ == '__main__':
	try:
		CoffeeEdit(file=sys.argv[1]).mainloop()
	except IndexError:
		CoffeeEdit().mainloop()
