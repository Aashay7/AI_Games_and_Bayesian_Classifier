# SeekTruth.py : Classify text objects into two categories
# Written by hatha, aagond, saimorap
# References:
#1. https://stackoverflow.com/questions/18429143/strip-punctuation-with-regex-python
#2. https://docs.python.org/3/library/re.html
#3. https://www.datacamp.com/community/tutorials/python-list-comprehension
#4. List of stop words is derived from NLTK: stopwords.words('english')
#5. The algorithm for this code was designed based on the pseudo code given in CSCI-B555 Programming Assignment 1- Prof Roni Khardon. 
#   The concept of smoothing factor "m" was learnt from the B555 class and was applied here.
# Based on skeleton code by D. Crandall, October 2021


import sys
import re
import numpy as np

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}



#Used to create a Bag of Words
def vocab(train_x):
    vocabulary=[]
    for i in range(len(train_x)):
        for word in train_x[i].split(" "):
            if word not in vocabulary:
                vocabulary.append(word)
    return vocabulary


# Calculate Prior Probability of the class. P(class)=count(occurences of that class)/total len(data)
def calc_prior(labels,class1,class2):
    count1=0
    count2=0
    prior={}
    for i in range(len(labels)):
        if labels[i]==class1:
            count1+=1
        else:
            count2+=1
    total=count1+count2
    prior[class1]=float(count1/total)
    prior[class2]=float(count2/total)
    return prior

# Count Word frequency in that class. If word exists in Bag of Words but not in that class dictionary, give it count of 0.
def word_count(vocabulary,class1,class2,label,train_docs):
    dict_count={class1:{}, class2:{}}
    
    for i in range(len(label)):
        for word in train_docs[i].split(" "):
            if word in dict_count[label[i]].keys():
                dict_count[label[i]][word]+=1
            else:
                dict_count[label[i]][word]=1
                    
                                        
    for word in vocabulary:
        if word not in dict_count[class1].keys():
            dict_count[class1][word]=0
        if word not in dict_count[class2].keys():
            dict_count[class2][word]=0
            
    #Token count is count of total frequency of words in that class.         
    token1=sum(dict_count[class1].values())
    token2=sum(dict_count[class2].values())
    return dict_count,token1,token2
    


# The smoothing factor m was added here. This concept was learnt in algorithm provided in Assignment 1 of B555 course.
# Laplace smoothing used here. Explained in detail in Readme file.             
def calc_MAP(vocabulary,features,labels,class1,class2):
    m=1
    map_val={class1:{}, class2:{}}
    
    dict_count,token_1,token_2= word_count(vocabulary,class1,class2,labels,features)
    total_len=len(vocabulary)
    for word in vocabulary:
        map_val[class1][word]= float((dict_count[class1][word]+m)/(token_1+(total_len*m)))
        map_val[class2][word]= float((dict_count[class2][word]+m)/(token_2+(total_len*m)))
    
    return map_val

# Calc MAP estimate of words in that sentence. In order to avoid underflow error, we consider log addition of probabilities rather 
# than multiplication of probabilities.
def calc_estimate(test_feature, map_val,vocabulary,prior,class1,class2):
    val_1=np.log(prior[class1])
    val_2=np.log(prior[class2])
    for word in test_feature.split(" "):
        if word in vocabulary:
            
            val_1+=np.log(map_val[class1][word])
            val_2+=np.log(map_val[class2][word])
                
    return val_1, val_2



# https://stackoverflow.com/questions/18429143/strip-punctuation-with-regex-python For replacing all things other than alphabets and spaces.
# https://docs.python.org/3/library/re.html Documentation to understand \, ^ in regex.
# https://www.datacamp.com/community/tutorials/python-list-comprehension To use list comprehension to make code modular.

# Turn entire data to lower case. Remove all stop words and characters that are not spaces or alphabets.

def data_process(data):
    clean_data=[]
    stop_words=[]
    with open("stop_words.txt") as f:
        for word in f:
            a=word.strip()
            stop_words.append(a)
    
    
    for i in range(len(data)):
        data[i]=data[i].lower()

        data[i]=' '.join([word for word in data[i].split() if word not in stop_words])
            
        data[i]=re.sub(r'[^\w\s]','',data[i])
        data[i]=re.sub('-','',data[i])
        
        clean_data.append(data[i])
    
        
    return clean_data


    

        
# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
# Classifier function is the part where we actually call above functions and compare estimate values of both classes. We consider the prediction to
# be the value where estimate is higher.

def classifier(train_data, test_data):
    
    train_doc = train_data["objects"]
    train_labels=train_data["labels"]
    test_doc=test_data["objects"]
    train_docs,test_docs=data_process(train_doc), data_process(test_doc)
    class_A, class_B = train_data["classes"][0], train_data["classes"][1] 
    pred_list=[]
    vocabulary=vocab(train_docs)
    prior_val=calc_prior(train_labels,class_A,class_B)
    
    map_val = calc_MAP(vocabulary, train_docs,train_labels, class_A, class_B)
    for i in range(len(test_docs)):
        est_A, est_B= calc_estimate(test_docs[i], map_val, vocabulary, prior_val, class_A, class_B) 
        
        if est_A>est_B:
            pred_list.append(class_A)
        else:
            pred_list.append(class_B)
            
    return pred_list
    





if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))