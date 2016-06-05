																
																Title  : Semantic Parser for Kannada


'>'    : Folder name
'#'    : File name
'#...' : Includes many files


Folder Structure:
  >kaarakas :
      >kaaraka_code :
          #Kaarakas.py        : Main Kaaraka code.
          #sentences.txt      : Input sentences.
          #sentences_tags.txt : Input sentences including tags.
          #verbs.yaml         : Expectation of kaarakas in the verb.
          #output.json        : Output file having kaarakas of each sentence.This file is used in the GUI.

-----------------------------------------------------------------------------------------------------------------------------

      >kaaraka_gui :
          >css  :
              #main.css       : CSS file required for styling html.
              #w3.css         : The external css file used from www.w3schools.com

          >gif  :
              #...            : Includes the gif files for the particular verb having name as verb.

          >img  :
              #...            : Includes the jpg files for the nouns.

          >js   :
              #jq.js          : Jquery file used.
              #main.js        : Js file for handling all the gui action,events.

          #gui_kaarakas.py    : Runner file for gui, which processes '#output.json' file and generates and opens '#index.html'
          #sentences.txt      : Input sentences.
          #output.json        : JSON file which is generated in '#Kaarakas.py' used as input to the gui.
          #index.html         : GUI html file.

------------------------------------------------------------------------------------------------------------------------------

      >kathe       :
          >gui  :
            #...              : Includes the same gui file in the '>kaaraka_gui' folder having different images
                                and here background fixed as forest image.

          #...                : Other files are same as actual kaarakas code having different input file(#kathe.txt).

------------------------------------------------------------------------------------------------------------------------------

      >presentation :
          #kaarakas.pdf       : Presentation pdf file.
          #kaarakas.pptx      : Presentation pptx file.

------------------------------------------------------------------------------------------------------------------------------
      >report       :
          #Report-Cover.pdf   : Cover Page of the report.
          #Report-Detail.pdf  : Chapter wise contents of the report.

------------------------------------------------------------------------------------------------------------------------------
Thank you
