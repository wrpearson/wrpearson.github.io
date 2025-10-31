function showhide(element) {
  a = document.getElementById(element); 
  if(a.className == 'invisible') { 
    a.className='visible';
  } else {
    a.className='invisible';
  }
  return false;
}

function showhide(element, link) {
  a = document.getElementById(element);
  b = document.getElementById(link);
  if(a.className == 'invisible') {
    a.className='visible';
    b.innerHTML = '[hide answer]';
  } else {
    a.className='invisible';
    b.innerHTML = '[show answer]';
  }
  return false;
}

function showhidetext(element, link, text) {
  a = document.getElementById(element);
  b = document.getElementById(link);
  if(a.className == 'invisible') {
    a.className='visible';
    b.innerHTML = '[hide ' + text + ']';
  } else {
    a.className='invisible';
    b.innerHTML = '[show ' + text + ']';
  }
  return false;
}
