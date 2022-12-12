const way = document.getElementById('way');
const like_input = document.getElementById('like_input')
const between_input = document.getElementById('between_input')
const data_type_input = document.getElementById('data_type_input')

way.onchange = function () {
  switch (way.value){
    case 'like':
      like_input.style.display = "flex";
      between_input.style.display = "none";
      data_type_input.style.display = "none";

      break;
    case 'is_not':
      like_input.style.display = "flex";
      between_input.style.display = "none";
      data_type_input.style.display = "none";
      break;
    case 'between':
      like_input.style.display = "none";
      between_input.style.display = "flex";
      data_type_input.style.display = "none";
      break;
    case 'wrong_data_type':
      like_input.style.display = "none";
      between_input.style.display = "none";
      data_type_input.style.display = "flex";
      break;
    default:
      like_input.style.display = "flex";
      between_input.style.display = "none";
      data_type_input.style.display = "none";
  }
}
