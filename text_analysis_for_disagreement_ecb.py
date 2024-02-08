import json
import re

from openai import OpenAI
client = OpenAI()

years = [80]
text_files = glob.gloc(r"ecb_raw/*.txt")

for target_year in years: 

  # Manually set target year
  # target_year = '2012'
  # Individual disagreement results saved here
  summary_dict = {}

  disagreement_files[target_year] = []
  doc_list = text_files_by_year[target_year]

  scores_over_meetings = []
  disagreement_scores_over_meetings = []
  files_analyzed = []


  for doc in text_files:

    print(doc)

    

    disagreement = 0
    # Open output text file
    doc_ = doc.split('/').copy()
    new_doc = str('analyzed' + ''.join(doc[:-4])) 

    summary_dict[''.join(doc_[2:4])] = []

    
    with open(doc,'r') as firstfile, open(new_doc,'w') as secondfile:

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
        sentence = sentence.replace("-\d+-")
        if (re.search("MS", sentence) != None) or (re.search("MR", sentence) != None ) or (re.search("CHAIRMAN", sentence) != None ) or (re.search("VICE", sentence) != None ):
          #start = True
          all_text.append(cur_text)
          cur_text = []
          
          #cur_text.append(sentence)
        
        cur_text.append(sentence)

      #print(all_text)
      count = 0
      for text_list in all_text:
        if len(text_list) <= 50:
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
            secondfile.write("****************DISAGREEMENT DETECTED*******************")
            print("****************DISAGREEMENT DETECTED*******************")
            summary_dict[''.join(doc_[2:4])].append(".".join(text_list))
          secondfile.write("Passage number " + str(count) + ".\n")
          print("Passage number " + str(count) + ".\n")
          cur_text = ".".join(text_list)
          secondfile.write(cur_text + '.' + '\n')
          print(cur_text + '.' + '\n\n')
          secondfile.write("Does the passage contain contention or disagreement? Response from the model: " + response)
          print("Does the passage contain contention or disagreement? Response from the model: " + response)
          secondfile.write('\n\n\n')
          print('\n\n\n\n')



  with open(str(doc[:-4]) + "_results.json", "w") as outfile: 
    json.dump(summary_dict, outfile)
          


 


          




      


      






