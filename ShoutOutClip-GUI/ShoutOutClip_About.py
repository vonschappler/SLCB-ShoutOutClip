import os
import ttk
import Tkinter as tk
import ShoutOutClip_Theme

def createTab(mainInt):
   tab = ttk.Frame(mainInt)
   tab.pack()
   tab.columnconfigure(0, weight=10)
   tab.rowconfigure(0, weight=10)

   tabHelpFrame = ttk.Labelframe(tab, text=' Aditional Information ', takefocus=0)
   tabHelpFrame.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S, padx=10, pady=10)
   tabHelpText = tk.Text(tabHelpFrame, width=1, height=1, wrap=tk.WORD, takefocus=0)
   try:
      aboutFile = open(os.path.abspath(os.path.join(os.path.dirname(__file__), "assets/ShoutOutClip_About.txt")))
      tabHelpText.insert(tk.END, aboutFile.read())
      aboutFile.close()
   except:
      pass
   tabHelpText.config(state='disabled', selectbackground=ShoutOutClip_Theme.darkGray, selectforeground=ShoutOutClip_Theme.darkWhite, cursor='arrow')
   tabHelpText.pack(fill=tk.BOTH, expand=tk.YES, pady=[5,10])
   tabHelpFrame.columnconfigure(0, weight=10)
   tabHelpFrame.rowconfigure(0, weight=1)
   tabHelpText.grid(column=0, row=0, sticky=tk.W+tk.E+tk.N+tk.S, pady=5)
   scrollY = ttk.Scrollbar(tabHelpFrame, orient=tk.VERTICAL, command=tabHelpText.yview)
   scrollY.grid(column=1, row=0, sticky=tk.E+tk.N+tk.S)
   tabHelpText['yscrollcommand'] = scrollY.set
   return tab