img_neg=document.createElement("img");
flag=false;
body_flag=false;
img_neg.className="dot_neg";
img_neg.src="gif/404.gif";
circle = document.getElementById('box')
body=document.documentElement;
event_tag="";
kartThere=false;
karmThere=false;
sampThere=false;
function updateKaarakas(exact_verb,topY)
{
    var imgs = document.getElementsByClassName(exact_verb),
        total = imgs.length,
        coords = {},
        diam, radius1, radius2, imgW;
    var temp_img=document.getElementById(exact_verb);
    diam = parseInt( window.getComputedStyle(circle).getPropertyValue('width') );
    radius = diam/2;
    imgW = imgs[0].getBoundingClientRect().width;
    console.log('diam:'+diam+'\nimgW:'+imgW);
    radius2 = radius - imgW+55
    var i,
        alpha = Math.PI / 2,
        len = imgs.length,
        corner = 2 * Math.PI / total;
    for ( i = 0 ; i < total; i++ ){

      imgs[i].style.left = parseInt( ( radius - imgW / 2 ) + ( radius2 * Math.cos( alpha ) ) ) + 'px'
      imgs[i].style.top =  parseInt( ( radius - imgW / 2 ) - ( radius2 * Math.sin( alpha ) ) +topY) + 'px'
      alpha = alpha - corner;
    }

  }
    popDivMain=document.createElement("div");
    popDivMain.className="w3-card-12 white";
    popDivMain.style.backgroundColor="white";
    img = document.createElement('img');
    img.style.height=150+"px";
    popDivMain.appendChild(img);
    popDivText=document.createElement("div");
    popDivText.className="w3-container w3-center";
    popDivText.style.color="#455A64";
    popDivMain.appendChild(popDivText);
    popDivMain.style.position="absolute";

    function showToolTip(data,event)
    {
       x = event.clientX,
       y = event.clientY;
       val=data.split('<')[0];
      document.body.appendChild(popDivMain)
      popDivMain.style.top = (y - 80) + 'px';
      popDivMain.style.left = (x + 20) + 'px';
      popDivText.innerHTML=val;

        img.src = 'img/'+val.trim()+'.jpg';
        img.onerror = onErrorHandler;
    }
    function onErrorHandler()
    {
      img.src="img/404.jpg"
    }

    function hideToolTip(data)
    {
      document.body.removeChild(popDivMain);
    }


    //Animation funtion
    function animateKarma(className)
    {
      temp_divs=document.getElementsByClassName(className);
      from_div="";
      to_div="";
      what_div="";
      for(var i=0;i<temp_divs.length;i++)
      {

        if(temp_divs[i].innerHTML.indexOf('kartha')>-1)
        {
          from_div=temp_divs[i];
          img_neg.style.position="absolute";
          img_neg.style.top=window.innerHeight/2+"px"
        }
        if(temp_divs[i].innerHTML.indexOf('sampradana')>-1)
        {
          to_div=temp_divs[i];

        }
        if(temp_divs[i].innerHTML.indexOf('karma')>-1)
        {
          what_div=temp_divs[i];
        }
      }
    var img_move = document.createElement("H4");
    img_move.style.backgroundColor="#808080";
    img_move.style.left=from_div.offsetLeft+"px";
    img_move.style.top=from_div.offsetTop+"px";
    var t = document.createTextNode((what_div.innerHTML).split("(")[0]);
    my_span=document.createElement("span");
    kaaraka_img=document.createElement("img");
    extract_karma=what_div.innerHTML.split(">")[1].split("(")[0];
    my_span.innerHTML=extract_karma+"(karma)";
    my_span.style.fontSize=12+"px";
    my_span.style.color="#FFFFFF";
    my_span.style.padding=2+"px";
    my_span.style.borderRadius=6+"px";
    my_span.style.backgroundColor="rgba(0,0,0,0.5)"
    img_move.appendChild(my_span);
    img_move.style.backgroundImage ="url(\'img/"+extract_karma+".jpg\')";
    img_move.style.backgroundRepeat="no-repeat";
    img_move.style.backgroundSize= "auto 100%";
    img_move.style.backgroundPosition="center";
    circle.appendChild(img_move);

    var div2Pos = $(to_div).position();
                var div2Width = $(to_div).css("width");
                var div2Height = $(to_div).css("height");

                  $(img_move).animate({left:div2Pos.left,top:div2Pos.top, width:div2Width, height:div2Height}, 1000,function(){
                    setTimeout(function(){
                    circle.removeChild(img_move);
                  },2000)

                  });


    }

    function init(anim_data,kaarak_data,event)
    {

      anim_func=JSON.parse(anim_data.replace(/'/g,"\""));
      if(anim_func=="INTG")
      {
        img_neg.src="gif/intg.gif";
        document.body.appendChild(img_neg);
        flag=true;
      }
      else if(anim_func=="NEG")
      {
        img_neg.src="gif/cross.gif";
        document.body.appendChild(img_neg);
        flag=true;
      }
      else if(anim_func=="PROH")
      {
        img_neg.src="gif/cross.gif";
        document.body.appendChild(img_neg);
        flag=true;
      }
      else if (anim_func=="PRES") {
        img_neg.src="gif/pres.gif";
        document.body.appendChild(img_neg);
        flag=true;
      }
      else{
        if(flag==true)
          {document.body.removeChild(img_neg);
          flag=false;
          }
      }
      body.style.backgroundImage ="None";

      /////////////////////////////////////Colorize Selected Lines
      sentence_h2=document.getElementsByTagName("H2");
      for(i=0;i<sentence_h2.length;i++)
      {
        sentence_h2[i].style.color="#455A64";
        sentence_h2[i].style.fontSize=15+"px";
      }
      event.target.style.color="#007FFF";
      event.target.style.fontSize=16+"px";

      /////////////////////////////////////

      ////////////////////////////////////Remove H4
      var childh4s = circle.getElementsByTagName('H4');
      console.log("Total H4 before"+childh4s.length);

      while (circle.firstChild) {
        circle.removeChild(circle.firstChild);
      }

      kaarak_data=kaarak_data.replace(/'/g,"\"")
      console.log(kaarak_data);
      obj = JSON.parse(kaarak_data);
      console.log("Obj:"+obj.length);
      verb_top=0;
      for(i=0;i<obj.length;i++)
      {
        for(key in obj[i]) {
          if (obj[i].hasOwnProperty(key)) {
          color="#808080";
          console.log("Key Name"+key);

          //img_verb=>Image which represtents verbs
          var img_verb=document.createElement("img");
          img_verb.className="dot";
          img_verb.name="img_verb"
          img_verb.id=key.split("||")[0];
          img_verb.src="gif/"+key.split("||")[1]+".gif";

          //kriyaView => Text to represtent name of the kriya
          kriyaView=document.createElement("span");
          kriyaView.innerHTML=(key.split("||")[0]).replace("_"," ");
          kriyaView.style.fontSize=25+"px";
          kriyaView.style.color="#FFFFFF";
          kriyaView.style.padding=2+"px";
          kriyaView.style.borderRadius=6+"px";
          kriyaView.style.backgroundColor="rgba(0,0,0,0.3)"
          kriyaView.style.position="absolute";
          kriyaView.style.left=100+"px";
          kriyaView.style.top=(window.innerHeight/2)+(window.innerHeight*i)-30+"px";

          //hr => Line which sperates each kriya
          var hr = document.createElement('span');
          hr.style.position="absolute";
          hr.style.height=1+"px";
          hr.style.backgroundColor="#808080";
          hr.style.width=circle.offsetWidth+"px";
          hr.style.top=window.innerHeight*(i+1)+"px";
          hr.style.left=-8+"px";
          img_verb.style.position="absolute";
          img_verb.setAttribute("alt",key.split("||")[1]);
          img_verb.style.color="white";
          if(i>0){
            img_verb.style.top=(window.innerHeight*i)+(window.innerHeight/2)+"px";
          }
          circle.appendChild(img_verb);
          circle.appendChild(kriyaView);
          circle.appendChild(hr);
          for (karaka in obj[i][key])
          {
            switch (karaka.trim()) {
              case "kartha":
                kartThere=true;
                color='#FF5722'
                break;
              case "sampradana":
                sampThere=true;
                color='#03A9F4'
                break;
              case "destination":
                color='#3F51B5'
                body_flag=true;
                break;
              case "apaadaana":
                color='#4CAF50'

                break;
              case "karma":
                karmThere=true;
                color='#009688'
                break;
              case "adhikaraNa":
                color='#E91E63'
                  body_flag=true;
                break;
              case "karaNa":
                color='#FFC107'
                break;
            }

            if (obj[i][key].hasOwnProperty(karaka)) {
            if(obj[i][key][karaka].length!=0)
            {
              if(body_flag==true)
              {
                  body.style.backgroundImage = "url(\'img/"+obj[i][key][karaka][0].split("||")[1]+".jpg\')";
                  body.style.backgroundRepeat="no-repeat";
                  body_flag=false;
                  console.log("YES")
              }

              console.log(karaka+":"+obj[i][key][karaka]);
              var h4 = document.createElement("H4");
              h4.style.backgroundColor=color;
              var t = document.createTextNode(obj[i][key][karaka]);
              my_span=document.createElement("span");
              kaaraka_img=document.createElement("img");
              my_span.innerHTML=obj[i][key][karaka][0].split("||")[1]+"("+karaka+")";
              my_span.style.fontSize=12+"px";
              my_span.style.color="#FFFFFF";
              my_span.style.padding=2+"px";
              my_span.style.borderRadius=6+"px";
              my_span.style.backgroundColor="rgba(0,0,0,0.3)"
              h4.appendChild(my_span);
              h4.setAttribute("onmouseover","showToolTip(\'"+obj[i][key][karaka][0].split("||")[1]+"\',event)");
              h4.setAttribute("onmouseout","hideToolTip(\'"+obj[i][key][karaka][0].split("||")[1]+"\',event)");
              h4.style.backgroundImage ="url(\'img/"+(obj[i][key][karaka][0].split("||")[1])+".jpg\')";
              h4.style.backgroundRepeat="no-repeat";
              h4.style.backgroundSize= "auto 100%";
              h4.style.backgroundPosition="center";
              h4.className=key.split("||")[0];
              circle.appendChild(h4);
              }

            }
            }
            if(i==0) {
              updateKaarakas(key.split("||")[0],0)
            }
            else {
              updateKaarakas(key.split("||")[0],window.innerHeight*i+35);
            }

            if(kartThere&&karmThere&&sampThere)
            {
              //Move karma from kartha to apaadaana
              animateKarma(key.split("||")[0]);
              kartThere=false;
              karmThere=false;
              sampThere=false;
            }
          }
        }
    }

  }
