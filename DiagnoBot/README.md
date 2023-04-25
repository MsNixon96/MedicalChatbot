# CSCI-595-Project
Project work for CSCI-595-Medical Chatbot Project

## Getting Started Locally

To run the assistant locally you'll first need to clone. 

```
git clone https://github.com/MsNixon96/CSCI-595-Project.git
```

Next, install rasa. 

```
pip install rasa
```

Next you'll need to train the assistant. 

```
rasa train
```

Once trained, you can now talk to it. Since we're using custom python code 
in there we'll need to run an action server on the side. So first start an
action server (in a split terminal. one terminal starts action server, another server runs rasa server) via;

```
rasa run actions --cors "*" --debug
```

or using;

```
rasa run actions
```

With this running you can now talk to your assistant. 

```
rasa run -m models --enable-api --cors "*" --debug
```

or using;

```
rasa shell
```

## Extra Inspection 

If you want to get more of a view of what is happening you can also run; 

```
rasa shell nlu
```

By running it this way you'll get more of a glimpse in what the NLU components think.

If you want to supply the assistant with new data you can also 
handle this interactively via after running action server since we have custom actions. Rasa interactive can be used to create new stories, rules and etc. via the terminal;

```
rasa interactive
```
