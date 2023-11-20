import nltk
#nltk.download('all')
#nltk.download('all', download_dir='/project/redditsa/')
nltk.data.path.append("/project/redditsa/nltk_Data");
#nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


vader = SentimentIntensityAnalyzer()

def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())
    dontDelete=["no", "nor", "aren't", "couldn't", "didn't", "doesn't", "don't", "hasn't", "hadn't", "haven't", "isn't", "shouldn't", "wasn't", "weren't", "won't", "wouldn't"]
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english') or token in dontDelete]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    processed_text = ' '.join(lemmatized_tokens)
    return processed_text


fileDirectory="/project/redditsa/reddit-scraping/api-results/WEN DFV?.md"
userComments={}
userReplies={}
whoRepliedToWho={}

firstComment=True
firstReply=True
replyIsMostRecent=False
currentComment=[]
currentReply=[]
user=""
commentScore=0
postTime=""
repliedUser=""
replyPostTime=""

replyScore=0
totalPositives=0
totalNegatives=0
totalNeutrals=0
totalCount=0
totalScore=0
tempScore=0

with open(fileDirectory) as file_object:
    for currentLine in file_object:
        line=currentLine.split();
        if (len(line) > 2):
            if (line[1]=="commented" or line[2]=="commented"):
                if (firstComment==True):
                    firstComment=False
                    user=line[0]
                    if (user=="[deleted"):
                        user="[deleted user]"
                        postTime=line[4:6]
                        commentScore=line[6]
                        currentComment=line[8:]
                        replyIsMostRecent=False
                    else:
                        postTime=line[3:5]
                        commentScore=line[5]
                        currentComment=line[7:]
                        replyIsMostRecent=False
                else:
                    
                    print(user + " commented on " + postTime[0] + " at " + postTime[1] + " with a score of " + replyScore) 
                    print(' '.join(currentComment))
                    print("----------------------------------------------")
                    print("Sentiment analysis is as follows: ")
                    print(vader.polarity_scores(preprocess_text(' '.join(currentComment))))
                    tempScore=vader.polarity_scores(preprocess_text(' '.join(currentComment)))["compound"]
                    totalScore=tempScore+totalScore
                    totalCount=totalCount+1
                    if (tempScore > 0):
                        totalPositives=totalPositives+1
                    elif (tempScore < 0):
                        totalNegatives=totalNegatives+1
                    else:
                        totalNeutrals=totalNeutrals+1
                    print("\n")
                    print("\n")
                    user=line[0]
                    if (user=="[deleted"):
                        user="[deleted user]"
                        postTime=line[4:6]
                        commentScore=line[6]
                        currentComment=line[8:]
                        replyIsMostRecent=False
                    else:
                        currentComment=line[7:]
                        commentScore=line[5]
                        postTime=line[3:5]
                        replyIsMostRecent=False
            elif (line[1]=="replied" or line[2]=="replied"):
                if (firstReply==False):
                    print(repliedUser + " replied on " + replyPostTime[0] + " at " + replyPostTime[1] + " with a score of " + replyScore)
                    print(' '.join(currentReply))
                    print("----------------------------------------------")
                    print("Sentiment analysis is as follows: ")
                    print(vader.polarity_scores(preprocess_text(' '.join(currentReply))))
                    print("\n")
                    print("\n")
                    tempScore=vader.polarity_scores(preprocess_text(' '.join(currentReply)))["compound"]
                    totalScore=tempScore+totalScore
                    totalCount=totalCount+1
                    if (tempScore > 0):
                        totalPositives=totalPositives+1
                    elif (tempScore < 0):
                        totalNegatives=totalNegatives+1
                    else:
                        totalNeutrals=totalNeutrals+1
                else:
                    firstReply=False
                repliedUser=line[0]
                if (repliedUser=="[deleted"):
                    repliedUser="[deleted user]"
                    replyPostTime=line[6:8]
                    currentReply=line[10:]
                    replyScore=line[8]
                    replyIsMostRecent=True
                else:
                    replyPostTime=line[5:7]
                    currentReply=line[9:]
                    replyScore=line[7]
                    replyIsMostRecent=True
            else:
                if (replyIsMostRecent == False):
                    currentComment = currentComment + line
                else:
                    currentReply = currentReply + line
        elif (len(line)<=2 and firstComment==False):
            if (replyIsMostRecent == False):
               currentComment = currentComment + line
            else:
                currentReply = currentReply + line
print(user + " commented on " + postTime[0] + " at " + postTime[1] + " with a score of " + replyScore)
print(' '.join(currentComment))
print("----------------------------------------------")
print("Sentiment analysis is as follows: ")
print(vader.polarity_scores(preprocess_text(' '.join(currentComment))))
tempScore=vader.polarity_scores(preprocess_text(' '.join(currentComment)))["compound"]
totalScore=tempScore+totalScore
totalCount=totalCount+1
if (tempScore > 0):
    totalPositives=totalPositives+1
elif (tempScore < 0):
    totalNegatives=totalNegatives+1
else:
    totalNeutrals=totalNeutrals+1
print("\n")
print("\n")
print(repliedUser + " replied on " + replyPostTime[0] + " at " + replyPostTime[1] + " with a score of " + replyScore)
print(' '.join(currentReply))
print("----------------------------------------------")
print("Sentiment analysis is as follows: ")
print(vader.polarity_scores(preprocess_text(' '.join(currentReply))))
tempScore=vader.polarity_scores(preprocess_text(' '.join(currentReply)))["compound"]
totalScore=tempScore+totalScore
totalCount=totalCount+1
if (tempScore > 0):
    totalPositives=totalPositives+1
elif (tempScore < 0):
    totalNegatives=totalNegatives+1
else:
    totalNeutrals=totalNeutrals+1
print("\n")
print("\n")
print("\n")
print("FINAL SCORE:" )
print("TOTAL NUMBER OF POSITIVE COMMENTS/REPLIES: " + str(totalPositives) + " out of " + str(totalCount))
print("TOTAL NUMBER OF NEGATIVE COMMENTS/REPLIES: " + str(totalNegatives) + " out of " + str(totalCount))
print("TOTAL NUMBER OF NEUTRAL COMMENTS/REPLIES: " + str(totalNeutrals) + " out of " + str(totalCount))
print("AVERAGE COMMENT/REPLY SENTIMENT: " + str(totalScore/totalCount))
#sample = 'I really REALLY hate NVIDIA!!!'
#print("\n\n")
#print(vader.polarity_scores(sample))

#df = pd.read_csv('sampleFile.csv')
#print("\n\n")
#print(df.head())

#print("\n\n")
#with open("sampleFile.csv") as file_object:
#    for line in file_object:
#        print(vader.polarity_scores(line))
#print(df.value_counts())
