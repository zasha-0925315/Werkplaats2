// creating variables to use later
const columnSelect = document.getElementById('column_select');
const like = document.getElementById('like')
const isNot = document.getElementById('is_not')
const between = document.getElementById('between')
const wrongDataType = document.getElementById('wrong_data_type')
const booleanValue = document.getElementById('boolean_value')
const date1900 = document.getElementById('date_1900')

const way = document.getElementById('way');
const likeInput = document.getElementById('like_input')
const betweenInput = document.getElementById('between_input')
const dataTypeInput = document.getElementById('data_type_input')
const dataType = document.getElementById('data_type')

// Switch funtions to change what is displayed on the page
function displayWayOption() {
  switch (columnSelect.value){
    case 'id':
      like.style.display = "flex";
      isNot.style.display = "flex";
      between.style.display = "flex";
      wrongDataType.style.display = "none";
      booleanValue.style.display = "none";
      date1900.style.display = "none";
      way.selectedIndex = 0;
      likeInput.style.display = "flex";
      betweenInput.style.display = "none";
      dataTypeInput.style.display = "none";
      break;
    case 'voornaam':
      like.style.display = "flex";
      isNot.style.display = "flex";
      between.style.display = "none";
      wrongDataType.style.display = "none";
      booleanValue.style.display = "none";
      date1900.style.display = "none";
      way.selectedIndex = 0;
      likeInput.style.display = "flex";
      betweenInput.style.display = "none";
      dataTypeInput.style.display = "none";
      break;
    case 'achternaam':
      like.style.display = "flex";
      isNot.style.display = "flex";
      between.style.display = "none";
      wrongDataType.style.display = "none";
      booleanValue.style.display = "none";
      date1900.style.display = "none";
      way.selectedIndex = 0;
      likeInput.style.display = "flex";
      betweenInput.style.display = "none";
      dataTypeInput.style.display = "none";
      break;
    case 'geboortejaar':
      like.style.display = "flex";
      isNot.style.display = "flex";
      between.style.display = "flex";
      wrongDataType.style.display = "flex";
      booleanValue.style.display = "none";
      date1900.style.display = "flex";
      way.selectedIndex = 0;
      dataType.selectedIndex = 1;
      likeInput.style.display = "flex";
      betweenInput.style.display = "none";
      dataTypeInput.style.display = "none";
      break;
    case 'medewerker':
      like.style.display = "none";
      isNot.style.display = "none";
      between.style.display = "none";
      wrongDataType.style.display = "flex";
      booleanValue.style.display = "flex";
      date1900.style.display = "none";
      way.selectedIndex = 3;
      dataType.selectedIndex = 0;
      likeInput.style.display = "none";
      betweenInput.style.display = "none";
      dataTypeInput.style.display = "flex";
      break;
    case 'met pensioen':
      like.style.display = "none";
      isNot.style.display = "none";
      between.style.display = "none";
      wrongDataType.style.display = "flex";
      booleanValue.style.display = "flex";
      date1900.style.display = "none";
      way.selectedIndex = 3;
      dataType.selectedIndex = 0;
      likeInput.style.display = "none";
      betweenInput.style.display = "none";
      dataTypeInput.style.display = "flex";
      break;
    case 'leerdoel':
      like.style.display = "flex";
      isNot.style.display = "flex";
      between.style.display = "none";
      wrongDataType.style.display = "none";
      booleanValue.style.display = "none";
      date1900.style.display = "none";
      way.selectedIndex = 0;
      likeInput.style.display = "flex";
      betweenInput.style.display = "none";
      dataTypeInput.style.display = "none";
      break;
    default:
      like.style.display = "flex";
      isNot.style.display = "flex";
      between.style.display = "flex";
      wrongDataType.style.display = "flex";
      booleanValue.style.display = "flex";
      date1900.style.display = "flex";
      way.selectedIndex = 0;
  }


}

function displayInput() {
  switch (way.value){
    case 'like':
      likeInput.style.display = "flex";
      betweenInput.style.display = "none";
      dataTypeInput.style.display = "none";
      break;
    case 'is_not':
      likeInput.style.display = "flex";
      betweenInput.style.display = "none";
      dataTypeInput.style.display = "none";
      break;
    case 'between':
      likeInput.style.display = "none";
      betweenInput.style.display = "flex";
      dataTypeInput.style.display = "none";
      break;
    case 'wrong_data_type':
      likeInput.style.display = "none";
      betweenInput.style.display = "none";
      dataTypeInput.style.display = "flex";
      if (columnSelect.value === 'geboortejaar'){
        dataType.selectedIndex = 1
      }

      break;
    default:
      likeInput.style.display = "flex";
      betweenInput.style.display = "none";
      dataTypeInput.style.display = "none";
  }
}

// Event listeners to check if someting happend on the page
window.addEventListener("load", displayWayOption)
columnSelect.addEventListener("change", displayWayOption)
window.addEventListener("load", displayInput)
way.addEventListener("change", displayInput)
