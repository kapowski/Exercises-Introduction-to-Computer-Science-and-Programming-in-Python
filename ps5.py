# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1
class NewsStory:
    def __init__ (self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
        
    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate
        


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase

    def is_phrase_in(self,text):
        
        # function cleans entered text, removing excess spaces and any punctuation while converting it to lower case
        def text_cleaner(entered_text, cleaned_text):
            for char in entered_text:
                if char not in string.punctuation:
                    cleaned_text += char.lower()
                else:
                    cleaned_text += ' '
            
            cleaned_text = cleaned_text.split()
            cleaned_text = ' '.join(cleaned_text) + ' '
            return cleaned_text
        
        # creates blank texts to be used for text_cleaner function
        text_cleaned = ''
        phrase_cleaned = ''
        
        # cleans text and phrase (I was not sure if phrase needed to be cleaned but added the option anyways)
        text_cleaned = text_cleaner(text, text_cleaned)
        phrase_cleaned = text_cleaner(self.phrase, phrase_cleaned)
        
        # checks to see if the cleaned phrase is in the cleaned text and returns true if so
        if phrase_cleaned in text_cleaned:
            return True
        else:
            return False 
      

# Problem 3
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story): 
        return self.is_phrase_in(story.get_title())


# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story): 
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

    def __init__(self, time):
        
        self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S").replace(tzinfo=pytz.timezone("EST"))

# Problem 6
class BeforeTrigger(TimeTrigger):
    def evaluate(self,story):
        
        story_pub_time = story.get_pubdate()
        story_pub_time = story_pub_time.replace(tzinfo=pytz.timezone("EST"))
        
        if story_pub_time < self.time:
            return True
        else:
            return False 
    
class AfterTrigger(TimeTrigger):
    def evaluate(self,story):
        
        story_pub_time = story.get_pubdate()
        story_pub_time = story_pub_time.replace(tzinfo=pytz.timezone("EST"))
        
        if story_pub_time > self.time:
            return True
        else:
            return False 


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, trig):
        self.trig = trig
    
    def evaluate(self, story):
        return not self.trig.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    def __init__(self, trig_1, trig_2):
        self.trig_1 = trig_1
        self.trig_2 = trig_2
    
    def evaluate(self, story):
        return self.trig_1.evaluate(story) and self.trig_2.evaluate(story)
    

# Problem 9
class OrTrigger(Trigger):
    def __init__(self, trig_1, trig_2):
        self.trig_1 = trig_1
        self.trig_2 = trig_2
   
    def evaluate(self, story):
        return self.trig_1.evaluate(story) or self.trig_2.evaluate(story)
    


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    
    filtered_stories = []
    
    for trigger in triggerlist:
        for story in stories:
            if trigger.evaluate(story):
                filtered_stories.append(story)
    
    return filtered_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    t_map = {"TITLE": TitleTrigger,"DESCRIPTION": DescriptionTrigger,"AFTER": AfterTrigger,"BEFORE": BeforeTrigger,"NOT": NotTrigger,"AND": AndTrigger,"OR": OrTrigger}
    t_num_dict = {}
    t_dict = {}
    trigger_list = []
    
    for line in lines:
        split_line = line.split(',')
        if split_line[0] != "ADD":
            if split_line[1] != "AND" and split_line[1] != "OR":
                t_num_dict.update({split_line[0]:split_line[2]})
                t_dict[split_line[0]] = t_map[split_line[1]](split_line[2])
            if split_line[1] == "AND" or split_line[1] == "OR":
                if split_line[2] and split_line[3] in t_num_dict:
                    t_dict[split_line[0]] = t_map[split_line[1]](t_dict[split_line[2]],t_dict[split_line[3]])
        else:
            for word in split_line:
                for key, value in t_dict.items():
                    if key in word:
                        trigger_list.append(value)
       
    return trigger_list

    # print(lines) # for now, print it so you see what it contains!
    # print(trigger_dict)


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("Ukraine")
        # t2 = DescriptionTrigger("Russia")
        # t3 = DescriptionTrigger("war")
        # t4 = AndTrigger(t2, t3)
        # triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

