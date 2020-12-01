'''
Label MDSD data with binary labels 

1-2 Stars = Negative
3 Stars = Discarded
4-5 Stars = Positive

MDSD Data is stored as a series of XML records in the following format:

<review>
    <unique_id> </unique_id>
    <unique_id> </unique_id>
    <asin></asin>
    <product_name></product_name>
    <product_type></product_type>
    <helpful></helpful>
    <rating></rating>
    <title></title>
    <date></date>
    <reviewer></reviewer>
    <review_text></review_text>
</review>

All fields except review_text, rating and the first ocurance of unique ID will be discarded


TODO: Automatically work for all of categories and create/delete the files
'''
import os
import sys
from bs4 import BeautifulSoup

if len(sys.argv) != 3:
    print('Usage: python <combine.py> <path to MDSD> <path to output dir>')
    quit()

# Target files for positive and negative reviews respectively
target_pos = os.path.join(sys.argv[2] , 'pos.csv')
target_neg = os.path.join(sys.argv[2] , 'neg.csv')

if os.path.isfile(target_pos) or os.path.isfile(target_neg):
    print('It looks like pos.csv or neg.csv already exist at ' + sys.argv[2] + \
          'make sure you aren\'t parsing the data twice!')
    quit()

categories = os.listdir(sys.argv[1])
#categories = ['tools_&_hardware','cell_phones_&_service', 'stopwords']

# open each category in turn
cat_counter = 0
for category_dir in categories:
    if not os.path.isdir(os.path.join(sys.argv[1], category_dir)):
        print('skipping file ' + category_dir)
        continue
    # give an update to assure the user all is not lost
    cat_counter += 1
    print('Parsing category ' + category_dir + ' --- ' + str(cat_counter) + ' / ' + str(len(categories)))
    # open all.review from that directory
    with open( os.path.join(sys.argv[1], category_dir, 'all.review'), 'r', encoding='iso-8859-1') as input_reviews: 
        # construct each review in turn
        current_record = ''
        for line in input_reviews:
            current_record += line
            if '</review>\n' in line:
                # We have come to the end of a record
                # parse + fix encoding
                current_record = bytes(current_record, 'utf-8').decode('utf-8', 'ignore')
                cr_soup = BeautifulSoup(current_record,'lxml')
                # check polarity and write one per line to positive and negative files
                if any(rat in cr_soup.find('rating').contents[0] for rat in ['4.0','5.0']):
                    #create and add it to file in positive
                    with open(target_pos , 'a', encoding='utf-8') as file:
                        file.write(cr_soup.find('review_text').contents[0].replace('\n', ' ') +'\n')
                    
                
                if any(rat in cr_soup.find('rating').contents[0] for rat in ['1.0','2.0']):
                    #create and add it to file in negative
                    #print(cr_soup.find('review_text').contents[0].replace('\n', ' '))
                    with open(target_neg , 'a', encoding='utf-8') as file:
                        file.write(cr_soup.find('review_text').contents[0].replace('\n', ' ') +'\n')

                current_record = ''

            
'''
# Line number: Todo: find efficient wat to get this
line_total = 39001829
category='kitchen_&_housewares'

# Target directories to save reviews in
target_pos=os.path.join(os.getcwd(), ('MDSD_Sort/' + category + '/pos/positive.csv'))
target_neg=os.path.join(os.getcwd(), ('MDSD_Sort/' + category + '/neg/negative.csv'))

# Open file in /data/MDSD_All/<category>/unprocessed.review
path_to_xml = os.path.join(os.getcwd(), ('MDSD_All/' + category + '/all.review'))
# Encoding to handle garbage characters
xml_records = open(path_to_xml, 'r', encoding='iso-8859-1')

# Consider individual record [the records are not well formated xml as no root node]
line_counter = 0
record_counter = 0
# Store current data instance
current_record = ''
for line in xml_records:
    print('Line: ' + str(line_counter) + '/' + str(line_total)+ ' ----- $$$$$$$$$$$$$$$$$$$')
    line_counter += 1
    current_record += line
    #TODO: check this doesn't prune '\n''s
    if '</review>\n' in line:
        # We have come to the end of a record
        # parse + fix encoding
        current_record = bytes(current_record, 'utf-8').decode('utf-8', 'ignore')

        #print('Record ------- ' + current_record)
        cr_soup = BeautifulSoup(current_record,'lxml')
        # check polarity and write one per line to positive and negative files
        if any(rat in cr_soup.find('rating').contents[0] for rat in ['4.0','5.0']):
            #create and add it to file in positive
            with open(target_pos , 'a', encoding='utf-8') as file:
                file.write(cr_soup.find('review_text').contents[0].replace('\n', ' ') +'\n')
            
        
        if any(rat in cr_soup.find('rating').contents[0] for rat in ['1.0','2.0']):
            #create and add it to file in negative
            #print(cr_soup.find('review_text').contents[0].replace('\n', ' '))
            with open(target_neg , 'a', encoding='utf-8') as file:
                file.write(cr_soup.find('review_text').contents[0].replace('\n', ' ') +'\n')


        #print(cr_soup.find('rating').contents)
        current_record = ''


xml_records.close()

'''