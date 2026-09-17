import os, sys, tkinter as tk

try:
    import pygame
except ImportError:
    pygame = None

def path(p):
    return os.path.join(getattr(sys, "_MEIPASS", os.path.dirname(__file__)), p)

SCENES = {
 "start": ("exterior_crime.jpg", "Murder at the Blackwood Manor", "At 11:47 PM, Sir Adrian Blackwood is found dead inside his locked study. A storm has trapped everyone in the manor. You are the lead investigator, Detective {name}. The killer is still inside.", [("Examine the body", "study"), ("Question the household", "hall")], None),
 "study": ("locked_study.jpg", "The Locked Study", "There is no sign of forced entry. A shattered teacup smells faintly of almonds. The victim's stopped watch reads 11:32. Under the desk lies a torn piece of blue silk.", [("Collect the evidence", "collect_study"), ("Inspect the hidden doorway", "passage")], None),
 "collect_study": ("locked_study.jpg", "Evidence Secured", "You seal the teacup, stopped watch and blue silk as evidence. Someone suddenly runs past the study door.", [("Chase the figure", "chase"), ("Protect the crime scene", "hall")], ("Poisoned Teacup", "Stopped Watch", "Blue Silk")),
 "hall": ("suspects_hall.jpg", "Three Suspects", "Lady Eleanor wears a blue evening dress and claims she was in the library. Dr. Graves says the victim died at midnight. Butler Hale says nobody entered the study—but he owns its master key.", [("Question Lady Eleanor", "eleanor"), ("Question Dr. Graves", "doctor"), ("Question Butler Hale", "butler")], None),
 "eleanor": ("suspects_hall.jpg", "Lady Eleanor", "Eleanor admits arguing with the victim about his will. Her dress is intact, but her blue silk scarf is missing. She says Dr. Graves brought the victim his nightly tea.", [("Collect her statement", "hall"), ("Search her room", "room")], ("Eleanor's Statement",)),
 "doctor": ("doctor_lab.jpg", "Dr. Graves", "The doctor insists death occurred at midnight. Yet if the stopped watch is accurate, his timeline is false. In his medical case is a bottle labelled bitter-almond compound.", [("Seize the bottle", "doctor_evidence"), ("Return to the suspects", "hall")], None),
 "doctor_evidence": ("doctor_lab.jpg", "A Dangerous Discovery", "You seize the chemical bottle. Dr. Graves reaches toward his coat pocket. Decide quickly.", [("Order him to freeze", "arrest_doctor"), ("Step closer", "escape")], ("Almond Compound",)),
 "butler": ("suspects_hall.jpg", "Butler Hale", "Hale admits lending the master key to Dr. Graves at 11:25, supposedly for medicine. He heard the hidden passage close seven minutes later.", [("Collect his testimony", "hall"), ("Search the passage", "passage")], ("Master-Key Testimony",)),
 "room": ("eleanor_room.jpg", "Eleanor.s Room", "You find the missing scarf—cut, but dusty. The torn edge does not match the silk from the study. Someone planted misleading evidence.", [("Collect the scarf", "hall")], ("Unmatched Scarf",)),
 "passage": ("hidden_passage.jpg", "The Hidden Passage", "The passage connects the study to the laboratory. A medical cufflink lies in the dust beside fresh footprints.", [("Collect the cufflink", "hall"), ("Follow the footprints", "doctor")], ("Medical Cufflink",)),
 "chase": ("hidden_passage.jpg", "Footsteps in the Dark", "The figure disappears toward the laboratory. A medical cufflink falls onto the stairs.", [("Take it and question the doctor", "doctor"), ("Search elsewhere", "hall")], ("Medical Cufflink",)),
 "arrest_doctor": ("final_accusation.jpg", "Final Accusation", "Dr. Graves is detained. Now present your conclusion. Who murdered Sir Adrian Blackwood?", [("Accuse Lady Eleanor", "wrong"), ("Accuse Butler Hale", "wrong"), ("Accuse Dr. Graves", "solve")], None),
 "solve": ("final_accusation.jpg", "CASE SOLVED", "The poisoned tea, false timeline, master key, cufflink and chemical bottle expose Dr. Graves. He used the hidden passage and planted blue silk to frame Eleanor. You solved the Blackwood murder.", [], None),
 "wrong": ("exterior_crime.jpg", "THE KILLER ESCAPES", "Your accusation collapses under questioning. During the confusion, Dr. Graves disappears into the storm, taking the final proof with him.", [], None),
 "escape": ("doctor_lab.jpg", "TOO LATE", "You move too close. Graves kills the lights and escapes through the hidden passage. By sunrise, only his abandoned car remains.", [], None),
}

