from tkinter import *
from tkinter import messagebox
import os
import webbrowser
import numpy as np
import pandas as pd

class HyperlinkManager:
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)
        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

# Load datasets with error handling
def load_dataset(file_name):
    try:
        return pd.read_csv(file_name)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {file_name}")
        return None

training_dataset = load_dataset('Training.csv')
test_dataset = load_dataset('Testing.csv')

if training_dataset is not None:
    X = training_dataset.iloc[:, 0:132].values
    Y = training_dataset.iloc[:, -1].values

    dimensionality_reduction = training_dataset.groupby(training_dataset['prognosis']).max()

    from sklearn.preprocessing import LabelEncoder
    labelencoder = LabelEncoder()
    y = labelencoder.fit_transform(Y)

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

    from sklearn.tree import DecisionTreeClassifier
    classifier = DecisionTreeClassifier()
    classifier.fit(X_train, y_train)

    cols = training_dataset.columns[:-1]

    from sklearn.tree import _tree

    def print_disease(node):
        node = node[0]
        val = node.nonzero()
        disease = labelencoder.inverse_transform(val[0])
        return disease

    def recurse(node, depth):
        global val, ans, tree_, feature_name, symptoms_present
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            yield name + " ?"
            ans = ans.lower()
            val = 1 if ans == 'yes' else 0
            if val <= threshold:
                yield from recurse(tree_.children_left[node], depth + 1)
            else:
                symptoms_present.append(name)
                yield from recurse(tree_.children_right[node], depth + 1)
        else:
            present_disease = print_disease(tree_.value[node])
            QuestionDigonosis.objRef.txtDigonosis.insert(END, f"You may have: {present_disease}\n")

    def tree_to_code(tree, feature_names):
        global tree_, feature_name, symptoms_present
        tree_ = tree.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]
        symptoms_present = []

    def execute_bot():
        tree_to_code(classifier, cols)

class QuestionDigonosis(Frame):
    objIter = None
    objRef = None
    def __init__(self, master=None):
        master.title("Question")
        master.state("normal")
        QuestionDigonosis.objRef = self
        super().__init__(master=master)
        self["bg"] = "light blue"
        self.createWidget()

    def createWidget(self):
        self.lblQuestion = Label(self, text="Question", width=12, bg="bisque")
        self.lblQuestion.grid(row=0, column=0, rowspan=4)
        self.txtQuestion = Text(self, width=100, height=4)
        self.txtQuestion.grid(row=0, column=1, rowspan=4, columnspan=20)
        self.txtDigonosis = Text(self, width=100, height=14)
        self.txtDigonosis.grid(row=4, column=1, columnspan=20, rowspan=20, pady=5)
        self.btnNo = Button(self, text="No", width=12, bg="bisque", command=self.btnNo_Click)
        self.btnNo.grid(row=25, column=0)
        self.btnYes = Button(self, text="Yes", width=12, bg="bisque", command=self.btnYes_Click)
        self.btnYes.grid(row=25, column=1, columnspan=20, sticky="e")
        self.btnClear = Button(self, text="Clear", width=12, bg="bisque", command=self.btnClear_Click)
        self.btnClear.grid(row=27, column=0)
        self.btnStart = Button(self, text="Start", width=12, bg="bisque", command=self.btnStart_Click)
        self.btnStart.grid(row=27, column=1, columnspan=20, sticky="e")

    def btnNo_Click(self):
        global val, ans
        ans = 'no'
        str1 = QuestionDigonosis.objIter.__next__()
        self.txtQuestion.delete(0.0, END)
        self.txtQuestion.insert(END, str1 + "\n")

    def btnYes_Click(self):
        global val, ans
        ans = 'yes'
        self.txtDigonosis.delete(0.0, END)
        str1 = QuestionDigonosis.objIter.__next__()

    def btnClear_Click(self):
        self.txtDigonosis.delete(0.0, END)
        self.txtQuestion.delete(0.0, END)

    def btnStart_Click(self):
        execute_bot()
        self.txtDigonosis.delete(0.0, END)
        self.txtQuestion.delete(0.0, END)
        self.txtDigonosis.insert(END, "Please Click on Yes or No for the Above symptoms in Question")
        QuestionDigonosis.objIter = recurse(0, 1)
        str1 = QuestionDigonosis.objIter.__next__()
        self.txtQuestion.insert(END, str1 + "\n")

root = Tk()
frmMainForm = QuestionDigonosis(root)
frmMainForm.pack()
root.mainloop()


