import webbrowser
import json
import sys

#Input Data From Parser File
def process_kaaraka_dict(kaar_dict):
	return_dict={}
	for my_key in kaar_dict:
		return_dict[my_key]=kaar_dict[my_key][0].split("||")[1]
	return return_dict


data_dict = eval(open("output.json", "r").read().strip())
sentence="""<h5 style="color:#007FFF">Sentences<h5><hr>"""
count=1

with open('sentences.txt') as f:
	for line in f:
		a=[]
		b=[]
		anim_info=[]
		line=line.strip()
		print(line)
		kriya_count=0;
		for i in range(len(data_dict[line]["kriyaapada_order"])):
			kriya=data_dict[line]["kriyaapada_order"][i]
			print (kriya)
			kriya_count+=1;
			b.append("{\'"+kriya+"\':"+str(data_dict[line]["kaarakas"][kriya])+"}")


		a.append(str(b))
		if((kriya_count==2) and "PRES" in str(data_dict[line]["kriyaapada_data"].values() )or "PRES" in str(data_dict[line]["namapada_data"].values())):
			anim_info.append("PRES")
		if("NEG" in str(data_dict[line]["kriyaapada_data"].values() )or "NEG" in str(data_dict[line]["namapada_data"].values())):
			anim_info.append("NEG")
		if("PROH" in str(data_dict[line]["kriyaapada_data"].values() )or "PROH" in str(data_dict[line]["namapada_data"].values())):
			anim_info.append("PROH")
		if("INTG" in str(data_dict[line]["kriyaapada_data"].values()) or "INTG" in str(data_dict[line]["namapada_data"].values())):
			anim_info.append("INTG")
		print("a befor :"+str(a));
		a=str(a).replace("\"{","{").replace("}\"","}").replace("'","\\'").replace("\\\\","\\").replace("\\\'{\\\'{","{{\\'").replace("\\'{","{\\'").replace("}\\'","}")
		a=a.replace("[{","[").replace("}]","]")
		a=a.replace("\\'[","{").replace("]\\'","}")
		print(a)
		print("--------"*23)
		sentence+="\n<h2 style='font-size:15px;color: #455A64;text-align:left;padding-left:10px;cursor:pointer ' onclick=\"init(\'"+str(anim_info).replace("'","\\'")+"\',\'"+a+"\',"+"event)\">"+str(count)+"."+line+"</h2>"
		count+=1
#created a html file
f=open('index_kathe.html','w')
message="""
<!DOCTYPE html>
<html>
<meta charset=utf-8>
<meta name="viewport" content="width=device-width, initial-scale=1">
<head>
<link rel="stylesheet"  type="text/css" href="css/w3.css">
<link rel="stylesheet" type="text/css" href="css/main.css">
<style>
html {
    height: 100%;
    margin:0px;
    background: url("img/ಕಾಡು.jpg") no-repeat center center;
    background-size: cover;
    background-attachment: fixed;
}
</style>
</head>

<body id="body">

<div class="box" z-default=10 z-hover=30 style="background-color:rgba(255,255,255,0.8);position:fixed;left:0px;width:25%;">
  <h3 class="box-content"style="text-align: center;color:#455A64">Semantic Kannada Parser</h3>
</div>

<div class="box"
style="position:fixed;left:0px;top:52px;overflow:scroll;padding-bottom:50px;float:left;width:25%;height:100%;color:black ;background-color:rgba(255,255,255,0.8);"z-default=10 z-hover=30>
"""+sentence+"""
</div>

<div class="box" style="position:fixed;right:0px;height:auto;float:right;width:15%;color:black ;margin-left:20px;padding-top:20px;margin-top: -14px;background-color:rgba(255,255,255,0.8);"z-default=10 z-hover=30>

<table style="font-size:12px;text-align:left;color:#455A64">
<tr><td><div class="color_info" style="background-color:#FF5722"></div></td> <td>Kartha(ಕರ್ತೃ)</td></tr>
        <tr><td><div class="color_info" style="background-color:#009688"></div></td> <td>Karma(ಕರ್ಮ)</td></tr>

        <tr><td><div class="color_info" style="background-color:#FFC107"></div></td> <td>KaraNa(ಕರಣ)</td></tr>
		        <tr><td><div class="color_info"style="background-color:#03A9F4"></div></td> <td>Sampradana(ಸಂಪ್ರದಾನ)</td></tr>
        <tr><td><div class="color_info"style="background-color:#4CAF50"></div></td> <td>Apadana(ಅಪಾದಾನ)</td></tr>

         <tr><td><div class="color_info"style="background-color:#E91E63"></div></td> <td>AdhikaraNa(ಅಧಿಕರಣ)</td></tr>
          <tr><td><div class="color_info"style="background-color:#3F51B5"></div></td> <td>Destination</td></tr>
</table>
</div>


     <div id="box" style="margin: 0 auto; top:20px " align="center">

  	<img id="img_anim" class="dot" src="gif/kannada.gif" onerror="this.onerror=null;this.src=\'gif/404.gif\'"  alt="">

  </div>




<script type="text/javascript" src="js/jq.js">
</script>
	<script type="text/javascript" src="js/main.js">
	</script>
</body>
</html>

"""
f.write(message)
f.close()

webbrowser.open_new_tab('index_kathe.html')
