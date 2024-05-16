import json
import re
import glob
from openai import OpenAI
client = OpenAI()
import textwrap

years = [80]
text_files = glob.glob(r"cgm/*.txt")

for target_year in years: 

  # Manually set target year
  # target_year = '2012'
  # Individual disagreement results saved here
  summary_dict = {}

  #disagreement_files[target_year] = []
  #doc_list = text_files_by_year[target_year]

  scores_over_meetings = []
  disagreement_scores_over_meetings = []
  files_analyzed = []


  for doc in text_files:

    print(doc)

    

    disagreement = 0
    # Open output text file
    doc_ = doc.split('/').copy()
    new_doc = str('cgm_analyzed/analyzed_' + doc_[1]) 

    summary_dict[''.join(doc)] = []

    
    with open(doc,'r') as firstfile, open(new_doc,'w') as secondfile:

      print('./'+new_doc)
      average_sentiment = 0
      instace_of_disagreement = 0
      count_sent = 0
      start_count = 0

      text = firstfile.read()
      text_split = text
      text_split = re.split("[.!?]", text_split)
      #print(text_split)
      all_text = []
      cur_text = []
      for sentence in text_split:
        sentence = re.sub('(\w+ \d+–\d+, \d+ of \d+)', '', sentence)
        sentence = re.sub('(\w+ \d+, \d+ of \d+)', '', sentence)
        sentence = sentence.replace("\t", "")
        sentence = sentence.replace("    ", "")
        sentence = sentence.replace("|", "")
        sentence = sentence.replace("-\d+-", "")
        sentence = sentence.replace("\n", " ")
        sentence = sentence.replace("(\* [\w\s]+.)", " ")
        sentence = sentence.replace("(-*)", "")
        if (re.search("(.+ \(\d+ \- \d+\))", sentence) != None) or (re.search("(The Chairman .+ \(\d+ \- \d+\))", sentence) != None ) or (re.search("(Mr. .+ \(\d+ \- \d+\))", sentence) != None ) or (re.search("(Ms. .+ \(\d+ \- \d+\))", sentence) != None ) or (re.search("(Le Pr*sident)", sentence) != None) or (re.search("(M. \w+)", sentence) != None) or (re.search("(M. ([a-zA-Z]+.) ([a-zA-Z]+.) \w+)", sentence) != None) or (re.search("(M. ([a-zA-Z]+.) \w+)", sentence) != None) or (re.search("(Mr. ([a-zA-Z]+.) \w+)", sentence) != None) or (re.search("(Mr. ([a-zA-Z]+.) \w+)", sentence) != None):
          #start = True
          all_text.append(cur_text)
          cur_text = []
          
          #cur_text.append(sentence)
        
        cur_text.append(sentence)

      #print(all_text)
      count = 0
      for text_list in all_text:
        tokens = sum([len(sentence.split(' ')) for sentence in text_list])
        if tokens >= 1000:
          count += 1
          secondfile.write('This passage was too long for model to process and thus had to be split: ')
          secondfile.write('Passsage number ' + str(count) + '\n')
          cur_text_ = ". ".join(text_list)
          #cur_text = re.sub('(.+ \(\d+ \- \d+\))|(The Chairman .+ \(\d+ \- \d+\))|(Mr. .+ \(\d+ \- \d+\))|(Ms. .+ \w \(\d+ \- \d+\))', '', cur_text_)
          part_1, part_2, part_3 = '', '', ''
          parts = []
          i = 1
          while tokens/i >= 1000:
            i+= 1
          if tokens / i <= 1000:
            
            split_num = int(tokens/i)
            k = 0
            while k <= tokens: 
             parts.append(cur_text_[k:k+split_num])
             k+= split_num
            #part_2 = cur_text_[int(tokens/2):]
            #parts = [part_1, part_2]
          #if tokens / 3 <= 1000:
            #part_1 = cur_text_[:int(tokens/3)]
            #part_2 = cur_text_[int(tokens/3):tokens - int(tokens/3)]
            #part_3 = cur_text_[int(tokens/3) + int(tokens/3):]
            #parts = [part_1, part_2, part_3]
          if 1 == 1:
            for part in parts:
              print(part)
              completion = client.chat.completions.create(
              model="gpt-3.5-turbo",
              messages=[
                {"role": "system", "content": 'Is there contention or disagreement in the following passage. Answer yes or no and give an explanation: ' + part},
              ]
              )

          #print(completion.choices[0].message.content)
              response = completion.choices[0].message.content

          #print(response_re)

              if "Yes" in response[0:5]:
                disagreement += 1
                secondfile.write("****************DISAGREEMENT DETECTED*******************")
                print("****************DISAGREEMENT DETECTED*******************")

              secondfile.write(part + '.' + '\n\n')
              secondfile.write("Does the passage contain contention or disagreement? Response from the model: " + response)
              print("Does the passage contain contention or disagreement? Response from the model: " + response)
        else:
          cur_text_ = ". ".join(text_list)
          cur_text = re.sub('(.+ \(\d+ \- \d+\))|(The Chairman .+ \(\d+ \- \d+\))|(Mr. .+ \(\d+ \- \d+\))|(Ms. .+ \w \(\d+ \- \d+\))', '', cur_text_)
          count += 1


          completion = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[
              {"role": "system", "content": 'Is there contention or disagreement in the following passage. Answer yes or no and give an explanation: ' + cur_text},
          ]
          )

          #print(completion.choices[0].message.content)
          response = completion.choices[0].message.content

          #print(response_re)
        
          if "Yes" in response[0:5]:
            disagreement += 1
            secondfile.write("****************DISAGREEMENT DETECTED*******************\n")
            print("****************DISAGREEMENT DETECTED*******************\n")
            #summary_dict[''.join(doc_[1])].append(".".join(text_list))
          secondfile.write("Passage number " + str(count) + ".\n")
          print("Passage number " + str(count) + ".\n")
          cur_text = ".".join(text_list)
          secondfile.write(cur_text + '.' + '\n')
          print(cur_text + '.' + '\n\n')
          secondfile.write("Does the passage contain contention or disagreement? Response from the model:\n " + response + "\n")
          print("Does the passage contain contention or disagreement? Response from the model: " + response + "\n")
          secondfile.write('\n\n\n')
          print('\n\n\n\n')



  #with open(str(doc[1]) + "_results.json", "w") as outfile: 
    #json.dump(summary_dict, outfile)
          


 


          




      


      






