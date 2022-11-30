const way = document.getElementById('way');
const like_input = document.getElementById('like_input')
const between_input = document.getElementById('between_input')

way.onchange = function () {
  switch (way.value){
    case 'LIKE':
      like_input.style.display = "block";
      between_input.style.display = "none";
      break;
    case 'IS NOT':
      like_input.style.display = "block";
      between_input.style.display = "none";
      break;
    case 'BETWEEN':
      like_input.style.display = "none";
      between_input.style.display = "block";
      break;
    default:
      like_input.style.display = "block";
      between_input.style.display = "none";
  }
}