TIMED = {"doctor_evidence": 8}

class Game:
 def __init__(self, root):
    self.r=root; self.r.title("Murder at the Blackwood Manor"); self.r.geometry("1080x820"); self.r.configure(bg="#06101b")
    self.img={}; self.evidence=[]; self.job=None; self.audio=False
    if pygame:
      try:
       pygame.mixer.init(); pygame.mixer.music.load(path("sounds/atmosphere.ogg")); pygame.mixer.music.set_volume(.25); pygame.mixer.music.play(-1); self.audio=True
      except Exception: pass
    self.welcome()
 def clear(self):
    if self.job: self.r.after_cancel(self.job); self.job=None
    for w in self.r.winfo_children(): w.destroy()
 def btn(self,p,t,c): return tk.Button(p,text=t,command=c,font=("Segoe UI",11,"bold"),bg="#9a252d",fg="white",activebackground="#d0a349",relief="flat",cursor="hand2",padx=18,pady=9,wraplength=300)
 def welcome(self):
    self.clear(); self.evidence=[]; f=tk.Frame(self.r,bg="#06101b"); f.pack(expand=True,fill="both")
    tk.Label(f,text="MURDER AT THE\nBLACKWOOD MANOR",font=("Georgia",36,"bold"),fg="#d0a349",bg="#06101b").pack(pady=(130,25))
    tk.Label(f,text="A CRIME INVESTIGATION GAME",font=("Segoe UI",14,"bold"),fg="#849bb2",bg="#06101b").pack()
    tk.Label(f,text="Detective's name",font=("Segoe UI",11),fg="white",bg="#06101b").pack(pady=(35,5))
    self.entry=tk.Entry(f,font=("Segoe UI",15),justify="center"); self.entry.pack(ipady=7); self.entry.focus()
    self.btn(f,"OPEN THE CASE",self.begin).pack(pady=18)
 def begin(self): self.name=self.entry.get().strip() or "Morgan"; self.go("start")
 def image(self,n):
    if n not in self.img: self.img[n]=tk.PhotoImage(file=path("assets/"+n)).subsample(2,2)
    return self.img[n]
 def go(self,s):
    self.clear(); black=tk.Frame(self.r,bg="black"); black.pack(expand=True,fill="both")
    tk.Label(black,text="◆",font=("Georgia",30),fg="#9a252d",bg="black").pack(expand=True)
    self.r.after(180,lambda:self.show(s))
 def show(self,s):
    self.clear(); image,title,text,choices,found=SCENES[s]
    if found:
      for x in found:
       if x not in self.evidence:self.evidence.append(x)
    f=tk.Frame(self.r,bg="#06101b"); f.pack(expand=True,fill="both")
    bar=tk.Frame(f,bg="#101e2c"); bar.pack(fill="x")
    tk.Label(bar,text="EVIDENCE: "+(" • ".join(self.evidence) or "None"),font=("Segoe UI",9,"bold"),fg="#d0a349",bg="#101e2c",wraplength=880).pack(side="left",padx=12,pady=9)
    tk.Button(bar,text="Restart",command=self.welcome,bg="#101e2c",fg="white",relief="flat").pack(side="right",padx=12)
    tk.Label(f,image=self.image(image),bg="#06101b").pack(pady=(8,3))
    tk.Label(f,text=title,font=("Georgia",24,"bold"),fg="#d0a349",bg="#06101b").pack()
    tk.Label(f,text=text.format(name=self.name),font=("Segoe UI",11),fg="#e7edf4",bg="#06101b",wraplength=900,justify="center").pack(padx=30,pady=9)
    controls=tk.Frame(f,bg="#06101b"); controls.pack(pady=5)
    if not choices:
      self.btn(controls,"INVESTIGATE AGAIN",self.welcome).pack(side="left",padx=6); self.btn(controls,"EXIT",self.r.destroy).pack(side="left",padx=6)
    for label,dest in choices:self.btn(controls,label,lambda d=dest:self.go(d)).pack(side="left",padx=5)
    if s in TIMED:self.timer(f,TIMED[s],"escape")
 def timer(self,parent,seconds,dest):
    lab=tk.Label(parent,text=f"DANGER: {seconds} SECONDS",font=("Segoe UI",10,"bold"),fg="#ff625b",bg="#06101b");lab.pack(pady=8)
    def tick(n):
      if n<=0:self.job=None;self.go(dest)
      else:lab.config(text=f"DANGER: {n} SECONDS");self.job=self.r.after(1000,lambda:tick(n-1))
    self.job=self.r.after(1000,lambda:tick(seconds-1))

if __name__=="__main__":
 root=tk.Tk();Game(root);root.mainloop()
