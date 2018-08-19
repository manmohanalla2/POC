function addDevice()
{
  var dict = {};
  dict['watched'] = true;
  var data = JSON.stringify(dict);
  var xhr = new XMLHttpRequest();
  xhr.timeout = 1000;
  xhr.withCredentials = true;
  xhr.addEventListener("readystatechange", function () 
  {
  if(this.readyState === 4)
  {
    if (this.status == 201) 
      {
        var response = JSON.parse(this.responseText);
      }
    }
  });
  xhr.open("POST", '/tutorial_watched');
  xhr.setRequestHeader("content-type", "application/json");
  xhr.setRequestHeader("cache-control", "no-cache");
  xhr.send(data);
};

function getListDevices()
{
  var dict = {};
  dict['watched'] = true;
  var data = JSON.stringify(dict);
  var xhr = new XMLHttpRequest();
  xhr.timeout = 1000;
  xhr.withCredentials = true;
  xhr.addEventListener("readystatechange", function () 
  {
  if(this.readyState === 4)
  {
    if (this.status == 201) 
      {
        var response = JSON.parse(this.responseText);
      }
    }
  });
  xhr.open("POST", '/tutorial_watched');
  xhr.setRequestHeader("content-type", "application/json");
  xhr.setRequestHeader("cache-control", "no-cache");
  xhr.send(data);
};

function deleteDevice()
{
  var dict = {};
  dict['watched'] = true;
  var data = JSON.stringify(dict);
  var xhr = new XMLHttpRequest();
  xhr.timeout = 1000;
  xhr.withCredentials = true;
  xhr.addEventListener("readystatechange", function () 
  {
  if(this.readyState === 4)
  {
    if (this.status == 201) 
      {
        var response = JSON.parse(this.responseText);
      }
    }
  });
  xhr.open("POST", '/tutorial_watched');
  xhr.setRequestHeader("content-type", "application/json");
  xhr.setRequestHeader("cache-control", "no-cache");
  xhr.send(data);
};