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
firstComment=True
currentComment=[]
user=""
postTime=""

with open(fileDirectory) as file_object:
    for currentLine in file_object:
        line=currentLine.split();
        if (len(line) > 2):
            if (line[1]=="commented" or line[2]=="commented"):
                if (firstComment==True):
                    firstComment=False
                    user=line[0]
                    postTime=line[3:5]
                    currentComment=line[5:]
                else:
                    #print(currentComment)
                    #print(' '.join(currentComment)) 
                    #print(vader.polarity_scores(' '.join(currentComment)))
                    #print("\n")
                    print(user + " commented on " + postTime[0] + " at " + postTime[1])
                    print(' '.join(currentComment))
                    print("----------------------------------------------")
                    print("Sentiment analysis is as follows: ")
                    print(vader.polarity_scores(preprocess_text(' '.join(currentComment))))
                    print("\n")
                    print("\n")
                    currentComment=line[5:]
                    user=line[0]
                    postTime=line[3:5]
            else:
                currentComment = currentComment + line
        elif (len(line)<=2 and firstComment==False):
            currentComment = currentComment + line
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
